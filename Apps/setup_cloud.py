#!/usr/bin/env python3
"""
Setup script for SecureCloud File Storage
This script helps you configure Google Drive API for cloud storage
"""

import os
import json
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle

# Google Drive API setup
SCOPES = ['https://www.googleapis.com/auth/drive.file']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.pickle'

def setup_google_drive():
    """Setup Google Drive API credentials"""
    print("🔐 SecureCloud Setup - Google Drive Configuration")
    print("=" * 50)
    
    # Check if credentials file exists
    if not os.path.exists(CREDENTIALS_FILE):
        print(f"❌ {CREDENTIALS_FILE} not found!")
        print("\nTo get your Google Drive API credentials:")
        print("1. Go to https://console.cloud.google.com/")
        print("2. Create a new project or select existing one")
        print("3. Enable Google Drive API")
        print("4. Create credentials (OAuth 2.0 Client ID)")
        print("5. Download the JSON file and rename it to 'credentials.json'")
        print("6. Place it in this directory")
        print("\nAfter placing credentials.json here, run this script again.")
        return False
    
    print("✅ Found credentials.json")
    
    try:
        # Create flow with specific redirect URI
        print("OAuth redirect URI used: http://localhost:8081")
        flow = InstalledAppFlow.from_client_secrets_file(
            CREDENTIALS_FILE, 
            SCOPES,
            redirect_uri='http://localhost:8081'
        )
        
        print("🔗 Starting OAuth flow...")
        print("A browser window will open. Please authorize the application.")
        print("If you get an error about redirect URI, follow these steps:")
        print("1. Go to Google Cloud Console > APIs & Services > Credentials")
        print("2. Edit your OAuth 2.0 Client ID")
        print("3. Add 'http://localhost:8081' to Authorized redirect URIs")
        print("4. Save and try again")
        print()
        
        # Run the flow with specific port
        creds = flow.run_local_server(port=8081, prompt='consent')
        
        # Save credentials
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
        
        print("✅ Google Drive API configured successfully!")
        print(f"📁 Token saved to {TOKEN_FILE}")
        print("\n🎉 You can now run the main application!")
        return True
        
    except Exception as e:
        print(f"❌ Error during setup: {str(e)}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure you've added 'http://localhost:8081' to your OAuth redirect URIs")
        print("2. Try running this script again")
        print("3. If still having issues, you can use local-only mode")
        return False


def check_setup():
    """Check if setup is complete"""
    print("🔍 Checking SecureCloud setup...")
    
    if os.path.exists(CREDENTIALS_FILE):
        print("✅ credentials.json found")
    else:
        print("❌ credentials.json missing")
    
    if os.path.exists(TOKEN_FILE):
        print("✅ token.pickle found")
    else:
        print("❌ token.pickle missing")
    
    if os.path.exists('encrypted_files'):
        print("✅ encrypted_files directory exists")
    else:
        print("📁 Creating encrypted_files directory...")
        os.makedirs('encrypted_files', exist_ok=True)
        print("✅ encrypted_files directory created")

def create_simple_credentials():
    """Create a simple credentials file for testing"""
    print("🔧 Creating simple credentials for testing...")
    
    # Create a simple credentials structure
    credentials = {
        "installed": {
            "client_id": "your-client-id.apps.googleusercontent.com",
            "project_id": "your-project-id",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": "your-client-secret",
            "redirect_uris": ["http://localhost:8080"]
        }
    }
    
    with open('credentials_template.json', 'w') as f:
        json.dump(credentials, f, indent=2)
    
    print("📄 Created credentials_template.json")
    print("Please replace the placeholder values with your actual Google API credentials")

if __name__ == "__main__":
    print("🚀 SecureCloud File Storage Setup")
    print("=" * 40)
    
    check_setup()
    print()
    
    if not os.path.exists(TOKEN_FILE):
        if not os.path.exists(CREDENTIALS_FILE):
            print("❌ No credentials.json found!")
            print("\nWould you like to:")
            print("1. Create a template credentials file")
            print("2. Continue with local-only mode")
            
            choice = input("Enter choice (1 or 2): ").strip()
            if choice == "1":
                create_simple_credentials()
                print("\nPlease:")
                print("1. Get your credentials from Google Cloud Console")
                print("2. Replace the template values in credentials_template.json")
                print("3. Rename it to credentials.json")
                print("4. Run this script again")
            else:
                print("✅ Setup for local-only mode complete!")
                print("You can run the main application with: python File_transfer.py")
        else:
            setup_google_drive()
    else:
        print("✅ Setup already complete!")
        print("You can run the main application with: python File_transfer.py") 