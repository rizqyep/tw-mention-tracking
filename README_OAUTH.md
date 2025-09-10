# Twitter OAuth Callback API

This directory contains a FastAPI-based OAuth callback system for Twitter authentication.

## Files

- `callback_api.py` - Main FastAPI server with OAuth endpoints
- `oauth2.py` - OAuth2 utility functions
- `run_server.py` - Script to run the server
- `requirements.txt` - Python dependencies

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Update the redirect URI in your Twitter app settings to match your server:
   - For local development: `http://localhost:8000/callback`
   - For production: `https://yourdomain.com/callback`

3. Run the server:
```bash
python run_server.py
```

## Endpoints

### `GET /`
- Home page with OAuth initiation link
- Displays "Login with Twitter" button

### `GET /auth`
- Initiates OAuth flow
- Redirects user to Twitter authorization page
- Stores OAuth handler for callback processing

### `GET /callback`
- Handles OAuth callback from Twitter
- Exchanges authorization code for access token
- Displays success page with token information

### `GET /test-tweet`
- Test endpoint for making tweets (requires valid OAuth session)

## OAuth Flow

1. User visits `/auth`
2. Server redirects to Twitter authorization page
3. User authorizes the application
4. Twitter redirects to `/callback` with authorization code
5. Server exchanges code for access token
6. Server displays success page with token

## Configuration

Update the following in `callback_api.py` and `oauth2.py`:

- `tw_client_id` - Your Twitter app's client ID
- `tw_client_secret` - Your Twitter app's client secret
- `redirect_uri` - Your callback URL (must match Twitter app settings)

## Security Notes

- In production, store access tokens securely in a database
- Use proper session management instead of in-memory storage
- Implement proper error handling and logging
- Consider using environment variables for sensitive data

## Testing

1. Start the server: `python run_server.py`
2. Visit `http://localhost:8000`
3. Click "Login with Twitter"
4. Complete the OAuth flow
5. Check the success page for your access token

