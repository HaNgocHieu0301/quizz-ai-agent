import json
from typing import Dict, Any
from app.core.exceptions import ContentGenerationError


class FormatHelper:
    @staticmethod
    def format_ai_response(response_content: str) -> Dict[str, Any]:
        """Format AI response content"""
        try:
            content = response_content.strip()
            if content.startswith("```json"):
                content = content[7:]
            if content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            return json.loads(content.strip())
        except Exception as e:
            raise ContentGenerationError(f"Error formatting AI response: {str(e)}")