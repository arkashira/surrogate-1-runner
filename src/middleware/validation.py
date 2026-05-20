import jsonschema
from jsonschema import validate
from typing import Dict

def validate_payload(payload: Dict) -> bool:
    schema = {
        "type": "object",
        "properties": {
            "file_path": {"type": "string"},
            "content": {"type": "string"},
            "cursor_position": {"type": "integer"},
            "selection": {"type": "string"}
        },
        "required": ["file_path", "content", "cursor_position", "selection"]
    }
    try:
        validate(instance=payload, schema=schema)
        return True
    except jsonschema.exceptions.ValidationError:
        return False

def validation_middleware(environ, start_response):
    if environ['CONTENT_TYPE'] == 'application/json':
        try:
            payload = json.loads(environ['wsgi.input'].read())
            if validate_payload(payload):
                start_response('200 OK', [])
                return [b'']
            else:
                start_response('400 Bad Request', [])
                return [b'']
        except ValueError:
            start_response('400 Bad Request', [])
            return [b'']
    else:
        start_response('415 Unsupported Media Type', [])
        return [b'']