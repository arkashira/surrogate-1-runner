import os
from tool_setup import ToolSetup

class SetupWizard:
    def __init__(self):
        self.tool_setup = ToolSetup()
        self.selected_tools = []
    
    def run(self):
        print("🚀 Welcome to AxentX Tool Setup Wizard!")
        print("This will take less than 5 minutes. Let's get you started...")
        
        if not self.select_tools():
            return False
        if not self.configure_settings():
            return False
        if not self.finalize_setup():
            return False
            
        print("\n✅ Setup complete! Your tools are ready to use.")
        return True
    
    def select_tools(self):
        print("\n1️⃣ Step 1: Select Tools")
        print("Available tools:")
        for i, tool in enumerate(self.tool_setup.available_tools, 1):
            print(f"  {i}. {tool['name']} - {tool['description']}")
            
        while True:
            choice = input("\nEnter numbers separated by spaces (or 'q' to quit): ")
            if choice.lower() == 'q':
                return False
                
            try:
                indices = [int(x)-1 for x in choice.split()]
                self.selected_tools = [self.tool_setup.available_tools[i] for i in indices if 0 <= i < len(self.tool_setup.available_tools)]
                return True
            except:
                print("❌ Invalid selection. Try again.")

    def configure_settings(self):
        print("\n2️⃣ Step 2: Configure Settings")
        # Add actual configuration logic here
        return True
    
    def finalize_setup(self):
        print("\n3️⃣ Step 3: Finalizing Setup")
        for tool in self.selected_tools:
            print(f"Installing {tool['name']}...")
            self.tool_setup.install_tool(tool['name'])
        return True

if __name__ == "__main__":
    wizard = SetupWizard()
    wizard.run()