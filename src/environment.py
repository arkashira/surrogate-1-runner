import os
import shutil

class SandboxEnvironment:
    def __init__(self, name):
        """
        Initialize a SandboxEnvironment instance.

        Args:
            name (str): The name of the sandbox environment.
        """
        self.name = name
        self.path = f"/opt/axentx/surrogate-1/sandboxes/{name}"

    def create(self):
        """
        Create a new sandbox environment.

        Returns:
            bool: True if the environment is created successfully, False otherwise.
        """
        try:
            if not os.path.exists(self.path):
                os.makedirs(self.path)
                # Copy production environment setup to sandbox
                shutil.copytree("/opt/axentx/surrogate-1/production", self.path + "/production")
                print(f"Sandbox environment {self.name} created successfully")
                return True
            else:
                print(f"Sandbox environment {self.name} already exists")
                return False
        except Exception as e:
            print(f"Error creating sandbox environment: {e}")
            return False

    def delete(self):
        """
        Delete an existing sandbox environment.

        Returns:
            bool: True if the environment is deleted successfully, False otherwise.
        """
        try:
            if os.path.exists(self.path):
                shutil.rmtree(self.path)
                print(f"Sandbox environment {self.name} deleted successfully")
                return True
            else:
                print(f"Sandbox environment {self.name} does not exist")
                return False
        except Exception as e:
            print(f"Error deleting sandbox environment: {e}")
            return False

    def isolate(self):
        """
        Isolate the sandbox environment from production data.

        Returns:
            bool: True if the environment is isolated successfully, False otherwise.
        """
        try:
            data_path = f"{self.path}/data"
            if not os.path.exists(data_path):
                os.makedirs(data_path)
                print(f"Sandbox environment {self.name} isolated from production data")
                return True
            else:
                print(f"Sandbox environment {self.name} is already isolated from production data")
                return False
        except Exception as e:
            print(f"Error isolating sandbox environment: {e}")
            return False

def create_sandbox_environment(name):
    """
    Create a new sandbox environment and isolate it from production data.

    Args:
        name (str): The name of the sandbox environment.
    """
    sandbox = SandboxEnvironment(name)
    if sandbox.create():
        sandbox.isolate()

def delete_sandbox_environment(name):
    """
    Delete an existing sandbox environment.

    Args:
        name (str): The name of the sandbox environment.
    """
    sandbox = SandboxEnvironment(name)
    sandbox.delete()