"""Access control: role-based system access for identity management."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set


@dataclass
class Role:
    name: str
    permissions: Set[str] = field(default_factory=set)


@dataclass
class User:
    username: str
    role: str
    active: bool = True


class AccessControl:
    """Minimal RBAC for biometric/identity operations."""

    def __init__(self) -> None:
        self.roles: Dict[str, Role] = {
            "admin": Role("admin", {"read", "write", "enroll", "delete", "export", "audit"}),
            "operator": Role("operator", {"read", "enroll", "export"}),
            "viewer": Role("viewer", {"read"}),
        }
        self.users: Dict[str, User] = {}

    def add_user(self, username: str, role: str) -> User:
        if role not in self.roles:
            raise ValueError(f"Unknown role '{role}'")
        user = User(username, role)
        self.users[username] = user
        return user

    def can(self, username: str, permission: str) -> bool:
        user = self.users.get(username)
        if not user or not user.active:
            return False
        role = self.roles.get(user.role)
        return role is not None and permission in role.permissions

    def require(self, username: str, permission: str) -> None:
        if not self.can(username, permission):
            raise PermissionError(f"User '{username}' lacks permission '{permission}'")
