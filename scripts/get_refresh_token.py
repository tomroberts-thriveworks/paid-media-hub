"""One-time OAuth sign-in that stores GOOGLE_ADS_REFRESH_TOKEN in your local .env.

Run on the machine that will use the tool (not a personal/shared one):
    pip install -e ".[google]"
    python scripts/get_refresh_token.py
Needs GOOGLE_ADS_CLIENT_ID and GOOGLE_ADS_CLIENT_SECRET already in .env.
The token is written to .env and never printed.
"""
import os
import re
import sys
from pathlib import Path

from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/adwords"]
ENV = Path(".env")


def write_env(key: str, value: str) -> None:
    text = ENV.read_text() if ENV.exists() else ""
    line = f"{key}={value}"
    if re.search(rf"^{key}=.*$", text, flags=re.M):
        text = re.sub(rf"^{key}=.*$", line, text, flags=re.M)
    else:
        text = text.rstrip("\n") + ("\n" if text else "") + line + "\n"
    ENV.write_text(text)


def main() -> int:
    load_dotenv()
    cid, secret = os.getenv("GOOGLE_ADS_CLIENT_ID"), os.getenv("GOOGLE_ADS_CLIENT_SECRET")
    if not cid or not secret:
        print("Set GOOGLE_ADS_CLIENT_ID and GOOGLE_ADS_CLIENT_SECRET in .env first.")
        return 1
    config = {"installed": {
        "client_id": cid, "client_secret": secret,
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "redirect_uris": ["http://localhost"],
    }}
    flow = InstalledAppFlow.from_client_config(config, SCOPES)
    creds = flow.run_local_server(port=0, access_type="offline", prompt="consent")
    if not creds.refresh_token:
        print("Google returned no refresh token. Revoke the app at "
              "myaccount.google.com/permissions and run again.")
        return 1
    write_env("GOOGLE_ADS_REFRESH_TOKEN", creds.refresh_token)
    print("Saved GOOGLE_ADS_REFRESH_TOKEN to .env (not displayed).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
