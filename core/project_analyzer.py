import os
import ast
import tomllib
from typing import Dict, List, Optional

class ProjectAnalyzer:
    """
    Analyzes a project's file structure, imports, and dependencies to build a dependency graph.
    """
    
    def __init__(self, project_root: str):
        """
        Initialize the analyzer with the project root directory.
        
        Args:
            project_root: Path to the project's root directory.
        """
        self.project_root = project_root
        self.source_files: List[str] = []
        self.package_deps: Dict[str, List[str]] = {}
    
    def _get_source_files(self) -> List[str]:
        """Recursively find all Python source files in the project."""
        files = []
        for root, _, filenames in os.walk(self.project_root):
            for filename in filenames:
                if filename.endswith('.py') and not filename.startswith('.'):
                    files.append(os.path.relpath(os.path.join(root, filename), self.project_root))
        return files
    
    def _parse_imports(self, file_path: str) -> List[str]:
        """
        Parse a Python file and extract all import statements.
        
        Args:
            file_path: Path to the Python file.
            
        Returns:
            List of imported module names.
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        tree = ast.parse(content)
        imports = []
        
        for node in ast.walk(tree):
            if isinstance(node, (ast.Import, ast.ImportFrom)):
                for name in node.names:
                    imports.append(name.name)
        
        return imports
    
    def _get_package_dependencies(self) -> Dict[str, List[str]]:
        """
        Extract dependencies from pyproject.toml (Poetry format).
        
        Returns:
            Dictionary mapping dependency names to versions.
        """
        toml_path = os.path.join(self.project_root, 'pyproject.toml')
        if not os.path.exists(toml_path):
            return {}
        
        with open(toml_path, 'r', encoding='utf-8') as f:
            data = tomllib.load(f)
        
        # Extract dependencies from Poetry's configuration
        poetry_deps = data.get('tool', {}).get('poetry', {}).get('dependencies', {})
        return poetry_deps
    
    def build_file_graph(self) -> Dict[str, List[str]]:
        """
        Build a dependency graph showing which files import which modules.
        
        Returns:
            Dictionary where keys are file paths and values are lists of imported modules.
        """
        self.source_files = self._get_source_files()
        self.package_deps = self._get_package_dependencies()
        
        graph: Dict[str, List[str]] = {file: [] for file in self.source_files}
        
        for file in self.source_files:
            file_path = os.path.join(self.project_root, file)
            imports = self._parse_imports(file_path)
            graph[file].extend(imports)
        
        return graph
    
    def get_project_summary(self) -> Dict[str, Optional[Dict]]:
        """
        Get a summary of the project including file count and dependencies.
        
        Returns:
            Dictionary with project statistics.
        """
        return {
            'file_count': len(self.source_files),
            'package_dependencies': self.package_deps,
            'source_files': self.source_files[:10]  # Sample first 10 files for display
        }