#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "sample-data.json"
VERIFICATIONS = ROOT / "data" / "verifications.json"

REQUIRED_REPAIR_FIELDS = {
    "id",
    "category",
    "title",
    "summary",
    "why_it_matters",
    "caveat",
    "source_name",
    "source_url",
    "source_checked",
}

REQUIRED_CHECK_FIELDS = {
    "id",
    "status",
    "checked_on",
    "evidence",
    "note",
}

ALLOWED_STATUSES = {
    "verified",
    "verified_with_note",
    "needs_follow_up",
    "corrected",
}


def load_json(path):
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)


def fail(errors, message):
    errors.append(message)


def validate_required_fields(kind, item, required, errors):
    item_id = item.get("id", "<missing id>")
    for field in sorted(required):
        if item.get(field) in (None, ""):
            fail(errors, f"{kind} {item_id}: missing {field}")


def validate_repairs(repairs, errors):
    seen = set()
    for repair in repairs:
        validate_required_fields("repair", repair, REQUIRED_REPAIR_FIELDS, errors)
        repair_id = repair.get("id")
        if repair_id in seen:
            fail(errors, f"repair {repair_id}: duplicate id")
        seen.add(repair_id)

        source_url = repair.get("source_url", "")
        if source_url and not source_url.startswith("https://"):
            fail(errors, f"repair {repair_id}: source_url must use https")

        for field in ("title", "summary", "why_it_matters", "caveat"):
            if "\n" in repair.get(field, ""):
                fail(errors, f"repair {repair_id}: {field} must be one line")


def validate_verifications(repairs, checks, errors):
    repair_ids = {repair["id"] for repair in repairs}
    check_ids = set()

    for check in checks:
        validate_required_fields("verification", check, REQUIRED_CHECK_FIELDS, errors)
        check_id = check.get("id")
        if check_id in check_ids:
            fail(errors, f"verification {check_id}: duplicate id")
        check_ids.add(check_id)

        status = check.get("status")
        if status not in ALLOWED_STATUSES:
            fail(errors, f"verification {check_id}: unknown status {status}")

    missing_checks = sorted(repair_ids - check_ids)
    extra_checks = sorted(check_ids - repair_ids)

    for repair_id in missing_checks:
        fail(errors, f"repair {repair_id}: missing verification")

    for check_id in extra_checks:
        fail(errors, f"verification {check_id}: no matching repair")


def main():
    errors = []
    repairs = load_json(DATA).get("repairs", [])
    verification_payload = load_json(VERIFICATIONS)
    checks = verification_payload.get("checks", [])

    validate_repairs(repairs, errors)
    validate_verifications(repairs, checks, errors)

    if errors:
        for error in errors:
            print(error, file=sys.stderr)
        return 1

    print(f"Validated {len(repairs)} repairs and {len(checks)} verification records.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
