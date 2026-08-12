"""Dynamic mock server for external API dependencies."""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any


@dataclass
class MockEndpoint:
    method: str  # GET, POST, ...
    path: str
    status: int = 200
    response: dict[str, Any] = field(default_factory=dict)
    delay_ms: int = 0


@dataclass
class MockServer:
    endpoints: list[MockEndpoint] = field(default_factory=list)
    requests: list[dict[str, Any]] = field(default_factory=list)

    def add(self, endpoint: MockEndpoint) -> None:
        self.endpoints.append(endpoint)

    def match(self, method: str, path: str) -> MockEndpoint | None:
        for ep in self.endpoints:
            if ep.method.upper() == method.upper() and ep.path == path:
                self.requests.append({"method": method, "path": path})
                return ep
        return None

    def respond(self, method: str, path: str) -> tuple[int, dict[str, Any]]:
        ep = self.match(method, path)
        if not ep:
            self.requests.append({"method": method, "path": path, "miss": True})
            return 404, {"error": "not found"}
        return ep.status, ep.response

    def as_wsgi(self):  # pragma: no cover - needs a WSGI server
        server = self

        def application(environ, start_response):
            method = environ.get("REQUEST_METHOD", "GET")
            path = environ.get("PATH_INFO", "/")
            status, body = server.respond(method, path)
            data = json.dumps(body).encode("utf-8")
            start_response(f"{status} OK", [("Content-Type", "application/json")])
            return [data]

        return application

    def reset(self) -> None:
        self.requests.clear()
