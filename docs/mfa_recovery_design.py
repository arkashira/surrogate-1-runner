class MFARecoveryProcess:
    def __init__(self):
        self.recovery_methods = {
            "sms": self.sms_recovery,
            "email": self.email_recovery,
            "authenticator_app": self.authenticator_app_recovery
        }

    def sms_recovery(self):
        # Send a recovery code to the user's phone number
        print("Sending recovery code to phone number")

    def email_recovery(self):
        # Send a recovery code to the user's email address
        print("Sending recovery code to email address")

    def authenticator_app_recovery(self):
        # Generate a recovery code and display it to the user
        print("Generating recovery code for authenticator app")

    def start_recovery(self, method):
        if method in self.recovery_methods:
            self.recovery_methods[method]()
        else:
            print("Invalid recovery method")

def main():
    recovery_process = MFARecoveryProcess()
    recovery_process.start_recovery("sms")

if __name__ == "__main__":
    main()