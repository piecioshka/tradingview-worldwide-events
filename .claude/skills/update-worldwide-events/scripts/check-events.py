#!/usr/bin/env python3
"""Sanity checks for data/events-*.md in tradingview-worldwide-events.

Usage: check-events.py [--since YYYY-MM-DD] [--data-dir data] [--no-http]

Checks: same date set in every language file, descending order, no double quotes in
descriptions, description length, a real link on every row newer than --since, and
HTTP status of those links. Exit code 1 when any check fails.
"""

import argparse
import glob
import os
import re
import sys
import urllib.request

ROW = re.compile(r"^\| (\d{4}-\d{2}-\d{2}) +\| (.*?) +\| (high|medium|low) +\| (.*?) +\|$")
LINK = re.compile(r"\[[^\]]+\]\(<?(https?://[^)>]+)>?\)")
MAX_DESC = 90


def parse(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            line = line.rstrip("\n")
            if not line.startswith("| ") or line.startswith("| Date") or line.startswith("| ---"):
                continue
            m = ROW.match(line)
            if not m:
                rows.append((n, None, line, None, None))
                continue
            rows.append((n, m.group(1), m.group(2), m.group(3), m.group(4)))
    return rows


def http_status(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return r.status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception as e:  # noqa: BLE001
        return f"ERR {type(e).__name__}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", help="check links only for rows newer than this date")
    ap.add_argument("--data-dir", default="data")
    ap.add_argument("--no-http", action="store_true")
    args = ap.parse_args()

    files = sorted(glob.glob(os.path.join(args.data_dir, "events-*.md")))
    if not files:
        print(f"no events-*.md in {args.data_dir}")
        return 1

    problems = []
    dates_by_file = {}
    for path in files:
        rows = parse(path)
        dates = []
        for n, date, desc, prio, link in rows:
            if date is None:
                problems.append(f"{path}:{n}: unparsable row: {desc[:60]}")
                continue
            dates.append(date)
            if '"' in desc:
                problems.append(f"{path}:{n}: double quote in description (breaks Pine string)")
            if len(desc) > MAX_DESC:
                problems.append(f"{path}:{n}: description {len(desc)} chars (> {MAX_DESC})")
            is_new = args.since is None or date > args.since
            if is_new:
                m = LINK.search(link)
                if not m:
                    problems.append(f"{path}:{n}: {date} has no link")
                elif not args.no_http:
                    status = http_status(m.group(1))
                    if status != 200:
                        problems.append(f"{path}:{n}: {date} link -> {status}: {m.group(1)}")
        if dates != sorted(dates, reverse=True):
            problems.append(f"{path}: rows are not sorted descending by date")
        if len(dates) != len(set(dates)):
            dup = sorted({d for d in dates if dates.count(d) > 1})
            problems.append(f"{path}: duplicate dates {dup}")
        dates_by_file[path] = set(dates)

    base = files[0]
    for path in files[1:]:
        only_base = sorted(dates_by_file[base] - dates_by_file[path])
        only_other = sorted(dates_by_file[path] - dates_by_file[base])
        if only_base:
            problems.append(f"{path}: missing dates present in {base}: {only_base}")
        if only_other:
            problems.append(f"{base}: missing dates present in {path}: {only_other}")

    for p in problems:
        print(p)
    print(f"{len(files)} files, {len(dates_by_file[base])} events, {len(problems)} problems")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
