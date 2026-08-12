#!/usr/bin/env python3
"""
Build the full Autonomous Computer AI Assistant structure.

Scaffolds the complete capability-based source code architecture described in
the project spec: top-level entry/router/UI files + 12 packages of independent
modules, each implementing the same execute(task, context) contract.

Run:  python3 build_structure.py
"""

import json
import os
from pathlib import Path
from typing import Dict

ROOT = Path("/workspace/project/candy")

# --------------------------------------------------------------------------- #
# Module catalogue. Each entry: filename -> one-line description.
# Files that share a name across categories keep their distinct identity via
# the package they live in (actions/, autonomy/, security/, ...).
# --------------------------------------------------------------------------- #

ACTIONS = {
    # 1. SYSTEM & HARDWARE [28]
    "system_monitor.py": "Monitor CPU, RAM, GPU, temperature and battery.",
    "self_healing.py": "Auto-repair crashes, free RAM and fix Wi-Fi.",
    "computer_control.py": "Shutdown, restart, sleep and volume control.",
    "computer_settings.py": "Wi-Fi, brightness and bluetooth settings.",
    "desktop.py": "Wallpaper, icons and clean-desktop management.",
    "network_manager.py": "Wi-Fi, VPN and network troubleshooting.",
    "window_manager.py": "Snap, tile and move windows.",
    "process_manager.py": "Kill and prioritise running processes.",
    "update_manager.py": "System and application updates.",
    "power_manager.py": "Power profiles and battery saver.",
    "disk_manager.py": "Cleanup, defrag and disk health.",
    "printer_manager.py": "Manage printers and print jobs.",
    "hardware_diagnostics.py": "Test RAM, CPU and GPU health.",
    "bios_manager.py": "Update BIOS and check settings.",
    "fan_controller.py": "Control fans and liquid cooling.",
    "usb_manager.py": "Mount, eject and inspect USB devices.",
    "bluetooth_manager.py": "Pair and manage bluetooth devices.",
    "display_manager.py": "Multi-monitor setup.",
    "audio_manager.py": "Control sound devices.",
    "driver_manager.py": "Update device drivers.",
    "registry_cleaner.py": "Clean the Windows registry.",
    "terminal_manager.py": "Run shell, bash and powershell commands.",
    "accounts_manager.py": "Manage users, passwords and permissions.",
    "app_manager.py": "Open, close, install and uninstall apps.",
    "cache_cleaner.py": "Clear temp files and caches.",
    "screenshot_ocr.py": "Read text from screenshots.",
    "keyboard_controller.py": "Type, shortcuts and macros.",
    "mouse_controller.py": "Click, move, drag and scroll.",
    "peripheral_manager.py": "Manage wired and wireless peripherals.",

    # 2. FILES & DATA [26]
    "file_controller.py": "Create, move, copy and delete files.",
    "file_opener.py": "Smart-open files by name.",
    "file_processor.py": "Read, summarise and convert files.",
    "file_downloader.py": "Download files from links.",
    "pdf_reader.py": "Extract and summarise PDFs.",
    "backup_manager.py": "Auto-backup to the cloud.",
    "cloud_sync.py": "Sync folders to cloud storage.",
    "document_generator.py": "Generate CVs, letters and proposals.",
    "archive_manager.py": "Zip, unzip and encrypt archives.",
    "duplicate_finder.py": "Find duplicate files.",
    "data_scraper.py": "Scrape data from websites.",
    "database_manager.py": "Manage SQLite, MySQL and MongoDB.",
    "excel_manager.py": "Read/write Excel with formulas.",
    "csv_processor.py": "Clean, merge and analyse CSV.",
    "image_processor.py": "Resize, compress and OCR images.",
    "video_processor.py": "Convert and compress video.",
    "audio_processor.py": "Convert, trim and normalise audio.",
    "version_control.py": "Track file versions.",
    "file_recovery.py": "Recover deleted files.",
    "file_encryptor.py": "Encrypt files.",
    "file_decryptor.py": "Decrypt files.",
    "file_comparator.py": "Diff and compare files.",
    "metadata_editor.py": "Edit file metadata.",
    "torrent_manager.py": "Download torrents.",
    "pdf_editor.py": "Edit PDF documents.",
    "document_scanner.py": "Scan documents to PDF.",

    # 3. WEB, INFO & RESEARCH [25]
    "web_search.py": "Google/Bing search with summarisation.",
    "weather_report.py": "Weather forecasts.",
    "internet_speed.py": "Test internet speed.",
    "ip_checker.py": "Public IP information.",
    "url_launcher.py": "Open URLs in the browser.",
    "research_paper_reader.py": "Summarise research papers.",
    "news_briefing.py": "Daily news summary.",
    "price_tracker.py": "Track product prices and deals.",
    "knowledge_base.py": "Personal wiki.",
    "stock_tracker.py": "Track stocks and crypto.",
    "trend_analyzer.py": "Find trending topics.",
    "fact_checker.py": "Verify claims online.",
    "reddit_scraper.py": "Track subreddits.",
    "twitter_scraper.py": "Track X trends.",
    "youtube_research.py": "Find and research videos.",
    "academic_search.py": "Google Scholar search.",
    "patent_search.py": "Search patents.",
    "translation_service.py": "Translate 100+ languages.",
    "domain_checker.py": "Check domain availability.",
    "ssl_checker.py": "Check website SSL security.",
    "seo_auditor.py": "Audit website SEO.",
    "link_checker.py": "Find broken links.",
    "whois_lookup.py": "WHOIS domain info.",
    "job_board_scraper.py": "Find job listings.",
    "real_estate_scraper.py": "Find properties.",

    # 4. MEDIA & CREATIVE [27]
    "screen_processor.py": "AI understanding of the screen.",
    "screen_recorder.py": "Record the screen.",
    "screenshot.py": "Capture screenshots.",
    "webcam_control.py": "Take photo and video with webcam.",
    "youtube_control.py": "Play, pause and search YouTube.",
    "youtube_downloader.py": "Download YouTube videos.",
    "youtube_video.py": "Transcript and summarise videos.",
    "music_player.py": "Play local music.",
    "voice_cloner.py": "Custom-voice text-to-speech.",
    "image_generator.py": "Generate AI art.",
    "video_editor.py": "Cut, merge and caption video.",
    "podcast_generator.py": "Convert docs to audio podcast.",
    "thumbnail_maker.py": "Auto YouTube thumbnails.",
    "subtitle_generator.py": "Auto-generate subtitles.",
    "3d_model_generator.py": "Generate 3D models.",
    "logo_generator.py": "Generate brand logos.",
    "animation_maker.py": "Make 2D/3D animations.",
    "sound_effect_generator.py": "Generate AI sound effects.",
    "color_palette_generator.py": "Generate brand color palettes.",
    "meme_generator.py": "Auto-generate memes.",
    "gif_maker.py": "Create GIFs.",
    "photo_restorer.py": "Fix old photos.",
    "background_remover.py": "Remove image backgrounds.",
    "voice_transcriber.py": "Speech to text.",
    "karaoke_generator.py": "Remove vocals for karaoke.",
    "watermark_remover.py": "Remove watermarks.",
    "ai_avatar_generator.py": "Generate AI avatars.",

    # 5. COMMS, SOCIAL & PRODUCTIVITY [27]
    "send_message.py": "Send SMS and Discord messages.",
    "gmail_sender.py": "Send Gmail.",
    "whatsapp_sender.py": "Send WhatsApp messages.",
    "contacts.py": "Manage contacts.",
    "social_media.py": "Post and interact on social media.",
    "instagram_downloader.py": "Download Instagram posts.",
    "calendar_manager.py": "Google and Outlook calendar.",
    "meeting_assistant.py": "Join, record and transcribe meetings.",
    "email_manager.py": "Read, draft and sort inbox.",
    "expense_tracker.py": "Track spending.",
    "slack_discord.py": "Slack and Discord teamwork.",
    "note_taker.py": "Auto meeting notes.",
    "task_manager.py": "To-do lists and Kanban.",
    "project_manager.py": "Manage projects and deadlines.",
    "linkedin_manager.py": "Post and connect on LinkedIn.",
    "twitter_manager.py": "Post tweets and threads.",
    "telegram_bot.py": "Telegram bot automation.",
    "zoom_manager.py": "Schedule and join Zoom meetings.",
    "survey_creator.py": "Create forms and polls.",
    "crm_sender.py": "Email CRM leads.",
    "newsletter_manager.py": "Email campaigns.",
    "signature_generator.py": "Email signatures.",
    "auto_responder.py": "Smart auto-replies.",
    "contact_enricher.py": "Find contact information.",
    "voice_call_manager.py": "Make VoIP calls.",
    "form_filler.py": "Auto-fill forms.",
    "document_collab.py": "Google Docs collaboration.",

    # 7. LEARNING & EDUCATION [19]
    "reminder.py": "Set reminders.",
    "proactive.py": "Act without being asked.",
    "location_tracker.py": "Get current location.",
    "phone_location.py": "Find a lost phone.",
    "gui_control.py": "Click and type on the UI.",
    "habit_tracker.py": "Track habits.",
    "flashcard_generator.py": "Generate Anki cards.",
    "anomaly_detector.py": "Detect anomalies and alert.",
    "tutor.py": "1-on-1 tutor.",
    "course_creator.py": "Make courses.",
    "quiz_generator.py": "Auto quizzes.",
    "language_learner.py": "Learn languages.",
    "exam_simulator.py": "Mock exams.",
    "progress_tracker.py": "Track learning progress.",
    "citation_manager.py": "Manage citations.",
    "mindmap_generator.py": "Visual notes / mindmaps.",
    "speed_reader.py": "Speed-reading trainer.",
    "scholarship_finder.py": "Find scholarships.",
    "research_paper_writer.py": "Write research papers.",

    # 8. LIFESTYLE & HEALTH [22]
    "qr_generator.py": "Generate QR codes.",
    "presentation_tools.py": "Make slides.",
    "google_apps.py": "Google Docs and Sheets.",
    "shopping_sites.py": "Open shopping stores.",
    "meal_planner.py": "Meal plans.",
    "fitness_coach.py": "Workout and form check.",
    "sleep_tracker.py": "Analyse sleep data.",
    "water_reminder.py": "Hydration reminders.",
    "meditation_guide.py": "Guided meditation.",
    "health_monitor.py": "Track vitals from a watch.",
    "recipe_generator.py": "Cook from ingredients.",
    "grocery_list.py": "Auto shopping list.",
    "travel_planner.py": "Plan trips.",
    "dating_coach.py": "Dating advice.",
    "style_advisor.py": "Outfit suggestions.",
    "mood_tracker.py": "Track emotions.",
    "therapy_chat.py": "Mental health chat.",
    "vitamin_tracker.py": "Supplement tracking.",
    "allergy_checker.py": "Check food allergies.",
    "doctor_finder.py": "Find doctors.",
    "insurance_manager.py": "Manage health insurance.",
    "appointment_booker.py": "Book doctor appointments.",

    # 9. GAMING & ENTERTAINMENT [17]
    "game_launcher.py": "Launch games and boost FPS.",
    "clip_recorder.py": "Record gameplay highlights.",
    "streaming_tools.py": "OBS and Twitch streaming.",
    "playlist_generator.py": "AI music playlists.",
    "game_coach.py": "Analyse gameplay and give tips.",
    "game_finder.py": "Discover new games.",
    "achievement_tracker.py": "Track achievements.",
    "mod_manager.py": "Install game mods.",
    "server_manager.py": "Host game servers.",
    "tournament_tracker.py": "Track esports tournaments.",
    "game_price_tracker.py": "Track game sales.",
    "walkthrough_generator.py": "Generate game guides.",
    "save_manager.py": "Backup game saves.",
    "controller_mapper.py": "Map controller buttons.",
    "game_stream_recorder.py": "Record streams.",
    "game_review_writer.py": "Write game reviews.",
    "vr_manager.py": "Manage VR headsets.",

    # 10. FINANCE & BUSINESS [22]
    "invoice_generator.py": "Create and send invoices.",
    "tax_calculator.py": "Calculate taxes.",
    "budget_manager.py": "Monthly budget.",
    "investment_advisor.py": "Stock and crypto advice.",
    "crm_manager.py": "Manage customers.",
    "payroll_manager.py": "Manage payroll.",
    "ad_manager.py": "Manage FB/Google ads.",
    "analytics_dashboard.py": "Business analytics.",
    "lead_generator.py": "Find sales leads.",
    "contract_generator.py": "Legal contracts.",
    "accounting_manager.py": "Bookkeeping.",
    "expense_reporter.py": "Submit expenses.",
    "subscription_tracker.py": "Track subscriptions.",
    "crypto_trader.py": "Auto crypto trading.",
    "fundraising_helper.py": "Pitch decks.",
    "loan_calculator.py": "Calculate loans.",
    "inventory_manager.py": "Track stock.",
    "employee_manager.py": "HR employee management.",
    "profit_calculator.py": "P&L calculations.",
    "business_plan_generator.py": "Write business plans.",
    "grant_finder.py": "Find business grants.",
    "competitor_analyzer.py": "Analyse competitors.",

    # 11. LEGAL & COMPLIANCE [15]
    "document_signer.py": "E-sign documents.",
    "legal_research.py": "Research laws.",
    "policy_checker.py": "Check policies for compliance.",
    "nda_generator.py": "Generate NDAs.",
    "copyright_checker.py": "Check content copyright.",
    "contract_reviewer.py": "Legal contract review.",
    "gdpr_checker.py": "Check GDPR compliance.",
    "trademark_search.py": "Check trademarks.",
    "privacy_policy_generator.py": "Generate privacy policy.",
    "terms_generator.py": "Generate terms of service.",
    "lawsuit_tracker.py": "Track legal cases.",
    "legal_document_translator.py": "Translate legal docs.",
    "compliance_calendar.py": "Track compliance deadlines.",
    "patent_filer.py": "File patents.",
    "will_generator.py": "Generate wills.",

    # 12. IOT & SMART HOME [16]
    "smart_home.py": "Lights, AC and smart plugs.",
    "device_controller.py": "Control IoT devices.",
    "security_camera.py": "Monitor security cameras.",
    "voice_assistant_bridge.py": "Bridge to Alexa / Google Home.",
    "energy_monitor.py": "Monitor home energy.",
    "door_lock_manager.py": "Smart locks.",
    "thermostat_controller.py": "Climate control.",
    "plant_monitor.py": "Monitor and water plants.",
    "pet_feeder.py": "Feed pets automatically.",
    "smoke_detector.py": "Fire safety monitoring.",
    "leak_detector.py": "Water leak detection.",
    "garage_door.py": "Control garage door.",
    "robot_vacuum.py": "Control robot vacuum.",
    "weather_station.py": "Home weather data.",
    "irrigation_system.py": "Automatic watering.",
    "air_quality_monitor.py": "Monitor air quality.",
}

