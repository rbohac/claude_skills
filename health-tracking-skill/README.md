# Health Tracking Skill for Claude Code

A Claude Code skill that allows you to quickly log blood pressure readings and testosterone shot schedules to Google Sheets with flexible, natural language input.

## Features

- **Flexible Input Parsing**: Enter data in any order, skill intelligently parses it
- **Blood Pressure Tracking**: Log systolic, diastolic, and pulse readings
- **Testosterone Shot Tracking**: Log injection amount and injection site
- **Automatic Timestamping**: All entries are automatically timestamped
- **Google Sheets Integration**: Data is logged directly to your Google Sheet

## Installation

### 1. Install Python Dependencies

```bash
cd health-tracking-skill
pip install -r requirements.txt
```

### 2. Set Up Google Sheets API

#### Create a Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select an existing one)
3. Enable the Google Sheets API:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Google Sheets API"
   - Click "Enable"

#### Create Service Account Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "Service Account"
3. Fill in the service account details:
   - Name: `claude-health-tracker` (or any name you prefer)
   - Click "Create and Continue"
4. Grant access (you can skip this and click "Continue")
5. Click "Done"
6. Click on the newly created service account
7. Go to the "Keys" tab
8. Click "Add Key" > "Create New Key"
9. Select "JSON" format
10. Download the JSON file
11. Save it securely (e.g., `~/credentials/health-tracker-credentials.json`)

**Important**: Copy the service account email address (looks like `name@project-id.iam.gserviceaccount.com`). You'll need this in the next step.

#### Share Your Google Sheet

1. Open your Google Sheet
2. Click the "Share" button
3. Paste the service account email address
4. Give it "Editor" permissions
5. Uncheck "Notify people" (it's a service account, not a person)
6. Click "Share"

#### Get Your Spreadsheet ID

Your spreadsheet ID is in the URL:
```
https://docs.google.com/spreadsheets/d/SPREADSHEET_ID_HERE/edit
```

### 3. Configure the Skill

Copy the example configuration and fill in your details:

```bash
cp config.example.json config.json
```

Edit `config.json`:

```json
{
  "google_sheets": {
    "spreadsheet_id": "YOUR_SPREADSHEET_ID",
    "credentials_path": "/path/to/your/service-account-credentials.json",
    "tabs": {
      "blood_pressure": "ABP",
      "shot_schedule": "shot schedule"
    }
  },
  "timezone": "America/New_York"
}
```

**Configuration Fields:**
- `spreadsheet_id`: Your Google Sheet ID (from the URL)
- `credentials_path`: Full path to your downloaded credentials JSON file
- `tabs.blood_pressure`: Name of your blood pressure tab (default: "ABP")
- `tabs.shot_schedule`: Name of your shot schedule tab (default: "shot schedule")
- `timezone`: Your timezone (e.g., "America/New_York", "America/Chicago", "UTC")

### 4. Set Up Your Google Sheet

Create or use an existing Google Sheet with two tabs:

#### Tab 1: ABP (Blood Pressure)
| Column | Header | Description |
|--------|--------|-------------|
| A | Date/Time | Auto-populated timestamp |
| B | Systolic | Systolic blood pressure |
| C | Diastolic | Diastolic blood pressure |
| D | Pulse | Heart rate (BPM) |

#### Tab 2: shot schedule
| Column | Header | Description |
|--------|--------|-------------|
| A | Date/Time | Auto-populated timestamp |
| B | (Empty) | Reserved for future use |
| C | Amount | Testosterone amount (mg) |
| D | Side | L (left) or R (right) |

**Note**: You can add headers in row 1 if you like. The skill will automatically find the next empty row.

## Usage

### In Claude Code

Use the `/health` skill command followed by your health data:

#### Blood Pressure Examples

All of these formats work:

```
/health bp 120/80 65
/health blood pressure 120/80 65
/health 120/80 pulse 65
/health 65 120/80
/health 120/80 65 bp
```

**Logs to ABP tab:**
- Column A: Current timestamp
- Column B: 120 (systolic)
- Column C: 80 (diastolic)
- Column D: 65 (pulse)

#### Testosterone Shot Examples

All of these formats work:

```
/health testosterone shot left side 0.45
/health T shot left 0.45
/health 0.45 T left
/health shot right 0.45
/health left 0.45 shot
/health T 0.45 R
```

**Logs to shot schedule tab:**
- Column A: Current timestamp
- Column B: (empty)
- Column C: 0.45 (amount in mg)
- Column D: L or R (side)

### Flexible Input Rules

The parser is smart and flexible:

- **Order doesn't matter**: Put numbers, keywords in any order
- **Keywords are flexible**:
  - Blood pressure: `bp`, `blood pressure`, `bloodpressure`
  - Shots: `testosterone`, `T`, `shot`, `injection`
  - Side: `left`, `right`, `L`, `R`
- **Case insensitive**: `BP`, `bp`, `Bp` all work
- **Pattern recognition**:
  - `XXX/YYY` is automatically recognized as blood pressure
  - Decimal numbers (0.45, .45) recognized for shot amounts
  - Whole numbers recognized for pulse

## Testing

You can test the parser directly:

```bash
python3 health_tracker.py bp 120/80 65
python3 health_tracker.py T shot left 0.45
```

## Troubleshooting

### "Configuration file not found"
- Make sure you've copied `config.example.json` to `config.json`
- Check that `config.json` is in the same directory as `health_tracker.py`

### "Credentials file not found"
- Verify the `credentials_path` in `config.json` points to your downloaded JSON file
- Use absolute paths (e.g., `/home/user/credentials/file.json`)

### "Error accessing tab"
- Verify tab names in `config.json` match your Google Sheet tab names exactly (case-sensitive)
- Make sure you've shared the sheet with your service account email

### "Permission denied" or "403 Forbidden"
- Ensure you've shared the Google Sheet with the service account email
- Verify the service account has "Editor" permissions

### "Could not determine entry type"
- Make sure you're using recognized keywords (`bp`, `shot`, `T`, etc.)
- For blood pressure, use the `XXX/YYY` format
- For shots, include a number and side (left/right/L/R)

## Security Notes

- **Never commit `config.json`** to version control (it's in `.gitignore`)
- **Never commit credentials JSON files** (they're in `.gitignore`)
- Keep your credentials file in a secure location
- The service account only has access to sheets you explicitly share with it

## Examples of Successful Logs

```
Input: /health bp 120/80 65
Output: ✓ Blood pressure logged: 120/80, pulse 65 at 2025-10-22 14:30:15

Input: /health T shot left 0.45
Output: ✓ Shot logged: 0.45mg, L side at 2025-10-22 14:32:00
```

## License

This skill is part of the claude_skills repository.
