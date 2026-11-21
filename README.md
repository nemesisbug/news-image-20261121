# The World in One Day — 21 November 2026

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/nemesisbug/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/nemesisbug/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

Entry for [make.fun's "Sum up 21 November's world news in one image"](https://make.fun/bounty/news-image-20261121) bounty ($100 in USDC, top 50 paid).

A one-page newspaper front page that sums up the world's news of
**Saturday 21 November 2026** in a single image. Every story on the page
happened, or was first reported, on that day.

## What the image shows

- **Date-forward masthead** — "Saturday 21 November 2026" as the giant
  serif headline, front and centre.
- **Lead stories** — Russian missiles land in Poland; Wall Street enters
  correction as the AI rout deepens; Cyclone Akvan crosses the Odisha
  coast.
- **33 stories from 5 regions** — Asia-Pacific 9, Europe 8, Middle
  East 2, Americas 11, Worldwide 3.
- **The day by hours** — seven time-anchored events as reported.
- **Twelve more stories** in three columns — the overnight Kyiv
  bombardment, Trump's January peace-deal push, GTA 6's $3.79bn day,
  the JPMorgan/Visa/Mastercard vendor breach, the NSE's rise to 5th
  largest, India's Wellington fightback, YouTube's $3bn school
  settlement, Indonesia's $30bn fires, the EU's EUR 1bn Ukraine aid,
  the UK's drone pledge, the Hormuz tanker mines, and Medvedev's ATP
  Finals win.
- **Where it happened** — a world map with six numbered pins, an
  18-item "Also on this page" list, a verdict box, markets, a date-check
  box naming what was deliberately left off, and a sources line.

## How it is made

`build_image.py` draws the whole page with Pillow (deterministic — the
same bytes on every run) from the story list in the same file. `main.py`
(Python 3.13, standard library only) copies the resulting `entry.png` to
`$MAKEFUN_OUTPUT_DIR` (default `/output`). No network is used at run time.

```sh
python3 build_image.py   # writes entry.png (1024x1024)
python3 main.py          # copies entry.png to /output/entry.png
```

## How sure are we?

Every story carries a REPORTED / CLAIM / FORECAST tag: REPORTED means
confirmed by named sources, CLAIM means one side says it and it is
unverified, FORECAST means a schedule or a projection. The date-check box
lists the big headlines that are not 21 November's news and were left off
on purpose.