AUTOMATION = {
    "workflow_engine.py": "Execute multi-step workflows.",
    "workflow_builder.py": "Convert natural language to workflows.",
    "scheduler.py": "Run tasks at scheduled times.",
    "triggers.py": "Event-based workflow start.",
    "conditions.py": "IF/ELSE workflow logic.",
    "task_queue.py": "Manage job queues.",
    "recurring_tasks.py": "Daily and weekly routines.",
    "browser_automation.py": "Autonomous browser workflows.",
    "app_automation.py": "Automate desktop apps.",
    "desktop_automation.py": "Automate desktop operations.",
    "file_automation.py": "Auto-sort and organise files.",
    "email_automation.py": "Automated email workflows.",
    "data_entry_automation.py": "Move data between systems.",
    "document_automation.py": "Auto-generate documents.",
    "spreadsheet_automation.py": "Automate spreadsheet tasks.",
    "social_automation.py": "Automated social posting.",
    "finance_automation.py": "Automate finance tasks.",
    "report_generator.py": "Auto-generate reports.",
    "backup_automation.py": "Automatic backups.",
    "update_automation.py": "Automatic system updates.",
    "meeting_automation.py": "Automate meeting workflows.",
    "research_automation.py": "Automated research pipelines.",
    "content_automation.py": "Automated content creation.",
    "notification_automation.py": "Smart notifications.",
    "terminal_automation.py": "Automatically run commands.",
    "accounts_automation.py": "Manage user accounts.",
    "app_launch_automation.py": "Auto open and close apps.",
}

