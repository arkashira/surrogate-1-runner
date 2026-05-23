
import json
import requests
import time

class LicenseValidator:
    def __init__(self, license_key):
        self.license_key = license_key
        self.base_url = "https://api.axentx.com/v1/license"

    def validate(self):
        response = requests.get(f"{self.base_url}/validate", params={"key": self.license_key})
        if response.status_code != 200:
            raise Exception("Failed to validate license")
        data = response.json()
        if data["status"] != "active":
            raise Exception("License is not active")
        self.premium_features_unlocked = data["premium_features_unlocked"]

def main():
    license_key = "your_license_key_here"  # Replace with actual license key
    license_validator = LicenseValidator(license_key)
    license_validator.validate()
    print("Premium features unlocked: ", license_validator.premium_features_unlocked)

if __name__ == "__main__":
    main()