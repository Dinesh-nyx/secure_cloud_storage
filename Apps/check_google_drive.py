#!/usr/bin/env python3
"""
Simple script to check Google Drive connection and list files
"""

import os
import json
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle

# Google Drive API setup
SCOPES = ['https://www.googleapis.com/auth/drive.file']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.pickle'

def get_google_drive_service():
    """Get Google Drive service instance"""
    creds = None
    
    # Load existing token
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'rb') as token:
            creds = pickle.load(token)
    
    # If no valid credentials, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if os.path.exists(CREDENTIALS_FILE):
                flow = InstalledAppFlow.from_client_secrets_file(
                    CREDENTIALS_FILE, 
                    SCOPES,
                    redirect_uri='http://localhost:8080'
                )
                creds = flow.run_local_server(port=8080, prompt='consent')
            else:
                return None
        
        # Save credentials
        with open(TOKEN_FILE, 'wb') as token:
            pickle.dump(creds, token)
    
    return build('drive', 'v3', credentials=creds)

def list_all_files():
    """List all files from Google Drive"""
    try:
        service = get_google_drive_service()
        if not service:
            print("❌ Google Drive not configured")
            return
        
        print("🔍 Fetching files from Google Drive...")
        
        # List files
        results = service.files().list(
            pageSize=50,
            fields="nextPageToken, files(id, name, createdTime, size)"
        ).execute()
        
        files = results.get('files', [])
        
        if not files:
            print("📁 No files found in Google Drive")
        else:
            print(f"📁 Found {len(files)} files in Google Drive:")
            for file in files:
                print(f"  📄 {file['name']} (ID: {file['id']})")
        
        # Check for encrypted files specifically
        encrypted_files = [f for f in files if f['name'].endswith('.enc')]
        if encrypted_files:
            print(f"\n🔐 Found {len(encrypted_files)} encrypted files:")
            for file in encrypted_files:
                print(f"  🔒 {file['name']} (ID: {file['id']})")
        else:
            print("\n❌ No encrypted files found in Google Drive")
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")

def check_local_metadata():
    """Check local metadata files"""
    print("\n🔍 Checking local metadata files...")
    
    if not os.path.exists('encrypted_files'):
        print("❌ encrypted_files directory not found")
        return
    
    metadata_files = [f for f in os.listdir('encrypted_files') if f.endswith('.meta.json')]
    
    if not metadata_files:
        print("❌ No metadata files found")
        return
    
    print(f"📁 Found {len(metadata_files)} metadata files:")
    for meta_file in metadata_files:
        try:
            with open(os.path.join('encrypted_files', meta_file), 'r') as f:
                metadata = json.load(f)
                print(f"  📄 {metadata['filename']} -> Cloud ID: {metadata['cloud_id']}")
        except Exception as e:
            print(f"  ❌ Error reading {meta_file}: {str(e)}")

if __name__ == "__main__":
    print("🔐 Google Drive Connection Check")
    print("=" * 40)
    
    check_local_metadata()
    list_all_files() 