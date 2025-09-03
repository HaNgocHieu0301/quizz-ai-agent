# AI Learning Tools Generator

A FastAPI-based service that automatically generates interactive learning tools (flashcards and multiple-choice questions) from various file formats using Google Gemini 2.0 Flash AI model.

## Features

- 📁 **Multi-format Support**: Process text (.txt, .md), documents (.pdf, .docx), and images (.png, .jpg, .jpeg)
- 🤖 **AI-Powered**: Uses Google Gemini 2.0 Flash for fast, accurate content generation
- 📚 **Educational Content**: Generates flashcards and multiple-choice questions
- 🎯 **Customizable**: Configure number of flashcards and MCQs to generate
- 🐳 **Docker Ready**: Containerized for easy deployment
- ⚡ **Fast**: Optimized for speed with average response time <15 seconds
- 🛡️ **Robust**: Comprehensive error handling and validation

## Quick Start

### Prerequisites

- Python 3.11+
- Google Gemini API key
- Docker (optional)

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd ai-agent
```

2. **Set up environment**
```bash
cp .env.example .env
# Edit .env with your Gemini API key
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the application**
```bash
# HTTP (development)
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# HTTPS (for remote access)
python run_https.py
```

### Docker Deployment

1. **Build and run with Docker Compose**
```bash
# Set your API key in .env file first
docker-compose up --build
```

2. **Or build Docker image manually**
```bash
docker build -t ai-learning-generator .
docker run -p 8000:8000 -e GEMINI_API_KEY=your_key_here ai-learning-generator
```

## HTTPS Setup (Local Development)

To run this application with HTTPS locally on any computer, follow these steps to set up SSL certificates.

### Option 1: Self-Signed Certificates (Quick Setup)

1. **Create certificates directory**
```bash
mkdir -p certs
```

2. **Generate self-signed certificate**
```bash
# Generate private key
openssl genrsa -out certs/key.pem 2048

# Generate certificate (valid for 365 days)
openssl req -new -x509 -key certs/key.pem -out certs/cert.pem -days 365 \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"
```

3. **Update environment configuration**
```bash
# In your .env file, set:
USE_HTTPS=True
SSL_CERT_PATH=certs/cert.pem
SSL_KEY_PATH=certs/key.pem
```

4. **Run with HTTPS enabled**
```bash
python run_https.py
```

5. **Access the application**
```bash
# Open in your browser
https://localhost:8000
```

⚠️ **Note**: Browsers will show a security warning for self-signed certificates. Click "Advanced" → "Proceed to localhost (unsafe)" to continue.

### Option 2: Using mkcert (Trusted Local Certificates)

For a better development experience without browser security warnings:

1. **Install mkcert**
```bash
# macOS
brew install mkcert  # macOS
# Ubuntu/Debian
sudo apt install libnss3-tools
wget -O mkcert https://dl.filippo.io/mkcert/latest?for=linux/amd64
chmod +x mkcert
sudo mv mkcert /usr/local/bin/

# Windows (using Chocolatey)
choco install mkcert
```

2. **Create local CA and generate certificates**
```bash
# Install local CA
mkcert -install

# Generate certificate for localhost
mkcert -key-file certs/key.pem -cert-file certs/cert.pem localhost 127.0.0.1
```

3. **Update environment and run**
```bash
# In your .env file:
USE_HTTPS=True
SSL_CERT_PATH=certs/cert.pem
SSL_KEY_PATH=certs/key.pem

# Run the application
python run_https.py
```
4. **Access without warnings**
```bash
# Open in your browser (no security warnings!)
https://localhost:8000
```

### Docker HTTPS Setup

1. **Mount certificates in Docker**
```bash
# Create docker-compose.override.yml
version: '3.8'
services:
  app:
    volumes:
      - ./certs:/app/certs:ro
    environment:
      - USE_HTTPS=true
    ports:
      - "8000:8000"
```

2. **Run with HTTPS**
```bash
docker-compose -f docker-compose.yml -f docker-compose.override.yml up --build
```

## API Usage

### Endpoint: `/api/v1/generate`

**Method**: POST  
**Content-Type**: multipart/form-data

#### Parameters

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `file` | File | Yes | - | File to process (.txt, .md, .pdf, .docx, .png, .jpg, .jpeg) |
| `num_flashcards` | Integer | No | 5 | Number of flashcards to generate (1-20) |
| `num_mcqs` | Integer | No | 5 | Number of MCQs to generate (1-20) |

#### Example Request

**Local HTTP:**
```bash
curl -X POST "http://localhost:8000/api/v1/generate" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf" \
  -F "num_flashcards=10" \
  -F "num_mcqs=5"
```

**Local HTTPS:**
```bash
curl -X POST "https://localhost:8000/api/v1/generate" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf" \
  -F "num_flashcards=10" \
  -F "num_mcqs=5" \
  -k  # Skip SSL verification for self-signed certificates (not need with mkcert)
```

#### Example Response

