#!/usr/bin/env python3
"""
Health Tracking Skill for Claude Code
Logs blood pressure and testosterone shots to Google Sheets
"""

import sys
import json
import os
import re
from datetime import datetime
from typing import Dict, Optional, Tuple, Any
import pytz

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


class HealthDataParser:
    """Flexible parser for health tracking commands"""

    # Keywords for different tracking types
    BP_KEYWORDS = ['bp', 'blood pressure', 'bloodpressure']
    SHOT_KEYWORDS = ['testosterone', 't', 'shot', 'injection', 'inject']
    SIDE_KEYWORDS = {
        'left': 'L',
        'l': 'L',
        'right': 'R',
        'r': 'R'
    }

    @classmethod
    def parse(cls, input_text: str) -> Dict[str, Any]:
        """
        Parse input text and determine what type of health data it is
        Returns dict with 'type' and relevant data fields
        """
        input_lower = input_text.lower().strip()

        # Check if it's a blood pressure entry
        if cls._is_blood_pressure(input_lower):
            return cls._parse_blood_pressure(input_text)

        # Check if it's a testosterone shot entry
        elif cls._is_shot(input_lower):
            return cls._parse_shot(input_text)

        else:
            return {
                'type': 'unknown',
                'error': 'Could not determine entry type. Use "bp" for blood pressure or "shot/T/testosterone" for injections.'
            }

    @classmethod
    def _is_blood_pressure(cls, text: str) -> bool:
        """Check if text indicates blood pressure entry"""
        # Look for BP keywords or blood pressure pattern XXX/YYY
        has_bp_keyword = any(kw in text for kw in cls.BP_KEYWORDS)
        has_bp_pattern = bool(re.search(r'\d{2,3}/\d{2,3}', text))
        return has_bp_keyword or has_bp_pattern

    @classmethod
    def _is_shot(cls, text: str) -> bool:
        """Check if text indicates shot entry"""
        return any(kw in text for kw in cls.SHOT_KEYWORDS)

    @classmethod
    def _parse_blood_pressure(cls, text: str) -> Dict[str, Any]:
        """
        Parse blood pressure entry
        Expected data: systolic/diastolic and pulse
        Examples: "bp 120/80 65", "65 120/80", "blood pressure 120/80 pulse 65"
        """
        # Find blood pressure reading (XXX/YYY pattern)
        bp_match = re.search(r'(\d{2,3})/(\d{2,3})', text)
        if not bp_match:
            return {
                'type': 'blood_pressure',
                'error': 'Could not find blood pressure reading (format: XXX/YYY)'
            }

        systolic = int(bp_match.group(1))
        diastolic = int(bp_match.group(2))

        # Find pulse - look for standalone numbers
        # Remove the BP reading from text first
        text_without_bp = text.replace(bp_match.group(0), '')
        pulse_match = re.search(r'\b(\d{2,3})\b', text_without_bp)

        if not pulse_match:
            return {
                'type': 'blood_pressure',
                'error': 'Could not find pulse reading (provide a number like 65)'
            }

        pulse = int(pulse_match.group(1))

        return {
            'type': 'blood_pressure',
            'systolic': systolic,
            'diastolic': diastolic,
            'pulse': pulse
        }

    @classmethod
    def _parse_shot(cls, text: str) -> Dict[str, Any]:
        """
        Parse testosterone shot entry
        Expected data: amount and side (left/right)
        Examples: "T shot left 0.45", "0.45 right testosterone", "shot L 0.45"
        """
        text_lower = text.lower()

        # Find amount (decimal number)
        amount_match = re.search(r'\b(\d*\.?\d+)\b', text)
        if not amount_match:
            return {
                'type': 'shot',
                'error': 'Could not find amount (provide a number like 0.45)'
            }

        amount = float(amount_match.group(1))

        # Find side (left/right/L/R)
        side = None
        for keyword, value in cls.SIDE_KEYWORDS.items():
            if keyword in text_lower.split():  # Check whole words
                side = value
                break

        if not side:
            return {
                'type': 'shot',
                'error': 'Could not determine injection side. Please specify "left/L" or "right/R"'
            }

        return {
            'type': 'shot',
            'amount': amount,
            'side': side
        }


