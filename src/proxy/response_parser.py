import json
from typing import Dict, Any, List

class ResponseParser:
    @staticmethod
    def parse_response(response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse the OpenAI response and convert structured output to LangChain-compatible tool_call format.

        Args:
            response (Dict[str, Any]): The OpenAI response to parse.

        Returns:
            Dict[str, Any]: The parsed response with tool_calls if applicable.
        """
        if 'response_format' in response and response['response_format'] == 'structured_output':
            content = response.get('content', '')
            try:
                json_content = json.loads(content)
                tool_calls = [{
                    'function': {
                        'name': json_content.get('function_name', ''),
                        'arguments': json_content.get('arguments', {})
                    }
                }]
                response['tool_calls'] = tool_calls
                del response['content']
            except json.JSONDecodeError:
                pass
        return response