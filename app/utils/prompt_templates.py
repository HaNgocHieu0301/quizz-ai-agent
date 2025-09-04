"""
Prompt templates for AI content generation using LangChain
"""

from langchain.prompts import PromptTemplate
from app.utils.ai_response_schema import AIResponseSchemaHandler


class ContentGenerationTemplates:
    """Templates for main content generation (flashcards + MCQs)"""
    
    # Vocabulary-focused text content template
    VOCAB_TEXT_TEMPLATE = PromptTemplate(
        input_variables=["content", "num_flashcards", "num_mcqs", "format_template"],
        template="""
Analyze the following text content and generate vocabulary-focused educational materials.

TEXT CONTENT:
{content}

FOCUS: Generate vocabulary-focused learning materials that emphasize key terms and their meanings.
- Flashcards should focus on important vocabulary words and their definitions
- MCQs should test understanding of vocabulary meanings and usage
- Prioritize prominent words, technical terms, and key concepts that learners should know

Please generate exactly {num_flashcards} flashcards and {num_mcqs} multiple choice questions based on the content.

REQUIREMENTS:
1. Content should be educational and suitable for learning/studying
2. Each MCQ should have one correct answer with 3 other wrong options
3. Focus on the most important and relevant information for learners

{format_template}
""")
    
    # Knowledge-focused text content template
    KNOWLEDGE_TEXT_TEMPLATE = PromptTemplate(
        input_variables=["content", "num_flashcards", "num_mcqs", "format_template"],
        template="""
Analyze the following text content and generate comprehensive educational materials.

TEXT CONTENT:
{content}

FOCUS: Generate comprehensive learning materials covering key concepts, facts, and important information.
- Flashcards should focus on key terms, concepts, definitions, and important facts  
- MCQs should test understanding and comprehension of the subject matter
- Cover the main ideas and learning objectives from the content

Please generate exactly {num_flashcards} flashcards and {num_mcqs} multiple choice questions based on the content.

REQUIREMENTS:
1. Content should be educational and suitable for learning/studying
2. Each MCQ should have one correct answer with 3 other wrong options
3. Focus on the most important and relevant information for learners

{format_template}
""")
    
    # Vocabulary-focused image content template
    VOCAB_IMAGE_TEMPLATE = PromptTemplate(
        input_variables=["num_flashcards", "num_mcqs", "format_template"],
        template="""
Analyze the content shown in this image and generate vocabulary-focused educational materials based on what you can see and read.

FOCUS: Generate vocabulary-focused learning materials from the image content.
- Focus on important vocabulary words, technical terms, and key concepts visible in the image
- Flashcards should emphasize word-meaning relationships
- MCQs should test vocabulary understanding and definitions

Please generate exactly {num_flashcards} flashcards and {num_mcqs} multiple choice questions based on:
- Any text visible in the image
- Diagrams, charts, or visual information  
- Key concepts or information presented
- Important facts or data shown

REQUIREMENTS:
1. Content should be educational and suitable for learning/studying
2. Each MCQ should have one correct answer with 3 other wrong options
3. Focus on the most important and relevant information for learners

{format_template}
""")
    
    # Knowledge-focused image content template
    KNOWLEDGE_IMAGE_TEMPLATE = PromptTemplate(
        input_variables=["num_flashcards", "num_mcqs", "format_template"],
        template="""
Analyze the content shown in this image and generate comprehensive educational materials based on what you can see and read.

FOCUS: Generate comprehensive learning materials covering all key information in the image.
- Focus on key concepts, facts, processes, and important information shown
- Cover diagrams, charts, visual information, and any text content
- Test overall understanding and comprehension of the subject matter

Please generate exactly {num_flashcards} flashcards and {num_mcqs} multiple choice questions based on:
- Any text visible in the image
- Diagrams, charts, or visual information  
- Key concepts or information presented
- Important facts or data shown

REQUIREMENTS:
1. Content should be educational and suitable for learning/studying
2. Each MCQ should have one correct answer with 3 other wrong options
3. Focus on the most important and relevant information for learners

{format_template}
""")
    
    @classmethod
    def get_text_template(cls, content_type: str) -> PromptTemplate:
        """Get appropriate text template based on content type"""
        return cls.VOCAB_TEXT_TEMPLATE if content_type == "vocab" else cls.KNOWLEDGE_TEXT_TEMPLATE
    
    @classmethod
    def get_image_template(cls, content_type: str) -> PromptTemplate:
        """Get appropriate image template based on content type"""
        return cls.VOCAB_IMAGE_TEMPLATE if content_type == "vocab" else cls.KNOWLEDGE_IMAGE_TEMPLATE


class ChoicesGenerationTemplates:
    """Templates for choices generation (multiple choice options)"""
    
    # Question-based choices template
    QUESTION_TEMPLATE = PromptTemplate(
        input_variables=["input_text"],
        template="""
Analyze the following QUESTION and generate answer choices. Automatically determine whether this is vocabulary-focused or knowledge-focused based on the question context.

QUESTION: {input_text}

INSTRUCTIONS:
- Automatically determine if this is vocabulary-focused (about word meanings, definitions, terminology) or knowledge-focused (about concepts, facts, processes)
- Generate 1 correct answer and 3 incorrect but plausible options
- For vocabulary questions: Focus on word meanings, definitions, and terminology
- For knowledge questions: Focus on factual information, concepts, and explanations
- All options should be relevant to the question topic
- Incorrect options should be believable but definitely wrong
- Keep answers concise and clear

Respond with ONLY a JSON object in this exact format:
{{
    "correct_choice": "The correct answer here",
    "options": [
        "First incorrect but plausible option",
        "Second incorrect but plausible option", 
        "Third incorrect but plausible option"
    ]
}}
""")
    
    # Term-based choices template
    TERM_TEMPLATE = PromptTemplate(
        input_variables=["input_text"],
        template="""
Analyze the following TERM and generate definition choices. Automatically determine whether this is vocabulary-focused or knowledge-focused based on the term context.

TERM: {input_text}

INSTRUCTIONS:
- Automatically determine if this is vocabulary-focused (language/word learning) or knowledge-focused (academic/technical concepts)
- Generate 1 correct definition and 3 incorrect but plausible definitions
- For vocabulary terms: Focus on word meanings and linguistic definitions
- For knowledge terms: Focus on technical, scientific, or academic explanations
- All definitions should be relevant to the term's subject area
- Incorrect definitions should be believable but definitely wrong for this specific term
- Keep definitions concise and clear

Respond with ONLY a JSON object in this exact format:
{{
    "correct_choice": "The correct definition of the term here",
    "options": [
        "First incorrect but plausible definition",
        "Second incorrect but plausible definition",
        "Third incorrect but plausible definition"  
    ]
}}
""")
    
    @classmethod
    def get_choices_template(cls, input_text: str) -> PromptTemplate:
        """Get appropriate choices template based on whether input is a question or term"""
        is_question = any(word in input_text.lower() for word in ["what", "how", "why", "when", "where", "who", "which", "?"])
        return cls.QUESTION_TEMPLATE if is_question else cls.TERM_TEMPLATE


class PromptTemplateManager:
    """Main manager for all prompt templates"""
    
    def __init__(self):
        self.content_templates = ContentGenerationTemplates()
        self.choices_templates = ChoicesGenerationTemplates()
    
    def get_content_generation_prompt(self, content: str, num_flashcards: int, num_mcqs: int, 
                                    content_type: str = "knowledge", is_image: bool = False) -> str:
        """Generate prompt for content generation (flashcards + MCQs)"""
        format_template = AIResponseSchemaHandler.get_complete_format_template()
        
        if is_image:
            template = self.content_templates.get_image_template(content_type)
            return template.format(
                num_flashcards=num_flashcards,
                num_mcqs=num_mcqs,
                format_template=format_template
            )
        else:
            template = self.content_templates.get_text_template(content_type)
            return template.format(
                content=content,
                num_flashcards=num_flashcards,
                num_mcqs=num_mcqs,
                format_template=format_template
            )
    
    def get_choices_generation_prompt(self, input_text: str) -> str:
        """Generate prompt for choices generation"""
        template = self.choices_templates.get_choices_template(input_text)
        return template.format(input_text=input_text)


# Global instance for easy access
prompt_manager = PromptTemplateManager()