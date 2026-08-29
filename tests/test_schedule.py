import json
import tempfile
import unittest
from datetime import date
from pathlib import Path
from unittest import mock

from scripts import build_today, generate_schedule, validate_data


class ScheduleTests(unittest.TestCase):
    def setUp(self):
        self.repairs = [
            {"id": "repair-a", "title": "Repair A"},
            {"id": "repair-b", "title": "Repair B"},
            {"id": "repair-c", "title": "Repair C"},
        ]

    def test_schedule_is_deterministic_complete_and_balanced(self):
        first = generate_schedule.build_schedule(self.repairs, 2028)
        second = generate_schedule.build_schedule(list(reversed(self.repairs)), 2028)

        self.assertEqual(first, second)
        self.assertEqual(len(first["days"]), 366)

        scheduled_ids = list(first["days"].values())
        self.assertTrue(
            all(left != right for left, right in zip(scheduled_ids, scheduled_ids[1:]))
        )

        counts = [scheduled_ids.count(repair["id"]) for repair in self.repairs]
        self.assertLessEqual(max(counts) - min(counts), 1)

    def test_existing_schedule_is_immutable_by_default(self):
        payload = generate_schedule.build_schedule(self.repairs, 2026)

        with tempfile.TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "2026.json"
            self.assertTrue(generate_schedule.write_schedule(payload, output))
            original = output.read_text(encoding="utf-8")

            changed = dict(payload)
            changed["strategy"] = "unexpected-replacement"
            self.assertFalse(generate_schedule.write_schedule(changed, output))
            self.assertEqual(output.read_text(encoding="utf-8"), original)

    def test_today_payload_uses_scheduled_id(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "repairs.json"
            schedules = root / "schedules"
            schedules.mkdir()

            source.write_text(
                json.dumps({"repairs": self.repairs}), encoding="utf-8"
            )
            (schedules / "2026.json").write_text(
                json.dumps(
                    {
                        "year": 2026,
                        "days": {"2026-08-29": "repair-b"},
                    }
                ),
                encoding="utf-8",
            )

            payload = build_today.build_payload(
                date(2026, 8, 29), source=source, schedules=schedules
            )

            self.assertEqual(payload["date"], "2026-08-29")
            self.assertEqual(payload["repair"]["id"], "repair-b")

    def test_validation_rejects_missing_repair_id(self):
        payload = generate_schedule.build_schedule(self.repairs, 2026)
        payload["days"]["2026-08-29"] = "missing-repair"

        with tempfile.TemporaryDirectory() as temporary_directory:
            schedules = Path(temporary_directory)
            (schedules / "2026.json").write_text(
                json.dumps(payload), encoding="utf-8"
            )
            errors = []

            with mock.patch.object(validate_data, "SCHEDULES", schedules):
                validate_data.validate_schedules(self.repairs, errors)

            self.assertTrue(
                any("references missing repair missing-repair" in error for error in errors)
            )


if __name__ == "__main__":
    unittest.main()
