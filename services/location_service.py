from utils.ip_geolocator import IPGeolocator

class LocationService:
    def __init__(self, allowed_regions, api_key):
        self.allowed_regions = allowed_regions
        self.geolocator = IPGeolocator(api_key)

    def is_access_allowed(self, ip_address):
        return self.geolocator.is_region_allowed(ip_address, self.allowed_regions)

    def block_access(self, ip_address):
        if not self.is_access_allowed(ip_address):
            return f"Access denied for IP: {ip_address}"
        return "Access granted"