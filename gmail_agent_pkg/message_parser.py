"""
Email message parsing utilities
"""
import re
import base64
from dateutil import parser as date_parser
from logger_config import LoggerConfig

logger = LoggerConfig.setup_logger('gmail_agent')


class MessageParser:
    """Parse and extract information from Gmail messages"""

    @staticmethod
    def extract_first_url(text):
        """
        Extract the first URL found in text

        Args:
            text: Text to search for URLs

        Returns:
            First URL found or empty string
        """
        if not text:
            return ''

        url_pattern = r'https?://github\.com[^\s<>"{}|\\^`\[\]]+'

        match = re.search(url_pattern, text)
        if match:
            url = match.group(0)
            url = re.sub(r'[,;.\)]+$', '', url)
            return url

        return ''

    @staticmethod
    def get_message_body(payload):
        """
        Extract text from email message payload

        Args:
            payload: Gmail message payload

        Returns:
            Email body text
        """
        body = ''

        if 'body' in payload and 'data' in payload['body']:
            body = base64.urlsafe_b64decode(payload['body']['data']).decode('utf-8', errors='ignore')
        elif 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    if 'data' in part['body']:
                        body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
                        break
                elif part['mimeType'] == 'text/html' and not body:
                    if 'data' in part['body']:
                        body = base64.urlsafe_b64decode(part['body']['data']).decode('utf-8', errors='ignore')
                elif 'parts' in part:
                    body = MessageParser.get_message_body(part)
                    if body:
                        break

        return body

    @staticmethod
    def parse_message_metadata(msg, query):
        """
        Parse message metadata and extract key information

        Args:
            msg: Gmail message object
            query: Search query used

        Returns:
            Dictionary with parsed message data
        """
        headers = msg['payload']['headers']
        subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
        date_str = next((h['value'] for h in headers if h['name'] == 'Date'), '')
        from_email = next((h['value'] for h in headers if h['name'] == 'From'), '')

        try:
            date_obj = date_parser.parse(date_str)
            timestamp = date_obj.strftime('%Y-%m-%d %H:%M:%S')
        except Exception as e:
            logger.warning(f"Failed to parse date '{date_str}': {e}")
            timestamp = date_str

        body = MessageParser.get_message_body(msg['payload'])
        repo_url = MessageParser.extract_first_url(body)

        return {
            'id': msg['id'],
            'timestamp': timestamp,
            'subject': subject,
            'from': from_email,
            'search_criteria': query,
            'repo_url': repo_url
        }
