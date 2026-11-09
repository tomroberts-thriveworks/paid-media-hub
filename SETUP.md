# Setup on a new machine
```bash
git clone <repo-url> && cd paid-media-hub
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[google,dev]"
cp .env.example .env    # then fill in values; never commit .env
pytest
```
Credentials (developer token, OAuth client secret, refresh token) are created and
stored only on the machine that runs the tool.
