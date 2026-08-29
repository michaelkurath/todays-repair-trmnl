#!/usr/bin/env python3
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "sample-data.json"
TARGET = ROOT / "data" / "today.json"


def main():
    payload = json.loads(SOURCE.read_text(encoding="utf-8"))
    repairs = payload["repairs"]
    day_of_year = date.today().timetuple().tm_yday
    repair = repairs[day_of_year % len(repairs)]
    TARGET.write_text(json.dumps({"repair": repair}, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()

