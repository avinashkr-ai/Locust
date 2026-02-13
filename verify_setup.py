#!/usr/bin/env python3
"""
Setup Verification Script
Run this to check if your environment is properly configured
"""

import sys
import subprocess

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro} (OK)\n")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (Need 3.8+)\n")
        return False

def check_package(package_name):
    """Check if a package is installed"""
    try:
        __import__(package_name)
        print(f"   ✅ {package_name}")
        return True
    except ImportError:
        print(f"   ❌ {package_name} (Not installed)")
        return False

def check_packages():
    """Check if all required packages are installed"""
    print("🔍 Checking required packages...")
    packages = {
        'fastapi': 'FastAPI',
        'uvicorn': 'Uvicorn',
        'pydantic': 'Pydantic',
        'locust': 'Locust'
    }
    
    all_installed = True
    for package, display_name in packages.items():
        if not check_package(package):
            all_installed = False
    
    print()
    return all_installed

def check_files():
    """Check if required files exist"""
    print("🔍 Checking project files...")
    import os
    
    files = [
        'main.py',
        'database.py',
        'db_init.py',
        'locustfile.py',
        'requirements.txt',
        'README.md'
    ]
    
    all_exist = True
    for file in files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} (Missing)")
            all_exist = False
    
    print()
    return all_exist

def main():
    print("=" * 50)
    print("FastAPI Load Testing - Setup Verification")
    print("=" * 50)
    print()
    
    python_ok = check_python_version()
    packages_ok = check_packages()
    files_ok = check_files()
    
    print("=" * 50)
    print("SUMMARY")
    print("=" * 50)
    
    if python_ok and packages_ok and files_ok:
        print("✅ All checks passed! You're ready to go!")
        print()
        print("Next steps:")
        print("1. Initialize database: python db_init.py")
        print("2. Start the server: uvicorn main:app --reload")
        print("3. Run load test: locust -f locustfile.py --host=http://localhost:8000")
        print()
        print("Or use the all-in-one script:")
        print("  Windows: setup_and_start.bat")
        print("  Mac/Linux: ./setup_and_start.sh")
        return 0
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print()
        if not python_ok:
            print("- Install Python 3.8 or higher")
        if not packages_ok:
            print("- Run: pip install -r requirements.txt")
        if not files_ok:
            print("- Make sure all project files are in the current directory")
        return 1

if __name__ == "__main__":
    sys.exit(main())
