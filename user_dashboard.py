from auth.rbac import RoleBasedAccessControl

def show_user_dashboard():
    user_role = get_user_role()
    rbac = RoleBasedAccessControl()

    print("User Dashboard")
    print("--------------")
    print(f"Your Role: {user_role}")
    print("Your Access Permissions:")
    for permission in rbac.roles.get(user_role, []):
        print(f"- {permission}")

# Example usage
show_user_dashboard()