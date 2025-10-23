# Claude Skills Repository

A collection of custom skills for Claude.ai (web interface) to enhance productivity and automate workflows.

## Available Skills

### Health Tracking Skill

Track your health metrics directly from Claude.ai conversations to Google Sheets with flexible natural language input.

**Location**: `health-tracking-skill/`
**Download**: `health-tracking-skill.zip` (ready to upload to Claude.ai)

**Features**:
- Log blood pressure readings (systolic, diastolic, pulse)
- Track testosterone shot schedule (amount, injection site)
- Flexible natural language input - enter data in any order
- Automatic timestamping with timezone support
- Direct Google Sheets API integration
- Smart parsing that understands various input formats

**Platform**: Claude.ai (web interface) - requires Pro, Max, Team, or Enterprise plan

**Quick Start**:
1. Download `health-tracking-skill.zip`
2. Go to Claude.ai → Settings → Capabilities → Skills
3. Click "Upload skill" and select the ZIP file
4. Follow the setup guide in `CLAUDE_AI_SETUP.md`

**Usage Examples**:

Once configured, just chat naturally with Claude:
```
Log my blood pressure: 120/80 with pulse 65
```
```
I took my T shot today, left side, 0.45mg
```
```
bp 118/76 pulse 68
```
```
Shot 0.45 right
```

**Documentation**:
- [CLAUDE_AI_SETUP.md](health-tracking-skill/CLAUDE_AI_SETUP.md) - Complete setup guide for Claude.ai
- [README.md](health-tracking-skill/README.md) - Detailed technical documentation
- [SKILL.md](health-tracking-skill/SKILL.md) - Skill instructions for Claude

## How It Works

1. **Upload**: Add the skill to your Claude.ai account via Settings
2. **Configure**: Provide your Google Sheets API credentials and spreadsheet ID
3. **Use**: Simply tell Claude about your health metrics in natural language
4. **Automatic**: Claude parses, validates, and logs to your Google Sheet

The skill intelligently handles various input formats and orders, so you don't need to remember exact syntax.

## Requirements

- Claude.ai account (Pro, Max, Team, or Enterprise)
- Google Cloud account (free tier works)
- Google Sheet for data storage
- Code Execution enabled in Claude.ai

## Adding New Skills

To add a new skill to this repository:

1. Create a new directory for your skill
2. Add a `SKILL.md` file with YAML frontmatter (name and description)
3. Implement your skill logic (Python/Node.js scripts, templates, etc.)
4. Add setup documentation
5. Create a ZIP file for easy upload
6. Update this main README

## Skill Format

Skills for Claude.ai use the following structure:

```
skill-name/
├── SKILL.md              # Required: Skill instructions with YAML frontmatter
├── script.py            # Optional: Executable scripts
├── config.example.json  # Optional: Configuration templates
├── README.md            # Optional: Detailed documentation
└── requirements.txt     # Optional: Dependencies
```

## Contributing

Feel free to add new skills or improve existing ones! Submit pull requests with:
- Well-documented skills
- Setup instructions
- Example use cases
- Ready-to-upload ZIP packages

## License

MIT License - feel free to use and modify these skills for your own needs.

---

**Note**: This repository focuses on skills for Claude.ai (web interface). For Claude Code (CLI) skills, the format is similar but installation differs (uses `~/.claude/skills/` directory).
