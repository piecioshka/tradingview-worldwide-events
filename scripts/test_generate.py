#!/usr/bin/env python3
"""Regression tests for generate-events.py and check-events.py.

Run: python3 scripts/test_generate.py
"""

import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


gen = load("gen", os.path.join(HERE, "generate-events.py"))
check = load("check", os.path.join(HERE, "check-events.py"))

def _read(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def _write(path, text):
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)


ROW_HEADER = """# Events

| Date       | Description | Priority | Link |
| ---------- | ----------- | -------- | ---- |
"""


class Sandbox:
    """A throwaway copy of data/ + the Pine file, so tests never touch the repo."""

    def __enter__(self):
        self.dir = tempfile.mkdtemp()
        os.makedirs(os.path.join(self.dir, "data"))
        shutil.copy(os.path.join(ROOT, "worldwide-events.pine"), self.dir)
        return self

    def __exit__(self, *exc):
        shutil.rmtree(self.dir, ignore_errors=True)

    def write(self, rows):
        for lang in ("en", "pl"):
            path = os.path.join(self.dir, "data", f"events-{lang}.md")
            with open(path, "w", encoding="utf-8") as f:
                f.write(ROW_HEADER + "\n".join(rows) + "\n")

    def run_generator(self):
        return subprocess.run(
            [sys.executable, os.path.join(HERE, "generate-events.py")],
            cwd=self.dir, capture_output=True, text=True,
        )

    def pine(self):
        return _read(os.path.join(self.dir, "worldwide-events.pine"))

    def validate(self):
        return subprocess.run(
            [sys.executable, os.path.join(HERE, "check-events.py"), "--no-http"],
            cwd=self.dir, capture_output=True, text=True,
        )


GOOD = "| 2026-09-08 | Plain description | high | - |"


class TestGeneratorRobustness(unittest.TestCase):
    def test_backslash_escapes_are_not_interpreted(self):
        """Event text must never be parsed as an re replacement template."""
        for payload in (r"Fed cut rates by \1 pp", r"Marker \g<1> here", r"Path C:\temp"):
            with self.subTest(payload=payload), Sandbox() as box:
                box.write([f"| 2026-09-08 | {payload} | high | - |"])
                r = box.run_generator()
                if r.returncode == 0:
                    self.assertIn(payload, box.pine())
                    self.assertNotIn("if barstate.isfirst\n pp", box.pine())

    def test_missing_marker_is_an_error(self):
        with Sandbox() as box:
            box.write([GOOD])
            path = os.path.join(box.dir, "worldwide-events.pine")
            src = _read(path)
            _write(path, src.replace("// @generated lang-input\n", ""))
            self.assertNotEqual(box.run_generator().returncode, 0)

    def test_duplicated_marker_is_an_error(self):
        with Sandbox() as box:
            box.write([GOOD])
            path = os.path.join(box.dir, "worldwide-events.pine")
            src = _read(path)
            block = "// @generated lang-arrays\nvar labels_en = array.new_string()\nvar labels_pl = array.new_string()\n// @end-generated\n"
            _write(path, src.replace(block, block * 2, 1))
            self.assertNotEqual(box.run_generator().returncode, 0)

    def test_missing_events_sentinel_is_an_error(self):
        with Sandbox() as box:
            box.write([GOOD])
            path = os.path.join(box.dir, "worldwide-events.pine")
            src = _read(path)
            _write(path, src.replace("if barstate.islast", "if barstate.isLAST"))
            self.assertNotEqual(box.run_generator().returncode, 0)

    def test_duplicate_date_is_an_error(self):
        with Sandbox() as box:
            box.write([GOOD, "| 2026-09-08 | Another one | low | - |"])
            self.assertNotEqual(box.run_generator().returncode, 0)

    def test_generator_is_idempotent(self):
        with Sandbox() as box:
            box.write([GOOD])
            self.assertEqual(box.run_generator().returncode, 0)
            once = box.pine()
            self.assertEqual(box.run_generator().returncode, 0)
            self.assertEqual(once, box.pine())


class TestTimestamps(unittest.TestCase):
    def test_bare_date_becomes_midnight_utc(self):
        self.assertEqual(gen.to_iso_utc("2026-09-08"), "2026-09-08T00:00:00+00:00")

    def test_time_of_day_is_kept(self):
        self.assertEqual(gen.to_iso_utc("2026-09-08 14:30"), "2026-09-08T14:30:00+00:00")
        self.assertEqual(gen.to_iso_utc("2026-09-08 14:30:05"), "2026-09-08T14:30:05+00:00")

    def test_invalid_time_is_an_error(self):
        with self.assertRaises(SystemExit):
            gen.to_iso_utc("2026-09-08 14")

    def test_row_with_time_flows_through_the_generator(self):
        with Sandbox() as box:
            box.write(["| 2026-09-08 14:30 | Timed event | high | - |"])
            self.assertEqual(box.run_generator().returncode, 0)
            self.assertIn('timestamp("2026-09-08T14:30:00+00:00")', box.pine())

    def test_validator_accepts_a_time_of_day(self):
        with Sandbox() as box:
            box.write(["| 2026-09-08 14:30 | Timed event | high | - |"])
            self.assertEqual(box.validate().returncode, 0)


class TestValidatorCatches(unittest.TestCase):
    def assert_rejected(self, row):
        with Sandbox() as box:
            box.write([row])
            self.assertNotEqual(box.validate().returncode, 0, f"accepted: {row}")

    def test_backslash(self):
        self.assert_rejected(r"| 2026-09-08 | Loss of \9 pct | high | - |")

    def test_pipe_in_description(self):
        self.assert_rejected("| 2026-09-08 | Desc with | pipe | high | - |")

    def test_double_quote(self):
        self.assert_rejected('| 2026-09-08 | A "quoted" word | high | - |')

    def test_good_row_passes(self):
        with Sandbox() as box:
            box.write([GOOD])
            self.assertEqual(box.validate().returncode, 0)


class TestLinkRegex(unittest.TestCase):
    def test_angle_bracket_url_keeps_parentheses(self):
        m = check.LINK.search("[Wikipedia](<https://pl.wikipedia.org/wiki/Foo_(1987)>)")
        self.assertEqual(m.group(1), "https://pl.wikipedia.org/wiki/Foo_(1987)")

    def test_plain_url(self):
        m = check.LINK.search("[CNBC](https://www.cnbc.com/a.html)")
        self.assertEqual(m.group(2), "https://www.cnbc.com/a.html")


if __name__ == "__main__":
    unittest.main(verbosity=2)
