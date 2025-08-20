from flask import Flask, request, send_file, jsonify, render_template
from werkzeug.utils import secure_filename
from Crypto.Cipher import AES
import os
import json
import base64
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import io
import pickle

app = Flask(__name__)
UPLOAD_FOLDER = 'encrypted_files'
KEY = b'ThisIsASecretKey'  # 16 bytes key for AES-128

# Google Drive API setup
SCOPES = ['https://www.googleapis.com/auth/drive.file']
CREDENTIALS_FILE = 'credentials.json'
TOKEN_FILE = 'token.pickle'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_google_drive_service():
    """Get Google Drive service instance"""
    creds = None
    
    # Load existing token
    if os.path.exists(TOKEN_FILE):
        try:
            with open(TOKEN_FILE, 'rb') as token:
                creds = pickle.load(token)
        except Exception as e:
            print(f"Failed to load token.pickle: {str(e)}")
            creds = None
    
    # If no valid credentials, get new ones
    if not creds or not creds.valid:
        try:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                if os.path.exists(CREDENTIALS_FILE):
                    print("OAuth redirect URI used: http://localhost:8081")
                    flow = InstalledAppFlow.from_client_secrets_file(
                        CREDENTIALS_FILE, 
                        SCOPES,
                        redirect_uri='http://localhost:8081'
                    )
                    creds = flow.run_local_server(port=8081, prompt='consent')
                else:
                    print("Credentials file not found.")
                    return None
        except Exception as e:
            print(f"OAuth setup failed: {str(e)}")
            print("Please run: python setup_cloud.py")
            return None
        
        # Save credentials
        try:
            with open(TOKEN_FILE, 'wb') as token:
                pickle.dump(creds, token)
        except Exception as e:
            print(f"Failed to save token.pickle: {str(e)}")
    
    try:
        service = build('drive', 'v3', credentials=creds)
        print("Google Drive service initialized successfully.")
        return service
    except Exception as e:
        print(f"Failed to build Google Drive service: {str(e)}")
        return None

# AES encryption
def encrypt_file(file_data, key):
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(file_data)
    return cipher.nonce + tag + ciphertext

# AES decryption
def decrypt_file(encrypted_data, key):
    nonce = encrypted_data[:16]
    tag = encrypted_data[16:32]
    ciphertext = encrypted_data[32:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt_and_verify(ciphertext, tag)

# Upload to cloud storage
def upload_to_cloud(file_data, filename):
    """Upload encrypted file to Google Drive"""
    print(f"☁️ Starting cloud upload for: {filename}")
    print(f"📊 File size: {len(file_data)} bytes")
    
    try:
        print("🔐 Initializing Google Drive service...")
        service = get_google_drive_service()
        if not service:
            print("❌ Google Drive service initialization failed")
            return None, "Google Drive not configured"
        
        print("✅ Google Drive service initialized successfully")
        
        # Create file metadata
        file_metadata = {
            'name': filename + '.enc',
            'parents': []  # Upload to root folder
        }
        print(f"📝 File metadata created: {file_metadata['name']}")
        
        # Create media upload
        print("📤 Creating media upload object...")
        media = MediaIoBaseUpload(
            io.BytesIO(file_data),
            mimetype='application/octet-stream',
            resumable=True
        )
        
        # Upload file
        print("🚀 Starting file upload to Google Drive...")
        try:
            file = service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            cloud_id = file.get('id')
            print(f"✅ Cloud upload successful! File ID: {cloud_id}")
            print(f"🔗 Google Drive URL: https://drive.google.com/file/d/{cloud_id}/view")
            return cloud_id, None
        except Exception as e:
            print(f"❌ Cloud upload failed: {str(e)}")
            return None, str(e)
    except Exception as e:
        print(f"❌ Error initializing Google Drive service: {str(e)}")
        return None, str(e)

# Download from cloud storage
def download_from_cloud(file_id):
    """Download encrypted file from Google Drive"""
    try:
        service = get_google_drive_service()
        if not service:
            return None, "Google Drive not configured"
        
        # Download file
        request = service.files().get_media(fileId=file_id)
        file_data = request.execute()
        
        return file_data, None
    except Exception as e:
        return None, str(e)

# List files from cloud
def list_cloud_files():
    """List all encrypted files from Google Drive"""
    try:
        service = get_google_drive_service()
        if not service:
            return [], "Google Drive not configured"
        
        # List files
        results = service.files().list(
            pageSize=50,
            fields="nextPageToken, files(id, name, createdTime)"
        ).execute()
        
        files = results.get('files', [])
        return files, None
    except Exception as e:
        return [], str(e)

@app.route('/')
def index():
    return render_template('fullinterface.html')

# Upload endpoint
@app.route('/upload', methods=['POST'])
def upload_file():
    print("\n" + "="*60)
    print("📁 NEW FILE UPLOAD REQUEST")
    print("="*60)
    
    if 'file' not in request.files:
        print("❌ No file part in request")
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        print("❌ No selected file")
        return jsonify({'error': 'No selected file'}), 400

    filename = secure_filename(file.filename)
    print(f"📄 Original filename: {file.filename}")
    print(f"🔒 Secure filename: {filename}")
    
    file_data = file.read()
    print(f"📊 Original file size: {len(file_data)} bytes")
    
    print("🔐 Encrypting file with AES-128...")
    encrypted_data = encrypt_file(file_data, KEY)
    print(f"🔒 Encrypted file size: {len(encrypted_data)} bytes")

    # Save locally
    encrypted_path = os.path.join(app.config['UPLOAD_FOLDER'], filename + '.enc')
    print(f"💾 Saving encrypted file locally: {encrypted_path}")
    with open(encrypted_path, 'wb') as f:
        f.write(encrypted_data)
    print("✅ Local storage completed")

    # Upload to cloud
    print("\n☁️ Starting cloud upload process...")
    cloud_file_id, cloud_error = upload_to_cloud(encrypted_data, filename)
    
    if cloud_file_id:
        # Save metadata
        metadata = {
            'filename': filename,
            'cloud_id': cloud_file_id,
            'local_path': encrypted_path
        }
        metadata_path = os.path.join(app.config['UPLOAD_FOLDER'], filename + '.meta.json')
        print(f"📝 Saving metadata: {metadata_path}")
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f)
        
        print("✅ METADATA SAVED SUCCESSFULLY")
        print(f"📋 Cloud ID: {cloud_file_id}")
        print(f"📁 Encrypted filename: {filename}.enc")
        print("🎉 UPLOAD COMPLETED SUCCESSFULLY (Local + Cloud)")
        print("="*60 + "\n")
        
        return jsonify({
            'message': 'File uploaded and encrypted successfully (Local + Cloud)',
            'filename': filename + '.enc',
            'cloud_id': cloud_file_id
        }), 200
    else:
        print("⚠️ CLOUD UPLOAD FAILED - Local storage only")
        print(f"❌ Cloud error: {cloud_error}")
        print("="*60 + "\n")
        
        return jsonify({
            'message': 'File uploaded locally only (Cloud upload failed)',
            'filename': filename + '.enc',
            'cloud_error': cloud_error
        }), 200

