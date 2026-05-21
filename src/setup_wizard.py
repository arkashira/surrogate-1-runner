import os
import time

def setup_surrogate_1():
    print("Welcome to the Surrogate-1 setup wizard!")
    print("This process should take less than 15 minutes.")
    
    # Step 1: Install dependencies
    print("Installing dependencies...")
    os.system("pip install -r requirements.txt")
    
    # Step 2: Configure environment variables
    print("Configuring environment variables...")
    os.environ["SURROGATE_1_DATA_DIR"] = "/path/to/data"
    os.environ["SURROGATE_1_MODEL_DIR"] = "/path/to/model"
    
    # Step 3: Initialize database
    print("Initializing database...")
    os.system("python init_db.py")
    
    # Step 4: Run setup script
    print("Running setup script...")
    os.system("python setup.py")
    
    print("Setup complete! Please restart the service.")
    
def main():
    start_time = time.time()
    setup_surrogate_1()
    end_time = time.time()
    print(f"Setup took {end_time - start_time} seconds.")

if __name__ == "__main__":
    main()