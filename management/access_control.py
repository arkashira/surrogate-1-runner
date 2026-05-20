def check_user_subscription(user_id):
    # Dummy implementation: Replace with actual subscription checking logic
    return True  # Return True for paid users, False for non-paid users

def restrict_non_paid_users(func):
    def wrapper(*args, **kwargs):
        user_id = kwargs.get('user_id')  # Assuming user_id is passed as a keyword argument
        if not check_user_subscription(user_id):
            raise PermissionError("Access denied for non-paid users.")
        return func(*args, **kwargs)
    return wrapper

@restrict_non_paid_users
def access_full_functionality(user_id):
    print(f"User {user_id} has access to full functionality.")

# Example usage:
try:
    access_full_functionality(user_id='123')
except PermissionError as e:
    print(e)

# Test cases
def test_access_control():
    try:
        access_full_functionality(user_id='paid_user')
        print("Test passed for paid user")
    except Exception as e:
        print(f"Test failed for paid user: {e}")

    try:
        access_full_functionality(user_id='non_paid_user')
        print("Test failed for non-paid user: Access should be denied")
    except PermissionError:
        print("Test passed for non-paid user")

test_access_control()