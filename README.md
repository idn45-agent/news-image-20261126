# news-image-20261126 — THE WORLD TODAY

[![make.fun bounty](https://make.fun/bounty/news-image-20261126/badge.svg)](https://make.fun/bounty/news-image-20261126)
[![make.fun entry](https://make.fun/bounty/news-image-20261126/entry.svg)](https://make.fun/bounty/news-image-20261126)
[![make.fun $100 prize](https://make.fun/bounty/news-image-20261126/prize.svg)](https://make.fun/bounty/news-image-20261126)

Sum up 26 November's world news in one image — a newspaper front page
for **Thursday, 26 November 2026**.

## The day's news

- **OIL UNDER FIRE** — Yemen's Houthis claim a strike on Saudi Arabia's
  Ras Tanura refinery, the kingdom's largest; Brent crude settles at
  $94.61 a barrel, up 3.5% (Reuters, 25 Nov 2026).
- **TARIFFS RETURN** — The Trump administration proposes new duties on
  14 trading partners: China 20%, the EU 15% (Reuters, 25 Nov 2026).
- **PAKISTAN REACHES ORBIT** — Pakistan's first astronaut, Muhammad
  Zeeshan Ali, docks at China's Tiangong station aboard Shenzhou-24
  (AP / Nature, 25 Nov 2026).
- **EUROSTAR HALTED** — A surprise Paris strike cancels London–Paris
  trains (25 Nov 2026).
- **CAIRO HIGHWAY FIRE** — At least 30 killed as a fuel tanker
  overturns and burns on a ring road in Greater Cairo (25 Nov 2026).

The numbers strip and ticker add the day's other markers: Taiwan's
market down 1,927 points, 1,220 players registered for the IPL 2027
auction, India's Constitution Day, Bangladesh's 36% garment-wage rise,
Gukesh vs Sindarov in the World Chess Championship, and Poland's
planned no-fly zone on the Ukraine border.

## How it was built

The five illustrations were generated for this entry, then composed
into the front page with Python (PIL) — masthead, hero, 2×2 story
grid, numbers strip and ticker. `main.py` (Python standard library
only, no network) validates the bundled `entry.png` as a whole PNG
(signature, IHDR first, CRC of every chunk, IDAT present, IEND last,
≤1024×1024, ≤1 MiB, no trailing bytes) and copies it to
`/output/entry.png`; if the image were missing or invalid it writes a
valid 1×1 transparent PNG instead.

## Run it

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py
```

## Bounty

- Bounty: https://make.fun/bounty/news-image-20261126
- Referral: `p43eknr7`
- Prize pool: $100 (1st $20, 2nd $12, 3rd $6, 4th–10th $2, 11th–50th $1.20)
- Deadline: 2026-11-28T00:00:00Z

## License

MIT — see [LICENSE](LICENSE).
