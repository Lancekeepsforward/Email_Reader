from groq import Groq, APIStatusError
import os
from pathlib import Path
import json
import sys
from dotenv import load_dotenv
from ..utils.email_sample import EmailSample
import copy

load_dotenv(dotenv_path=".env")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("MODEL_DEEPSEEK1")
client = Groq(api_key=GROQ_API_KEY)
CONFIG_DIR = os.getenv("CONFIG_DIR")
RULES_AGENTS = json.loads(Path(CONFIG_DIR, "rules_agents.json").read_text(encoding="utf-8"))


class BaseAgent:
    def __init__(self, model: str = MODEL, client: Groq = client):
        self.model = model
        self.client = client
        self.system: list[dict[str:"role", str:"content"]] = RULES_AGENTS
        self.history: list[dict[str:"role", str:"content"]] = copy.deepcopy(RULES_AGENTS)
        self.system_length = len(RULES_AGENTS)
        self.assistant_length = 0
        self.user_length = 0
    
    @staticmethod
    def evaluate_token_length(email_samples: list[EmailSample]) -> int:
        total_tokens = 0
        for email_sample in email_samples:
            total_tokens += email_sample.word_count
        return total_tokens

    def get_response(self, email_samples: list[EmailSample]) -> str:
        print("getting response")
        messages = self.history + self._get_prompt(email_samples)
        self.history.extend(messages)
        self.user_length += len(messages)
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True,
                temperature=1,  # 控制输出的随机性/创造性 (0-2)
                top_p=1,  # 控制词汇选择的多样性 (0-1)
                stop=None,  # 定义停止生成的条件
                # max_completion_tokens=1024,  # 限制模型回复的最大 token 数
            )
        except APIStatusError as e:
            problem = eval(e.response.text)
            print(problem.get("error", {}).get("message", "Unknown error"))
            raise Exception(problem.get("error", {}).get("message", "Unknown error"))
        except Exception as e:
            print(e)
            raise Exception(e)
        content = ""
        for chunk in completion:
            temp = chunk.choices[0].delta.content or ""
            content += temp
        print(content, end="", flush=True)  # 只会在内容有\n时候换行
        self.history.append({"role": "assistant", "content": content})
        self.assistant_length += len(content)
        return content

    def _get_prompt(self, email_samples: list[EmailSample]) -> list[dict[str:"role", str:"content"]]:
        results = [{"role": "user", "content": repr(email_samples)}]
        return results
    
    def get_response_with_query(self, query: str) -> str:
        messages = self.history + [{"role": "user", "content": query}]
        self.history.extend(messages)
        self.user_length += len(messages)
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                stream=True,
                temperature=1,
                top_p=1,
                stop=None,
            )
        except APIStatusError as e:
            problem = eval(e.response.text)
            print(problem.get("error", {}).get("message", "Unknown error"))
            raise Exception(problem.get("error", {}).get("message", "Unknown error"))
        except Exception as e:
            print(e)
            raise Exception(e)
        content = ""
        for chunk in completion:
            temp = chunk.choices[0].delta.content or ""
            content += temp
            print(temp, end="", flush=True)  # 只会在内容有\n时候换行
        self.history.append({"role": "assistant", "content": content})
        self.assistant_length += len(content)
        return content
    
    def __str__(self):
        return f"BaseAgent(model={self.model}, client={self.client.__class__}, system_length={self.system_length}, assistant_length={self.assistant_length}, user_length={self.user_length})"
    
    def __repr__(self):
        return self.__str__()
    
def test_base_agent():
    for key, value in APIStatusError.__dict__.items():
        print(key, value)
    
if __name__ == "__main__":
    test_base_agent()

    
