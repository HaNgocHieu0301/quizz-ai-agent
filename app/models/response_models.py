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

class GenerateChoicesData(BaseModel):
    correct_choice: str
    options: List[str]  # 3 incorrect but related options

class GenerateChoicesResponse(BaseModel):
    status: str
    metadata: ResponseMetadata
    data: GenerateChoicesData
