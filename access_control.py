import json
import os
from functools import wraps

class AccessControl:
    def __init__(self, roles_file='roles.json'):
        self.roles_file = roles_file
        self.roles = self._load_roles()

    def _load_roles(self):
        try:
            with open(self.roles_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save_roles(self):
        with open(self.roles_file, 'w') as f:
            json.dump(self.roles, f, indent=4)

    def add_role(self, role_name, permissions):
        self.roles[role_name] = permissions
        self._save_roles()

    def remove_role(self, role_name):
        if role_name in self.roles:
            del self.roles[role_name]
            self._save_roles()

    def assign_role(self, user_id, role_name):
        if role_name not in self.roles:
            raise ValueError(f"Role {role_name} does not exist")

        user_roles = self._get_user_roles(user_id)
        if role_name not in user_roles:
            user_roles.append(role_name)
            self._save_user_roles(user_id, user_roles)

    def remove_role_from_user(self, user_id, role_name):
        user_roles = self._get_user_roles(user_id)
        if role_name in user_roles:
            user_roles.remove(role_name)
            self._save_user_roles(user_id, user_roles)

    def _get_user_roles(self, user_id):
        roles_file = f'user_roles/{user_id}.json'
        try:
            with open(roles_file, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []

    def _save_user_roles(self, user_id, roles):
        os.makedirs('user_roles', exist_ok=True)
        with open(f'user_roles/{user_id}.json', 'w') as f:
            json.dump(roles, f)

    def check_permission(self, user_id, permission):
        user_roles = self._get_user_roles(user_id)
        for role in user_roles:
            if role in self.roles and permission in self.roles[role]:
                return True
        return False

    def enforce_access(self, user_id, permission):
        def decorator(f):
            @wraps(f)
            def wrapped(*args, **kwargs):
                if self.check_permission(user_id, permission):
                    return f(*args, **kwargs)
                else:
                    raise PermissionError(f"User {user_id} does not have permission to {permission}")
            return wrapped
        return decorator