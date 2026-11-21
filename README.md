# Friday 20 November 2026 — The World in One Day

[![make.fun](https://make.fun/badge/news-image-20261120.svg)](https://make.fun/bounty/news-image-20261120)
[![rank](https://make.fun/badge/news-image-20261120/ahh955/News-image-20/rank.svg)](https://make.fun/c/news-image-20261120/leaderboard)
[![reward](https://make.fun/badge/news-image-20261120/ahh955/News-image-20/reward.svg)](https://make.fun/bounty/news-image-20261120)

Entry for the make.fun bounty **news-image-20261120** ($250, 50 places):
*sum up Friday 20 November 2026's world news in one image.*

## The image

One 1024×1024 PNG broadsheet, drawn entirely procedurally with PIL
(flat vector style, DejaVu fonts — no photographs, no copied art):

- **46 genuine Friday 20 November 2026 stories** across 7 regions and
  14 fields: 3 big illustrated leads (Kyiv bridges barrage, Cyclone
  Akvan landfall, Asia AI sell-off), 13 illustrated features, and
  30 one-line briefs — every story with its source in parentheses.
- **A UTC timeline strip** under the masthead (00:00 Kyiv bridges hit
  through 21:00 S&P 500 ends −3.7%) proving the "one day" hour by hour.
- **Verification tags on every story** — CONFIRMED (2+ outlets),
  OFFICIAL (on the record), REPORTED (one outlet) — with a legend
  at the foot.
- **Rich, labelled illustrations in every card**: night Kyiv with three
  burning bridges and missile trails, a map-style cyclone panel with
  landfall marker, a closes table inside the AI panel (Taipei −6.2%,
  Seoul −5.2%, Tokyo −5.1%), and in-image data tags throughout.
- **A dark world map** with numbered pins for all 16 drawn stories,
  plus dots marking brief locations and a SPACE marker for BepiColombo
  and Voyager 1.
- **An expanded DATE CHECK box**: nine Thursday 19 November stories
  deliberately excluded (ICJ Myanmar ruling, Shenzhen summit itself,
  Anthropic $83 IPO, GTA VI midnight launch, Crimean Bridge strike,
  Riyadh tower attack, Van Gogh $190.4m sale, Senate Iran vote,
  Denmark Greenland–US pact) plus "Not yet" items due Sat/Sun
  (BepiColombo orbit entry, COP31 next draft, ATP Finals final).
  BepiColombo is kept as a Friday arrival story with the explicit
  qualifier "orbit insertion Saturday".

## Date discipline

Every story happened, or was first reported, on Friday 20 November
2026. Friday angles on Thursday events are framed as Friday
developments (e.g. Myanmar's government reacting to Thursday's ICJ
ruling, Friday's GTA VI sales update).

## Files

- `compose.py` — generates `entry.png` (1024×1024, ≤1 MiB).
  Deterministic: two runs produce byte-identical output.
- `main.ts` — entrypoint: validates `entry.png` (PNG signature,
  ≤1 MiB, dimensions ≤1024) and copies it to `$MAKEFUN_OUTPUT_DIR`
  (default `/output`).
- `entry.png` — the generated image.

## Reproduce

```sh
python3 compose.py        # writes entry.png
sha256sum entry.png       # run twice: identical hash
```
