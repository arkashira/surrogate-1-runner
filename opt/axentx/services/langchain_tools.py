LANGCHAIN_TOOL_WHITELIST = [
    'search', 'calculate', 'fetch_document', 'translate', 'summarize',
    'analyze_sentiment', 'generate_image', 'transcribe_audio', 'extract_keywords',
    'classify_text', 'aggregate', 'transform', 'validate', 'generate',
    'classify', 'predict', 'explain'
]

def is_langchain_tool(tool_name: str) -> bool:
    """Check if a tool name is in the whitelisted LangChain tools."""
    return tool_name in LANGCHAIN_TOOL_WHITELIST

def detect_langchain_tool_calls(tool_calls: list) -> list:
    """Detect and return whitelisted LangChain tool calls from a list of tool calls."""
    return [tool_call['name'] for tool_call in tool_calls
            if is_langchain_tool(tool_call.get('name'))]