from .agent.base_agent import BaseAgent
from .utils import get_email_samples, fetch_save_emails

def main():
    fetch_save_emails()
    email_samples = get_email_samples()
    agent = BaseAgent()
    agent.chat_loop(email_samples)
    print("Quit.")

if __name__ == "__main__":
    main()