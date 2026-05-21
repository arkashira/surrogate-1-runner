
from typing import Dict, List
from axentx.common.models import UserRole

class RBAC:
    def __init__(self):
        self.roles: Dict[str, List[str]] = {
            UserRole.ADMIN: ['access_all', 'manage_users'],
            UserRole.MODERATOR: ['access_own', 'manage_own'],
            UserRole.USER: ['access_own'],
        }

    def can_access(self, user_role: UserRole, resource: str) -> bool:
        return resource in self.roles.get(user_role, [])

    def can_perform_action(self, user_role: UserRole, action: str) -> bool:
        return any(action in role_actions for role_actions in self.roles.values())