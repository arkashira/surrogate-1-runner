import os
import yaml

class ComplianceConfig:
    SUPPORTED_PROFILES = ['hipaa', 'soc2']

    def __init__(self, repo_root):
        self.config_path = os.path.join(repo_root, '.surrogate', 'compliance.yml')
        self.enabled = False
        self.profile = None
        self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_path):
            return

        with open(self.config_path, 'r') as file:
            config = yaml.safe_load(file)

        if not isinstance(config, dict):
            return

        self.enabled = config.get('enabled', False)
        self.profile = config.get('profile')

        if not isinstance(self.enabled, bool) or (self.profile not in self.SUPPORTED_PROFILES and self.profile is not None):
            self.enabled = False
            self.profile = None

    def is_scan_enabled(self):
        return self.enabled

    def get_profile(self):
        return self.profile

    @classmethod
    def should_skip_scan(cls, repo_root):
        config = cls(repo_root)
        return not config.is_scan_enabled()