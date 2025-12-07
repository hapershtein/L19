"""
Gmail authentication module
"""
import os
import pickle
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from logger_config import LoggerConfig

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
logger = LoggerConfig.setup_logger('gmail_agent')


class GmailAuthenticator:
    """Handle Gmail API authentication"""

    def __init__(self, credentials_file='credentials.json', token_file='token.pickle'):
        """
        Initialize authenticator

        Args:
            credentials_file: Path to the OAuth 2.0 credentials JSON file
            token_file: Path to the token file
        """
        self.credentials_file = credentials_file
        self.token_file = token_file

    def authenticate(self):
        """
        Authenticate with Gmail API using OAuth 2.0

        Returns:
            Gmail API service instance
        """
        logger.info("Starting Gmail API authentication")
        creds = None

        if os.path.exists(self.token_file):
            logger.debug(f"Loading existing token from {self.token_file}")
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)
            logger.info("Loaded existing authentication token")

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                logger.info("Token expired, refreshing access token")
                print("Refreshing access token...")
                creds.refresh(Request())
                logger.info("Access token refreshed successfully")
            else:
                if not os.path.exists(self.credentials_file):
                    logger.error(f"Credentials file not found: {self.credentials_file}")
                    raise FileNotFoundError(
                        f"Credentials file '{self.credentials_file}' not found. "
                        "Please download it from Google Cloud Console."
                    )

                logger.info("Starting OAuth 2.0 authentication flow")
                print("Starting OAuth 2.0 authentication flow...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES
                )

                try:
                    logger.debug("Attempting browser authentication")
                    creds = flow.run_local_server(port=0, open_browser=True)
                    logger.info("Browser authentication successful")
                except Exception as e:
                    logger.warning(f"Browser authentication failed: {e}")
                    logger.info("Falling back to console authentication")
                    print(f"\nCouldn't open browser automatically: {e}")
                    print("\nUsing console authentication flow instead...")
                    print("You'll receive a URL to visit in your browser.\n")
                    creds = flow.run_console()
                    logger.info("Console authentication successful")

            logger.debug(f"Saving credentials to {self.token_file}")
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)
            logger.info("Credentials saved for future use")

        service = build('gmail', 'v1', credentials=creds)
        logger.info("Gmail API service built successfully")
        print("Successfully authenticated with Gmail API")

        return service
