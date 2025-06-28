import os
import glob
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')

_SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']
_CONFIG_DIR = Path(os.getenv("CONFIG_DIR"))
_TOKEN_FILE = _CONFIG_DIR / "token.json"
_CREDENTIAL_FILE = os.getenv("CREDENTIAL")

def _get_token_file() -> Credentials:
    if _TOKEN_FILE.exists():
        print(f"[ACCESSING '{_TOKEN_FILE}', EXISTS: '{_TOKEN_FILE.exists()}']")
        try:
            creds = Credentials.from_authorized_user_file(_TOKEN_FILE, _SCOPES)
            print(f"Token file is {creds.valid}.")
            return creds
        except Exception as e:
            return _authenticate()


def _refresh_token(creds: Credentials) -> Credentials:
    creds.refresh(Request())
    with open(_TOKEN_FILE, 'w') as token:
        token.write(creds.to_json())
    return creds

def _authenticate() -> Credentials:
    # 查找 client_secret 文件
    client_secret_file = glob.glob(str(_CONFIG_DIR / _CREDENTIAL_FILE))
    if not client_secret_file:
        print("Error: Can't find client_secret file!")
        print("You need to download the client_secret file from Google Cloud Console.")
        raise FileNotFoundError("Client secret file not found")
    
    flow = InstalledAppFlow.from_client_secrets_file(
        client_secret_file[0], _SCOPES)
    creds = flow.run_local_server(port=0)
    with open(_TOKEN_FILE, 'w') as token:
        token.write(creds.to_json())
    return creds


def main() -> Credentials:
    """
    Get the credentials for the Gmail API.
    """
    creds = _get_token_file()
    if not creds:
        creds = _authenticate()
    if creds.expired:
        creds = _refresh_token(creds)
        print("Token refreshed successfully!")
    return creds

if __name__ == "__main__":
    print(main().to_json())
