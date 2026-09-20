#!/usr/bin/env python3
"""CLI alarm clock. Alarms persist to alarms.json; `run` watches and rings them."""
import argparse
import json
import sys
import threading
import time
from datetime import datetime
from pathlib import Path

DEFAULT_PATH = Path(__file__).parent / "alarms.json"


def load_alarms(path=DEFAULT_PATH):
    if not path.exists():
        return []
    return json.loads(path.read_text())


def save_alarms(alarms, path=DEFAULT_PATH):
    path.write_text(json.dumps(alarms, indent=2))


def is_due(alarm, now):
    return now.strftime("%H:%M") == alarm["time"]


def add_alarm(time_str, label, path=DEFAULT_PATH):
    datetime.strptime(time_str, "%H:%M")  # raises ValueError if malformed
    alarms = load_alarms(path)
    next_id = max((a["id"] for a in alarms), default=0) + 1
    alarms.append({"id": next_id, "time": time_str, "label": label})
    save_alarms(alarms, path)
    return next_id


def remove_alarm(alarm_id, path=DEFAULT_PATH):
    alarms = load_alarms(path)
    remaining = [a for a in alarms if a["id"] != alarm_id]
    save_alarms(remaining, path)
    return len(remaining) != len(alarms)


def ring(alarm):
    print(f"\n\U0001F570  ALARM: {alarm['label']} ({alarm['time']}) — press Enter to dismiss")
    stop_event = threading.Event()
    threading.Thread(target=lambda: (input(), stop_event.set()), daemon=True).start()
    while not stop_event.is_set():
        print("\a", end="", flush=True)
        stop_event.wait(1)


def run(path=DEFAULT_PATH):
    print("Watching for alarms... (Ctrl+C to stop)")
    try:
        while True:
            alarms = load_alarms(path)
            now = datetime.now()
            due = [a for a in alarms if is_due(a, now)]
            if due:
                for alarm in due:
                    ring(alarm)
                due_ids = {a["id"] for a in due}
                save_alarms([a for a in alarms if a["id"] not in due_ids], path)
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopped watching.")


def main():
    parser = argparse.ArgumentParser(description="A simple CLI alarm clock.")
    sub = parser.add_subparsers(dest="command", required=True)

    p_add = sub.add_parser("add", help="Schedule a one-time alarm")
    p_add.add_argument("time", help="HH:MM, 24-hour")
    p_add.add_argument("label", help="What the alarm is for")

    sub.add_parser("list", help="Show pending alarms")

    p_remove = sub.add_parser("remove", help="Cancel a pending alarm")
    p_remove.add_argument("id", type=int)

    sub.add_parser("run", help="Watch for and ring due alarms")

    args = parser.parse_args()

    if args.command == "add":
        try:
            alarm_id = add_alarm(args.time, args.label)
        except ValueError:
            print(f"Invalid time '{args.time}', expected HH:MM (24-hour).", file=sys.stderr)
            sys.exit(1)
        print(f"Added alarm {alarm_id}: {args.time} — {args.label}")
    elif args.command == "list":
        alarms = sorted(load_alarms(), key=lambda a: a["time"])
        if not alarms:
            print("No pending alarms.")
        for a in alarms:
            print(f"[{a['id']}] {a['time']} — {a['label']}")
    elif args.command == "remove":
        if remove_alarm(args.id):
            print(f"Removed alarm {args.id}.")
        else:
            print(f"No alarm with id {args.id}.", file=sys.stderr)
            sys.exit(1)
    elif args.command == "run":
        run()


if __name__ == "__main__":
    main()
