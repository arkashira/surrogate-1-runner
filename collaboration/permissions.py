from enum import Enum
from typing import List

class Role(Enum):
    VIEWER = 'viewer'
    COLLABORATOR = 'collaborator'

class PermissionError(Exception):
    pass

def validate_credentials(credentials: dict) -> bool:
    # Placeholder for credential validation logic
    return True

def check_role_permission(role: Role, command: str) -> None:
    if role == Role.VIEWER and command != 'observe':
        raise PermissionError("Viewer role cannot execute commands.")
    elif role == Role.COLLABORATOR:
        # Log the command execution for auditing
        print(f"Command executed by collaborator: {command}")
    else:
        raise PermissionError("Invalid role.")

def invite_collaborator(credentials: dict, role: Role) -> None:
    if not validate_credentials(credentials):
        raise PermissionError("Invalid credentials.")
    
    print(f"Collaborator invited with role: {role.value}")

# Example usage
if __name__ == "__main__":
    try:
        invite_collaborator({'username': 'test', 'password': 'secret'}, Role.COLLABORATOR)
        check_role_permission(Role.COLLABORATOR, 'execute_command')
        check_role_permission(Role.VIEWER, 'observe')
    except PermissionError as e:
        print(e)