SMART_AGENTS = {
    "research_agent.py": "Research topics end to end.",
    "study_agent.py": "Learn and quiz a subject.",
    "work_agent.py": "Handle email and calendar.",
    "system_agent.py": "IT support and self-healing.",
    "travel_agent.py": "Book trips.",
    "shopping_agent.py": "Find deals.",
    "social_agent.py": "Manage social media.",
    "finance_agent.py": "Manage finances as CFO.",
    "health_agent.py": "Health advice as a doctor.",
    "legal_agent.py": "Legal help as a lawyer.",
    "content_agent.py": "Create content.",
    "news_agent.py": "Write news as a journalist.",
    "gaming_agent.py": "Coach and play games.",
    "hr_agent.py": "Recruiting and HR.",
    "sales_agent.py": "Close deals.",
    "marketing_agent.py": "Run campaigns.",
    "support_agent.py": "Customer support.",
    "data_agent.py": "Analyse data as a data scientist.",
    "iot_agent.py": "Manage the smart home.",
    "ceo_agent.py": "Strategic decisions.",
}

SENSORS = {
    "activity_monitor.py": "Track app and website usage.",
    "keystroke_analyzer.py": "Analyse typing patterns.",
    "screen_watcher.py": "Read the screen via OCR.",
    "audio_listener.py": "Wake-word audio listening.",
    "notification_watcher.py": "Read system notifications.",
    "file_system_watcher.py": "Watch folders for changes.",
    "biometric_sensor.py": "Heart-rate and face biometrics.",
    "context_engine.py": "Combine all sensor streams into context.",
    "emotion_detector.py": "Detect mood from voice and face.",
    "environment_sensor.py": "Room light, temperature and noise.",
    "gps_tracker.py": "GPS location tracking.",
    "network_sniffer.py": "Monitor network traffic.",
}

