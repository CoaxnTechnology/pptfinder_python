import requests
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")


def fetch_ppt_results(keyword: str, num_results: int = 50):
    results = []
    start_index = 1

    while len(results) < num_results:
        url = (
            "https://www.googleapis.com/customsearch/v1"
            f"?key={GOOGLE_API_KEY}"
            f"&cx={SEARCH_ENGINE_ID}"
            f"&q={keyword}+filetype:ppt+OR+filetype:pptx"
            f"&start={start_index}"
        )

        response = requests.get(url)
        data = response.json()

        if "items" not in data:
            break

        for item in data["items"]:
            results.append({
                "title": item.get("title"),
                "link": item.get("link")
            })

            if len(results) >= num_results:
                break

        start_index += 10

        if "queries" not in data or "nextPage" not in data["queries"]:
            break

    return results
