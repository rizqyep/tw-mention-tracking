# X API Authentication Example

This repository provides an example of how to authenticate with X (formerly Twitter) using OAuth2 in Python. The implementation includes environment variable management, API authentication, and database interaction.

## Features

- Authenticate with X API using OAuth2
- Manage API keys securely via `.env` files
- Store and retrieve authentication tokens
- Send authenticated requests to X API

## X API Limits
The free tier of X API is extremely limited and only allows 17 posts per day, and 500 posts per month per app. Make sure to implement rate controls and test your code locally.

## Prerequisites

Ensure you have the following installed on your system:

- Python 3.9 or higher
- `git` (optional, for cloning the repository)
- A registered X API developer account with client credentials

## Setup

### 1. Clone the Repository

```sh
git clone https://github.com/hakehardware/x_api_auth_example.git
cd x_api_auth_example
```

### 2. Create a Virtual Environment (Optional but Recommended)

To keep dependencies isolated, use a virtual environment:

```sh
python -m venv venv
```

Activate the virtual environment:

- **Windows:**
  ```sh
  venv\Scripts\activate
  ```
- **Linux/macOS:**
  ```sh
  source venv/bin/activate
  ```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Copy the example environment file and configure your credentials:

```sh
cp .env.example .env
```

Edit the `.env` file and add your X API credentials:

```ini
X_CLIENT_ID="YOUR APP'S CLIENT ID"
X_APP_SECRET="YOUR APP'S SECRET"
```

You must also set the callback URL to be `http://localhost:5000/oauth/callback`

### 5. Run the Authentication Script

To test authentication with X:

```sh
python example.py
```
You must navigate to `http://localhost:5000` in order to authorize the app manually. This only needs to be done once as the access token and refresh token will be stored in the database and refereshed automatically.

If everything worked, you should get a sucess message in the browser, and the post should be visable on the account which approved the app.

## Logging and Debugging

Enable logging for better visibility of API requests and responses. Modify `logging` settings in the script to output detailed logs for debugging. DEBUG should be helpful for testing, and INFO for less verbose logging.

## Security Considerations

- Never share your `.env` file or API credentials.
- Use environment variables instead of hardcoding credentials in scripts.
- Regularly update dependencies with:
  ```sh
  pip install --upgrade -r requirements.txt
  ```

## Contributing

Feel free to submit issues or pull requests to improve this project.

## License

This project is open-source and available under the [MIT License](LICENSE).

---

Happy coding! 🚀
