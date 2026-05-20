from config.parser import load_config

class ConfigManager:
    def __init__(self, config_path):
        self.config = load_config(config_path)

    def get_ci_platform(self):
        return self.config.get('ci_platform')

    def get_pre_hooks(self):
        return self.config.get('pre_hooks')

    def get_post_hooks(self):
        return self.config.get('post_hooks')

    def get_test_runner(self):
        return self.config.get('test_runner')