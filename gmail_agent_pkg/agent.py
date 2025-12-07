"""
Gmail Agent main class
"""
from googleapiclient.errors import HttpError
from logger_config import LoggerConfig
from .authenticator import GmailAuthenticator
from .message_parser import MessageParser
from .excel_exporter import ExcelExporter

logger = LoggerConfig.setup_logger('gmail_agent')


class GmailAgent:
    """Agent to retrieve Gmail messages and export to Excel"""

    def __init__(self, credentials_file='credentials.json'):
        """
        Initialize the Gmail Agent

        Args:
            credentials_file: Path to the OAuth 2.0 credentials JSON file
        """
        self.credentials_file = credentials_file
        self.authenticator = GmailAuthenticator(credentials_file)
        self.service = None

    def authenticate(self):
        """Authenticate with Gmail API using OAuth 2.0"""
        self.service = self.authenticator.authenticate()

    def search_emails(self, query, max_results=100):
        """
        Search for emails using Gmail search syntax

        Args:
            query: Gmail search query
            max_results: Maximum number of emails to retrieve

        Returns:
            List of email data dictionaries
        """
        logger.info(f"Starting email search with query: '{query}', max_results: {max_results}")

        if not self.service:
            logger.error("Gmail service not initialized - authentication required")
            raise RuntimeError("Not authenticated. Call authenticate() first.")

        try:
            print(f"Searching for emails with query: '{query}'")
            logger.debug(f"Calling Gmail API messages().list() with userId='me', query='{query}'")
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()

            messages = results.get('messages', [])
            logger.info(f"API returned {len(messages)} message IDs")

            if not messages:
                logger.info("No messages found matching query")
                print("No messages found.")
                return []

            print(f"Found {len(messages)} messages. Retrieving details...")
            logger.info(f"Starting to retrieve full details for {len(messages)} messages")

            email_data = []
            for i, message in enumerate(messages, 1):
                msg_id = message['id']
                logger.debug(f"Processing message {i}/{len(messages)}, ID: {msg_id}")

                msg = self.service.users().messages().get(
                    userId='me',
                    id=msg_id,
                    format='full'
                ).execute()

                parsed_data = MessageParser.parse_message_metadata(msg, query)
                email_data.append(parsed_data)

                if parsed_data['repo_url']:
                    logger.debug(f"Message {i}: Extracted URL: {parsed_data['repo_url']}")
                else:
                    logger.debug(f"Message {i}: No URL found in body")

                if i % 10 == 0:
                    print(f"  Retrieved {i}/{len(messages)} messages...")
                    logger.info(f"Progress: Retrieved {i}/{len(messages)} messages")

            logger.info(f"Successfully retrieved all {len(email_data)} emails")
            print(f"Successfully retrieved {len(email_data)} emails")
            return email_data

        except HttpError as error:
            logger.error(f"Gmail API HttpError: {error}")
            LoggerConfig.log_exception(logger, error, "search_emails")
            print(f"An error occurred: {error}")
            return []
        except Exception as error:
            logger.error(f"Unexpected error in search_emails: {error}")
            LoggerConfig.log_exception(logger, error, "search_emails")
            return []

    def export_to_excel(self, email_data, output_file='gmail_export.xlsx'):
        """
        Export email data to Excel file

        Args:
            email_data: List of email data dictionaries
            output_file: Output Excel file path
        """
        ExcelExporter.export_to_excel(email_data, output_file)