AUTONOMY = {
    "goal_manager.py": "Track long-term goals.",
    "decision_engine.py": "Decide whether to act.",
    "self_healing.py": "Auto-fix problems.",
    "routine_optimizer.py": "Optimise daily routine.",
    "interruption_manager.py": "Decide when to notify.",
    "focus_mode.py": "Block distractions.",
    "learning_loop.py": "Learn from feedback.",
    "prediction_engine.py": "Predict what the user needs.",
    "risk_assessor.py": "Assess action risks.",
    "ethics_guard.py": "Check ethics of actions.",
    "resource_allocator.py": "Allocate CPU and RAM.",
    "priority_manager.py": "Rank tasks by priority.",
}

SECURITY = {
    "permission_manager.py": "Manage permissions.",
    "safety_guard.py": "Block dangerous actions.",
    "audit_log.py": "Record all actions.",
    "privacy_filter.py": "Redact sensitive data.",
    "antivirus_scanner.py": "Scan for malware.",
    "password_manager.py": "Store passwords securely.",
    "vpn_manager.py": "Automatic VPN.",
    "firewall_manager.py": "Manage the firewall.",
    "intrusion_detector.py": "Detect intrusions.",
    "data_encryptor.py": "Encrypt data.",
    "backup_verifier.py": "Verify backups.",
    "compliance_auditor.py": "Compliance checks.",
}

INTEGRATIONS = {
    "os_bridge.py": "Deep operating-system control.",
    "app_bridge.py": "Chrome and VSCode APIs.",
    "driver_controller.py": "Hardware: GPU and fan control.",
    "device_sync.py": "Sync devices.",
    "smart_home.py": "Smart-home devices.",
    "cloud_api.py": "All cloud providers.",
    "payment_gateway.py": "Stripe and PayPal.",
    "ai_model_router.py": "Route to Gemini, Claude and GPT.",
    "notion_api.py": "Sync Notion notes.",
    "trello_api.py": "Trello task boards.",
    "slack_api.py": "Slack team chat.",
    "discord_api.py": "Discord server management.",
    "spotify_api.py": "Spotify music.",
    "youtube_api.py": "YouTube upload API.",
    "github_api.py": "GitHub repository management.",
}

AI_MODELS = {
    "llm_gemini.py": "Google Gemini model wrapper.",
    "llm_claude.py": "Anthropic Claude model wrapper.",
    "llm_gpt.py": "OpenAI GPT model wrapper.",
    "llm_llama.py": "Meta Llama model wrapper.",
    "vision_model.py": "Image understanding model.",
    "stt_model.py": "Speech-to-text model.",
    "tts_model.py": "Text-to-speech model.",
    "embedding_model.py": "Vector embedding model.",
    "fine_tune_manager.py": "Fine-tune custom models.",
    "model_evaluator.py": "Compare and evaluate models.",
}

MEMORY_FILES = [
    "user_profile.json",
    "conversation_history.db",
    "facts.json",
    "routines.db",
    "goals.db",
    "skills.db",
    "preferences.db",
    "knowledge_graph.db",
]

ALL_PACKAGES = [
    ("actions", ACTIONS),
    ("automation", AUTOMATION),
    ("smart_agents", SMART_AGENTS),
    ("sensors", SENSORS),
    ("autonomy", AUTONOMY),
    ("security", SECURITY),
    ("integrations", INTEGRATIONS),
    ("ai_models", AI_MODELS),
]


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #

def to_class_name(file_stem: str) -> str:
    """Convert a snake_case file stem to a PascalCase class name."""
    parts = file_stem.replace("-", "_").split("_")
    # Handle leading digits (e.g. "3d_model_generator")
    parts = [p if not p[0].isdigit() else "_" + p for p in parts if p]
    return "".join(word.capitalize() for word in parts)


def safe_stem(filename: str) -> str:
    return filename[:-3] if filename.endswith(".py") else filename


# --------------------------------------------------------------------------- #
# Templates
# --------------------------------------------------------------------------- #

TPL_MODULE = '''"""
{pkg} - {stem}
{bar}
{description}

Independent {pkg} module for the Autonomous Computer AI Assistant.
Implements the standard execute(task, context) capability contract.
"""

from typing import Any, Dict, Optional


class {class_name}:
    """{description}"""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {{}}
        self.name = "{stem}"
        self.description = "{description}"

    def execute(self, task: str, context: Optional[Dict[str, Any]] = None) -> Any:
        """Execute a task with this capability."""
        # TODO: implement {pkg}-specific logic
        return {{"module": self.name, "task": task, "status": "stub"}}

    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description
'''

