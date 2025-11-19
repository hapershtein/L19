#!/usr/bin/env python3
"""
Gmail Agent - Retrieve and export emails to Excel
"""
import os
import pickle
import argparse
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment, PatternFill
from dateutil import parser as date_parser

# Gmail API scopes
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


class GmailAgent:
    """Agent to retrieve Gmail messages and export to Excel"""

    def __init__(self, credentials_file='credentials.json'):
        """
        Initialize the Gmail Agent

        Args:
            credentials_file: Path to the OAuth 2.0 credentials JSON file
        """
        self.credentials_file = credentials_file
        self.token_file = 'token.pickle'
        self.service = None

    def authenticate(self):
        """Authenticate with Gmail API using OAuth 2.0"""
        creds = None

        # Check if token.pickle exists (stores user's access and refresh tokens)
        if os.path.exists(self.token_file):
            with open(self.token_file, 'rb') as token:
                creds = pickle.load(token)

        # If there are no valid credentials, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                print("Refreshing access token...")
                creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    raise FileNotFoundError(
                        f"Credentials file '{self.credentials_file}' not found. "
                        "Please download it from Google Cloud Console."
                    )

                print("Starting OAuth 2.0 authentication flow...")
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES
                )
                creds = flow.run_local_server(port=0)

            # Save the credentials for the next run
            with open(self.token_file, 'wb') as token:
                pickle.dump(creds, token)

        self.service = build('gmail', 'v1', credentials=creds)
        print("Successfully authenticated with Gmail API")

    def search_emails(self, query, max_results=100):
        """
        Search for emails using Gmail search syntax

        Args:
            query: Gmail search query (e.g., 'from:example@gmail.com subject:invoice')
            max_results: Maximum number of emails to retrieve

        Returns:
            List of email data dictionaries
        """
        if not self.service:
            raise RuntimeError("Not authenticated. Call authenticate() first.")

        try:
            print(f"Searching for emails with query: '{query}'")
            results = self.service.users().messages().list(
                userId='me',
                q=query,
                maxResults=max_results
            ).execute()

            messages = results.get('messages', [])

            if not messages:
                print("No messages found.")
                return []

            print(f"Found {len(messages)} messages. Retrieving details...")

            email_data = []
            for i, message in enumerate(messages, 1):
                msg_id = message['id']

                # Get full message details
                msg = self.service.users().messages().get(
                    userId='me',
                    id=msg_id,
                    format='metadata',
                    metadataHeaders=['From', 'To', 'Subject', 'Date']
                ).execute()

                # Extract headers
                headers = msg['payload']['headers']
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                date_str = next((h['value'] for h in headers if h['name'] == 'Date'), '')
                from_email = next((h['value'] for h in headers if h['name'] == 'From'), '')

                # Parse date
                try:
                    date_obj = date_parser.parse(date_str)
                    timestamp = date_obj.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    timestamp = date_str

                email_data.append({
                    'id': msg_id,
                    'timestamp': timestamp,
                    'subject': subject,
                    'from': from_email,
                    'search_criteria': query
                })

                if i % 10 == 0:
                    print(f"  Retrieved {i}/{len(messages)} messages...")

            print(f"Successfully retrieved {len(email_data)} emails")
            return email_data

        except HttpError as error:
            print(f"An error occurred: {error}")
            return []

    def export_to_excel(self, email_data, output_file='gmail_export.xlsx'):
        """
        Export email data to Excel file

        Args:
            email_data: List of email data dictionaries
            output_file: Output Excel file path
        """
        if not email_data:
            print("No data to export.")
            return

        print(f"Exporting {len(email_data)} emails to {output_file}...")

        # Create workbook and select active sheet
        wb = Workbook()
        ws = wb.active
        ws.title = "Gmail Export"

        # Define headers
        headers = ['ID', 'TimeStamp', 'Subject', 'Search Criteria']
        ws.append(headers)

        # Style the header row
        header_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
        header_font = Font(bold=True, color='FFFFFF')

        for cell in ws[1]:
            cell.fill = header_fill
            cell.font = header_font
            cell.alignment = Alignment(horizontal='center', vertical='center')

        # Add data rows
        for email in email_data:
            ws.append([
                email['id'],
                email['timestamp'],
                email['subject'],
                email['search_criteria']
            ])

        # Adjust column widths
        ws.column_dimensions['A'].width = 20  # ID
        ws.column_dimensions['B'].width = 20  # TimeStamp
        ws.column_dimensions['C'].width = 50  # Subject
        ws.column_dimensions['D'].width = 30  # Search Criteria

        # Save the workbook
        wb.save(output_file)
        print(f"Successfully exported to {output_file}")


def main():
    """Main function to run the Gmail agent"""
    parser = argparse.ArgumentParser(
        description='Gmail Agent - Retrieve and export emails to Excel',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search for emails from a specific sender
  python gmail_agent.py --query "from:example@gmail.com" --output results.xlsx

  # Search for emails with specific subject
  python gmail_agent.py --query "subject:invoice" --max 50

  # Search for unread emails
  python gmail_agent.py --query "is:unread"

  # Complex search
  python gmail_agent.py --query "from:boss@company.com after:2024/01/01 has:attachment"
        """
    )

    parser.add_argument(
        '--query',
        type=str,
        required=True,
        help='Gmail search query (e.g., "from:example@gmail.com subject:invoice")'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='gmail_export.xlsx',
        help='Output Excel file path (default: gmail_export.xlsx)'
    )

    parser.add_argument(
        '--max',
        type=int,
        default=100,
        help='Maximum number of emails to retrieve (default: 100)'
    )

    parser.add_argument(
        '--credentials',
        type=str,
        default='credentials.json',
        help='Path to OAuth 2.0 credentials file (default: credentials.json)'
    )

    args = parser.parse_args()

    # Create and run the agent
    try:
        agent = GmailAgent(credentials_file=args.credentials)
        agent.authenticate()

        # Search for emails
        emails = agent.search_emails(args.query, max_results=args.max)

        # Export to Excel
        if emails:
            agent.export_to_excel(emails, output_file=args.output)
            print(f"\n✓ Complete! {len(emails)} emails exported to {args.output}")
        else:
            print("\nNo emails found matching the search criteria.")

    except FileNotFoundError as e:
        print(f"\nError: {e}")
        print("\nPlease follow the setup instructions in README.md")
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    main()
