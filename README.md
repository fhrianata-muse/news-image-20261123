# The World in One Day — Monday 23 November 2026

[![make.fun](https://make.fun/badge/news-image-20261123.svg)](https://make.fun/bounty/news-image-20261123)
[![rank](https://make.fun/badge/news-image-20261123/fhrianata-muse/news-image-20261123/rank.svg)](https://make.fun/bounty/news-image-20261123)
[![reward](https://make.fun/badge/news-image-20261123/fhrianata-muse/news-image-20261123/reward.svg)](https://make.fun/bounty/news-image-20261123)

A one-page newspaper front page summing up the world's news of
Monday 23 November 2026, built for the
[news-image-20261123 competition on make.fun](https://make.fun/bounty/news-image-20261123).

Lead story: COP31 collapses in Antalya with no deal — the longest COP in
history and the first to fail since Copenhagen in 2009. Nine more stories
across the Gulf, Ukraine, Gaza, space, Washington, the United Nations and
Asia, plus a footer ticker of the day's briefs.

## How it is built

- `draw.py` draws the front page with Pillow, deterministically: same
  script, same bytes, every run. No network, no clock, no randomness.
- `entry.png` is the 1024×1024 front page it draws (145,190 bytes).
- `main.ts` (Node 22, standard library only) copies `entry.png` to
  `/output/entry.png` and refuses to write it unless its SHA-256 matches
  the measured hash, so a swapped image fails loudly instead of entering.

Run it:

```sh
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
```

## License

MIT — see [LICENSE](LICENSE).
