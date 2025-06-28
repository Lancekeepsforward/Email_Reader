from googleapiclient.discovery import build
from credential import main as get_creds
from dotenv import load_dotenv
import json
import os
from pathlib import Path

load_dotenv(dotenv_path="./.env")
CONFIG_DIR = Path(os.getenv("CONFIG_DIR"))
EMAILS_ID_THREADING = CONFIG_DIR / "emails_id_threading.json"


def get_items() -> list:
    service = build("gmail", "v1", credentials=get_creds())
    results = (
        service.users()
        .messages()
        .list(
            userId="me",
            maxResults=int(input("Enter the number of emails to fetch: "))
            or 10,  # max results can be set to 500
            q=input("Enter the query for fetching emails: ")
            or "from:*@columbia.edu",  # default query is all Columbia emails
            # format="metadata" # format can be set to "metadata" or "full"
            # includeSpamTrash=True # include spam and trash emails
        )
        .execute()
    )
    items = results.get("messages", [])
    return items


def save_emails_id_threading(items: list) -> None:
    EMAILS_ID_THREADING.write_text(json.dumps(items, ensure_ascii=False, indent=2))


def main() -> None:
    """
    Fetch emails from Gmail and save the IDs and thread IDs to a JSON file.
    """
    items = get_items()
    if items:
        save_emails_id_threading(items)
    else:
        print("No emails found")


if __name__ == "__main__":
    main()