TPL_AI_MODEL = '''"""
ai_models - {stem}
{bar}
{description}
"""

import os
from typing import Any, Dict, Optional


class {class_name}:
    """{description}"""

    def __init__(self, api_key: Optional[str] = None, config: Optional[Dict[str, Any]] = None):
        self.api_key = api_key or os.getenv("{env_var}", "")
        self.config = config or {{}}
        self.model = None
        self.available = bool(self.api_key)

    def execute(self, prompt: str, context: Optional[Dict[str, Any]] = None) -> str:
        """Run a prompt through the model."""
        if not self.available:
            return "{class_name}: no API key configured"
        # TODO: wire to real provider SDK
        return f"{{class_name}} stub response for: {{prompt[:80]}}"

    def is_available(self) -> bool:
        return self.available
'''

TPL_INIT_ACTIONS = '''"""
actions package - 166+ individual tools.

Auto-registers every action module found in this directory so the orchestrator
can discover and invoke capabilities by name without manual imports.
"""

import importlib
import pkgutil
from typing import Any, Dict

from . import *  # noqa: F401,F403  - ensure all submodules import

_REGISTRY: Dict[str, Any] = {{}}


def _register(name: str, instance: Any) -> None:
    _REGISTRY[name] = instance


def get_actions() -> Dict[str, Any]:
    """Return a name -> instance map of all registered actions."""
    if not _REGISTRY:
        _autodiscover()
    return _REGISTRY


def get_action(name: str) -> Any:
    """Return a single registered action by name."""
    if not _REGISTRY:
        _autodiscover()
    return _REGISTRY.get(name)


def _autodiscover() -> None:
    """Import every sibling module and register its main class."""
    for finder, modname, ispkg in pkgutil.iter_modules(__path__):
        if ispkg or modname.startswith("_"):
            continue
        try:
            module = importlib.import_module(f"{{__name__}}.{{modname}}")
        except Exception as exc:  # pragma: no cover - keep loading siblings
            continue
        cls = _find_capability_class(module)
        if cls is None:
            continue
        try:
            instance = cls()
        except Exception:
            continue
        _register(instance.get_name() if hasattr(instance, "get_name") else modname, instance)


def _find_capability_class(module: Any) -> Any:
    """Pick the first user-defined class in a module that looks like a capability."""
    import inspect
    for _name, obj in inspect.getmembers(module, inspect.isclass):
        if obj.__module__ == module.__name__ and not _name.startswith("_"):
            return obj
    return None
'''

TPL_INIT_GENERIC = '''"""
{pkg} package - {count} modules.

Auto-registers every module in this directory so the smart orchestrator can
discover capabilities by name without manual imports.
"""

import importlib
import inspect
import pkgutil
from typing import Any, Dict

from . import *  # noqa: F401,F403

_REGISTRY: Dict[str, Any] = {{}}


def get_modules() -> Dict[str, Any]:
    if not _REGISTRY:
        _autodiscover()
    return _REGISTRY


def get_module(name: str) -> Any:
    if not _REGISTRY:
        _autodiscover()
    return _REGISTRY.get(name)


def _autodiscover() -> None:
    for finder, modname, ispkg in pkgutil.iter_modules(__path__):
        if ispkg or modname.startswith("_"):
            continue
        try:
            module = importlib.import_module(f"{{__name__}}.{{modname}}")
        except Exception:
            continue
        for _name, obj in inspect.getmembers(module, inspect.isclass):
            if obj.__module__ == module.__name__ and not _name.startswith("_"):
                try:
                    instance = obj()
                except Exception:
                    continue
                key = instance.get_name() if hasattr(instance, "get_name") else modname
                _REGISTRY[key] = instance
                break
'''


# --------------------------------------------------------------------------- #
# Top-level file contents
# --------------------------------------------------------------------------- #

MAIN_PY = '''#!/usr/bin/env python3
"""
Autonomous Computer AI Assistant - main entry point.

Starts the smart orchestrator, all background daemons (sensors, autonomy,
security) and launches the text-based UI.

Usage:
    python main.py                     # interactive mode
    python main.py --task "..."        # single task mode
    python main.py --no-daemons        # skip background daemons
"""

import argparse
import sys
import threading
import time

from smart_orchestrator import SmartOrchestrator
from ui import TextUI


def parse_args():
    p = argparse.ArgumentParser(description="Autonomous Computer AI Assistant")
    p.add_argument("--task", "-t", type=str, default=None, help="Single task to execute")
    p.add_argument("--no-daemons", action="store_true", help="Skip background daemons")
    p.add_argument("--verbose", "-v", action="store_true", help="Verbose logging")
    return p.parse_args()


def start_daemons(orchestrator: SmartOrchestrator):
    """Spin up sensor / autonomy / security background loops."""
    daemons = []

    def loop(fn, name, interval):
        while True:
            try:
                fn()
            except Exception as exc:
                print(f"[daemon:{name}] error: {exc}", file=sys.stderr)
            time.sleep(interval)

    specs = [
        (getattr(orchestrator.sensors, "poll_all", lambda: None), "sensors", 30),
        (getattr(orchestrator.autonomy, "tick", lambda: None), "autonomy", 15),
        (getattr(orchestrator.security, "audit_tick", lambda: None), "security", 60),
    ]
    for fn, name, interval in specs:
        t = threading.Thread(target=loop, args=(fn, name, interval), daemon=True, name=f"daemon-{name}")
        t.start()
        daemons.append(t)
    print("[main] background daemons started:", [d.name for d in daemons])
    return daemons


def main():
    args = parse_args()
    orchestrator = SmartOrchestrator()

    if not args.no_daemons:
        start_daemons(orchestrator)

    if args.task:
        result = orchestrator.run(args.task)
        print(f"\\nAssistant: {result}\\n")
        return

    ui = TextUI(orchestrator)
    ui.run()


if __name__ == "__main__":
    main()
'''

