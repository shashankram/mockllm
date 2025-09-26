import time
import uuid
from typing import Dict, Iterable, List, Literal, Optional, Union

from pydantic import BaseModel, Field

from anthropic.types.content_block import ContentBlock
from anthropic.types.text_block_param import TextBlockParam
from anthropic.types.image_block_param import ImageBlockParam
from anthropic.types.document_block_param import DocumentBlockParam
from anthropic.types.thinking_block_param import ThinkingBlockParam
from anthropic.types.tool_use_block_param import ToolUseBlockParam
from anthropic.types.tool_result_block_param import ToolResultBlockParam
from anthropic.types.search_result_block_param import SearchResultBlockParam
from anthropic.types.server_tool_use_block_param import ServerToolUseBlockParam
from anthropic.types.redacted_thinking_block_param import RedactedThinkingBlockParam
from anthropic.types.web_search_tool_result_block_param import (
    WebSearchToolResultBlockParam,
)


# OpenAI Models
class OpenAIMessage(BaseModel):
    """OpenAI chat message model."""

    role: str
    content: str


class OpenAIChatRequest(BaseModel):
    """OpenAI chat completion request model."""

    model: str
    messages: List[OpenAIMessage]
    temperature: Optional[float] = Field(default=0.7)
    max_tokens: Optional[int] = Field(default=150)
    stream: Optional[bool] = Field(default=False)


class OpenAIDeltaMessage(BaseModel):
    """OpenAI streaming delta message model."""

    role: Optional[str] = None
    content: Optional[str] = None


class OpenAIStreamChoice(BaseModel):
    """OpenAI streaming choice model."""

    delta: OpenAIDeltaMessage
    index: int = 0
    finish_reason: Optional[str] = None


class OpenAIChatChoice(BaseModel):
    """OpenAI regular chat choice model."""

    message: OpenAIMessage
    index: int = 0
    finish_reason: str = "stop"


class OpenAIChatResponse(BaseModel):
    """OpenAI chat completion response model."""

    id: str = Field(default_factory=lambda: f"mock-{uuid.uuid4()}")
    object: str = "chat.completion"
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str
    choices: List[Dict]
    usage: Dict[str, int]


class OpenAIStreamResponse(BaseModel):
    """OpenAI streaming response model."""

    id: str = Field(default_factory=lambda: f"mock-{uuid.uuid4()}")
    object: str = "chat.completion.chunk"
    created: int = Field(default_factory=lambda: int(time.time()))
    model: str
    choices: List[OpenAIStreamChoice]


# Anthropic Models
class AnthropicMessage(BaseModel):
    """Anthropic message model."""

    role: Literal["user", "assistant"]
    content: Union[
        str,
        Iterable[
            Union[
                TextBlockParam,
                ImageBlockParam,
                DocumentBlockParam,
                SearchResultBlockParam,
                ThinkingBlockParam,
                RedactedThinkingBlockParam,
                ToolUseBlockParam,
                ToolResultBlockParam,
                ServerToolUseBlockParam,
                WebSearchToolResultBlockParam,
                ContentBlock,
            ]
        ],
    ]


class AnthropicChatRequest(BaseModel):
    """Anthropic chat completion request model."""

    model: str
    max_tokens: Optional[int] = Field(default=1024)
    messages: List[AnthropicMessage]
    stream: Optional[bool] = Field(default=False)
    temperature: Optional[float] = Field(default=1.0)


class AnthropicChatResponse(BaseModel):
    """Anthropic chat completion response model."""

    id: str = Field(default_factory=lambda: f"mock-{uuid.uuid4()}")
    type: str = "message"
    role: str = "assistant"
    model: str
    content: List[Dict[str, str]]
    stop_reason: Optional[str] = "end_turn"
    stop_sequence: Optional[str] = None
    usage: Dict[str, int]


class AnthropicStreamDelta(BaseModel):
    """Anthropic streaming delta model."""

    type: str = "content_block_delta"
    index: int = 0
    delta: Dict[str, str]


class AnthropicStreamResponse(BaseModel):
    """Anthropic streaming response model."""

    type: str = "message_delta"
    id: str = Field(default_factory=lambda: f"mock-{uuid.uuid4()}")
    delta: AnthropicStreamDelta
    usage: Optional[Dict[str, int]] = None


# For backward compatibility
Message = OpenAIMessage
ChatRequest = OpenAIChatRequest
DeltaMessage = OpenAIDeltaMessage
StreamChoice = OpenAIStreamChoice
ChatChoice = OpenAIChatChoice
ChatResponse = OpenAIChatResponse
StreamResponse = OpenAIStreamResponse
