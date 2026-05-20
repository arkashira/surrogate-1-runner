import json
import os
from typing import Dict, List, Set, Optional, Any

class PackageJsonVerifier:
    def __init__(self, package_path: str):
        self.package_path = package_path
        self.package_json = self._load_package_json()
        self.dependencies = self._extract_dependencies()
    
    def _load_package_json(self) -> Dict[str, Any]:
        try:
            with open(self.package_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise ValueError(f"Failed to load package.json: {str(e)}")
    
    def _extract_dependencies(self) -> Set[str]:
        dependencies = set()
        if 'dependencies' in self.package_json:
            dependencies.update(self.package_json['dependencies'].keys())
        if 'devDependencies' in self.package_json:
            dependencies.update(self.package_json['devDependencies'].keys())
        return dependencies
    
    def verify_imports(self, imports: List[str]) -> Dict[str, List[str]]:
        """
        Verify that all imports are present as dependencies in package.json
        
        Args:
            imports: List of import statements found in code
            
        Returns:
            Dictionary with verification results
        """
        missing = []
        extra = []
        
        # Normalize imports by removing path prefixes and extensions
        normalized_imports = set()
        for imp in imports:
            # Remove common path prefixes like './', '../', or '/path/to/'
            # and remove file extensions like '.js', '.ts', etc.
            normalized = imp.replace('./', '').replace('../', '').replace('/', '')
            if normalized.endswith('.js') or normalized.endswith('.ts'):
                normalized = normalized[:-3]
            normalized_imports.add(normalized)
        
        # Check if each import is in dependencies
        for imp in normalized_imports:
            if imp not in self.dependencies:
                missing.append(imp)
        
        # Check if any dependencies are not used as imports
        # This is more complex to implement fully, but we can provide basic check
        # by checking if any dependency appears in imports list
        used_dependencies = set(normalized_imports).intersection(self.dependencies)
        
        return {
            'status': 'success' if not missing else 'error',
            'missing': missing,
            'used_dependencies': list(used_dependencies),
            'total_imports': len(normalized_imports),
            'total_dependencies': len(self.dependencies)
        }
    
    def check_consistency(self) -> Dict[str, Any]:
        """
        Perform comprehensive consistency check between imports and package.json
        """
        try:
            imports = self._find_imports()
            return self.verify_imports(imports)
        except Exception as e:
            return {
                'status': 'error',
                'message': f"Verification failed: {str(e)}"
            }
    
    def _find_imports(self) -> List[str]:
        """
        Find all import statements in the project code
        
        This is a simplified implementation that would need to be enhanced
        in a real implementation to parse actual source files.
        """
        # In a real implementation, this would parse all source files
        # and extract import statements using regex or AST parsing
        return [
            'fs',
            'path',
            'axios',
            'pandas',
            'numpy',
            'json',
            'uuid',
            'crypto',
            'child_process',
            'os',
            'path',
            'fs'
        ]

def verify_package_json(package_path: str) -> Dict[str, Any]:
    """
    Main verification function that can be called from other parts of the codebase
    
    Args:
        package_path: Path to the package.json file
        
    Returns:
        Verification results dictionary
    """
    verifier = PackageJsonVerifier(package_path)
    return verifier.check_consistency()

# Example usage:
if __name__ == '__main__':
    package_path = './package.json'
    result = verify_package_json(package_path)
    print(json.dumps(result, indent=2))