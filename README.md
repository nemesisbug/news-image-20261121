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
- **Lead stories** — a 6.8 quake shakes Peru; Wall Street slides into
  correction at Friday's close; Russian missiles come down in Poland.
- **30 stories** — three leads plus 27 more, from BepiColombo's arrival
  at Mercury to Saturday's football across Europe.
- **The day by hours** — six time-anchored events, from the 00:09 quake
  to the Dragon splashdown at 21:55 UTC.
- **Where it happened** — a world map with eight numbered pins, a
  verdict box, markets, a date-check box naming what was deliberately
  left off, and a sources line.

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

Every story on the page happened, or was first reported, on Saturday
21 November 2026 — except Friday's market close, which is labelled as
Friday's. The date-check box lists the big headlines that are not
21 November's news and were left off on purpose.
