#!/usr/bin/env python3
"""
Test script for image extraction functionality.
This script tests the Gemini API integration with a sample image.
"""

import os
import sys
from PIL import Image
import json

# Add utils to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.image_processing import (
    extract_data_from_image, validate_extracted_data, 
    format_extracted_data_for_display, get_extraction_confidence
)
from config import get_gemini_api_key

def test_image_extraction():
    """Test the image extraction functionality."""
    
    # Check if API key is provided
    api_key = get_gemini_api_key()
    if not api_key:
        print("❌ Please set the Gemini API key in Streamlit secrets")
        print("You can get an API key from: https://makersuite.google.com/app/apikey")
        print("For local development, create .streamlit/secrets.toml with:")
        print("[gemini]")
        print('api_key = "your_api_key_here"')
        return False
    
    # Test image path
    test_image_path = "data/Images/Example Results/Screenshot 2025-07-10 035525.png"
    
    if not os.path.exists(test_image_path):
        print(f"❌ Test image not found: {test_image_path}")
        return False
    
    print("🔍 Testing image extraction...")
    print(f"📷 Using test image: {test_image_path}")
    
    try:
        # Load the image
        image = Image.open(test_image_path)
        print(f"✅ Image loaded successfully: {image.size}")
        
        # Extract data
        print("🤖 Extracting data with Gemini API...")
        extracted_data = extract_data_from_image(image, api_key)
        
        if "error" in extracted_data:
            print(f"❌ Extraction failed: {extracted_data['error']}")
            return False
        
        print("✅ Data extracted successfully!")
        print(f"📊 Raw extracted data:")
        print(json.dumps(extracted_data, indent=2))
        
        # Validate the data
        print("\n🔍 Validating extracted data...")
        validation_errors = validate_extracted_data(extracted_data)
        
        if validation_errors:
            print("❌ Validation errors:")
            for error in validation_errors:
                print(f"  • {error}")
        else:
            print("✅ Data validation passed!")
        
        # Format for display
        formatted_data = format_extracted_data_for_display(extracted_data)
        confidence = get_extraction_confidence(extracted_data)
        
        print(f"\n📋 Formatted data:")
        print(json.dumps(formatted_data, indent=2))
        print(f"\n🎯 Confidence level: {confidence}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error during testing: {str(e)}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Deadshot Stats Image Extraction")
    print("=" * 50)
    
    success = test_image_extraction()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ All tests passed! Image extraction is working correctly.")
    else:
        print("❌ Tests failed. Please check the errors above.") 