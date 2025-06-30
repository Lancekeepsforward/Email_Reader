from .agent.base_agent import BaseAgent
from .utils import get_email_samples, fetch_save_emails

def main():
    email_samples = get_email_samples()
    # agent = BaseAgent()
    fetch_save_emails()
    print(BaseAgent.evaluate_token_length(email_samples))
    # try:
    #     response = agent.get_response(email_samples)
    #     print(response)
    # except Exception as e:
    #     print(e)

if __name__ == "__main__":
    main()