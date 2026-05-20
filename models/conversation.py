import uuid
from typing import List, Dict

from pydantic import BaseModel, Field, validator


class Message(BaseModel):
    role: str = Field(..., description="Either 'user' or 'assistant'")
    content: str = Field(..., description="The text of the message")

    @validator("role")
    def role_must_be_valid(cls, v):
        if v not in {"user", "assistant"}:
            raise ValueError("role must be 'user' or 'assistant'")
        return v


class Conversation(BaseModel):
    session_id: str = Field(..., description="Unique identifier for the conversation")
    messages: List[Message] = Field(default_factory=list, description="Chronological list of messages")


# In‑memory store for active conversations.
# In a production system this would be replaced by a persistent DB or cache.
_conversation_store: Dict[str, Conversation] = {}


def create_conversation() -> Conversation:
    """Create a new conversation session and store it."""
    session_id = str(uuid.uuid4())
    conv = Conversation(session_id=session_id, messages=[])
    _conversation_store[session_id] = conv
    return conv


def get_conversation(session_id: str) -> Conversation:
    """Retrieve a conversation by its session_id; raise KeyError if not found."""
    return _conversation_store[session_id]


def add_user_message(session_id: str, content: str) -> Conversation:
    """Append a user message, generate a simple AI response, and return the updated conversation."""
    conv = get_conversation(session_id)
    conv.messages.append(Message(role="user", content=content))

    # Placeholder AI response – in real product this would call an LLM.
    ai_reply = f"AI: {content}"
    conv.messages.append(Message(role="assistant", content=ai_reply))

    # Store back (not strictly needed for mutable objects, but keeps intent clear)
    _conversation_store[session_id] = conv
    return conv