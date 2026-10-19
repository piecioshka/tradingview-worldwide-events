# Contributing to Worldwide Events

How the event data is stored, how the Pine Script is generated and how changes are checked. For what the indicator does, see the [README](README.md).

## Requirements

Python 3 (the scripts use only the standard library; CI runs `python-version: "3.x"`).

## Editing events

Events are stored in `data/events-en.md` and `data/events-pl.md`. The Pine Script file is generated automatically - do not edit it by hand.

To regenerate `worldwide-events.pine` after modifying event data:

```bash
python scripts/generate-events.py
```

To add a new language, create `data/events-XX.md` (where `XX` is the ISO language code) using the same table format as the existing files. The generator and GitHub Actions workflow will pick it up automatically.

## Event data format

Each row is `| Date | Description | Priority | Link |`:

- **Date** - `YYYY-MM-DD`, or `YYYY-MM-DD HH:MM[:SS]` when the time of day is known. Rows are sorted descending and every language file must cover exactly the same set of dates. Times are **UTC**: the generator emits `timestamp("...T00:00:00+00:00")`, so an event lands on the same instant regardless of the chart's exchange timezone.
- **Description** - plain text, no double quotes (they would break the generated Pine string).
- **Priority** - `high`, `medium` or `low`; drives the marker color.
- **Link** - a source for the event, or `-` when none is recorded. Links are documentation for contributors only - they are **not** rendered by the indicator and never reach `worldwide-events.pine`.

Before committing changes to `data/`, run the validator:

```bash
python scripts/check-events.py --no-http
```

It checks that all language files share the same dates, that rows are sorted and unique, and that descriptions are Pine-safe. Drop `--no-http` to also verify that every link returns HTTP 200 (slow - it fetches each URL).

The generator and validator have their own regression tests:

```bash
python scripts/test_generate.py
```

Both run in CI on every pull request touching `data/`, `scripts/` or the Pine file.

## CI

`.github/workflows/generate-events.yml` runs `scripts/test_generate.py`, `scripts/check-events.py --no-http` and `scripts/generate-events.py`:

- on pull requests touching `data/events-*.md`, `worldwide-events.pine` or `scripts/**` it fails when the committed `worldwide-events.pine` does not match the data;
- on push to `main` with changed `data/events-*.md` it regenerates `worldwide-events.pine` and commits it as `github-actions[bot]`.

## Links

- Every link must lead to a page with real content about that specific event (no placeholder, no "article not found", no redirect to a generic page).
- `data/events-en.md` links may point to English articles.
- `data/events-pl.md` links may point **only** to Polish-language articles.

## Publishing on TradingView

- `docs/DESCRIPTION.md` - the indicator description (BBCode) pasted into the TradingView **Description** field.
- `releases/` - one release note per version, pasted into the TradingView release notes field; the versioning rules are in [releases/README.md](releases/README.md).

## Project structure

| Path                                      | What it holds                                     |
| ----------------------------------------- | ------------------------------------------------- |
| `data/events-en.md`, `data/events-pl.md`  | event tables, one file per language               |
| `worldwide-events.pine`                   | generated indicator (do not edit by hand)         |
| `scripts/generate-events.py`              | generator: event tables to Pine Script            |
| `scripts/check-events.py`                 | validator of the event data                       |
| `scripts/test_generate.py`                | regression tests of the generator and validator   |
| `docs/DESCRIPTION.md`                     | TradingView description                           |
| `releases/`                               | release notes                                     |
| `.claude/skills/update-worldwide-events/` | agent skill for researching and adding new events |

## Conventions

- Commit messages are plain imperative sentences in English (`Add 11 events from ...`, `Regenerate worldwide-events.pine`, `Release v1.0.3`).
- Temporary files go to `tmp/` (ignored by git).
