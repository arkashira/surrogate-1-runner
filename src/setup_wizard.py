import sys
from tool_setup import setup_tools, display_tooltips

def main():
    print("Welcome to the AxentX Setup Wizard!")
    print("This process will guide you through setting up your tools.\n")

    # Step 1: Introduction
    print("Step 1: Introduction")
    print("-------------------")
    print("The setup process will take less than 5 minutes.")
    print("You will be guided through each step with clear instructions.\n")
    input("Press Enter to continue...")

    # Step 2: Tool Setup
    print("\nStep 2: Tool Setup")
    print("------------------")
    print("We will now set up the necessary tools for you.")
    print("Follow the on-screen instructions.\n")
    setup_tools()

    # Step 3: Tooltips and Instructions
    print("\nStep 3: Tooltips and Instructions")
    print("-------------------------------")
    print("Here are some helpful tooltips to get you started:")
    display_tooltips()

    # Step 4: Completion
    print("\nStep 4: Completion")
    print("------------------")
    print("Congratulations! Your tools have been set up successfully.")
    print("You can now start creating content right away.\n")

if __name__ == "__main__":
    main()