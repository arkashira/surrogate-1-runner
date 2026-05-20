import os
import subprocess
from typing import List, Dict

class SOPCreator:
    def __init__(self, templates_dir: str, output_dir: str):
        self.templates_dir = templates_dir
        self.output_dir = output_dir

    def list_templates(self) -> List[str]:
        """List all available SOP templates."""
        return [f for f in os.listdir(self.templates_dir) if f.endswith('.md')]

    def create_sop(self, template_name: str, variables: Dict[str, str]) -> str:
        """Create an SOP from a template with given variables."""
        template_path = os.path.join(self.templates_dir, template_name)
        output_path = os.path.join(self.output_dir, f"{template_name.split('.')[0]}_{'_'.join(variables.values())}.md")

        with open(template_path, 'r') as template_file:
            template_content = template_file.read()

        for key, value in variables.items():
            template_content = template_content.replace(f'{{{{{key}}}}}', value)

        with open(output_path, 'w') as output_file:
            output_file.write(template_content)

        return output_path

    def sync_to_slack(self, file_path: str, channel: str) -> bool:
        """Sync the SOP to Slack."""
        try:
            subprocess.run(['slack', 'files', 'upload', '-c', channel, '-f', file_path], check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def sync_to_github(self, file_path: str, repo: str, branch: str) -> bool:
        """Sync the SOP to GitHub."""
        try:
            subprocess.run(['gh', 'repo', 'clone', repo, 'temp_repo'], check=True)
            subprocess.run(['cp', file_path, 'temp_repo'], check=True)
            subprocess.run(['cd', 'temp_repo', '&&', 'git', 'add', file_path], shell=True)
            subprocess.run(['cd', 'temp_repo', '&&', 'git', 'commit', '-m', f'Add SOP {file_path}'], shell=True)
            subprocess.run(['cd', 'temp_repo', '&&', 'git', 'push', 'origin', branch], shell=True)
            subprocess.run(['rm', '-rf', 'temp_repo'], check=True)
            return True
        except subprocess.CalledProcessError:
            return False

    def sync_to_notion(self, file_path: str, page_id: str) -> bool:
        """Sync the SOP to Notion."""
        try:
            subprocess.run(['notion', 'upload', '--page', page_id, file_path], check=True)
            return True
        except subprocess.CalledProcessError:
            return False