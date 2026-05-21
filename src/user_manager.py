from audit_logger import AuditLogger

class UserManager:
    def __init__(self):
        self.audit_logger = AuditLogger()

    def add_user(self, user_id, role):
        self.audit_logger.log_action(user_id, 'add_user', f'Role: {role}')

    def remove_user(self, user_id):
        self.audit_logger.log_action(user_id, 'remove_user', '')

    def modify_user_role(self, user_id, new_role):
        self.audit_logger.log_action(user_id, 'modify_user_role', f'New Role: {new_role}')