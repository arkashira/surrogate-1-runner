import requests

class IPGeolocator:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.ipgeolocation.io/ipgeo"

    def get_location(self, ip_address):
        response = requests.get(f"{self.base_url}?apiKey={self.api_key}&ip={ip_address}")
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def is_region_allowed(self, ip_address, allowed_regions):
        location = self.get_location(ip_address)
        if location and 'country_code2' in location:
            return location['country_code2'] in allowed_regions
        return False