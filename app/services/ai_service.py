import json
import base64
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage
from app.core.config import settings
from app.core.exceptions import AIServiceError, ContentGenerationError
from app.utils.format_helpers import FormatHelper
from app.utils.prompt_templates import prompt_manager
from app.utils.file_helpers import FileHelper

class AIService:
    """Handle AI interactions with Google Gemini"""
    
    def __init__(self):
        try:
            self.llm = ChatGoogleGenerativeAI(
                model=settings.gemini_model,
                google_api_key=settings.gemini_api_key,
                temperature=0.3
            )
        except Exception as e:
            raise AIServiceError(f"Failed to initialize Gemini AI: {str(e)}")
    
    async def generate_learning_content(
        self, 
        processed_data: Dict[str, Any], 
        num_flashcards: int = 5, 
        num_mcqs: int = 5,
        content_type: str = "knowledge"
    ) -> Dict[str, Any]:
        """
        Generate flashcards and MCQs from processed content
        
        Args:
            processed_data: Processed file data from FileProcessor
            num_flashcards: Number of flashcards to generate
            num_mcqs: Number of MCQs to generate
            content_type: Type of content to generate ('vocab' or 'knowledge')
            
        Returns:
            Dict containing generated cards
        """
        try:
            if processed_data["type"] == "text":
                return await self._generate_from_text(
                    processed_data["content"], num_flashcards, num_mcqs, content_type
                )
            elif processed_data["type"] == "image":
                return await self._generate_from_image(
                    processed_data["content"], num_flashcards, num_mcqs, content_type
                )
        except Exception as e:
            raise ContentGenerationError(f"Failed to generate content: {str(e)}")

    async def generate_choices(
        self, 
        input_text: str
    ) -> Dict[str, Any]:
        """
        Generate multiple choice options for a given question or term.
        The AI agent automatically determines the appropriate content type.
        """
        try:
            prompt = prompt_manager.get_choices_generation_prompt(input_text)
            response = await self.llm.ainvoke([HumanMessage(content=prompt)])
            return FormatHelper.format_ai_response(response.content)
        except Exception as e:
            raise ContentGenerationError(f"Failed to generate choices: {str(e)}")
    
    async def _generate_from_text(self, text_content: str, num_flashcards: int, num_mcqs: int, content_type: str = "knowledge") -> Dict[str, Any]:
        """Generate content from text using prompt templates"""
        prompt = prompt_manager.get_content_generation_prompt(
            content=text_content,
            num_flashcards=num_flashcards,
            num_mcqs=num_mcqs,
            content_type=content_type,
            is_image=False
        )
        
        try:
            response = await self.llm.ainvoke([HumanMessage(content=prompt)])
            return FormatHelper.format_ai_response(response.content)
        except Exception as e:
            raise AIServiceError(f"Gemini API call failed: {str(e)}")
    
    async def _generate_from_image(self, image_content: bytes, num_flashcards: int, num_mcqs: int, content_type: str = "knowledge") -> Dict[str, Any]:
        """Generate content from image using multimodal capabilities and prompt templates"""
        
        # Detect image format from image bytes
        mime_type = FileHelper.get_image_mime_type(image_content)
        
        # Convert image to base64 for Gemini
        image_b64 = base64.b64encode(image_content).decode()
        
        prompt = prompt_manager.get_content_generation_prompt(
            content="",
            num_flashcards=num_flashcards,
            num_mcqs=num_mcqs,
            content_type=content_type,
            is_image=True
        )
        
        try:
            # For multimodal input, we need to structure the message with both text and image
            message_content = [
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:{mime_type};base64,{image_b64}"
                    }
                }
            ]
            
            response = await self.llm.ainvoke([HumanMessage(content=message_content)])
            return FormatHelper.format_ai_response(response.content)
        except Exception as e:
            raise AIServiceError(f"Gemini multimodal API call failed: {str(e)}")
