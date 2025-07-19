#!/usr/bin/env python3
"""
Simple test script to verify the Deadshot Stats app functionality.
"""

import subprocess
import sys
import time
import os


def test_dependencies():
    """Test if all required dependencies are installed."""
    print("🔍 Testing dependencies...")

    required_packages = [
        "streamlit",
        "pandas",
        "plotly",
        "scikit-learn",
        "google-generativeai",
        "Pillow",
    ]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - Missing")
            missing_packages.append(package)

    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Please run: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All dependencies are installed!")
        return True


def test_data_files():
    """Test if required data files exist."""
    print("\n📁 Testing data files...")

    required_files = [
        "data/matches.csv",
        "app.py",
        "utils/data_processing.py",
        "utils/calculations.py",
        "utils/visualizations.py",
        "utils/image_processing.py",
    ]

    missing_files = []

    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - Missing")
            missing_files.append(file_path)

    if missing_files:
        print(f"\n⚠️  Missing files: {', '.join(missing_files)}")
        return False
    else:
        print("\n✅ All required files exist!")
        return True


def test_app_startup():
    """Test if the app can start without errors."""
    print("\n🚀 Testing app startup...")

    try:
        # Try to import the main app
        import sys

        sys.path.append(".")

        # Test imports
        from utils.data_processing import load_match_data
        from utils.calculations import get_player_stats
        from utils.visualizations import create_overview_cards
        from utils.image_processing import extract_data_from_image

        print("✅ All imports successful!")

        # Test data loading
        try:
            df = load_match_data()
            print(f"✅ Data loaded successfully! {len(df)} rows found.")
        except Exception as e:
            print(f"⚠️  Data loading warning: {e}")

        return True

    except Exception as e:
        print(f"❌ App startup failed: {e}")
        return False


def main():
    """Run all tests."""
    print("🧪 Deadshot Stats App Test Suite")
    print("=" * 50)

    tests = [
        ("Dependencies", test_dependencies),
        ("Data Files", test_data_files),
        ("App Startup", test_app_startup),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} test...")
        if test_func():
            passed += 1
            print(f"✅ {test_name} test passed!")
        else:
            print(f"❌ {test_name} test failed!")

    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! The app should work correctly.")
        print("\n🚀 To run the app:")
        print("streamlit run app.py")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
