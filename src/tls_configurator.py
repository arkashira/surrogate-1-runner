import json
import random
from typing import List

class TLSConfigurator:
    def __init__(self, config_path: str):
        with open(config_path, 'r') as file:
            self.config = json.load(file)

    def get_random_cipher_suites(self) -> List[str]:
        return random.sample(self.config['cipherSuites'], len(self.config['cipherSuites']))

    def get_random_extensions(self) -> List[str]:
        return random.sample(self.config['extensions'], len(self.config['extensions']))

    def get_random_user_agent(self) -> str:
        return random.choice(self.config['userAgents'])

# Example usage
if __name__ == "__main__":
    tls_config = TLSConfigurator('/opt/axentx/surrogate-1/config/fingerprints.json')
    print(tls_config.get_random_cipher_suites())
    print(tls_config.get_random_extensions())
    print(tls_config.get_random_user_agent())