# Nasdaq Intelligence 1.0

A free, mobile-friendly Nasdaq research dashboard on GitHub Pages.

## Features
- Dark market dashboard and QQQ historical daily-close chart
- Stock prices and locally saved watchlist
- Day trading, swing trading and long-term research modes
- Linked financial headlines
- Automated weekday refresh scheduled for 07:00 Europe/London

## Deployment
1. Open **Settings → Pages**, select **Deploy from a branch**, **main**, **/(root)** and Save.
2. Open **Actions → Morning market refresh → Run workflow** to collect the first snapshot.
3. Open https://fueltrack.github.io/Nasdaq-Intelligence/ once Pages finishes deploying.

The Python refresh script uses Yahoo Finance public chart endpoints and Google News RSS. These sources are unofficial and may fail or rate-limit. Quotes are daily closes, **not real-time**. GitHub Actions schedules can be delayed. Data may be stale if the refresh fails; check timestamps and workflow logs.

Educational market research only, not personalised investment advice. Verify data before trading.