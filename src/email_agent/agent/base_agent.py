from groq import Groq
import os
from pathlib import Path
import json
from dotenv import load_dotenv
from utils.email_sample import EmailSample
import copy

load_dotenv(dotenv_path="../.env")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL = os.getenv("MODEL_DEEPSEEK1")
client = Groq(api_key=GROQ_API_KEY)
RULES_AGENTS = json.loads(Path("config/rules_agents.json").read_text(encoding="utf-8"))


class BaseAgent:
    def __init__(self, model: str = MODEL, client: Groq = client):
        self.model = model
        self.client = client
        self.system: list[dict[str:"role", str:"content"]] = RULES_AGENTS
        self.history: list[dict[str:"role", str:"content"]] = copy.deepcopy(RULES_AGENTS)
        self.system_length = len(RULES_AGENTS)
        self.assistant_length = 0
        self.user_length = 0
        
    def get_response(self, email_samples: list[EmailSample]) -> str:
        messages = self.history + self._get_prompt(email_samples)
        self.history.extend(messages)
        self.user_length += len(messages)
        completion = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True,
            temperature=1,  # 控制输出的随机性/创造性 (0-2)
            top_p=1,  # 控制词汇选择的多样性 (0-1)
            stop=None,  # 定义停止生成的条件
            # max_completion_tokens=1024,  # 限制模型回复的最大 token 数
        )
        content = ""
        for chunk in completion:
            temp = chunk.choices[0].delta.content or ""
            content += temp
            print(temp, end="", flush=True)  # 只会在内容有\n时候换行
        self.history.append({"role": "assistant", "content": content})
        self.assistant_length += len(content)
        return content

    def _get_prompt(self, email_samples: list[EmailSample]) -> list[dict[str:"role", str:"content"]]:
        results = [{"role": "user", "content": repr(email_samples)}]
        return results
    
