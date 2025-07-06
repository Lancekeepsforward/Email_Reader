from googleapiclient.discovery import build
from .credential import main as get_creds
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


def fetch_emails(service, max_results=10, query="from:*@columbia.edu"):
    """
    Fetch emails with pagination to ensure we get exactly max_results emails that match the query.
    """
    all_messages = []
    page_token = None
    
    while len(all_messages) < max_results:
        # Calculate how many more we need
        remaining = max_results - len(all_messages)
        # Fetch a larger batch to account for filtering
        batch_size = min(remaining * 3, 500)  # Gmail API max is 500
        
        request = service.users().messages().list(
            userId="me",
            maxResults=batch_size,
            q=query,
            pageToken=page_token
        )
        
        response = request.execute()
        messages = response.get('messages', [])
        
        if not messages:
            break  # No more emails to fetch
            
        all_messages.extend(messages)
        page_token = response.get('nextPageToken')
        
        if not page_token:
            break  # No more pages
    
    # Return exactly max_results emails (or all available if less)
    return all_messages[:max_results]


def main() -> None:
    """
    Fetch emails from Gmail and save the IDs and thread IDs to a JSON file.
    """
    service = build("gmail", "v1", credentials=get_creds())
    
    max_results = int(input("Enter the number of emails to fetch: ")) or 10
    query = input("Enter the query for fetching emails: ") or "from:*@columbia.edu -subject:Spam"
    
    print(f"Fetching {max_results} emails matching query: '{query}'")
    
    results = fetch_emails(service, max_results, query)
    
    print(f"Found {len(results)} emails matching your criteria")
    
    if results:
        save_emails_id_threading(results)
    else:
        print("No emails found")


if __name__ == "__main__":
    main()
