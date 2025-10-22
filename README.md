# Claude Skills Repository

A collection of custom skills for Claude Code to enhance productivity and automate workflows.

## Available Skills

### Health Tracking Skill

Track your health metrics directly from Claude Code to Google Sheets.

**Location**: `health-tracking-skill/`

**Features**:
- Log blood pressure readings (systolic, diastolic, pulse)
- Track testosterone shot schedule (amount, injection site)
- Flexible natural language input - enter data in any order
- Automatic timestamping
- Direct Google Sheets integration

**Quick Start**:
```bash
cd health-tracking-skill
pip install -r requirements.txt
cp config.example.json config.json
# Edit config.json with your Google Sheets details
```

**Usage Examples**:
```
/health bp 120/80 65
/health T shot left 0.45
/health 65 120/80
/health 0.45 right shot
```

See [health-tracking-skill/README.md](health-tracking-skill/README.md) for detailed setup instructions.

## Adding New Skills

To add a new skill to this repository:

1. Create a new directory for your skill
2. Add a `skill.json` manifest file
3. Implement your skill logic
4. Add a README.md with setup and usage instructions
5. Update this main README with your skill information

## Contributing

Feel free to add new skills or improve existing ones!

## License

MIT License - feel free to use and modify these skills for your own needs.