```json
{
  "status": "success",
  "metadata": {
    "original_filename": "document.pdf",
    "ai_model": "gemini-2.0-flash",
    "processing_time_seconds": 8.45
  },
  "data": {
    "flashcards": [
      {
        "front": "What is Docker?",
        "back": "An open platform for developing, shipping, and running applications in containers."
      }
    ],
    "multiple_choice_questions": [
      {
        "question": "Which AI model is used in this project?",
        "options": {
          "A": "GPT-4",
          "B": "Gemini 2.0 Pro", 
          "C": "Gemini 2.0 Flash",
          "D": "Claude 3"
        },
        "correct_answer": "C"
      }
    ]
  }
}
```

## Supported File Formats

| Format | Extensions | Processing Method |
|--------|------------|-------------------|
| **Text Files** | .txt, .md | Direct text reading |
| **PDF Documents** | .pdf | PyMuPDF text extraction |
| **Word Documents** | .docx | python-docx text extraction |
| **Images** | .png, .jpg, .jpeg | Gemini multimodal processing |

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
# Required
GEMINI_API_KEY=your_gemini_api_key_here

# Optional - Application Settings
APP_NAME=AI Learning Tools Generator
APP_VERSION=1.0.0
DEBUG=True

# Optional - File Processing Limits  
MAX_FILE_SIZE_MB=10
MAX_FLASHCARDS=20
MAX_MCQS=20

# Optional - API Configuration
API_V1_PREFIX=/api/v1
CORS_ORIGINS=["*"]

# Optional - HTTPS Configuration (for remote access)
USE_HTTPS=False
SSL_CERT_PATH=certs/cert.pem
SSL_KEY_PATH=certs/key.pem
```

### Getting a Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Add it to your `.env` file

## Architecture

```
ai-agent/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── core/
│   │   ├── config.py          # Configuration management
│   │   └── exceptions.py      # Custom exceptions
│   ├── api/v1/endpoints/
│   │   └── generate.py        # API endpoints
│   ├── services/
│   │   ├── file_processor.py  # File processing logic
│   │   ├── ai_service.py      # Gemini AI integration
│   │   └── content_generator.py # Main orchestration
│   ├── models/
│   │   ├── request_models.py  # Pydantic request models
│   │   └── response_models.py # Pydantic response models
│   └── utils/
│       └── file_helpers.py    # File utilities
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## Development

### Running in Development Mode

```bash
# Install development dependencies
pip install -r requirements.txt

# Run with auto-reload
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# Access API documentation
open http://localhost:8000/docs
```

### Testing

**Local HTTP Testing:**
```bash
# Test the health endpoint
curl http://localhost:8000/health

# Test file upload with a sample text file
echo "This is a test document about machine learning." > test.txt
curl -X POST "http://localhost:8000/api/v1/generate" \
  -F "file=@test.txt" \
  -F "num_flashcards=3" \
  -F "num_mcqs=2"
```

**Local HTTPS Testing:**
```bash
# Test the health endpoint
curl -k https://localhost:8000/health

# Test file upload with HTTPS
echo "This is a test document about machine learning." > test.txt
curl -X POST "https://localhost:8000/api/v1/generate" \
  -F "file=@test.txt" \
  -F "num_flashcards=3" \
  -F "num_mcqs=2" \
  -k  # Skip SSL verification for self-signed certificates (not need with mkcert)
```

## Error Handling

The API provides detailed error responses for various scenarios:

| HTTP Status | Error Type | Description |
|-------------|------------|-------------|
| 400 | `UnsupportedFileTypeError` | File format not supported |
| 400 | `FileProcessingError` | Failed to process file content |
| 413 | `FileSizeExceededError` | File size exceeds limit |
| 500 | `AIServiceError` | AI service unavailable or failed |

## Performance

- **Target Response Time**: <15 seconds for medium-sized files
- **File Size Limit**: 10MB (configurable)
- **Concurrent Requests**: Supports multiple concurrent requests
- **Memory Usage**: Optimized for efficient memory usage

## Deployment

### Production Docker Deployment

```bash
# Build production image
docker build -t ai-learning-generator:prod .

# Run in production mode
docker run -d \
  --name ai-learning-generator \
  -p 8000:8000 \
  -e GEMINI_API_KEY=your_key \
  -e DEBUG=False \
  --restart unless-stopped \
  ai-learning-generator:prod
```

### Health Checks

The application includes health check endpoints:

**HTTP:**
- `http://localhost:8000/health` - Basic health check
- `http://localhost:8000/api/v1/health` - Detailed service health

**HTTPS:**
- `https://localhost:8000/health` - Basic health check
- `https://localhost:8000/api/v1/health` - Detailed service health

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[MIT License](LICENSE)

## Support

For issues and questions:
1. Check the [documentation](http://localhost:8000/docs) when running
2. Review error responses for detailed information
3. Check logs for debugging information

---

**Built with FastAPI, LangChain, and Google Gemini 2.0 Flash** 🚀