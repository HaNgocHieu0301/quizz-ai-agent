#!/usr/bin/env python3
"""
Example script demonstrating how to use the AI Learning Tools Generator API
"""

import requests
import json
import os
import sys
from pathlib import Path

API_BASE_URL = "http://localhost:8000"

def create_sample_files():
    """Create sample files for testing"""
    samples_dir = Path("samples")
    samples_dir.mkdir(exist_ok=True)
    
    # Sample text file
    with open(samples_dir / "sample.txt", "w", encoding="utf-8") as f:
        f.write("""
Machine Learning Basics

Machine learning is a subset of artificial intelligence (AI) that provides systems 
the ability to automatically learn and improve from experience without being explicitly programmed.

Key Concepts:
1. Supervised Learning: Learning with labeled training data
2. Unsupervised Learning: Learning patterns in data without labels
3. Neural Networks: Computing systems inspired by biological neural networks
4. Deep Learning: Machine learning using deep neural networks

Applications:
- Image recognition
- Natural language processing
- Recommendation systems
- Autonomous vehicles

Popular algorithms include linear regression, decision trees, random forest, and support vector machines.
        """.strip())
    
    # Sample markdown file
    with open(samples_dir / "sample.md", "w", encoding="utf-8") as f:
        f.write("""
# Docker Container Technology

Docker is a platform designed to help developers build, share, and run container applications.

## What are Containers?

Containers are lightweight, standalone, executable packages that include everything needed to run an application:
- Code
- Runtime
- System tools
- Libraries
- Settings

## Key Benefits

1. **Portability**: Run anywhere Docker is installed
2. **Consistency**: Same environment across development, testing, and production
3. **Efficiency**: Share OS kernel, use fewer resources than VMs
4. **Scalability**: Easy to scale applications up or down

## Basic Commands

```bash
docker build -t myapp .
docker run -p 8080:80 myapp
docker ps
docker stop container_id
```

## Dockerfile Example

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```
        """)
    
    print(f"✅ Sample files created in {samples_dir}/")
    return samples_dir

def test_health_check():
    """Test the health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Health check passed")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to API. Make sure the server is running.")
        return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_file_upload(file_path, num_flashcards=3, num_mcqs=2):
    """Test file upload and content generation"""
    print(f"\nTesting content generation with {file_path}...")
    
    if not os.path.exists(file_path):
        print(f"❌ File not found: {file_path}")
        return False
    
    try:
        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f, "application/octet-stream")}
            data = {
                "num_flashcards": num_flashcards,
                "num_mcqs": num_mcqs
            }
            
            print(f"Uploading {os.path.basename(file_path)}...")
            response = requests.post(
                f"{API_BASE_URL}/api/v1/generate",
                files=files,
                data=data,
                timeout=30
            )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Content generation successful!")
            
            # Display results
            print(f"\n📊 Results for {result['metadata']['original_filename']}:")
            print(f"Model used: {result['metadata']['model_used']}")
            print(f"Processing time: {result['metadata']['processing_time_seconds']}s")
            
            print(f"\n📚 Generated {len(result['data']['flashcards'])} flashcards:")
            for i, card in enumerate(result['data']['flashcards'], 1):
                print(f"{i}. Front: {card['front']}")
                print(f"   Back: {card['back']}\n")
            
            print(f"❓ Generated {len(result['data']['multiple_choice_questions'])} MCQs:")
            for i, mcq in enumerate(result['data']['multiple_choice_questions'], 1):
                print(f"{i}. {mcq['question']}")
                for option, text in mcq['options'].items():
                    marker = "✓" if option == mcq['correct_answer'] else " "
                    print(f"   {marker} {option}. {text}")
                print()
            
            return True
        
        else:
            print(f"❌ API request failed: {response.status_code}")
            try:
                error_info = response.json()
                print(f"Error: {error_info}")
            except:
                print(f"Response: {response.text}")
            return False
    
    except requests.exceptions.Timeout:
        print("❌ Request timed out. The file might be too large or complex.")
        return False
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return False

def main():
    """Main function to run examples"""
    print("🚀 AI Learning Tools Generator - Example Usage\n")
    
    # Check if API is running
    if not test_health_check():
        print("\n💡 To start the API server, run:")
        print("python -m uvicorn app.main:app --reload")
        sys.exit(1)
    
    # Create sample files
    samples_dir = create_sample_files()
    
    # Test with different file types
    test_files = [
        samples_dir / "sample.txt",
        samples_dir / "sample.md"
    ]
    
    success_count = 0
    for file_path in test_files:
        if test_file_upload(file_path, num_flashcards=2, num_mcqs=2):
            success_count += 1
        print("-" * 80)
    
    print(f"\n📈 Results: {success_count}/{len(test_files)} tests passed")
    
    if success_count > 0:
        print("\n🎉 API is working correctly!")
        print("\n💡 Try uploading your own files:")
        print("- Text files (.txt, .md)")
        print("- PDF documents (.pdf)")
        print("- Word documents (.docx)")
        print("- Images (.png, .jpg, .jpeg)")
        print(f"\nAPI Documentation: {API_BASE_URL}/docs")
    else:
        print("\n⚠️ API tests failed. Please check the server logs.")

if __name__ == "__main__":
    main()