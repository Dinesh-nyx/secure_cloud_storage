# 🔐 SecureCloud File Storage

A secure file storage application with local and cloud storage capabilities, featuring AES encryption for data security.

## ✨ Features

- **🔒 AES Encryption**: All files are encrypted before storage
- **☁️ Cloud Storage**: Google Drive integration for backup
- **💾 Local Storage**: Local encrypted file storage
- **🌐 Web Interface**: Modern, responsive web UI
- **📱 Cross-Platform**: Works on Windows, Mac, and Linux

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Setup Google Drive API (Optional)

For cloud storage functionality:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google Drive API
4. Create OAuth 2.0 credentials
5. Download the JSON file and rename it to `credentials.json`
6. Place it in the Apps directory

### 3. Run Setup Script

```bash
python setup_cloud.py
```

This will configure Google Drive API access.

### 4. Start the Application

```bash
python File_transfer.py
```

The application will be available at `http://localhost:5000`

## 📁 File Structure

```
Apps/
├── File_transfer.py          # Main application
├── fullinterface.html        # Web interface
├── setup_cloud.py           # Setup script
├── requirements.txt          # Python dependencies
├── credentials.json         # Google Drive API credentials (you need to add this)
├── token.pickle            # OAuth token (generated during setup)
└── encrypted_files/        # Local encrypted storage
```

## 🔧 Configuration

### Google Drive API Setup

1. **Get API Credentials**:
   - Visit [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project
   - Enable Google Drive API
   - Create OAuth 2.0 Client ID
   - Download credentials as `credentials.json`

2. **Run Setup**:
   ```bash
   python setup_cloud.py
   ```

### Security Settings

The encryption key is defined in `File_transfer.py`:
```python
KEY = b'ThisIsASecretKey'  # 16 bytes key for AES-128
```

**⚠️ Important**: Change this key for production use!

## 🎯 Usage

### Web Interface

1. Open `http://localhost:5000` in your browser
2. Select a file to upload
3. Click "Upload to Cloud Storage"
4. Files are automatically encrypted and stored both locally and in Google Drive
5. Download files using the download links

### API Endpoints

- `POST /upload` - Upload and encrypt a file
- `GET /download/<filename>` - Download and decrypt a file
- `GET /files` - List all available files

## 🔒 Security Features

- **AES-128 Encryption**: All files are encrypted using AES-128 in EAX mode
- **Secure Storage**: Encrypted files stored both locally and in cloud
- **No Plain Text**: Original files are never stored unencrypted
- **Metadata Protection**: File metadata is also encrypted

## 🛠️ Troubleshooting

### Common Issues

1. **Google Drive not working**:
   - Ensure `credentials.json` is in the Apps directory
   - Run `python setup_cloud.py` to configure OAuth
   - Check internet connection

2. **Encryption errors**:
   - Verify the encryption key in `File_transfer.py`
   - Check file permissions

3. **Port already in use**:
   - Change the port in `File_transfer.py` line 69
   - Or kill the process using the port

### Local-Only Mode

If you don't want cloud storage, the application will work with local storage only. Files will be encrypted and stored locally.

## 📝 API Response Examples

### Successful Upload
```json
{
  "message": "File uploaded and encrypted successfully (Local + Cloud)",
  "filename": "document.pdf.enc",
  "cloud_id": "1ABC123DEF456"
}
```

### Upload with Cloud Error
```json
{
  "message": "File uploaded locally only (Cloud upload failed)",
  "filename": "document.pdf.enc",
  "cloud_error": "Google Drive not configured"
}
```

## 🔄 Updates and Maintenance

- **Backup**: Regularly backup the `encrypted_files` directory
- **Updates**: Keep dependencies updated with `pip install -r requirements.txt --upgrade`
- **Security**: Regularly rotate the encryption key

## 📄 License

This project is for educational and personal use. Please ensure compliance with Google Drive API terms of service.

## 🤝 Contributing

Feel free to submit issues and enhancement requests!

---

**Note**: This application provides both local and cloud storage with encryption. Files are always encrypted before storage and decrypted only when downloaded. 