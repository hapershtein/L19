"""
Gmail authentication module for email drafting
"""
import os
import sys
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from logger_config import LoggerConfig

logger = LoggerConfig.setup_logger('email_drafter')

SCOPES = ['https://www.googleapis.com/auth/gmail.compose']


class GmailAuthenticator:
    """Handle Gmail API authentication for draft creation"""

    def __init__(self, credentials_file='credentials.json', token_file='token_drafter.pickle'):
        """
        Initialize authenticator

        Args:
            credentials_file: Path to OAuth credentials
            token_file: Path to token file
        """
        self.credentials_file = credentials_file
        self.token_file = token_file

    def authenticate(self):
        """
        Authenticate with Gmail API

        Returns:
            Gmail API service instance
        """
        logger.info("Starting Gmail API authentication for draft creation")
        logger.info(f"Using separate token file: {self.token_file} (for gmail.compose scope)")
        creds = None

        if os.path.exists(self.token_file):
            logger.debug(f"Loading existing token from {self.token_file}")
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Token refresh failed: {e}")
                    print("Re-authenticating...")
                    creds = None

            if not creds:
                if not os.path.exists(self.credentials_file):
                    print(f"Error: Credentials file '{self.credentials_file}' not found!")
                    print("Please download your OAuth 2.0 credentials from Google Cloud Console")
                    sys.exit(1)

                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES)

                try:
                    creds = flow.run_local_server(port=0, open_browser=True)
                except Exception as e:
                    print(f"\nCouldn't open browser automatically: {e}")
                    print("\nUsing console authentication flow instead...")
                    print("Please copy the URL below and paste it into your browser,")
                    print("then paste the authorization code back here.\n")
                    creds = flow.run_console()

            logger.debug(f"Saving credentials to {self.token_file}")
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)
            logger.info("Credentials saved for future use")

        service = build('gmail', 'v1', credentials=creds)
        logger.info("Successfully authenticated with Gmail API")
        print("✓ Successfully authenticated with Gmail API\n")

        return service
