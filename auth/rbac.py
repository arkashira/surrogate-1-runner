class RoleBasedAccessControl:
    def __init__(self):
        self.roles = {
            'admin': ['admin', 'engineer', 'read-only'],
            'engineer': ['engineer', 'read-only'],
            'read-only': ['read-only']
        }

    def check_access(self, user_role, required_permission):
        return required_permission in self.roles.get(user_role, [])

def integrate_with_existing_rbac_system():
    # Assuming there is an existing function called get_user_role() which returns the user's role
    user_role = get_user_role()
    rbac = RoleBasedAccessControl()

    # Check if the user has the required permission for shell access
    if rbac.check_access(user_role, 'shell_access'):
        print("User has shell access.")
    else:
        print("User does not have shell access.")

def display_access_permissions_in_dashboard():
    user_role = get_user_role()
    rbac = RoleBasedAccessControl()

    print(f"User Role: {user_role}")
    print("Access Permissions:")
    for permission in rbac.roles.get(user_role, []):
        print(f"- {permission}")

# Example usage
integrate_with_existing_rbac_system()
display_access_permissions_in_dashboard()