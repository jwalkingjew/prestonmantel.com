# Deployment — GitHub Pages + prestonmantel.com

## Pipeline
- Repo: `prestonmantel.com` on Preston's GitHub (public — required for free Pages).
- Push to `main` → `.github/workflows/deploy.yml` uploads the committed `site/` directory to GitHub Pages. CI never runs `build.py`; you build locally and commit the output, so what's in git is exactly what's live.
- Pages settings: Source = **GitHub Actions** (Settings → Pages). Custom domain = `prestonmantel.com`, Enforce HTTPS = on (checkbox appears once the certificate is issued, ~15 min–24 h after DNS resolves).
- `build.py` writes `site/CNAME` (containing `prestonmantel.com`) on every build so the custom domain never gets wiped by a deploy.

## DNS records (one-time, at the domain registrar)
| Type | Host | Value |
|---|---|---|
| A | `@` | `185.199.108.153` |
| A | `@` | `185.199.109.153` |
| A | `@` | `185.199.110.153` |
| A | `@` | `185.199.111.153` |
| CNAME | `www` | `<github-username>.github.io` |

Delete any pre-existing A/AAAA/ALIAS records on `@` (registrar parking pages). Optional hardening: verify the domain at GitHub → Settings → Pages → Verified domains (GitHub provides a TXT record) so nobody can hijack the domain if the Pages site is ever deleted.

## Verification commands
```bash
gh run list --limit 3                       # deploy status
dig +short prestonmantel.com A              # expect the four 185.199.x.153 IPs
dig +short www.prestonmantel.com CNAME      # expect <username>.github.io.
curl -sI https://prestonmantel.com | head -5   # expect HTTP/2 200, server: GitHub.com
```

## Rollback
The site is fully determined by git: `git revert <bad-commit> && git push`. Deploys take ~30–60 s.

## Local preview
```bash
python3 build.py && python3 -m http.server 8000 -d site
```
