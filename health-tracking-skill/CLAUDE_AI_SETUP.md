# Health Tracker Skill - Claude.ai Setup Guide

This guide shows you how to upload and use the Health Tracker skill on Claude.ai (web interface).

## Prerequisites

- Claude.ai account (Pro, Max, Team, or Enterprise plan)
- Google Cloud account (free tier works)
- Google Sheet for storing health data

## Step 1: Upload the Skill to Claude.ai

1. **Download the skill as ZIP** (if not already packaged)
   - Package the `health-tracking-skill` folder as a ZIP file
   - Or use the provided `health-tracking-skill.zip`

2. **Upload to Claude.ai**
   - Go to [Claude.ai](https://claude.ai)
   - Click Settings (gear icon)
   - Navigate to **Capabilities** tab
   - Scroll to **Skills** section
   - Click **"Upload skill"**
   - Select the `health-tracking-skill.zip` file
   - Toggle the skill **ON** after upload

3. **Verify Code Execution is enabled**
   - In Settings > Capabilities
   - Ensure "Code Execution" is toggled ON
   - This is required for skills to work

## Step 2: Set Up Google Sheets API

### 2.1 Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project:
   - Click project dropdown (top bar)
   - Click "New Project"
   - Name it (e.g., "Claude Health Tracker")
   - Click "Create"

3. Enable Google Sheets API:
   - In the search bar, type "Google Sheets API"
   - Click on "Google Sheets API"
   - Click **"Enable"**

### 2.2 Create Service Account Credentials

1. Go to **"APIs & Services"** > **"Credentials"**
2. Click **"Create Credentials"** > **"Service Account"**
3. Fill in details:
   - **Name**: `claude-health-tracker`
   - **Service account ID**: (auto-generated)
   - Click **"Create and Continue"**
4. Skip the optional steps (click "Continue" then "Done")
5. Click on the newly created service account email
6. Go to **"Keys"** tab
7. Click **"Add Key"** > **"Create New Key"**
8. Select **"JSON"** format
9. Click **"Create"** - a JSON file will download
10. **IMPORTANT**: Copy the service account email address
    - It looks like: `claude-health-tracker@project-name.iam.gserviceaccount.com`
    - You'll need this in the next step

### 2.3 Set Up Your Google Sheet

1. **Create or open your Google Sheet**

2. **Create two tabs:**
   - Tab 1: Name it **"ABP"** (for Blood Pressure)
   - Tab 2: Name it **"shot schedule"** (for testosterone shots)

3. **(Optional) Add headers in Row 1:**

   **ABP tab:**
   | A | B | C | D |
   |---|---|---|---|
   | Date/Time | Systolic | Diastolic | Pulse |

   **shot schedule tab:**
   | A | B | C | D |
   |---|---|---|---|
   | Date/Time | (empty) | Amount | Side |

4. **Share the sheet with your service account:**
   - Click the **"Share"** button (top right)
   - Paste the service account email address
   - Set permission to **"Editor"**
   - **Uncheck** "Notify people"
   - Click **"Share"**

5. **Get your Spreadsheet ID:**
   - Look at your sheet's URL:
   ```
   https://docs.google.com/spreadsheets/d/1abc123DEF456ghi789JKL/edit
                                      ^^^^^ THIS PART ^^^^^
   ```
   - Copy the long ID between `/d/` and `/edit`

## Step 3: Configure the Skill in Claude.ai

Now you'll provide Claude with your configuration. In a conversation with Claude:

### 3.1 Upload Your Credentials File

1. Start a new conversation with Claude
2. Click the paperclip icon (attach files)
3. Upload your downloaded `credentials.json` file
4. Tell Claude: "I'm setting up the Health Tracker skill. This is my Google Sheets service account credentials file."

### 3.2 Provide Configuration

Tell Claude your configuration details. Copy and adapt this message:

```
I'm setting up the Health Tracker skill. Here's my configuration:

Spreadsheet ID: YOUR_SPREADSHEET_ID_HERE
Timezone: America/New_York
Blood Pressure Tab: ABP
Shot Schedule Tab: shot schedule

Please create the config.json file with this information.
```

**Replace:**
- `YOUR_SPREADSHEET_ID_HERE` with your actual spreadsheet ID
- `America/New_York` with your timezone (e.g., "America/Chicago", "America/Los_Angeles", "UTC")

### 3.3 Let Claude Set It Up

Claude will:
1. Read your credentials file
2. Create the `config.json` file
3. Verify the configuration
4. Test the connection to your Google Sheet

## Step 4: Start Using the Skill

Now you can log health data naturally! Just tell Claude things like:

**Blood Pressure:**
```
Log my blood pressure: 120/80 with pulse 65
```
```
bp 120/80 65
```
```
My BP today was 130/85, pulse was 72
```

**Testosterone Shots:**
```
I took my T shot today, left side, 0.45mg
```
```
Shot: 0.45 right
```
```
testosterone injection 0.45 left side
```

Claude will automatically:
- Parse your input (any order works!)
- Log to the correct tab in your Google Sheet
- Confirm the entry was recorded

## Troubleshooting

### "Credentials file not found"
- Make sure you uploaded the credentials JSON file to Claude
- Provide the file again in the conversation

### "Permission denied" or "Cannot access spreadsheet"
- Verify you shared the sheet with the service account email
- Check the service account has "Editor" permissions
- Confirm the spreadsheet ID is correct

### "Cannot find tab"
- Check your tab names match exactly: "ABP" and "shot schedule"
- Tab names are case-sensitive!
- If you used different names, tell Claude the correct tab names

### "Could not parse entry"
- Include BP in format: `XXX/YYY` (e.g., 120/80) with a pulse number
- Include shot with: amount (number) and side (left/right or L/R)

### Skill not appearing
- Check Settings > Capabilities > Skills - toggle it ON
- Ensure Code Execution is enabled
- Requires Pro, Max, Team, or Enterprise plan

## Privacy & Security Notes

- Your credentials file is only stored in the conversation context
- Claude reads it to authenticate with Google Sheets API
- The service account only has access to sheets you explicitly share
- Consider creating a dedicated Google Sheet for health data
- You can revoke service account access anytime in Google Cloud Console

## Using Across Multiple Conversations

The skill is tied to your Claude.ai account, but configuration is per-conversation. For new conversations:

**Option A: Quick setup**
- Upload your credentials JSON
- Provide your spreadsheet ID
- Claude will configure it automatically

**Option B: Keep setup conversation**
- Bookmark your initial setup conversation
- Return to it whenever you want to log health data
- Configuration persists in that conversation

## Updates and Modifications

To change settings:
- **Different timezone**: Tell Claude "Update my timezone to [timezone]"
- **Different tab names**: Tell Claude "Use 'Blood Pressure' for the BP tab instead of 'ABP'"
- **New spreadsheet**: Provide the new spreadsheet ID and share it with the service account

## Example First Use

Here's a complete example of your first interaction:

**You:**
```
I've uploaded the Health Tracker skill. Here's my setup:
- Spreadsheet ID: 1abc123DEF456ghi789JKL
- Timezone: America/New_York
- I've attached my credentials.json file
- My sheet has tabs "ABP" and "shot schedule"

Please set this up and then log my blood pressure: 118/76 pulse 68
```

**Claude will:**
1. Create config.json with your settings
2. Verify the connection
3. Parse your BP reading
4. Log it to your Google Sheet
5. Confirm: "✓ Blood pressure logged: 118/76, pulse 68 at 2025-10-23 14:30:00"

## Questions?

If you encounter issues:
1. Check the main README.md for detailed documentation
2. Verify all prerequisites are met
3. Ensure your Google Sheet is properly shared
4. Confirm your spreadsheet ID is correct

---

**Ready to start?** Go to Step 1 and upload the skill to Claude.ai!
