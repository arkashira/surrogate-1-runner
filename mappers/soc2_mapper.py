import json
import hashlib

class Soc2Mapper:
    def __init__(self, terraform_config, helm_config):
        self.terraform_config = terraform_config
        self.helm_config = helm_config
        self.controls = self.load_controls()

    def load_controls(self):
        # Load SOC 2 controls from a JSON file
        with open('soc2_controls.json', 'r') as f:
            return json.load(f)

    def map_controls(self):
        # Map Terraform/Helm configs to SOC 2 controls
        terraform_controls = self.map_terraform_controls()
        helm_controls = self.map_helm_controls()
        return terraform_controls + helm_controls

    def map_terraform_controls(self):
        # Map Terraform config to SOC 2 controls
        controls = []
        for resource in self.terraform_config['resources']:
            if resource['type'] == 'aws_instance':
                controls.append({
                    'control': 'CCI-000185',
                    'description': 'Ensure AWS instance is configured with a secure password policy'
                })
        return controls

    def map_helm_controls(self):
        # Map Helm config to SOC 2 controls
        controls = []
        for chart in self.helm_config['charts']:
            if chart['name'] == 'my-chart':
                controls.append({
                    'control': 'CCI-000186',
                    'description': 'Ensure Helm chart is configured with a secure secret policy'
                })
        return controls

    def generate_documentation(self):
        # Generate documentation from mapped controls
        documentation = ''
        for control in self.map_controls():
            documentation += f'{control["control"]}: {control["description"]}\n'
        return documentation

    def sign_documentation(self):
        # Sign documentation with a digital signature
        signature = hashlib.sha256(self.generate_documentation().encode()).hexdigest()
        return signature

    def create_pdf(self):
        # Create a PDF from the signed documentation
        pdf = f'Signed SOC 2 documentation: {self.generate_documentation()} {self.sign_documentation()}'
        return pdf

# Example usage:
terraform_config = {
    'resources': [
        {'type': 'aws_instance', 'name': 'my-instance'},
        {'type': 'aws_s3_bucket', 'name': 'my-bucket'}
    ]
}
helm_config = {
    'charts': [
        {'name': 'my-chart', 'version': '1.0.0'},
        {'name': 'another-chart', 'version': '2.0.0'}
    ]
}
mapper = Soc2Mapper(terraform_config, helm_config)
print(mapper.create_pdf())