UI_PY = '''#!/usr/bin/env python3
"""Text-based UI for the Autonomous Computer AI Assistant."""

import sys

try:
    from rich.console import Console
    from rich.panel import Panel

    _CONSOLE = Console()
    _HAS_RICH = True
except ImportError:
    _CONSOLE = None
    _HAS_RICH = False


def _print(text: str):
    if _HAS_RICH:
        _CONSOLE.print(Panel.fit(text, title="Assistant"))
    else:
        print(f"\\nAssistant: {text}\\n")


class TextUI:
    """Simple REPL that drives the smart orchestrator."""

    BANNER = (
        "=" * 60
        + "\\n  Autonomous Computer AI Assistant\\n"
        + "  Gemini 2.5 Flash (reasoning) + Gemini 1.5 Flash (processing)\\n"
        + "  Type 'exit' to quit\\n"
        + "=" * 60
    )

    def __init__(self, orchestrator):
        self.orchestrator = orchestrator

    def run(self):
        print(self.BANNER)
        while True:
            try:
                user_input = input("\\nYou: ").strip()
            except (EOFError, KeyboardInterrupt):
                print("\\nShutting down.")
                break
            if not user_input:
                continue
            if user_input.lower() in {"exit", "quit", "bye"}:
                print("Shutting down.")
                break
            try:
                result = self.orchestrator.run(user_input)
            except Exception as exc:
                result = f"I hit an error: {exc}"
            _print(result)


if __name__ == "__main__":
    from smart_orchestrator import SmartOrchestrator

    TextUI(SmartOrchestrator()).run()
'''

SETUP_PY = '''#!/usr/bin/env python3
"""
setup.py - installs dependencies, creates runtime directories, checks perms.

Run:  python setup.py
"""

import os
import subprocess
import sys
from pathlib import Path

REQUIREMENTS = [
    "loguru>=0.7.0",
    "pyyaml>=6.0",
    "requests>=2.31.0",
    "google-generativeai>=0.8.0",
    "litellm>=1.0.0",
    "rich>=13.0.0",
    "psutil>=5.9.0",
]

RUNTIME_DIRS = ["memory", "logs", "config", "core"]


def install_deps():
    print("[setup] installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", *REQUIREMENTS])


def ensure_dirs(root: Path):
    for d in RUNTIME_DIRS:
        (root / d).mkdir(parents=True, exist_ok=True)
        print(f"[setup] ensured directory: {d}")


def ensure_secrets(root: Path):
    keys_file = root / "config" / "api_keys.json"
    if not keys_file.exists():
        import json as _json
        template = {
            "GEMINI_API_KEY": "",
            "ANTHROPIC_API_KEY": "",
            "OPENAI_API_KEY": "",
            "GOOGLE_API_KEY": "",
        }
        keys_file.write_text(_json.dumps(template, indent=2) + "\\n")
        print("[setup] created config/api_keys.json template")


def main():
    root = Path(__file__).resolve().parent
    ensure_dirs(root)
    ensure_secrets(root)
    try:
        install_deps()
    except subprocess.CalledProcessError as exc:
        print(f"[setup] dependency install failed: {exc}", file=sys.stderr)
    print("[setup] done. Set your API keys in config/api_keys.json then run: python main.py")


if __name__ == "__main__":
    main()
'''

ORCHESTRATOR_PY = '''#!/usr/bin/env python3
"""
orchestrator.py - LLM planner.

Breaks a high-level objective into concrete, executable steps and hands each
step to the smart orchestrator for routing to a capability.
"""

import json
import os
from typing import Any, Dict, List, Optional


class Orchestrator:
    """Plans multi-step tasks using the reasoning LLM."""

    def __init__(self, model_router: Any = None):
        self.model_router = model_router

    def _reason(self, prompt: str) -> str:
        if self.model_router is None:
            return prompt
        try:
            return self.model_router.reason(prompt)
        except Exception:
            return prompt

    def plan(self, objective: str, context: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Return an ordered list of step dicts: {step, capability, args}."""
        ctx = json.dumps(context or {})
        prompt = (
            "Break the following objective into a numbered list of concrete steps. "
            "For each step suggest which capability should perform it.\\n\\n"
            f"Objective: {objective}\\nContext: {ctx}\\n\\n"
            "Return JSON like: [{\\"step\\": \\"...\\", \\"capability\\": \\"...\\", \\"args\\": \\"...\\"}]"
        )
        text = self._reason(prompt)
        steps = self._parse_steps(text, objective)
        return steps

    def _parse_steps(self, text: str, objective: str) -> List[Dict[str, Any]]:
        steps: List[Dict[str, Any]] = []
        for line in text.splitlines():
            stripped = line.strip()
            if not stripped or not (stripped[0].isdigit() or stripped.startswith(("- ", "* "))):
                continue
            steps.append({"step": stripped, "capability": None, "args": None})
        if not steps:
            steps.append({"step": objective, "capability": None, "args": None})
        return steps
'''

