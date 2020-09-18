# Adamah
Library and helpers for working with API of www.adamah.at

## Configuration
Add `settings.json` to `/config`, see `/config/settings.sample.json` for reference.

## Functions
### Regular check for new details on upcoming box
``` bash
python3 check_deliveries.py
```
Checks for upcoming boxes having content available. Sends notification email to the recipients configured in `settings.json`.