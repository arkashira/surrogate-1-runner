import json
import yaml
import os
from typing import Dict, List, Optional

class UnifiedParser:
    def __init__(self, config_path: str, config_type: str):
        self.config_path = config_path
        self.config_type = config_type

    def parse(self) -> Dict:
        """
        Parse the configuration file and return a dictionary of resources.
        """
        if self.config_type == 'terraform':
            with open(self.config_path, 'r') as file:
                for line in file:
                    if line.strip().startswith('resource'):
                        parts = line.strip().split()
                        resource_type = parts[1].strip('"')
                        resource_name = parts[2].strip('"')
                        resources[f"{resource_type}.{resource_name}"] = {
                            'type': resource_type,
                            'name': resource_name,
                            'attributes': {}
                        }
            return resources
        elif self.config_type == 'helm':
            with open(self.config_path, 'r') as file:
                config = yaml.safe_load(file)
            return config
        else:
            raise ValueError("Unsupported configuration type")

    def map_to_pdpa_controls(self, config: Dict) -> Dict:
        """
        Map the parsed resources to PDPA controls.
        """
        pdpa_controls = {}
        if self.config_type == 'terraform':
            for resource_id, resource in config.items():
                if resource['type'] == 'aws_s3_bucket':
                    pdpa_controls[resource_id] = {
                        'control': 'PDPA-1',
                        'description': 'Personal data must be collected, used, disclosed, and processed in a lawful manner.'
                    }
                elif resource['type'] == 'aws_dynamodb_table':
                    pdpa_controls[resource_id] = {
                        'control': 'PDPA-2',
                        'description': 'Personal data must be collected for specified, explicit, and legitimate purposes.'
                    }
                # Add more mappings as needed
        elif self.config_type == 'helm':
            if 'resources' in config:
                for resource in config['resources']:
                    if resource['kind'] == 'Deployment':
                        pdpa_controls[resource['metadata']['name']] = {
                            'control': 'PDPA-3',
                            'description': 'Personal data must be accurate and up-to-date.'
                        }
                    elif resource['kind'] == 'Service':
                        pdpa_controls[resource['metadata']['name']] = {
                            'control': 'PDPA-4',
                            'description': 'Personal data must be retained only as long as necessary for the purposes for which it was collected.'
                        }
                    # Add more mappings as needed
        return pdpa_controls

    def generate_documentation(self, pdpa_controls: Dict) -> str:
        """
        Generate PDPA compliance documentation from the mapped controls.
        """
        documentation = "PDPA Compliance Documentation\n\n"
        for resource_id, control in pdpa_controls.items():
            documentation += f"Resource: {resource_id}\n"
            documentation += f"PDPA Control: {control['control']}\n"
            documentation += f"Description: {control['description']}\n\n"
        return documentation

    def save_documentation(self, documentation: str, output_path: str) -> None:
        """
        Save the generated documentation to a file.
        """
        with open(output_path, 'w') as file:
            file.write(documentation)

    def generate_pdf(self, documentation: str, output_path: str) -> None:
        """
        Generate a PDF version of the documentation.
        """
        from fpdf import FPDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for line in documentation.split('\n'):
            pdf.cell(200, 10, txt=line, ln=True)
        pdf.output(output_path)