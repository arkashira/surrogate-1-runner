import os
import json

class VersionCompatibilityChecker:
    def __init__(self, current_version, compatible_versions):
        self.current_version = current_version
        self.compatible_versions = compatible_versions

    def is_compatible(self):
        return self.current_version in self.compatible_versions

    def check_files(self, design_files):
        for file in design_files:
            if not self.is_file_compatible(file):
                raise ValueError(f"Incompatible design file: {file}")

    def is_file_compatible(self, file):
        # Placeholder for actual file compatibility logic
        # This should check the file format/version
        return True

def load_compatible_versions(file_path):
    with open(file_path, 'r') as f:
        return json.load(f)

if __name__ == "__main__":
    current_version = "9.0"  # Example current version
    compatible_versions_file = "/opt/axentx/surrogate-1/compatible_versions.json"
    compatible_versions = load_compatible_versions(compatible_versions_file)

    checker = VersionCompatibilityChecker(current_version, compatible_versions)
    design_files = ["design1.kicad_pcb", "design2.kicad_sch"]  # Example design files

    try:
        checker.check_files(design_files)
        print("All design files are compatible.")
    except ValueError as e:
        print(e)