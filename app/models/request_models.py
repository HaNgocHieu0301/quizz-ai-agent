from pydantic import BaseModel, Field
from typing import Optional
from fastapi import Form


class GenerateContentRequest(BaseModel):
    num_flashcards: Optional[int] = Field(
        default=5, 
        ge=1, 
        le=20,
        description="Number of flashcards to generate"
    )
    num_mcqs: Optional[int] = Field(
        default=5, 
        ge=1, 
        le=20,
        description="Number of multiple choice questions to generate"
    )