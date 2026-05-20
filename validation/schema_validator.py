import json
from jsonschema import validate, ValidationError

class SchemaValidator:
    def __init__(self, schema_path):
        with open(schema_path, 'r') as schema_file:
            self.schema = json.load(schema_file)

    def validate(self, instance):
        try:
            validate(instance=instance, schema=self.schema)
        except ValidationError as e:
            return str(e)
        return None