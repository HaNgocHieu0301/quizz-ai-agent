"""
Common AI response schema handler for content generation
"""


class AIResponseSchemaHandler:
    """Handles common AI response schemas and formatting"""
    
    @staticmethod
    def get_cards_json_format() -> str:
        """
        Returns the standard JSON format template for cards response
        
        Returns:
            str: JSON format template string
        """
        return """{{
"cards": [
    {{
        "term": "Question or term",
        "definition": "Answer or definition",
        "type": 1,
        "options": [
            "Option A text",
            "Option B text", 
            "Option C text"
        ]
    }}
]
}}"""
    
    @staticmethod
    def get_format_instructions() -> str:
        """
        Returns detailed instructions for the JSON format
        
        Returns:
            str: Format instructions
        """
        return """
RESPONSE FORMAT INSTRUCTIONS:
- Return response as valid JSON with the exact structure shown above
- "type": Use 1 for flashcards, 2 for multiple choice questions
- For flashcards (type=1): Set "options" to empty array []
- For MCQs (type=2): Include 3 incorrect options in "options" array (do not include the correct answer)
- "term": Contains the question text or vocabulary term
- "definition": Contains the answer or definition
- Ensure JSON is properly formatted and valid
"""
    
    @staticmethod
    def get_complete_format_template() -> str:
        """
        Returns the complete format template with instructions
        
        Returns:
            str: Complete template with JSON format and instructions
        """
        json_format = AIResponseSchemaHandler.get_cards_json_format()
        instructions = AIResponseSchemaHandler.get_format_instructions()
        
        return f"""
Return your response as a JSON object with this exact structure:
{json_format}

{instructions}
"""