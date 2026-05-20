import json
from typing import Dict, List, Optional
from pathlib import Path
from src.templates.template_schema import TemplateMetadata, TemplateSchema

class TemplateManager:
    def __init__(self, template_dir: str = "templates"):
        self.template_dir = Path(template_dir)
        self.template_dir.mkdir(exist_ok=True)

    def get_template_categories(self) -> List[str]:
        """Get all template categories."""
        categories = set()
        for template_file in self.template_dir.glob("*.json"):
            with template_file.open() as f:
                template = json.load(f)
                categories.add(template.get("category", "uncategorized"))
        return sorted(categories)

    def get_templates_by_category(self, category: str) -> List[Dict]:
        """Get templates by category."""
        templates = []
        for template_file in self.template_dir.glob("*.json"):
            with template_file.open() as f:
                template = json.load(f)
                if template.get("category") == category:
                    templates.append(template)
        return templates

    def get_template_by_id(self, template_id: str) -> Optional[Dict]:
        """Get template by ID."""
        template_file = self.template_dir / f"{template_id}.json"
        if template_file.exists():
            with template_file.open() as f:
                return json.load(f)
        return None

    def import_template(self, template_id: str) -> Optional[Dict]:
        """Import a template by ID."""
        template = self.get_template_by_id(template_id)
        if template:
            # Create a copy of the template with editable parameters
            imported_template = template.copy()
            imported_template["id"] = f"imported_{template_id}"
            imported_template["version"] = "1.0.0"
            return imported_template
        return None

    def update_template(self, template_id: str, new_template: Dict) -> bool:
        """Update a template."""
        template_file = self.template_dir / f"{template_id}.json"
        if template_file.exists():
            with template_file.open("w") as f:
                json.dump(new_template, f, indent=2)
            return True
        return False