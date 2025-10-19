from pydantic import BaseModel, Field, conlist

class ChatRequest(BaseModel):
    message: str = Field(
        ...,  # The '...' means this field is required
        title="User Message",
        description="The user's current chat message.",
        max_length=256  # Prevent excessively long messages
    )
    history: str = Field(
        ...,  # The '...' means this field is required
        title="Conversation History",
        description="The History used for LLM to remember the coversation",
        max_length=2000  # Prevent excessively long messages
    )
