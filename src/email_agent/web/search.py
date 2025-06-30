import httpx, pandas as pd
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env")


def google_search_web(
    query: str, api_key: str, search_engine_id: str, **params
) -> pd.DataFrame:
    url = "https://www.googleapis.com/customsearch/v1"
    params = {"key": api_key, "q": query, "cx": search_engine_id, **params}
    response = httpx.get(url, params=params)
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    api_key = os.getenv("GOOGLE_API_KEY")
    search_engine_id = os.getenv("SEARCH_ENGINE_ID")
    WEB_DIR = os.getenv("WEB_DIR")
    query = "What is the capital of France?"
    print(f"[api_key]: {api_key}")
    print(f"[search_engine_id]: {search_engine_id}")
    print(f"[query]: {query}")
    search_results = []
    for i in range(1, 4):
        response = google_search_web(
            query, 
            api_key, 
            search_engine_id, 
            start=i*10
        )
        print(f"[idx: {i}] response: ", response)
        search_results.extend(response.get("items", []))
    df = pd.json_normalize(search_results)
    df.to_csv(WEB_DIR + "/search_results.csv", index=False)

    
