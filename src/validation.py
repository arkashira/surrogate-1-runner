import json
from jsonschema import validate, ValidationError

def validate_workflow_definition(workflow_definition):
    """
    Validate a workflow definition against the schema.
    
    Args:
    workflow_definition (dict): The workflow definition to be validated.
    
    Returns:
    bool: True if the workflow definition is valid, False otherwise.
    """
    try:
        with open('/opt/axentx/surrogate-1/src/schema.json') as f:
            schema = json.load(f)
        validate(instance=workflow_definition, schema=schema)
        return True
    except ValidationError as e:
        print(f"Validation error: {e}")
        return False