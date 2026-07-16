# prestonmantel.com

Personal academic website of Preston Mantel, PhD candidate in Finance at the University of Cincinnati.

- Live site: https://prestonmantel.com
- Built from YAML data files in `data/` by `build.py` (Python, PyYAML only) into `site/`
- Deployed to GitHub Pages on every push to `main`

To update: edit `data/*.yaml`, run `python3 build.py`, preview with `python3 -m http.server 8000 -d site`, commit and push.

Agent/contributor context lives in [CLAUDE.md](CLAUDE.md) and [docs/](docs/).
