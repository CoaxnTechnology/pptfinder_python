import requests
import time
from typing import List, Dict


class GoogleSearchClient:
    """
    A reusable Google Custom Search API client
    for fetching PPT/PPTX results.
    """

    def __init__(self, api_key: str, search_engine_id: str):
        self.api_key = api_key
        self.search_engine_id = search_engine_id
        self.base_url = "https://www.googleapis.com/customsearch/v1"

    def search_ppt_files(self, keyword: str, limit: int = 100) -> List[Dict]:
        """
        Fetch PowerPoint (PPT/PPTX) results from Google search.

        Steps:
        - Fetch pages of 10 results each.
        - Filter PPT/PPTX links.
        - Deduplicate with dict.
        """

        results = []
        start_index = 1  # Google returns 10 per request

        while len(results) < limit:

            url = (
                f"{self.base_url}"
                f"?key={self.api_key}"
                f"&cx={self.search_engine_id}"
                f"&q={keyword}+filetype:ppt+OR+filetype:pptx"
                f"&start={start_index}"
            )

            response = requests.get(url)

            # ---- API Error ----
            if response.status_code != 200:
                print("Google API Error:", response.text)
                break

            data = response.json()
            items = data.get("items", [])

            if not items:
                break  # no results

            # ---- Process each Google result ----
            for item in items:
                link = item.get("link", "")

                # Collect only PPT/PPTX files
                if link.lower().endswith(".ppt") or link.lower().endswith(".pptx"):
                    results.append({
                        "title": item.get("title"),
                        "link": link,
                        "display_link": item.get("displayLink"),
                        "snippet": item.get("snippet", "")
                    })

                if len(results) >= limit:
                    break

            # Move to next page (10 results per page)
            start_index += 10

            # Prevent too fast API usage
            time.sleep(0.3)

        # ---- Deduplicate by link ----
        unique_results = list({entry["link"]: entry for entry in results}.values())

        return unique_results
