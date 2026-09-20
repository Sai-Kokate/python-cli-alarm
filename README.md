# Python CLI Alarm Clock

A tiny alarm clock you run from the terminal. No web UI, no database — alarms are
stored in a plain `alarms.json` file next to the script, and pure Python stdlib
runs the whole thing.

## Requirements

- Python 3.8+ (stdlib only — no dependencies to run the app)

## Usage

```bash
# Schedule a one-time alarm (24-hour HH:MM)
python3 alarm.py add 07:30 "Wake up"

# See pending alarms
python3 alarm.py list

# Cancel a pending alarm by id
python3 alarm.py remove 1

# Start watching — rings any due alarm with a repeating beep + banner
# until you press Enter. Leave this running for alarms to fire.
python3 alarm.py run
```

Alarms are one-time: once an alarm rings, it's removed from `alarms.json`.

## Testing

Tests use `pytest`. If it's not already installed:

```bash
python3 -m venv .venv
.venv/bin/pip install pytest
.venv/bin/python -m pytest
```

Covers the "is this alarm due" time logic and the add/list/remove persistence
round-trip via temp files — no real waiting/sleeping involved.
