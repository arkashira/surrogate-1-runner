from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field

from ..models.conversation import (
    Conversation,
    create_conversation,
    get_conversation,
    add_user_message,
)

router = APIRouter(prefix="/conversation", tags=["conversation"])


class StartResponse(BaseModel):
    session_id: str = Field(..., description="Identifier for the newly created session")
    messages: list = Field(default_factory=list, description="Initial empty message list")


class UserMessage(BaseModel):
    content: str = Field(..., description="User's input text")


class HistoryResponse(BaseModel):
    session_id: str
    messages: list


@router.post("/start", response_model=StartResponse, status_code=status.HTTP_201_CREATED)
def start_conversation():
    """
    Initialise a new conversation session.
    """
    conv: Conversation = create_conversation()
    return StartResponse(session_id=conv.session_id, messages=conv.messages)


@router.post("/{session_id}/message", response_model=HistoryResponse)
def post_message(session_id: str, payload: UserMessage):
    """
    Submit a user message to an existing session and receive the AI response.
    """
    try:
        conv = add_user_message(session_id, payload.content)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation session '{session_id}' not found",
        )
    return HistoryResponse(session_id=conv.session_id, messages=conv.messages)


@router.get("/{session_id}", response_model=HistoryResponse)
def get_history(session_id: str):
    """
    Retrieve the full message history for a given session.
    """
    try:
        conv = get_conversation(session_id)
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation session '{session_id}' not found",
        )
    return HistoryResponse(session_id=conv.session_id, messages=conv.messages)