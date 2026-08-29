#!/usr/bin/env python3
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "sample-data.json"
SCHEDULES = ROOT / "data" / "schedules"
TARGET = ROOT / "data" / "today.json"


def load_json(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def build_payload(selected_date, source=SOURCE, schedules=SCHEDULES):
    repairs = load_json(source)["repairs"]
    repairs_by_id = {repair["id"]: repair for repair in repairs}
    schedule_path = schedules / f"{selected_date.year}.json"

    if not schedule_path.exists():
        raise ValueError(
            f"Missing schedule for {selected_date.year}. "
            f"Run scripts/generate_schedule.py --year {selected_date.year}."
        )

    schedule = load_json(schedule_path)
    repair_id = schedule.get("days", {}).get(selected_date.isoformat())
    if not repair_id:
        raise ValueError(f"No repair scheduled for {selected_date.isoformat()}")
    if repair_id not in repairs_by_id:
        raise ValueError(
            f"Scheduled repair {repair_id!r} does not exist in {source}"
        )

    return {
        "date": selected_date.isoformat(),
        "repair": repairs_by_id[repair_id],
    }


def parse_args():
    parser = argparse.ArgumentParser(
        description="Build the tiny TRMNL payload from the committed annual schedule."
    )
    parser.add_argument(
        "--date",
        help="UTC date to build as YYYY-MM-DD (default: today in UTC)",
    )
    parser.add_argument("--output", type=Path, default=TARGET)
    return parser.parse_args()


def main():
    args = parse_args()
    selected_date = (
        datetime.strptime(args.date, "%Y-%m-%d").date()
        if args.date
        else datetime.now(timezone.utc).date()
    )
    payload = build_payload(selected_date)
    args.output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(
        f"Built {args.output} for {selected_date.isoformat()}: "
        f"{payload['repair']['id']}"
    )


if __name__ == "__main__":
    main()
