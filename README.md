# 🌍 Worldwide Events — TradingView Indicator

An indicator that overlays key historical events directly on the price chart — from 1940 to the present day.

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
- 🔗 Source links — each event links to its Wikipedia article
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

## Contributing

The indicator is open source — contributions, ideas, and modifications are very welcome. Together we can build a tool that helps investors better understand the market and make more informed decisions.

## Contact

Questions, suggestions, or want to share your ideas?

- 🐛 [Open an issue](https://github.com/piecioshka/tradingview-worldwide-events/issues)
