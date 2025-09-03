import json
import base64
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

from app.core.config import settings
from app.core.exceptions import AIServiceError, ContentGenerationError


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
        num_mcqs: int = 5
    ) -> Dict[str, Any]:
        """
        Generate flashcards and MCQs from processed content
        
        Args:
            processed_data: Processed file data from FileProcessor
            num_flashcards: Number of flashcards to generate
            num_mcqs: Number of MCQs to generate
            
        Returns:
            Dict containing generated flashcards and MCQs
        """
        try:
            if processed_data["type"] == "text":
                return await self._generate_from_text(
                    processed_data["content"], num_flashcards, num_mcqs
                )
            elif processed_data["type"] == "image":
                return await self._generate_from_image(
                    processed_data["content"], num_flashcards, num_mcqs
                )
        except Exception as e:
            raise ContentGenerationError(f"Failed to generate content: {str(e)}")
    
    async def _generate_from_text(self, text_content: str, num_flashcards: int, num_mcqs: int) -> Dict[str, Any]:
        """Generate content from text"""
        prompt = self._create_text_prompt(text_content, num_flashcards, num_mcqs)
        
        try:
            response = await self.llm.ainvoke([HumanMessage(content=prompt)])
            return self._parse_ai_response(response.content)
        except Exception as e:
            raise AIServiceError(f"Gemini API call failed: {str(e)}")
    
    async def _generate_from_image(self, image_content: bytes, num_flashcards: int, num_mcqs: int) -> Dict[str, Any]:
        """Generate content from image using multimodal capabilities"""
        
        # Detect image format from image bytes
        mime_type = self._detect_image_mime_type(image_content)
        
        # Convert image to base64 for Gemini
        image_b64 = base64.b64encode(image_content).decode()
        
        prompt = self._create_image_prompt(num_flashcards, num_mcqs)
        
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
            
            # FIXED: Use the multimodal message_content instead of just the text prompt
            response = await self.llm.ainvoke([HumanMessage(content=message_content)])
            return self._parse_ai_response(response.content)
        except Exception as e:
            raise AIServiceError(f"Gemini multimodal API call failed: {str(e)}")
    
    def _create_text_prompt(self, content: str, num_flashcards: int, num_mcqs: int) -> str:
        """Create prompt for text-based content generation"""
        return f"""
Analyze the following text content and generate educational materials.

TEXT CONTENT:
{content}

Please generate exactly {num_flashcards} flashcards and {num_mcqs} multiple choice questions based on the key concepts, facts, and important information from the text.

REQUIREMENTS:
1. Flashcards should focus on key terms, concepts, definitions, and important facts
2. Multiple choice questions should test understanding and comprehension
3. Each MCQ should have one correct answer with 3 other wrong options
4. Content should be educational and suitable for learning/studying

Return your response as a JSON object with this exact structure:
{{
    "cards": [
        {{
            "term": "Question or term",
            "definition": "Answer or definition"
            "type": "Flashcard or Mcq (flashcard = 1, mcp = 2)
            "options": [
                "Option A text",
                "Option B text", 
                "Option C text",
            ] (If type = flashcard = 1 options = []. Besides, options don't contain correct answer)
        }}
    ]
}}
Ensure the JSON is valid and properly formatted.
"""
    
    def _create_image_prompt(self, num_flashcards: int, num_mcqs: int) -> str:
        """Create prompt for image-based content generation"""
        return f"""
Analyze the content shown in this image and generate educational materials based on what you can see and read.

Please generate exactly {num_flashcards} flashcards and {num_mcqs} multiple choice questions based on:
- Any text visible in the image
- Diagrams, charts, or visual information
- Key concepts or information presented
- Important facts or data shown

REQUIREMENTS:
1. Flashcards should focus on key terms, concepts, definitions, and important facts from the image
2. Multiple choice questions should test understanding of the visual content
3. Each MCQ should have 4 options (A, B, C, D) with one correct answer
4. Content should be educational and suitable for learning/studying

Return your response as a JSON object with this exact structure:
{{
    "flashcards": [
        {{
            "front": "Question or term",
            "back": "Answer or definition"
        }}
    ],
    "multiple_choice_questions": [
        {{
            "question": "Question text",
            "options": {{
                "A": "Option A text",
                "B": "Option B text", 
                "C": "Option C text",
                "D": "Option D text"
            }},
            "correct_answer": "A"
        }}
    ]
}}

Ensure the JSON is valid and properly formatted.
"""
    
    def _parse_ai_response(self, response_content: str) -> Dict[str, Any]:
        """Parse and validate AI response"""
        try:
            # Try to extract JSON from the response
            content = response_content.strip()
            
            # Remove markdown code blocks if present
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            
            # Parse JSON
            parsed_data = json.loads(content.strip())
            
            # # Validate structure
            # if "flashcards" not in parsed_data or "multiple_choice_questions" not in parsed_data:
            #     raise ValueError("Missing required fields in AI response")
            
            # # Validate flashcards
            # for flashcard in parsed_data["flashcards"]:
            #     if "front" not in flashcard or "back" not in flashcard:
            #         raise ValueError("Invalid flashcard structure")
            
            # # Validate MCQs
            # for mcq in parsed_data["multiple_choice_questions"]:
            #     if not all(key in mcq for key in ["question", "options", "correct_answer"]):
            #         raise ValueError("Invalid MCQ structure")
                
            #     if not isinstance(mcq["options"], dict):
            #         raise ValueError("MCQ options must be a dictionary")
                
            #     if mcq["correct_answer"] not in mcq["options"]:
            #         raise ValueError("Correct answer not found in options")
            
            return parsed_data
            
        except json.JSONDecodeError as e:
            raise ContentGenerationError(f"Failed to parse AI response as JSON: {str(e)}")
        except ValueError as e:
            raise ContentGenerationError(f"Invalid AI response format: {str(e)}")
        except Exception as e:
            raise ContentGenerationError(f"Unexpected error parsing AI response: {str(e)}")
    
    def _detect_image_mime_type(self, image_content: bytes) -> str:
        """Detect MIME type from image bytes"""
        # Check image format by looking at file headers
        if image_content.startswith(b'\xff\xd8\xff'):
            return "image/jpeg"
        elif image_content.startswith(b'\x89PNG\r\n\x1a\n'):
            return "image/png"
        elif image_content.startswith(b'GIF87a') or image_content.startswith(b'GIF89a'):
            return "image/gif"
        elif image_content.startswith(b'RIFF') and b'WEBP' in image_content[:12]:
            return "image/webp"
        else:
            # Default to JPEG if we can't detect
            return "image/jpeg"