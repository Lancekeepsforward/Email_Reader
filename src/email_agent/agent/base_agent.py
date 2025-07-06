# LangChain RAG & Agent Architecture Implementation
import os
import json
import warnings
from typing import List
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.memory.summary_buffer import ConversationSummaryBufferMemory 
from ..utils.email_sample import EmailSample
from langchain.schema import Document
from langchain_community.vectorstores import FAISS
from langchain_groq import ChatGroq
from langchain.chains import ConversationChain
# Suppress warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", message=".*tokenizers.*")
os.environ["TOKENIZERS_PARALLELISM"] = "false"

# Load configuration
load_dotenv(dotenv_path=".env")
CONFIG_DIR = os.getenv("CONFIG_DIR")
RULES_AGENTS = json.loads(Path(CONFIG_DIR, "rules_agents.json").read_text(encoding="utf-8"))

class BaseAgent:
    """RAG + Agent architecture based on LangChain"""
    def __init__(self, model_name: str = None):
        # Validate required environment variables
        groq_api_key = os.getenv("GROQ_API_KEY")
        if not groq_api_key:
            raise ValueError("GROQ_API_KEY environment variable is required")
        
        embedding_model_name = os.getenv("EMBEDDING_MODEL_NAME")
        if not embedding_model_name:
            # Use a default embedding model if not specified
            embedding_model_name = "all-MiniLM-L6-v2"
            print(f"Warning: EMBEDDING_MODEL_NAME not set, using default: {embedding_model_name}")
        
        self.__client = Groq(api_key=groq_api_key)
        self.model_name = os.getenv("LLAMA3_8B") or os.getenv("MODEL_DEEPSEEK1")
        if not self.model_name:
            raise ValueError("Either LLAMA3_8B or MODEL_DEEPSEEK1 environment variable is required")
        
        self.model = ChatGroq(model=self.model_name, api_key=groq_api_key, temperature=0.8)
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model_name, model_kwargs={"device": "cpu"})
        self.memory = ConversationSummaryBufferMemory(llm=self.model, max_token_limit=2000)
        self.conversation_chain = ConversationChain(llm=self.model, memory=self.memory, verbose=True)
        self.rag_retriever = self._init_rag_retriever()
        self.saved_emails = {"id": []}
        self.new_emails = []

    def _init_rag_retriever(self) -> FAISS:
        """Initialize RAG retriever. Only load if exists; do not create with dummy text."""
        vectorstore_path = os.path.join(CONFIG_DIR, "ljs_columbia_email_vectorstore.faiss")
        if os.path.exists(vectorstore_path):
            # Note: allow_dangerous_deserialization=True is used because we trust our own vectorstore files
            # This is safe since we created these files ourselves and they haven't been modified by untrusted sources
            return FAISS.load_local(vectorstore_path, self.embeddings, allow_dangerous_deserialization=True)
        else:
            # No index exists yet; will be created when new emails are added
            return None

    def _filter_email_samples(self, email_samples: List[EmailSample]) -> List[EmailSample]:
        """Filter new emails from email samples"""
        necessary_emails = []
        if os.path.exists(os.path.join(CONFIG_DIR, "ljs_columbia_email_saved.json")):
            self.saved_emails = json.loads(Path(CONFIG_DIR, "ljs_columbia_email_saved.json").read_text(encoding="utf-8"))
            for email in email_samples:
                if email.id not in self.saved_emails["id"]:
                    necessary_emails.append(email)
                    self.saved_emails["id"].append(email.id)
            with open(os.path.join(CONFIG_DIR, "ljs_columbia_email_saved.json"), "w", encoding="utf-8") as f:
                json.dump(self.saved_emails, f, ensure_ascii=False)
        else:
            necessary_emails = email_samples
            with open(os.path.join(CONFIG_DIR, "ljs_columbia_email_saved.json"), "w", encoding="utf-8") as f:
                json.dump(self.saved_emails, f, ensure_ascii=False)
        self.new_emails = necessary_emails
        return necessary_emails

    def _update_retriever(self, email_samples: List[EmailSample]) -> None:
        """Update RAG retriever. Create FAISS index if it does not exist."""
        necessary_emails = self._filter_email_samples(email_samples)
        content = [str(email) for email in necessary_emails]
        # for email in content:
        #     print(email)
        vectorstore_path = os.path.join(CONFIG_DIR, "ljs_columbia_email_vectorstore.faiss")
        if self.rag_retriever is None:
            if content:
                # Create new FAISS index with actual email content
                self.rag_retriever = FAISS.from_texts(content, self.embeddings)
                self.rag_retriever.save_local(vectorstore_path)
            else:
                # No data to create index
                print("No email content to create FAISS index.")
        else:
            if content:
                self.rag_retriever.add_texts(content)
                self.rag_retriever.save_local(vectorstore_path)

    def _get_top_k_emails(self, user_input: str, k: int = 5) -> str:
        """Get top k emails from RAG retriever"""
        emails = self.rag_retriever.similarity_search(user_input, k=k)
        email_content = "\n\n".join([email.page_content for email in emails])
        return email_content
    
    def _get_prompt(self, user_input: str, email_content: str) -> str:
        """Get prompt for RAG retrieval"""
        system_prompt = "\n\n".join([msg["content"] for msg in RULES_AGENTS if msg["role"] == "system"])
        prompt = f"""
        You are a helpful email assistant.
        system_prompt: {system_prompt}

        user_input: {user_input}

        Reference the following email materials:
        {email_content}
        """
        return prompt

    def _get_response(self, user_input: str) -> dict:
        """Process user input, combine RAG retrieval and historical messages to generate response"""
        emails = self._get_top_k_emails(user_input, int(input("How many emails to retrieve? (default: 5) :")))
        prompt = self._get_prompt(user_input, emails)
        response = self.conversation_chain.invoke(prompt)
        return response

    def chat_loop(self, email_samples: List[EmailSample]) -> None:
        """Interactive chat loop"""
        self._update_retriever(email_samples)
        print("Type 'exit' to quit.")
        while True:
            user_input = input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                print("Bye!")
                break
            response = self._get_response(user_input)
            print(f"Agent: {response['response']}")
    

def time_test(fun):
    import traceback
    import time
    def wrapper(*args, **kwargs):
        start_time = time.time()
        try:
            result = fun(*args, **kwargs)
        except Exception as e:
            print(f"[TEST] Error: {e}")
            traceback.print_exc()
            end_time = time.time()
            print(f"[TEST] Time taken: {round(end_time - start_time, 2)} seconds")
            return None
        return result
    return wrapper

@time_test
def test_base_agent() -> None:
    """Test BaseAgent functionality"""
    emails_dict = [
        {
            "id": "1",
            "thread_id": "1",
            "subject": "Test Email 1",
            "sender": "test_sender@example.com",
            "receiver": "test_receiver@example.com",
            "date": "2021-01-01 10:00:00AM",
            "content": "This is a email about I need to have a meeting with Kanva. I need to discuss the project progress with him."
        },
        {
            "id": "2",
            "thread_id": "2",
            "subject": "Test Email 2",
            "sender": "test_sender@example.com",
            "receiver": "test_receiver@example.com",
            "date": "2021-01-02 09:32:12PM",
            "content": "This is a email about my girlfriend. I need to pick her up from the airport at 10:00 AM tomorrow then we will go to the restaurant for lunch. she prefer chinese food."
        }
    ]
    emails = [EmailSample(**email_dict) for email_dict in emails_dict]
    agent = BaseAgent()
    agent.chat_loop(emails)
        

if __name__ == "__main__":
    test_base_agent() 
