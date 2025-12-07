"""
Gmail draft creation module
"""
import base64
from email.mime.text import MIMEText
from googleapiclient.errors import HttpError
from logger_config import LoggerConfig
from .gmail_auth import GmailAuthenticator
from .excel_reader import ExcelReader

logger = LoggerConfig.setup_logger('email_drafter')


class EmailDrafter:
    """Create Gmail draft messages from feedback messages"""

    def __init__(self, input_file='Output_34.xlsx', credentials_file='credentials.json'):
        """
        Initialize EmailDrafter

        Args:
            input_file: Excel file with feedback messages
            credentials_file: Path to OAuth credentials
        """
        self.input_file = input_file
        self.credentials_file = credentials_file
        self.authenticator = GmailAuthenticator(credentials_file)
        self.service = None
        self.data = []

    def authenticate(self):
        """Authenticate with Gmail API"""
        self.service = self.authenticator.authenticate()

    def read_excel_data(self):
        """Read feedback messages from Excel file"""
        self.data = ExcelReader.read_feedback_data(self.input_file)
        return self.data

    def create_draft(self, repo_id, feedback_message, subject_prefix=None):
        """
        Create a Gmail draft message

        Args:
            repo_id: Repository ID for subject line
            feedback_message: The feedback message content
            subject_prefix: Optional subject prefix

        Returns:
            Draft ID if successful, None otherwise
        """
        try:
            if subject_prefix:
                subject = f"{subject_prefix} - Feedback message to {repo_id}"
            else:
                subject = f"Feedback message to {repo_id}"

            message = MIMEText(feedback_message)
            message['subject'] = subject

            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')

            draft_body = {
                'message': {
                    'raw': raw_message
                }
            }

            draft = self.service.users().drafts().create(
                userId='me',
                body=draft_body
            ).execute()

            return draft['id']

        except HttpError as error:
            logger.error(f"HttpError creating draft for {repo_id}: {error}")
            LoggerConfig.log_exception(logger, error, f"create_draft for {repo_id}")
            print(f"  ✗ Error creating draft: {error}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error creating draft for {repo_id}: {e}")
            LoggerConfig.log_exception(logger, e, f"create_draft for {repo_id}")
            print(f"  ✗ Unexpected error: {e}")
            return None

    def create_all_drafts(self):
        """Create Gmail drafts for all feedback messages"""
        print(f"{'='*70}")
        print(f"Creating Gmail Draft Messages")
        print(f"{'='*70}\n")

        success_count = 0
        failed_count = 0
        results = []

        for idx, data_row in enumerate(self.data, 1):
            repo_id = data_row['id']
            feedback = data_row['feedback']
            subject_prefix = data_row.get('subject', None)

            logger.info(f"[{idx}/{len(self.data)}] Creating draft for ID: {repo_id}")
            print(f"[{idx}/{len(self.data)}] Creating draft for ID: {repo_id}")

            draft_id = self.create_draft(repo_id, feedback, subject_prefix)

            if draft_id:
                logger.info(f"Draft created successfully for {repo_id}, draft_id={draft_id}")
                print(f"  ✓ Draft created successfully (ID: {draft_id})")
                success_count += 1
                results.append({'id': repo_id, 'draft_id': draft_id, 'status': 'success'})
            else:
                logger.error(f"Failed to create draft for {repo_id}")
                print(f"  ✗ Failed to create draft")
                failed_count += 1
                results.append({'id': repo_id, 'draft_id': None, 'status': 'failed'})

        print(f"\n{'='*70}")
        print(f"Draft Creation Summary")
        print(f"{'='*70}")
        print(f"Total Feedback Messages: {len(self.data)}")
        print(f"Drafts Created: {success_count}")
        print(f"Failed: {failed_count}")
        print(f"\n✓ Drafts are available in your Gmail account under 'Drafts' folder")

        return {
            'total': len(self.data),
            'success': success_count,
            'failed': failed_count,
            'results': results
        }

    def run(self):
        """Main execution flow"""
        self.authenticate()
        self.read_excel_data()

        if not self.data:
            print("No feedback messages found to draft. Exiting.")
            return None

        results = self.create_all_drafts()
        return results
