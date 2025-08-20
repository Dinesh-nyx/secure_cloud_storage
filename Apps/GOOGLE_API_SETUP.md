# Google Drive API Setup Guide

This guide will help you set up Google Drive API for the File Transfer application.

## Prerequisites

- A Google account
- Python 3.7+ installed
- Required Python packages (install with `pip install -r requirements.txt`)

## Step-by-Step Setup

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Sign in with your Google account
3. Click on the project dropdown at the top
4. Click "New Project"
5. Enter a project name (e.g., "File Transfer App")
6. Click "Create"

### 2. Enable Google Drive API

1. In the left sidebar, go to **APIs & Services** → **Library**
2. Search for "Google Drive API"
3. Click on "Google Drive API" from the results
4. Click **Enable**

### 3. Configure OAuth Consent Screen

1. Go to **APIs & Services** → **OAuth consent screen**
2. Choose **External** user type
3. Fill in required information:
   - **App name**: File Transfer App
   - **User support email**: Your email address
   - **Developer contact information**: Your email address
4. Click **Save and Continue**
5. Skip optional fields and click **Save and Continue**
6. Click **Back to Dashboard**

### 4. Create OAuth 2.0 Credentials

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **OAuth client ID**
3. Choose **Desktop application** as application type
4. Enter a name: "File Transfer Desktop Client"
5. Click **Create**
6. Click **Download JSON**
7. Rename the downloaded file to `credentials.json`
8. Place it in the `Apps` directory of your project

### 5. Configure Redirect URIs

1. Go back to **Credentials** page
2. Click on your OAuth 2.0 Client ID
3. Add these **Authorized redirect URIs**:
   - `http://localhost:8081`
   - `http://localhost:8080`
4. Click **Save**

### 6. Test Your Setup

Run the test script to verify everything is working:

```bash
cd Apps
python test_google_api.py
```

## Troubleshooting

### Common Issues

1. **"redirect_uri_mismatch" error**
   - Make sure you've added the correct redirect URIs in Google Cloud Console
   - The app uses `http://localhost:8081` as the primary redirect URI

2. **"API not enabled" error**
   - Go to Google Cloud Console → APIs & Services → Library
   - Search for "Google Drive API" and enable it

3. **"Invalid credentials" error**
   - Make sure your `credentials.json` file is in the correct location
   - Verify the file hasn't been corrupted

4. **"Quota exceeded" error**
   - Google Drive API has usage limits
   - For personal use, the default quotas are usually sufficient

### File Structure

After setup, your `Apps` directory should contain:
```
Apps/
├── credentials.json          # Your OAuth credentials
├── token.pickle             # Generated after first authentication
├── test_google_api.py       # Test script
├── setup_cloud.py           # Setup script
├── check_google_drive.py    # Drive checker
└── File_transfer.py         # Main application
```

## Security Notes

- Keep your `credentials.json` file secure and don't share it
- The `token.pickle` file contains your access tokens
- Never commit these files to version control
- Add them to your `.gitignore` file

## API Quotas and Limits

- **Google Drive API v3** has daily quotas
- Default quotas are usually sufficient for personal use
- Monitor usage in Google Cloud Console → APIs & Services → Dashboard

## Next Steps

Once setup is complete:
1. Run `python setup_cloud.py` to configure the application
2. Run `python File_transfer.py` to start the main application
3. Access the web interface at `http://localhost:5000`


