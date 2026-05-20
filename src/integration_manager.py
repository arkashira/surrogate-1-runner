import subprocess
import json

class IntegrationManager:
    def __init__(self, user_id):
        self.user_id = user_id
        self.integrations_file = f"/opt/axentx/surrogate-1/data/integrations_{user_id}.json"
        self.load_integrations()

    def load_integrations(self):
        try:
            with open(self.integrations_file, 'r') as file:
                self.integrations_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.integrations_data = {
                'tools': [],
                'last_updated': None
            }

    def save_integrations(self):
        with open(self.integrations_file, 'w') as file:
            json.dump(self.integrations_data, file, indent=4)

    def add_integration(self, tool_name, tool_config):
        self.integrations_data['tools'].append({
            'name': tool_name,
            'config': tool_config
        })
        self.save_integrations()

    def remove_integration(self, tool_name):
        self.integrations_data['tools'] = [tool for tool in self.integrations_data['tools'] if tool['name'] != tool_name]
        self.save_integrations()

    def get_integrations(self):
        return self.integrations_data

    def run_integration(self, tool_name, command):
        tool = next((tool for tool in self.integrations_data['tools'] if tool['name'] == tool_name), None)
        if tool:
            try:
                result = subprocess.run(command, shell=True, check=True, text=True, capture_output=True)
                return result.stdout
            except subprocess.CalledProcessError as e:
                return f"Error running integration: {e.stderr}"
        else:
            return "Tool not found in integrations."