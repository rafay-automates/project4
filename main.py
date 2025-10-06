from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
from bs4 import BeautifulSoup

app = FastAPI()

# Allow frontend to call backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/search")
def search(
    query: str = Query(..., description="Keyword to search"),
    location: str = Query("", description="Location code (optional)")
):
    url = "https://social.agencydashboard.io/fetch-keywords-records"
    params = {
        "search_query": query,
        "locations": location,
        "language": "",
        "category": "1"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        soup = BeautifulSoup(data["data"], "html.parser")
        checkboxes = soup.find_all("input", {"name": "select_keywords[]"})

        results = []
        for checkbox in checkboxes:
            results.append({
                "Keyword": checkbox.get("data-id"),
                "CI": checkbox.get("data-ci"),
                "Search Volume": checkbox.get("data-searchvolume"),
                "Bid Low": checkbox.get("data-bidlow"),
                "Bid High": checkbox.get("data-bidhigh"),
            })

        return {"results": results}
    except Exception as e:
        return {"error": str(e), "results": []}
