class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

class UserManager:
    def __init__(self):
        self.users = []

    def add_user(self, user):
        self.users.append(user)

    def get_users(self):
        return self.users

    def authenticate_user(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                return True
        return False

def main():
    user_manager = UserManager()
    user1 = User("user1", "password1")
    user2 = User("user2", "password2")
    user_manager.add_user(user1)
    user_manager.add_user(user2)
    print(user_manager.get_users())

if __name__ == "__main__":
    main()