class GoogleSheetsLogger:
    """Handle Google Sheets API interactions"""

    def __init__(self, config: Dict):
        self.config = config
        self.service = self._authenticate()
        self.spreadsheet_id = config['google_sheets']['spreadsheet_id']
        self.tabs = config['google_sheets']['tabs']

        # Setup timezone
        tz_name = config.get('timezone', 'UTC')
        self.timezone = pytz.timezone(tz_name)

    def _authenticate(self):
        """Authenticate with Google Sheets API using service account"""
        creds_path = self.config['google_sheets']['credentials_path']

        if not os.path.exists(creds_path):
            raise FileNotFoundError(
                f"Credentials file not found: {creds_path}\n"
                "Please ensure your service account credentials are properly configured."
            )

        SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        creds = service_account.Credentials.from_service_account_file(
            creds_path, scopes=SCOPES
        )

        return build('sheets', 'v4', credentials=creds)

    def _get_next_empty_row(self, tab_name: str) -> int:
        """Find the next empty row in column A of the specified tab"""
        try:
            # Read column A to find the last filled row
            range_name = f"{tab_name}!A:A"
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()

            values = result.get('values', [])
            # Next empty row is one after the last filled row
            return len(values) + 1

        except HttpError as e:
            raise Exception(f"Error accessing tab '{tab_name}': {e}")

    def _get_current_timestamp(self) -> str:
        """Get current timestamp in the configured timezone"""
        now = datetime.now(self.timezone)
        return now.strftime('%Y-%m-%d %H:%M:%S')

    def log_blood_pressure(self, systolic: int, diastolic: int, pulse: int) -> str:
        """
        Log blood pressure to Google Sheets
        Columns: A=DateTime, B=Systolic, C=Diastolic, D=Pulse
        """
        tab_name = self.tabs['blood_pressure']
        next_row = self._get_next_empty_row(tab_name)
        timestamp = self._get_current_timestamp()

        # Prepare data
        values = [[timestamp, systolic, diastolic, pulse]]
        range_name = f"{tab_name}!A{next_row}:D{next_row}"

        # Write to sheet
        body = {'values': values}
        self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()

        return f"✓ Blood pressure logged: {systolic}/{diastolic}, pulse {pulse} at {timestamp}"

    def log_shot(self, amount: float, side: str) -> str:
        """
        Log testosterone shot to Google Sheets
        Columns: A=DateTime, B=(empty), C=Amount, D=Side
        """
        tab_name = self.tabs['shot_schedule']
        next_row = self._get_next_empty_row(tab_name)
        timestamp = self._get_current_timestamp()

        # Prepare data (Column B is empty as per requirements)
        values = [[timestamp, '', amount, side]]
        range_name = f"{tab_name}!A{next_row}:D{next_row}"

        # Write to sheet
        body = {'values': values}
        self.service.spreadsheets().values().update(
            spreadsheetId=self.spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()

        return f"✓ Shot logged: {amount}mg, {side} side at {timestamp}"


def load_config() -> Dict:
    """Load configuration from config.json"""
    # Look for config.json in the same directory as this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, 'config.json')

    if not os.path.exists(config_path):
        raise FileNotFoundError(
            f"Configuration file not found: {config_path}\n"
            "Please copy config.example.json to config.json and fill in your details."
        )

    with open(config_path, 'r') as f:
        return json.load(f)


def main():
    """Main entry point for the health tracking skill"""
    try:
        # Get input from command line arguments
        if len(sys.argv) < 2:
            print("Usage: health <entry>")
            print("\nExamples:")
            print("  health bp 120/80 65")
            print("  health 65 120/80")
            print("  health T shot left 0.45")
            print("  health 0.45 right shot")
            sys.exit(1)

        # Join all arguments as the input text
        input_text = ' '.join(sys.argv[1:])

        # Parse the input
        parsed_data = HealthDataParser.parse(input_text)

        if parsed_data.get('error'):
            print(f"Error: {parsed_data['error']}")
            print("\nExamples:")
            print("  Blood pressure: bp 120/80 65")
            print("  Testosterone shot: T shot left 0.45")
            sys.exit(1)

        # Load configuration
        config = load_config()

        # Initialize Google Sheets logger
        logger = GoogleSheetsLogger(config)

        # Log the appropriate type of entry
        if parsed_data['type'] == 'blood_pressure':
            result = logger.log_blood_pressure(
                parsed_data['systolic'],
                parsed_data['diastolic'],
                parsed_data['pulse']
            )
            print(result)

        elif parsed_data['type'] == 'shot':
            result = logger.log_shot(
                parsed_data['amount'],
                parsed_data['side']
            )
            print(result)

        else:
            print(f"Unknown entry type: {parsed_data['type']}")
            sys.exit(1)

    except FileNotFoundError as e:
        print(f"Configuration Error: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
