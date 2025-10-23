# Quick Start: Health Tracking Skill

Get your Health Tracking skill up and running in 5 minutes!

## What You'll Need

- [ ] Claude.ai account (Pro, Max, Team, or Enterprise)
- [ ] Google account
- [ ] 5-10 minutes

## Step 1: Upload to Claude.ai (1 minute)

1. Download `health-tracking-skill.zip` from this repository
2. Go to [Claude.ai](https://claude.ai)
3. Click **Settings** (gear icon) → **Capabilities** tab
4. Scroll to **Skills** section
5. Click **"Upload skill"** button
6. Select `health-tracking-skill.zip`
7. Toggle the skill **ON**
8. Ensure **"Code Execution"** is also enabled

✅ Skill uploaded!

## Step 2: Google Cloud Setup (3 minutes)

### A. Enable Google Sheets API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select existing)
3. Search for "Google Sheets API" and click **Enable**

### B. Create Service Account

1. Go to **APIs & Services** → **Credentials**
2. Click **Create Credentials** → **Service Account**
3. Name it `claude-health-tracker`
4. Click through to finish
5. Click on the new service account
6. Go to **Keys** tab → **Add Key** → **Create New Key**
7. Select **JSON** → **Create**
8. Download the JSON file
9. **Copy the service account email** (you'll need it next!)

✅ Credentials created!

## Step 3: Prepare Your Google Sheet (2 minutes)

1. Create a new Google Sheet (or open existing)
2. Create two tabs:
   - Tab 1: Name it **"ABP"**
   - Tab 2: Name it **"shot schedule"**
3. Click **Share** button (top right)
4. Paste your **service account email**
5. Set permission to **Editor**
6. Uncheck "Notify people"
7. Click **Share**
8. **Copy your Spreadsheet ID** from the URL:
   ```
   https://docs.google.com/spreadsheets/d/YOUR_ID_HERE/edit
   ```

✅ Sheet ready!

## Step 4: Configure in Claude.ai (2 minutes)

1. Start a new conversation with Claude
2. Click paperclip icon → upload your **credentials JSON file**
3. Send this message (fill in your details):

```
I'm setting up the Health Tracker skill. Here's my configuration:

Spreadsheet ID: YOUR_SPREADSHEET_ID_HERE
Timezone: America/New_York
Blood Pressure Tab: ABP
Shot Schedule Tab: shot schedule

Please create the config.json and test the connection.
```

Claude will set everything up for you!

✅ Configured!

## Step 5: Start Tracking! (30 seconds)

Try logging some data:

```
Log my blood pressure: 120/80 with pulse 65
```

or

```
I took my T shot today, left side, 0.45mg
```

Claude will:
- Parse your input
- Log to Google Sheets
- Confirm the entry

Check your Google Sheet - you should see the data!

✅ **You're all set!**

## Example Conversation

**You:**
> Log my blood pressure: 118/76 pulse 68

**Claude:**
> ✓ Blood pressure logged: 118/76, pulse 68 at 2025-10-23 14:30:00

**You:**
> T shot 0.45 left

**Claude:**
> ✓ Shot logged: 0.45mg, L side at 2025-10-23 14:32:00

## Tips

- **Any order works**: `120/80 65` or `65 120/80` both work
- **Natural language**: Just describe your data naturally
- **Check your sheet**: Data appears in real-time
- **Multiple conversations**: Upload credentials in each new chat

## Troubleshooting

- **Can't see skill**: Check Settings → Capabilities → Skills is ON
- **Permission error**: Verify you shared sheet with service account email
- **Can't parse**: Include BP as `XXX/YYY` with pulse number
- **Wrong tab**: Check tab names match: "ABP" and "shot schedule"

## Next Steps

- Read [CLAUDE_AI_SETUP.md](health-tracking-skill/CLAUDE_AI_SETUP.md) for detailed guide
- See [README.md](health-tracking-skill/README.md) for technical details
- Customize tab names and timezone as needed

---

**Having issues?** Check the full setup guide in `CLAUDE_AI_SETUP.md` or the detailed README.
