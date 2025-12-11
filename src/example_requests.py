#!/usr/bin/env python3
"""
Example script demonstrating the requests package
This shows how packages installed in your virtual environment work
"""

import requests

def main():
    print("✅ Successfully imported 'requests' package!")
    print(f"   Package version: {requests.__version__}\n")
    
    # Try a simple, reliable API endpoint
    print("Making a GET request to jsonplaceholder.typicode.com...")
    try:
        # This is a reliable testing API
        response = requests.get("https://jsonplaceholder.typicode.com/posts/1", timeout=5)
        
        # Check if the request was successful
        if response.status_code == 200:
            print(f"✅ Success! Status code: {response.status_code}")
            print(f"\nResponse data (first post):")
            data = response.json()
            print(f"  - Post ID: {data.get('id')}")
            print(f"  - Title: {data.get('title', 'N/A')[:50]}...")
            print(f"  - User ID: {data.get('userId')}")
        else:
            print(f"⚠️  Unexpected status code: {response.status_code}")
            print("   (But the package is working - this is just a server response)")
            
    except requests.exceptions.Timeout:
        print("⏱️  Request timed out (network might be slow)")
        print("   But the 'requests' package is installed and working!")
    except requests.exceptions.RequestException as e:
        print(f"⚠️  Network error: {e}")
        print("   This is a network/connectivity issue, NOT a package problem.")
        print("   The 'requests' package is correctly installed in your venv!")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
    
    print("\n" + "="*60)
    print("Key takeaway:")
    print("The 'requests' package is installed and working in your venv!")
    print("If you see 'Successfully imported', the package is correctly set up.")
    print("Network errors are separate from package installation issues.")
    print("="*60)

if __name__ == "__main__":
    main()

