#!/usr/bin/env python3
"""
Simple test script to verify the AI Agent setup and basic functionality.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, str(Path(__file__).parent))

async def test_imports():
    """Test that all modules can be imported correctly"""
    print("Testing imports...")
    
    try:
        from app.core.config import settings
        print("✅ Core config imported successfully")
        
        from app.core.exceptions import AIAgentException
        print("✅ Custom exceptions imported successfully")
        
        from app.models.request_models import GenerateContentRequest
        from app.models.response_models import GenerateContentResponse
        print("✅ Pydantic models imported successfully")
        
        from app.utils.file_helpers import validate_file_type
        print("✅ File utilities imported successfully")
        
        from app.services.file_processor import FileProcessor
        print("✅ File processor imported successfully")
        
        # Only test AI service if API key is available
        if os.getenv('GEMINI_API_KEY'):
            from app.services.ai_service import AIService
            print("✅ AI service imported successfully")
        else:
            print("⚠️ AI service not tested (no GEMINI_API_KEY)")
        
        from app.services.content_generator import ContentGeneratorService
        print("✅ Content generator imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_file_validation():
    """Test file validation functionality"""
    print("\nTesting file validation...")
    
    try:
        from app.utils.file_helpers import validate_file_type
        
        # Test valid file types
        assert validate_file_type("test.txt") == "text"
        assert validate_file_type("test.pdf") == "document"
        assert validate_file_type("test.png") == "image"
        print("✅ File type validation working correctly")
        
        # Test invalid file type
        try:
            validate_file_type("test.xyz")
            print("❌ Should have raised UnsupportedFileTypeError")
            return False
        except Exception:
            print("✅ Correctly rejects unsupported file types")
        
        return True
        
    except Exception as e:
        print(f"❌ File validation test failed: {e}")
        return False

async def test_file_processor():
    """Test file processor with sample data"""
    print("\nTesting file processor...")
    
    try:
        from app.services.file_processor import FileProcessor
        
        processor = FileProcessor()
        
        # Test text processing
        sample_text = "This is a test document about machine learning."
        result = await processor.process_file(sample_text.encode('utf-8'), "test.txt")
        
        assert result["type"] == "text"
        assert result["content"] == sample_text
        print("✅ Text file processing working correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ File processor test failed: {e}")
        return False

def test_configuration():
    """Test configuration loading"""
    print("\nTesting configuration...")
    
    try:
        from app.core.config import settings
        
        print(f"App name: {settings.app_name}")
        print(f"Supported extensions: {settings.all_supported_extensions}")
        print(f"Max file size: {settings.max_file_size_mb}MB")
        
        if settings.gemini_api_key:
            print("✅ Gemini API key configured")
        else:
            print("⚠️ No Gemini API key found in environment")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

async def main():
    """Run all tests"""
    print("🚀 Starting AI Agent Setup Tests\n")
    
    tests = [
        ("Import Tests", test_imports()),
        ("File Validation", test_file_validation()),
        ("File Processor", test_file_processor()),
        ("Configuration", test_configuration()),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Running: {test_name}")
        print('='*50)
        
        if asyncio.iscoroutine(test_func):
            result = await test_func
        else:
            result = test_func
            
        results.append((test_name, result))
    
    # Summary
    print(f"\n{'='*50}")
    print("TEST SUMMARY")
    print('='*50)
    
    passed = 0
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nTotal: {passed}/{len(results)} tests passed")
    
    if passed == len(results):
        print("\n🎉 All tests passed! The AI Agent is ready to use.")
        print("\nNext steps:")
        print("1. Set your GEMINI_API_KEY in the .env file")
        print("2. Run: python -m uvicorn app.main:app --reload")
        print("3. Visit: http://localhost:8000/docs")
    else:
        print(f"\n⚠️ {len(results) - passed} test(s) failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    asyncio.run(main())