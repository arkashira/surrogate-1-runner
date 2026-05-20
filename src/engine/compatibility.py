class CompatibilityRules:
    def __init__(self):
        self.socket_compatibilities = {
            "LGA 1200": ["Intel Core i5", "Intel Core i7"],
            "LGA 1700": ["Intel Core i5", "Intel Core i7", "Intel Core i9"],
            "AM4": ["AMD Ryzen 5", "AMD Ryzen 7", "AMD Ryzen 9"],
        }
        self.wattage_compatibilities = {
            "650W": ["NVIDIA GeForce RTX 3060", "NVIDIA GeForce RTX 3070"],
            "850W": ["NVIDIA GeForce RTX 3080", "NVIDIA GeForce RTX 3090"],
            "1000W": ["AMD Radeon RX 6800 XT", "AMD Radeon RX 6900 XT"],
        }
        self.form_factor_compatibilities = {
            "ATX": ["ASRock B450M Steel Legend Micro ATX", "ASUS PRIME B450-PLUS"],
            "Micro-ATX": ["MSI B450M BAZOOKA", "GIGABYTE B450M DS3H"],
            "Mini-ITX": ["ASRock B450M Steel Legend Mini ITX", "ASUS ROG STRIX B450-I"],
        }

    def check_socket_compatibility(self, cpu, motherboard):
        return motherboard.socket in self.socket_compatibilities and cpu.model in self.socket_compatibilities[motherboard.socket]

    def check_wattage_compatibility(self, gpu, psu):
        return gpu.wattage <= psu.wattage

    def check_form_factor_compatibility(self, motherboard, case):
        return motherboard.form_factor == case.form_factor

    def check_compatibility(self, components):
        cpu = components["cpu"]
        motherboard = components["motherboard"]
        gpu = components["gpu"]
        psu = components["psu"]
        case = components["case"]

        if not self.check_socket_compatibility(cpu, motherboard):
            return False
        if not self.check_wattage_compatibility(gpu, psu):
            return False
        if not self.check_form_factor_compatibility(motherboard, case):
            return False
        return True