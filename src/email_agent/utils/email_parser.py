from googleapiclient.discovery import build
from .credential import main as get_creds
from dotenv import load_dotenv
import json
import os
import base64
from jsonpath_ng.ext import parse
from pathlib import Path
from .email_sample import EmailSample
import re

load_dotenv(dotenv_path="./.env")
CONFIG_DIR = Path(os.getenv("CONFIG_DIR"))
EMAILS_ID_THREADING = CONFIG_DIR / "emails_id_threading.json"
EMAILS_DECODED_CONTENT = CONFIG_DIR / "email_decoded_content.json"


def get_email_id_threading() -> list:
    """
    Get the email ID and threading ID from the JSON file.
    """
    return json.loads(EMAILS_ID_THREADING.read_text(encoding="utf-8"))


def get_email_content_list(service: build, emails_id_threading: list) -> list[EmailSample]:
    """
    Get the email content from the Gmail API.
    """
    expression = parse("$.payload..body.data")
    email_samples = []
    for email in emails_id_threading:
        print(
            f"[Email {email['id']}]: ID: {email['id']}, Thread ID: {email['threadId']} FOUNDED!"
        )
        results = service.users().messages().get(userId="me", id=email["id"]).execute()
        email_sample = EmailSample(
            id=email["id"],
            thread_id=email["threadId"],
            sender=parse("$.payload.headers[?(@.name == 'From')].value")
            .find(results)[0]
            .value,
            receiver=parse("$.payload.headers[?(@.name == 'To')].value")
            .find(results)[0]
            .value,
            date=parse("$.payload.headers[?(@.name == 'Date')].value")
            .find(results)[0]
            .value,
            subject=parse("$.payload.headers[?(@.name == 'Subject')].value")
            .find(results)[0]
            .value,
        )
        content = next((item for item in expression.find(results) if item.value), None)
        if content:
            content = base64.urlsafe_b64decode(
                content.value + "=" * ((4 - len(content.value) % 4) % 4)
            ).decode("utf-8")
            email_sample.set_content(modify_content(content))
            email_samples.append(email_sample)
            # print(email_sample.get_content())
            # print("--------------------------------")
            # break
    return email_samples

def modify_content(content: str) -> str:
    """
    Modify the content of the email.
    """
    content = re.sub(r"[\n\r]+", r"\n", content.strip())
    return content

def main() -> list[EmailSample]:
    """
    Parse the emails from the JSON file and save the parsed emails to a JSON file.
    """
    service = build("gmail", "v1", credentials=get_creds())
    emails_id_threading = get_email_id_threading()
    email_samples = get_email_content_list(service, emails_id_threading)
    # for email_sample in email_samples:
    #     print(email_sample)
    #     print("--------------------------------")
    return email_samples


# def test_jsonpath_ng() -> None:
#     """
#     Test the jsonpath library.
#     """
#     json_data = json.loads(EMAILS_DECODED_CONTENT.read_text(encoding="utf-8"))
#     # print(json_data)
#     # expression = parse("$.payload.headers[?(@.name == 'From')].value")
#     # for match in expression.find(json_data):
#     #     print(match.value)
#     print(
#         parse("$.payload.headers[?(@.name == 'From')].value").find(json_data)[0].value
#     )
#     # expression = parse("$..body.data")
#     # for match in expression.find(json_data):
#     #     print(match.value)


if __name__ == "__main__":
    # test_jsonpath_ng()
    # Convert "=" to binary representation
    email_samples = main()
    print(len(email_samples))
    pass
