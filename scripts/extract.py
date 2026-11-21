import os
from pathlib import Path
import requests
import pandas as pd
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)
RAW_FILE = RAW_DIR / "open_library_raw.csv"


load_dotenv(BASE_DIR / ".env")


SEARCH_QUERY = os.getenv("SEARCH_QUERY", "data analytics")
RECORD_LIMIT = int(os.getenv("RECORD_LIMIT", "500"))


API_URL = "https://openlibrary.org/search.json"


params = {
    "q": SEARCH_QUERY,
    "limit": RECORD_LIMIT,
    "fields": (
        "key,title,author_name,first_publish_year,"
        "subject,isbn,language,publisher,edition_count,"
        "cover_i,publish_date"
    )
}

headers = {
    "User-Agent": "BookAnalyticsProject/1.0 (your-email@example.com)"
}

print("Connecting to Open Library API...")

response = requests.get(
    API_URL,
    params=params,
    headers=headers,
    timeout=30
)

response.raise_for_status()

data = response.json()

books = data.get("docs", [])

print("Total available:", data.get("numFound"))
print("Records extracted:", len(books))



df = pd.DataFrame(books)

selected_columns = [
    "key",
    "title",
    "author_name",
    "first_publish_year",
    "subject",
    "isbn",
    "language",
    "publisher",
    "edition_count",
    "cover_i",
    "publish_date"
]

df = df.reindex(columns=selected_columns)

df.to_csv(RAW_FILE, index=False, encoding="utf-8")

print("Raw data saved successfully!")
print("Dataset shape:", df.shape)
print(df.head())

