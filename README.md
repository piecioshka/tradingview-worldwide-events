# 🌍 Worldwide Events — TradingView Indicator

<!-- prettier-ignore-start -->

[![generate-events](https://github.com/piecioshka/tradingview-worldwide-events/actions/workflows/generate-events.yml/badge.svg)](https://github.com/piecioshka/tradingview-worldwide-events/actions/workflows/generate-events.yml)

<!-- prettier-ignore-end -->

From the Chaco War to today's headlines — overlay 90+ key historical events directly on your price chart and see how markets reacted.

**[View on TradingView →](https://www.tradingview.com/script/lX6YZhUm-Worldwide-Events/)**

![Worldwide Events indicator on a TradingView chart](screenshot.png)

## Features

- 📅 Historical events — from the Chaco War (1932) to the present day
- 📈 Plotted directly on the chart — see how the market reacted to each event
- 🎨 Color-coded categories — 🔴 High priority / 🟠 Medium priority / 🟡 Low priority
- 🔍 Date tooltip — hover over an event to see its date without cluttering the chart
- ⚙️ One-click filters — show only the categories you care about
- 🕰️ History going back to 1932 — Chaco War, WWII, Pearl Harbor, Black Monday, Lehman Brothers
- 💥 Financial crises — FTX, SVB, COVID crash, 2008 crisis
- 🌐 Geopolitics — wars, attacks, sanctions, oil embargoes
- 🏦 Monetary policy — every pivotal Fed and ECB decision on the timeline
- 🔄 Continuously updated — Liberation Day 2025, US-China tariffs, Iran
- ⚡ Zero configuration — works immediately after adding to the chart
- 🆓 Open source — full code available and modifiable

## Supported Languages

Event descriptions are available in the following languages:

| Code  | Language |
| ----- | -------- |
| 🇬🇧 EN | English  |
| 🇵🇱 PL | Polish   |

To add a new language, create `data/events-XX.md` (where `XX` is the language code) using the same table format as the existing files. The indicator and GitHub Actions workflow will pick it up automatically.

## Installation

1. 📈 Open [Worldwide Events on TradingView](https://www.tradingview.com/script/lX6YZhUm-Worldwide-Events/) and click **"Add to chart"**
2. ⚙️ Or find it manually: open any chart → click **"📊 Indicators"** → search for `"Worldwide Events"`
3. ⚙️ Adjust settings to your preferences
4. 🌐 Select the language in the Settings panel
5. 🗂️ Choose the event categories you want to see
6. 🗓️ Hover over an event icon to see its date
7. 📊 Analyze market reactions to key historical moments

## Development

Events are stored in `data/events-EN.md` and `data/events-PL.md`. The Pine Script file is generated automatically — do not edit it by hand.

To regenerate `worldwide-events.pine` after modifying event data:

```bash
python scripts/generate-events.py
```

To add a new language, create `data/events-XX.md` (where `XX` is the ISO language code) using the same table format as the existing files. The generator and GitHub Actions workflow will pick it up automatically.

### Event data format

Each row is `| Date | Description | Priority | Link |`:

- **Date** — `YYYY-MM-DD`, rows sorted descending. Every language file must cover exactly the same set of dates.
- **Description** — plain text, no double quotes (they would break the generated Pine string).
- **Priority** — `high`, `medium` or `low`; drives the marker color.
- **Link** — a source for the event, or `-` when none is recorded. Links are documentation for contributors only — they are **not** rendered by the indicator and never reach `worldwide-events.pine`.

Before committing changes to `data/`, run the validator:

```bash
python scripts/check-events.py --no-http
```

It checks that all language files share the same dates, that rows are sorted and unique, and that descriptions are Pine-safe. Drop `--no-http` to also verify that every link returns HTTP 200 (slow — it fetches each URL).

## Contributing

The indicator is open source — contributions, ideas, and modifications are very welcome. Together we can build a tool that helps investors better understand the market and make more informed decisions.

## Contact

Questions, suggestions, or want to share your ideas?

- 🐛 [Open an issue](https://github.com/piecioshka/tradingview-worldwide-events/issues)