SMART_ORCHESTRATOR_PY = '''#!/usr/bin/env python3
"""
smart_orchestrator.py - the central brain.

Wires together the AI model router, all action tools, the workflow/automation
engine, smart agents, sensors, autonomy, security and integrations. Routes a
natural-language objective through planning -> capability execution -> response.
"""

import json
import os
import re
from typing import Any, Dict, List, Optional

from orchestrator import Orchestrator

import actions
import automation
import smart_agents
import sensors
import autonomy
import security
import integrations
import ai_models


CAPABILITY_KEYWORDS: Dict[str, List[str]] = {
    "actions.web_search": ["search", "google", "look up", "find online"],
    "actions.url_launcher": ["open url", "open website", "open link", "go to"],
    "actions.file_controller": ["create file", "move file", "copy file", "delete file"],
    "actions.terminal_manager": ["run command", "terminal", "shell", "bash"],
    "actions.system_monitor": ["system status", "cpu", "ram", "monitor"],
    "actions.screenshot": ["screenshot", "capture screen"],
    "actions.music_player": ["play music"],
    "actions.calendar_manager": ["schedule", "calendar", "meeting"],
    "actions.gmail_sender": ["send email", "email"],
    "actions.reminder": ["remind me", "reminder"],
    "actions.weather_report": ["weather", "forecast"],
    "actions.translation_service": ["translate"],
    "actions.qr_generator": ["qr code"],
}


class SmartOrchestrator:
    """Central brain that routes objectives to the right capabilities."""

    def __init__(self):
        # AI layer
        self.ai_models = ai_models.get_modules()
        self.model_router = integrations.get_module("ai_model_router") or _FallbackRouter()
        self.integrations = integrations.get_modules()

        # Capability layers
        self.actions = actions.get_actions()
        self.automation = automation.get_modules()
        self.smart_agents = smart_agents.get_modules()
        self.sensors = sensors.get_modules()
        self.autonomy = autonomy.get_modules()
        self.security = security.get_modules()

        # Planner
        self.planner = Orchestrator(model_router=self.model_router)

        print(
            f"[orchestrator] loaded "
            f"actions={len(self.actions)} automation={len(self.automation)} "
            f"agents={len(self.smart_agents)} sensors={len(self.sensors)} "
            f"autonomy={len(self.autonomy)} security={len(self.security)} "
            f"integrations={len(self.integrations)} ai_models={len(self.ai_models)}"
        )

    # -- public API ---------------------------------------------------------

    def run(self, objective: str) -> str:
        """Plan and execute an objective end to end."""
        steps = self.planner.plan(objective)
        results: List[str] = []
        for step in steps:
            capability = self._route(step)
            outcome = self._execute(capability, step.get("step", str(step)))
            results.append(outcome)
        return self._summarize(objective, results)

    # -- routing ------------------------------------------------------------

    def _route(self, step: Dict[str, Any]) -> Optional[Any]:
        text = (step.get("step") or "").lower()
        # explicit hint from planner
        hint = step.get("capability")
        if hint:
            found = self.actions.get(hint) or self.automation.get(hint)
            if found:
                return found
        for cap_key, keywords in CAPABILITY_KEYWORDS.items():
            if any(kw in text for kw in keywords):
                pkg, _, name = cap_key.partition(".")
                registry = {"actions": self.actions, "automation": self.automation}.get(pkg, {})
                if name in registry:
                    return registry[name]
        return None

    def _execute(self, capability: Any, task: str) -> str:
        if capability is None:
            # fall back to the reasoning model
            return self.model_router.reason(task)
        try:
            result = capability.execute(task)
            if isinstance(result, dict):
                return result.get("status", json.dumps(result))
            return str(result)
        except Exception as exc:
            return f"capability error: {exc}"

    def _summarize(self, objective: str, results: List[str]) -> str:
        if len(results) == 1:
            return results[0]
        joined = " | ".join(results)
        try:
            return self.model_router.summarize(joined)
        except Exception:
            return joined


class _FallbackRouter:
    """Minimal stand-in used when no AI model router is configured."""

    def reason(self, prompt: str) -> str:
        return prompt

    def summarize(self, text: str) -> str:
        return text
'''

PROMPT_TXT = '''You are an advanced Autonomous Computer AI Assistant.

Personality rules:
- Be concise, direct and helpful.
- Plan multi-step objectives, then execute each step using the best available capability.
- Prefer the fastest capable tool; escalate to heavier reasoning only when needed.
- Never perform destructive actions without confirmation.
- Protect user privacy: never log or echo secrets, keys or personal data.
- When unsure, ask a clarifying question instead of guessing.

Reasoning engine: Gemini 2.5 Flash (planning, analysis, decisions).
Processing engine: Gemini 1.5 Flash (extraction, summarisation, fast lookup).
'''

API_KEYS_JSON = (
    "{\n"
    '  "GEMINI_API_KEY": "",\n'
    '  "ANTHROPIC_API_KEY": "",\n'
    '  "OPENAI_API_KEY": "",\n'
    '  "GOOGLE_API_KEY": "",\n'
    '  "REPLICATE_API_KEY": "",\n'
    '  "HUGGINGFACE_API_KEY": "",\n'
    '  "DISCORD_BOT_TOKEN": "",\n'
    '  "SLACK_BOT_TOKEN": "",\n'
    '  "NOTION_INTEGRATION_KEY": "",\n'
    '  "GITHUB_TOKEN": "",\n'
    '  "STRIPE_SECRET_KEY": "",\n'
    '  "SPOTIFY_CLIENT_ID": "",\n'
    '  "SPOTIFY_CLIENT_SECRET": "",\n'
    '  "YOUTUBE_API_KEY": "",\n'
    '  "TRELLO_API_KEY": ""\n'
    "}\n"
)


# --------------------------------------------------------------------------- #
# Builders
# --------------------------------------------------------------------------- #

