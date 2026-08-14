"""
actions - gmail_sender
=======================
Send Gmail.

Independent actions module for the Autonomous Computer AI Assistant.
Implements the standard execute(task, context) capability contract.
"""

import os
import smtplib
from email.message import EmailMessage
from typing import Any, Dict, Optional

from core.capability import Capability


class GmailSender(Capability):
    """Send Gmail."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__(config)
        self.name = "gmail_sender"
        self.description = "Send Gmail."

    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
        to, subject, body = self._parse(task)
        if not to:
            return self.error('No recipient found. Use: send email to <addr> subject "..." body "..."')
        user = os.getenv("GMAIL_USER") or os.getenv("SMTP_USER")
        pwd = os.getenv("GMAIL_APP_PASSWORD") or os.getenv("SMTP_PASSWORD")
        if not user or not pwd:
            return self.error("GMAIL_USER and GMAIL_APP_PASSWORD env vars not set. Configure SMTP credentials to send.")
        msg = EmailMessage()
        msg["From"] = user
        msg["To"] = to
        msg["Subject"] = subject or "(no subject)"
        msg.set_content(body or "")
        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(user, pwd)
                smtp.send_message(msg)
            return self.ok(f"Email sent to {to}.", to=to, subject=subject)
        except Exception as exc:
            return self.error(str(exc))

    def _parse(self, task: str):
        import re
        m = re.search(r"\bto\s+([\w.+-]+@[\w.-]+)", task, re.I)
        to = m.group(1) if m else ""
        subject = ""
        body = ""
        m = re.search(r'subject\s+["\']([^"\']+)["\']', task, re.I)
        if m:
            subject = m.group(1)
        m = re.search(r'body\s+["\']([^"\']+)["\']', task, re.I)
        if m:
            body = m.group(1)
        # If no explicit body, use any trailing quoted string after subject.
        if not body:
            quotes = re.findall(r'["\']([^"\']+)["\']', task)
            if quotes:
                body = quotes[-1] if not subject else (quotes[0] if quotes else "")
        return to, subject, body

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description
