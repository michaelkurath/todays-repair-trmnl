#!/usr/bin/env python3
import argparse
import hashlib
import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "sample-data.json"
SCHEDULES = ROOT / "data" / "schedules"
STRATEGY = "stable-cycle-v1"


def load_repairs(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)["repairs"]


def stable_cycle(repair_ids, year, cycle_number):
    seed = f"todays-repair:{STRATEGY}:{year}:{cycle_number}"

    def rank(repair_id):
        digest = hashlib.sha256(f"{seed}:{repair_id}".encode()).digest()
        return digest, repair_id

    return sorted(repair_ids, key=rank)


def build_schedule(repairs, year):
    repair_ids = [repair["id"] for repair in repairs]
    if not repair_ids:
        raise ValueError("Cannot generate a schedule without repairs")
    if len(repair_ids) != len(set(repair_ids)):
        raise ValueError("Cannot generate a schedule with duplicate repair IDs")

    current = date(year, 1, 1)
    end = date(year + 1, 1, 1)
    days = {}
    cycle_number = 0
    previous_id = None

    while current < end:
        cycle = stable_cycle(repair_ids, year, cycle_number)
        if previous_id == cycle[0] and len(cycle) > 1:
            cycle = cycle[1:] + cycle[:1]

        for repair_id in cycle:
            if current >= end:
                break
            days[current.isoformat()] = repair_id
            previous_id = repair_id
            current += timedelta(days=1)

        cycle_number += 1

    return {
        "schema_version": 1,
        "year": year,
        "timezone": "UTC",
        "strategy": STRATEGY,
        "repair_count_at_generation": len(repair_ids),
        "days": days,
    }


def write_schedule(payload, output, force=False):
    if output.exists() and not force:
        print(f"Schedule already exists; left unchanged: {output}")
        return False

    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {len(payload['days'])} scheduled days to {output}")
    return True


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate one immutable annual repair schedule."
    )
    parser.add_argument(
        "--year",
        type=int,
        default=datetime.now(timezone.utc).year,
        help="UTC calendar year to generate (default: current year)",
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=SOURCE,
        help="Repair dataset to schedule",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Output path (default: data/schedules/YEAR.json)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Explicitly replace an existing schedule",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    output = args.output or SCHEDULES / f"{args.year}.json"
    repairs = load_repairs(args.source)
    payload = build_schedule(repairs, args.year)
    write_schedule(payload, output, force=args.force)


if __name__ == "__main__":
    main()
