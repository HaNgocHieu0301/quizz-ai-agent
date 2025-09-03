from pydantic import BaseModel
from typing import List, Dict, Any, Optional

class Card(BaseModel):
    term: str
    definition: str
    type: int
    options: List[str]

class Flashcard(BaseModel):
    front: str
    back: str


class MultipleChoiceQuestion(BaseModel):
    question: str
    options: Dict[str, str]  # {"A": "option1", "B": "option2", ...}
    correct_answer: str


# class GeneratedContent(BaseModel):
#     flashcards: List[Flashcard]
#     multiple_choice_questions: List[MultipleChoiceQuestion]
class GeneratedContent(BaseModel):
    cards: List[Card]

class ResponseMetadata(BaseModel):
    original_filename: str
    ai_model: str
    processing_time_seconds: Optional[float] = None


class GenerateContentResponse(BaseModel):
    status: str
    metadata: ResponseMetadata
    data: GeneratedContent

class ErrorResponse(BaseModel):
    status: str = "error"
    error_type: str
    message: str
    details: Optional[Dict[str, Any]] = None