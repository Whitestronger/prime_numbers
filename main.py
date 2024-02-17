from fastapi import FastAPI

import requests
from bs4 import BeautifulSoup

# python -m uvicorn main:app --reload
# http://127.0.0.1:8000/B098LG3N6R <- put any amazon product ASIN here

app = FastAPI()

@app.get("/{asin}")
async def get_data(asin: str):
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })
    resp = session.get(f"https://amazon.co.uk/dp/{asin}")
    if resp.status_code != 200:
        return {"error": f"bad status code: {resp.status_code}"}
    try:
        soup = BeautifulSoup(resp.text, "html.parser")
        data = {
            "asin": asin,
            "name": soup.select_one("h1#title").text.strip(),
            "price": soup.select_one("span.a-offscreen").text
        }
        return {"results": data}
    except KeyError:
        return {"error": "Unable to parse page"}

