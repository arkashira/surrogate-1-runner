
import json
from typing import Any, Dict, List, TypeVar, Optional

T = TypeVar("T")

def generate_json_schema(function_definition: T) -> Dict[str, Any]:
    schema = {
        "type": "object",
        "properties": {
            **{k: {"type": "string"} for k in function_definition.__annotations__.keys() if k != "return"}
        },
        "required": list(function_definition.__annotations__.keys())
    }
    return schema

def build_openai_request(
    tool_function: T,
    inputs: List[Any],
    response_format: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    tool_call = {"name": tool_function.__name__, "arguments": inputs}
    if response_format is None:
        response_format = {"type": "json_schema", "schema": generate_json_schema(tool_function)}
    else:
        response_format["schema"] = generate_json_schema(tool_function)

    return {
        "model": "text-davinci-003",
        "prompt": f"Generate a response using the {tool_function.__name__} function with the following arguments: {inputs}. Response format: {json.dumps(response_format, indent=2)}.",
        "response_format": response_format
    }

def replace_tool_calls_with_response_format(request: Dict[str, Any]) -> Dict[str, Any]:
    if "tool_calls" in request:
        tool_call = request["tool_calls"]
        request["response_format"] = {
            "type": "json_schema",
            "schema": generate_json_schema(tool_call["name"])
        }
        del request["tool_calls"]
        request["response_format"]["schema"]["properties"]["arguments"] = {
            "type": "array",
            "items": {"type": "string"}
        }
    return request