# Download endpoint
@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    metadata_path = os.path.join(app.config['UPLOAD_FOLDER'], filename.replace('.enc', '.meta.json'))
    
    # Try local file first
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            encrypted_data = f.read()
    elif os.path.exists(metadata_path):
        # Try cloud download
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        
        cloud_data, cloud_error = download_from_cloud(metadata['cloud_id'])
        if cloud_data:
            encrypted_data = cloud_data
        else:
            return jsonify({'error': 'File not found locally or in cloud', 'cloud_error': cloud_error}), 404
    else:
        return jsonify({'error': 'File not found'}), 404

    try:
        decrypted_data = decrypt_file(encrypted_data, KEY)
    except Exception as e:
        return jsonify({'error': 'Decryption failed', 'details': str(e)}), 500

    decrypted_filename = filename.replace('.enc', '')
    decrypted_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_' + decrypted_filename)
    with open(decrypted_path, 'wb') as f:
        f.write(decrypted_data)

    return send_file(decrypted_path, as_attachment=True, download_name=decrypted_filename)

# List files endpoint
@app.route('/files', methods=['GET'])
def list_files():
    files = []
    cloud_file_names = set()
    
    # Get local files and check for metadata
    local_files = os.listdir(app.config['UPLOAD_FOLDER'])
    for file in local_files:
        if file.endswith('.enc'):
            # Check if there's metadata for this file
            metadata_path = os.path.join(app.config['UPLOAD_FOLDER'], file.replace('.enc', '.meta.json'))
            cloud_id = None
            if os.path.exists(metadata_path):
                try:
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)
                        cloud_id = metadata.get('cloud_id')
                except:
                    pass
            
            file_info = {'name': file, 'source': 'local'}
            if cloud_id:
                file_info['cloud_id'] = cloud_id
                file_info['source'] = 'both'
            files.append(file_info)
    
    # Get cloud files
    cloud_files, cloud_error = list_cloud_files()
    if cloud_error:
        print(f"Error fetching cloud files: {cloud_error}")
        # Return local files only if cloud fetch fails
        return jsonify(files)
    else:
        for file in cloud_files:
            if file['name'].endswith('.enc'):
                cloud_file_names.add(file['name'])
                # Check if this file is also local
                local_exists = any(f['name'] == file['name'] for f in files)
                source = 'both' if local_exists else 'cloud'
                files.append({
                    'name': file['name'], 
                    'source': source, 
                    'id': file['id'],
                    'cloud_id': file['id']
                })
    
    # Remove duplicates if any (local and cloud files with same name)
    unique_files = []
    seen_names = set()
    for f in files:
        if f['name'] not in seen_names:
            unique_files.append(f)
            seen_names.add(f['name'])
    
    return jsonify(unique_files)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
