# eclAIr books

eclAIr's copy of Bigcapital (AGPL-3.0), the ledger behind eclAIr books at books.mirepoixpartners.com. `main` is Bigcapital as
released (v0.25.45 today); `eclair` is that plus eclAIr's look and words. The source of this changed version is public, as the
AGPL asks.

What `eclair` changes, all in packages/webapp:
- `src/style/eclair/_tokens.scss`, written by `eclair/map_tokens.py`: every Bigcapital colour variable mapped to eclAIr's tokens by
  role, day and night (greys to the nearest eclAIr tone, reds to the deeper orange, greens to sage, blues to ink, the sidebar to paper).
- `src/style/eclair/_eclair.scss`: eclAIr's type (ET Book for what's read, Source Sans 3 for small labels), square quiet shapes,
  the button that acts in ink, links in ink, and no red. Loaded last in App.scss.
- Blues written straight into style files and two components, swept to ink by `eclair/sweep_blues.py`.
- `src/lang/en/index.json`, reworded by `eclair/word_pass.py`: plain names for the main screens, sentence case, no exclamation
  marks, short confirmations.
- `src/style/_variables.scss`: Bigcapital's blues as ink, Source Sans 3 as the UI font.

A push to `eclair` builds the web app image `ghcr.io/eclair-co/bigcapital-webapp:eclair` (.github/workflows/eclair-image.yml);
eclAIr books' front (eclAIr-co/eclAIr-claude-build, infra/books/front) runs it.

Taking a new Bigcapital version: put its tree on `main` as a new commit, rebase `eclair` onto it, then run the three scripts again
(`python3 eclair/map_tokens.py packages/webapp`, then `sweep_blues.py`, then `word_pass.py`) and check the screens.