def build_module_file(pkg: str, filename: str, description: str) -> str:
    stem = safe_stem(filename)
    class_name = to_class_name(stem)
    bar = "=" * (len(pkg) + len(stem) + 4)
    if pkg == "ai_models":
        env_var = {
            "llm_gemini": "GEMINI_API_KEY",
            "llm_claude": "ANTHROPIC_API_KEY",
            "llm_gpt": "OPENAI_API_KEY",
            "llm_llama": "HUGGINGFACE_API_KEY",
            "vision_model": "GOOGLE_API_KEY",
            "stt_model": "GOOGLE_API_KEY",
            "tts_model": "GOOGLE_API_KEY",
            "embedding_model": "GOOGLE_API_KEY",
            "fine_tune_manager": "OPENAI_API_KEY",
            "model_evaluator": "OPENAI_API_KEY",
        }.get(stem, "API_KEY")
        return TPL_AI_MODEL.format(
            pkg=pkg, stem=stem, class_name=class_name, bar=bar,
            description=description, env_var=env_var,
        ).replace("{class_name}: no API key configured", "{class_name}: no API key configured")
    return TPL_MODULE.format(
        pkg=pkg, stem=stem, class_name=class_name, bar=bar,
        description=description,
    )


def build_package(pkg: str, files: Dict[str, str]):
    pkg_dir = ROOT / pkg
    pkg_dir.mkdir(parents=True, exist_ok=True)

    # __init__.py
    if pkg == "actions":
        init_text = TPL_INIT_ACTIONS.format(pkg=pkg, count=len(files))
    else:
        init_text = TPL_INIT_GENERIC.format(pkg=pkg, count=len(files))
    (pkg_dir / "__init__.py").write_text(init_text)

    # module files
    for filename, description in files.items():
        content = build_module_file(pkg, filename, description)
        (pkg_dir / filename).write_text(content)


def build_memory():
    mem_dir = ROOT / "memory"
    mem_dir.mkdir(parents=True, exist_ok=True)
    # JSON stores get real (empty) JSON; DB stores get a marker file.
    for fname in MEMORY_FILES:
        path = mem_dir / fname
        if fname.endswith(".json"):
            path.write_text("{}\n")
        else:
            # .db files are binary; create an empty SQLite database if sqlite3 is available,
            # otherwise leave a placeholder so the path exists for tooling.
            try:
                import sqlite3
                conn = sqlite3.connect(str(path))
                conn.execute("CREATE TABLE IF NOT EXISTS entries (id INTEGER PRIMARY KEY, key TEXT, value TEXT)")
                conn.commit()
                conn.close()
            except Exception:
                path.write_text("# sqlite database placeholder\n")


def build_top_level():
    (ROOT / "main.py").write_text(MAIN_PY)
    (ROOT / "ui.py").write_text(UI_PY)
    (ROOT / "setup.py").write_text(SETUP_PY)
    (ROOT / "orchestrator.py").write_text(ORCHESTRATOR_PY)
    (ROOT / "smart_orchestrator.py").write_text(SMART_ORCHESTRATOR_PY)

    core_dir = ROOT / "core"
    core_dir.mkdir(parents=True, exist_ok=True)
    (core_dir / "prompt.txt").write_text(PROMPT_TXT)
    (core_dir / "__init__.py").write_text('"""core package - system prompt and shared constants."""\n')

    config_dir = ROOT / "config"
    config_dir.mkdir(parents=True, exist_ok=True)
    (config_dir / "api_keys.json").write_text(API_KEYS_JSON)


def build_readme():
    total = sum(len(files) for _, files in ALL_PACKAGES)
    readme = f"""# Autonomous Computer AI Assistant

Capability-based source code architecture. One capability = one source code module.

## Top-level files

| File | Role |
|------|------|
| `main.py` | Entry point; starts AI + all daemons |
| `ui.py` | Text-based Python UI |
| `setup.py` | Installs dependencies, sets up permissions and runtime dirs |
| `orchestrator.py` | LLM planner that breaks tasks into steps |
| `smart_orchestrator.py` | Central brain that routes to everything |

## Packages

| Package | Modules | Purpose |
|---------|--------|---------|
| `actions/` | {len(ACTIONS)} | Individual tools (system, files, web, media, comms, finance, legal, IoT, ...) |
| `automation/` | {len(AUTOMATION)} | Workflow modules |
| `smart_agents/` | {len(SMART_AGENTS)} | High-level role-based agents |
| `sensors/` | {len(SENSORS)} | Perception modules |
| `autonomy/` | {len(AUTONOMY)} | Decision modules |
| `security/` | {len(SECURITY)} | Safety modules |
| `integrations/` | {len(INTEGRATIONS)} | Connection modules |
| `ai_models/` | {len(AI_MODELS)} | AI model wrappers |
| `memory/` | {len(MEMORY_FILES)} | Data stores |
| `core/` | 1 | System prompt |
| `config/` | 1 | API keys |

**Total modules: {total}**

## AI engine

Powered exclusively by Google Gemini models:
- **Gemini 2.5 Flash** - reasoning, planning, autonomous decisions
- **Gemini 1.5 Flash** - fast processing, extraction, summarisation

The `integrations/ai_model_router.py` can also route to Claude / GPT / Llama.

## Quick start

```bash
python setup.py            # install deps + create runtime dirs/secrets
# edit config/api_keys.json with your keys
python main.py             # interactive mode
python main.py --task "Search the web for today's top AI news"
```

## Architecture

Every module in `actions/`, `automation/`, `smart_agents/`, `sensors/`,
`autonomy/`, `security/`, `integrations/` and `ai_models/` is fully
independent and exposes the standard `execute(task, context)` contract.
Each package `__init__.py` auto-registers its modules, so the smart
orchestrator discovers capabilities at runtime without manual imports.

## License

MIT License
"""
    (ROOT / "README_STRUCTURE.md").write_text(readme)


def main():
    build_top_level()
    for pkg, files in ALL_PACKAGES:
        build_package(pkg, files)
        print(f"[build] {pkg}: {len(files)} modules")
    build_memory()
    print(f"[build] memory: {len(MEMORY_FILES)} stores")
    build_readme()
    total = sum(len(files) for _, files in ALL_PACKAGES)
    print(f"[build] done. {total} modules + top-level files created.")


if __name__ == "__main__":
    main()
