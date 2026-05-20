import os

def check_java_dependency():
    # Check if Java is installed
    java_path = os.environ.get("JAVA_HOME")
    if java_path is None:
        return False
    return True

def get_alternative_solution():
    # Return alternative solution to Java dependency
    return "freerouter-native"