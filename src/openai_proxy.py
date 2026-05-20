import json
from typing import Dict, Any
from jsonschema import validate, ValidationError
from fastapi import HTTPException

class OpenAIProxy:
    def __init__(self, openai_client):
        self.openai_client = openai_client

    def generate_json_schema(self, tool: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a JSON schema from the tool's function definition."""
        schema = {
            "type": "object",
            "properties": {
                "name": {"type": "string", "const": tool["function"]["name"]},
                "description": {"type": "string", "const": tool["function"]["description"]},
                "parameters": {
                    "type": "object",
                    "properties": tool["function"]["parameters"]["properties"],
                    "required": tool["function"]["parameters"].get("required", []),
                },
            },
            "required": ["name", "description", "parameters"],
        }
        return schema

    def validate_schema(self, schema: Dict[str, Any], data: Dict[str, Any]) -> bool:
        """Validate the data against the JSON schema."""
        try:
            validate(instance=data, schema=schema)
            return True
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=f"Schema validation error: {e}")

    def rewrite_tool_calls(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Rewrite the tool calls to OpenAI's structured_output format."""
        if "tools" in request:
            tools = request["tools"]
            if len(tools) == 1:
                tool = tools[0]
                schema = self.generate_json_schema(tool)
                request["response_format"] = {"type": "json_schema", "json_schema": schema}
                del request["tools"]
        return request

    def forward_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Forward the request to OpenAI after schema validation."""
        if "tools" in request:
            request = self.rewrite_tool_calls(request)
        response = self.openai_client.chat.completions.create(**request)
        if "response_format" in request and "choices" in response:
            for choice in response.choices:
                if hasattr(choice, "message") and hasattr(choice.message, "tool_calls"):
                    schema = request["response_format"]["json_schema"]
                    for tool_call in choice.message.tool_calls:
                        self.validate_schema(schema, tool_call.function)
        return response