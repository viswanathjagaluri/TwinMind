from pydantic import BaseModel
from typing import List


class Suggestion(BaseModel):
    type: str
    text: str


class ChatMessage(BaseModel):
    question: str
    answer: str