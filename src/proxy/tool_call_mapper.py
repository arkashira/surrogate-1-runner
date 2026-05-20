"""
Utility to convert OpenAI structured output responses into a LangChain-compatible
tool_calls format.

The function `map_response_to_tool_calls` inspects an OpenAI response dict,
extracts the JSON payload from the `content` field when the response format
is declared as a JSON object, and transforms it into the minimal
LangChain tool call structure: