# AI Learning Tools Generator - Project Overview

## Project Description

A FastAPI-based service that automatically generates interactive learning tools (flashcards and multiple-choice questions) from various file formats using Google Gemini 2.0 Flash AI model. The application supports both file uploads and direct text input, with specialized content generation modes for vocabulary-focused learning and general knowledge acquisition.

## Key Features

### Content Generation
- **Multi-format Support**: Process text (.txt, .md), documents (.pdf, .docx), and images (.png, .jpg, .jpeg)
- **Text Input Support**: Generate content directly from text input without file upload
- **Content Type Selection**: Choose between vocabulary-focused ("vocab") or general knowledge ("knowledge") content generation
- **Customizable Output**: Configure number of flashcards and MCQs to generate (1-20 each)

### AI-Powered Learning
- **Google Gemini 2.0 Flash**: Fast, accurate content generation with multimodal capabilities
- **Intelligent Content Analysis**: Extracts key concepts, terms, and learning objectives
- **Vocabulary Focus Mode**: Generates vocabulary-focused flashcards emphasizing key terms and definitions
- **Knowledge Focus Mode**: Creates comprehensive learning materials covering key concepts and facts

### Technical Features
- **Fast Response**: Optimized for speed with average response time <15 seconds
- **Robust Error Handling**: Comprehensive validation and error responses
- **Docker Ready**: Containerized for easy deployment
- **HTTPS Support**: Local development with SSL/TLS support
- **Health Monitoring**: Built-in health check endpoints

## Architecture Overview

### Directory Structure
```
ai-agent/
├── app/
│   ├── main.py                 # FastAPI application entry point
│   ├── core/
│   │   ├── config.py          # Configuration management
│   │   └── exceptions.py      # Custom exception classes
│   ├── api/v1/endpoints/
│   │   └── generate.py        # API endpoints for content generation
│   ├── services/
│   │   ├── file_processor.py  # File processing and content extraction
│   │   ├── ai_service.py      # Gemini AI integration and prompt management
│   │   └── content_generator.py # Main orchestration service
│   ├── models/
│   │   ├── request_models.py  # Pydantic request validation models
│   │   └── response_models.py # Pydantic response models
│   └── utils/
│       ├── file_helpers.py    # File utility functions
│       └── prompt_templates.py # LangChain prompt templates for AI content generation
├── test_files/                # Sample files for testing
├── certs/                     # SSL certificates (local development)
├── Dockerfile                 # Container configuration
├── docker-compose.yml         # Docker Compose setup
├── run_https.py              # HTTPS server launcher
└── requirements.txt          # Python dependencies
```

### Core Components

#### 1. API Layer (`app/api/v1/endpoints/generate.py`)
- **Primary Endpoint**: `POST /api/v1/generate`
- **Choices Endpoint**: `POST /api/v1/generate-choices`
- **Test Generation Endpoint**: `POST /api/v1/generate-test`
- **Input Validation**: Ensures exactly one input method (file or text)
- **Parameter Handling**: Validates content type, flashcard/MCQ counts
- **Error Management**: Comprehensive error handling with detailed responses

#### 2. Content Generator Service (`app/services/content_generator.py`)
- **Unified Interface**: Both file and text inputs use the same response format
- **Processing Orchestration**: Coordinates file processing and AI content generation
- **Response Building**: Constructs standardized API responses with metadata

#### 3. AI Service (`app/services/ai_service.py`)
- **Gemini Integration**: Manages Google Gemini 2.0 Flash API calls
- **Template-Based Prompts**: Uses LangChain prompt templates for consistent and maintainable prompt generation
- **Multimodal Support**: Processes both text and image content
- **Response Parsing**: Converts AI responses to structured data

#### 4. File Processor (`app/services/file_processor.py`)
- **Format Detection**: Identifies and validates file types
- **Content Extraction**: Extracts text from various document formats
- **Size Validation**: Enforces file size limits

#### 5. Prompt Templates (`app/utils/prompt_templates.py`)
- **Structured Templates**: LangChain-based prompt templates for consistent AI interactions
- **Content Generation Templates**: Separate templates for vocab/knowledge and text/image content
- **Choices Generation Templates**: Specialized templates for multiple choice option generation
- **Template Manager**: Central management system for all prompt templates with automatic selection logic

## API Specification

### Main Endpoint: `/api/v1/generate`

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `type` | String | No | "knowledge" | Content generation type: "vocab" or "knowledge" |
| `file` | File | No* | - | File to process (.txt, .md, .pdf, .docx, .png, .jpg, .jpeg) |
| `text` | String | No* | - | Text content to process (alternative to file) |
| `num_flashcards` | Integer | No | 5 | Number of flashcards to generate (1-20) |
| `num_mcqs` | Integer | No | 5 | Number of MCQs to generate (1-20) |

*One of `file` or `text` is required

#### Content Types
- **vocab**: Generates vocabulary-focused learning materials emphasizing key terms and definitions
- **knowledge**: Creates comprehensive learning materials covering key concepts, facts, and information

#### Response Format
```json
{
  "status": "success",
  "metadata": {
    "original_filename": "document.pdf",
    "ai_model": "gemini-2.0-flash",
    "processing_time_seconds": 8.45
  },
  "data": {
    "cards": [
      {
        "term": "Question or term",
        "definition": "Answer or definition",
        "type": 1, // 1 = flashcard, 2 = MCQ
        "options": [] // Empty for flashcards, contains wrong answers for MCQs
      }
    ]
  }
}
```

### Choices Endpoint: `/api/v1/generate-choices`

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `input_text` | String | Yes | - | Question or term to generate choices for |

#### Input Types
- **Question**: Generates answer choices (1 correct + 3 incorrect but related answers)
- **Term**: Generates definition choices (1 correct definition + 3 incorrect but related definitions)

#### Automatic Content Type Detection
- **AI-Powered Decision**: The AI agent automatically determines whether to use vocabulary-focused or knowledge-focused approach
- **Vocabulary Mode**: Applied for language learning terms, word definitions, and terminology-focused inputs
- **Knowledge Mode**: Applied for academic concepts, factual information, and technical explanations
- **Context-Aware**: Decision is based on input context, subject matter, and linguistic patterns

#### Response Format
```json
{
  "status": "success",
  "metadata": {
    "original_filename": "text_input",
    "ai_model": "gemini-2.0-flash",
    "processing_time_seconds": 2.12
  },
  "data": {
    "correct_choice": "The correct answer or definition",
    "options": [
      "First incorrect but plausible option",
      "Second incorrect but plausible option",
      "Third incorrect but plausible option"
    ]
  }
}
```

### Test Generation Endpoint: `/api/v1/generate-test`

#### Parameters
| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `questions` | String | Yes | - | Comma-separated list of questions or terms to generate test from (1-50 items) |

#### Input Format
- **Comma-Separated String**: Questions/terms separated by commas
- **Example**: `"What is machine learning?,photosynthesis,What is the capital of France?"`
- **Mixed Content**: Combination of questions and terms in the same request
- **Parsing**: Automatically splits on commas and trims whitespace

#### Automatic Content Type Detection
- **AI-Powered Analysis**: The AI agent automatically determines the appropriate content type for each question/term
- **Vocabulary Mode**: Applied for terminology, definitions, and language learning content
- **Knowledge Mode**: Applied for factual questions, academic concepts, and general knowledge
- **Individual Processing**: Each question in the list is processed independently with optimal content type detection

#### Response Format (Key-Value Structure)
```json
{
  "status": "success",
  "metadata": {
    "original_filename": "test_input",
    "ai_model": "gemini-2.0-flash",
    "processing_time_seconds": 3.12
  },
  "data": {
    "test_questions": {
      "What is machine learning?": {
        "correct_answer": "A type of artificial intelligence that allows computer systems to learn from data without being explicitly programmed.",
        "options": [
          "A programming language used for developing web applications.",
          "A hardware component used in computer systems for data storage.",
          "A method of data encryption used to secure online transactions."
        ]
      },
      "photosynthesis": {
        "correct_answer": "The process by which plants use sunlight to synthesize foods from carbon dioxide and water.",
        "options": [
          "The process by which animals digest food.",
          "The process of cellular respiration in animals.", 
          "The breakdown of rocks by physical and chemical means."
        ]
      }
    }
  }
}
```

## Content Generation Logic

### Vocabulary Mode (type="vocab")
- **Focus**: Key vocabulary words and technical terms
- **Flashcards**: Word-meaning relationships, definitions, terminology
- **MCQs**: Vocabulary understanding, usage, and definitions
- **Target Audience**: Language learners, students studying specialized terminology

### Knowledge Mode (type="knowledge") 
- **Focus**: Comprehensive subject matter understanding
- **Flashcards**: Key concepts, facts, processes, important information
- **MCQs**: Understanding, comprehension, application of knowledge
- **Target Audience**: General learners, students studying academic subjects

## Configuration

### Environment Variables
```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Application Settings
APP_NAME=AI Learning Tools Generator
APP_VERSION=1.0.0
DEBUG=True

# File Processing Limits
MAX_FILE_SIZE_MB=10
MAX_FLASHCARDS=20
MAX_MCQS=20

# API Configuration
API_V1_PREFIX=/api/v1
CORS_ORIGINS=["*"]

# HTTPS Configuration
USE_HTTPS=False
SSL_CERT_PATH=certs/cert.pem
SSL_KEY_PATH=certs/key.pem
```

## Deployment Options

### Local Development
```bash
# HTTP
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# HTTPS
python run_https.py
```

### Docker Deployment
```bash
# Using Docker Compose
docker-compose up --build

# Manual Docker build
docker build -t ai-learning-generator .
docker run -p 8000:8000 -e GEMINI_API_KEY=your_key ai-learning-generator
```

## Recent Updates

### Content Generation Refactoring
1. **Unified Response Format**: Both file and text inputs now return the same `cards` array structure
2. **Content Type Parameter**: Added `type` parameter to API endpoint with "vocab" and "knowledge" modes
3. **Vocabulary-Focused Generation**: New specialized mode for generating vocabulary-focused learning materials
4. **Improved Prompt Engineering**: Enhanced AI prompts to better handle different content types
5. **Consistent Service Interface**: Aligned `generate_content` and `generate_content_from_text` methods

### API Enhancements
- Added content type validation
- Improved error messages and handling
- Enhanced parameter documentation
- Unified response structure across all endpoints
- **New Endpoint**: Added `/api/v1/generate-choices` for generating multiple choice options from questions or terms
- **Test Generation Endpoint**: Added `/api/v1/generate-test` for creating complete MCQ tests from lists of questions/terms
- **Intelligent Content Detection**: AI agent automatically determines optimal content type (vocab vs knowledge) based on input context
- **Key-Value Response Format**: Updated `/api/v1/generate-test` endpoint to return responses in key-value format where question/term is key and answer data is value

### Prompt Engineering Improvements
1. **LangChain Integration**: Migrated from manual string concatenation to LangChain prompt templates
2. **Template-Based Architecture**: Centralized prompt management with reusable, maintainable templates
3. **Automatic Template Selection**: Context-aware template selection based on content type and input format
4. **Code Optimization**: Reduced codebase by ~200 lines through template consolidation
5. **Enhanced Maintainability**: Single source of truth for all AI prompts with easy modification capabilities

### Test Generation Format Update
1. **Key-Value Structure**: Modified response format from array of objects to dictionary/object structure
2. **Response Models Update**: Updated `GenerateTestData` to use `Dict[str, TestAnswerData]` instead of `List[TestQuestion]`
3. **Enhanced Accessibility**: Questions/terms now serve as direct keys for easier data access and manipulation
4. **Backward Compatibility**: Maintained all existing functionality while improving response structure
5. **Template Integration**: Added `TestGenerationTemplates` class with dedicated prompt templates for test generation

## Performance Characteristics

- **Response Time**: <15 seconds for medium-sized files
- **File Size Limit**: 10MB (configurable)
- **Concurrent Requests**: Supports multiple simultaneous requests
- **Memory Usage**: Optimized for efficient resource utilization
- **AI Model**: Google Gemini 2.0 Flash for optimal speed/accuracy balance

## Error Handling

| HTTP Status | Error Type | Description |
|-------------|------------|-------------|
| 400 | `InvalidParameterError` | Invalid content type parameter |
| 400 | `MissingInputError` | Neither file nor text provided |
| 400 | `ConflictingInputError` | Both file and text provided |
| 400 | `UnsupportedFileTypeError` | File format not supported |
| 400 | `FileProcessingError` | Failed to process file content |
| 413 | `FileSizeExceededError` | File size exceeds limit |
| 500 | `AIServiceError` | AI service unavailable or failed |

## Testing

### Sample API Calls
```bash
# Vocabulary-focused generation from text
curl -X POST "http://localhost:8000/api/v1/generate" \
  -F "type=vocab" \
  -F "text=Machine learning is a subset of artificial intelligence..." \
  -F "num_flashcards=5" \
  -F "num_mcqs=3"

# Knowledge-focused generation from file
curl -X POST "http://localhost:8000/api/v1/generate" \
  -F "type=knowledge" \
  -F "file=@document.pdf" \
  -F "num_flashcards=10" \
  -F "num_mcqs=5"

# Generate choices for a question (AI automatically determines content type)
curl -X POST "http://localhost:8000/api/v1/generate-choices" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "input_text=What is machine learning?"

# Generate choices for a term (AI automatically determines content type)
curl -X POST "http://localhost:8000/api/v1/generate-choices" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "input_text=photosynthesis"

# Generate a complete MCQ test from multiple questions/terms (key-value format response)
curl -X POST "http://localhost:8000/api/v1/generate-test" \
  -F "questions=What is machine learning?,photosynthesis,What is the capital of France?,neural network"
```

## Technology Stack

- **Backend Framework**: FastAPI
- **AI Integration**: LangChain + Google Gemini 2.0 Flash
- **Document Processing**: PyMuPDF, python-docx
- **Validation**: Pydantic
- **Containerization**: Docker + Docker Compose
- **HTTPS**: OpenSSL, mkcert (for local development)

## Prompt Template Architecture

### Template Organization
- **ContentGenerationTemplates**: Handles flashcard and MCQ generation
  - `VOCAB_TEXT_TEMPLATE`: Vocabulary-focused text content
  - `KNOWLEDGE_TEXT_TEMPLATE`: Knowledge-focused text content
  - `VOCAB_IMAGE_TEMPLATE`: Vocabulary-focused image content
  - `KNOWLEDGE_IMAGE_TEMPLATE`: Knowledge-focused image content

- **ChoicesGenerationTemplates**: Handles multiple choice option generation
  - `QUESTION_TEMPLATE`: For question-based inputs
  - `TERM_TEMPLATE`: For term-based inputs

- **TestGenerationTemplates**: Handles complete test generation
  - `TEST_TEMPLATE`: For generating tests from lists of questions/terms with automatic content type detection

- **PromptTemplateManager**: Central coordinator with convenience methods
  - `get_content_generation_prompt()`: Returns appropriate content template
  - `get_choices_generation_prompt()`: Returns appropriate choices template
  - `get_test_generation_prompt()`: Returns test generation template

### Benefits
- **Consistency**: Standardized prompt structure across all AI interactions
- **Maintainability**: Single point of modification for prompt updates
- **Scalability**: Easy addition of new templates for different content types
- **Reusability**: Templates can be shared across different service methods
- **Validation**: Built-in parameter validation through LangChain

## Future Enhancement Opportunities

1. **Advanced Template Features**: Conditional prompts, few-shot examples, and dynamic template composition
2. **Content Difficulty Levels**: Template variants for different learning complexity levels
3. **Batch Processing**: Support for processing multiple files simultaneously
4. **Export Formats**: Generate content in various formats (Anki, CSV, JSON)
5. **Learning Analytics**: Track generation patterns and optimize prompts
6. **Template Customization**: User-defined prompt templates for specific subjects
7. **A/B Testing**: Template performance comparison and optimization

---

This overview provides comprehensive information about the AI Learning Tools Generator project structure, functionality, and recent enhancements. For detailed technical implementation, refer to the source code in the respective service modules.