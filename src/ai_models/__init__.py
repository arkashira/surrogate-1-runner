from .claude import ClaudeAPI

__all__ = ["ClaudeAPI"]

# Initialize Claude API with environment variable
claude_api = ClaudeAPI(api_key=os.getenv("CLAUDE_API_KEY"))