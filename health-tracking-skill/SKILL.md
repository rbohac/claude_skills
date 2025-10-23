---
name: Health Tracker
description: Track blood pressure readings and testosterone shot schedules in Google Sheets. Use when the user wants to log BP (format XXX/YYY with pulse) or testosterone shots (with amount and side L/R). Flexible natural language input accepted.
---

# Health Tracker

This skill logs health metrics to Google Sheets with flexible, natural language parsing.

## Capabilities

### Blood Pressure Tracking
Log systolic, diastolic, and pulse readings to the "ABP" tab in Google Sheets.

**Example inputs (all formats work):**
- `bp 120/80 65`
- `blood pressure 120/80 65`
- `120/80 pulse 65`
- `65 120/80`

**Logs to ABP tab:**
- Column A: Timestamp
- Column B: Systolic (e.g., 120)
- Column C: Diastolic (e.g., 80)
- Column D: Pulse (e.g., 65)

### Testosterone Shot Tracking
Log injection amount and injection site to the "shot schedule" tab in Google Sheets.

**Example inputs (all formats work):**
- `testosterone shot left side 0.45`
- `T shot left 0.45`
- `0.45 T left`
- `shot right 0.45`
- `T 0.45 R`

**Logs to shot schedule tab:**
- Column A: Timestamp
- Column B: (empty)
- Column C: Amount in mg (e.g., 0.45)
- Column D: Side - L or R (e.g., L)

## How to Use

When the user provides health data, invoke the Python script `health_tracker.py` with their input as arguments.

**Examples:**
```bash
python3 health_tracker.py bp 120/80 65
python3 health_tracker.py T shot left 0.45
```

## Setup Requirements

Before first use, the user must configure:

1. **Google Sheets API Credentials**
   - Create a Google Cloud project
   - Enable Google Sheets API
   - Create service account credentials (JSON file)
   - Share their Google Sheet with the service account email
   - Save credentials JSON file

2. **Configuration File**
   - Create `config.json` in the skill directory with:
     - `spreadsheet_id`: Google Sheet ID
     - `credentials_path`: Path to credentials JSON
     - `tabs.blood_pressure`: Tab name (default: "ABP")
     - `tabs.shot_schedule`: Tab name (default: "shot schedule")
     - `timezone`: User's timezone

3. **Python Dependencies**
   Install required packages:
   ```bash
   pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
   ```

## Parsing Logic

The script intelligently parses input regardless of order:

### Blood Pressure Detection
- Keywords: `bp`, `blood pressure`, `bloodpressure`
- Pattern: `XXX/YYY` for systolic/diastolic
- Standalone number: pulse/heart rate

### Shot Detection
- Keywords: `testosterone`, `T`, `shot`, `injection`
- Decimal number: amount (e.g., 0.45)
- Side keywords: `left`, `right`, `L`, `R`

## Error Handling

If parsing fails or configuration is missing, provide helpful error messages directing the user to:
1. Check their `config.json` exists and is properly formatted
2. Verify Google Sheets API credentials are set up
3. Ensure the Google Sheet is shared with the service account
4. Confirm tab names match the configuration

## First-Time Setup Guidance

If this is the user's first time using the skill, guide them through:

1. **Google Cloud Setup:**
   - Visit Google Cloud Console
   - Create/select project
   - Enable Google Sheets API
   - Create service account credentials
   - Download JSON credentials file

2. **Share Google Sheet:**
   - Copy service account email from credentials
   - Open their Google Sheet
   - Share with service account email (Editor permissions)
   - Get spreadsheet ID from URL

3. **Create config.json:**
   - Use `config.example.json` as template
   - Fill in spreadsheet_id, credentials_path, tab names, timezone

4. **Test the skill:**
   - Try a simple entry like `bp 120/80 65`
   - Verify it appears in the Google Sheet

## Reference Files

- `health_tracker.py`: Main Python script
- `config.example.json`: Configuration template
- `requirements.txt`: Python dependencies
- `README.md`: Detailed setup instructions
