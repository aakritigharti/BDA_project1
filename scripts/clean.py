import pandas as pd
import numpy as np
import ast
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

RAW_FILE = BASE_DIR / "data" / "raw" / "open_library_raw.csv"

CLEANED_DIR = BASE_DIR / "data" / "cleaned"
CLEANED_DIR.mkdir(parents=True, exist_ok=True)

CLEANED_FILE = CLEANED_DIR / "open_library_cleaned.csv"

df = pd.read_csv(RAW_FILE)

print("Available columns:")
print(df.columns.tolist())

print("Raw dataset loaded successfully!")
print("Original shape:", df.shape)

clean_df = df.copy()

clean_df = clean_df.drop_duplicates(
    subset=["key"],
    keep="first"
)

print("Duplicate records removed:", len(df) - len(clean_df))

clean_df = clean_df.dropna(subset=["title"])

def convert_list_to_text(value):

    if isinstance(value, list):
        return "; ".join(str(item) for item in value)

    if pd.isna(value):
        return None

    if isinstance(value, str):

        value = value.strip()

        if value.startswith("[") and value.endswith("]"):

            try:
                parsed = ast.literal_eval(value)

                if isinstance(parsed, list):
                    return "; ".join(str(item) for item in parsed)

            except (ValueError, SyntaxError):
                pass

        return value

    return str(value)

list_columns = [
    "author_name",
    "subject",
    "isbn",
    "language",
    "publisher",
    "publish_date"
]

for column in list_columns:
    clean_df[column] = clean_df[column].apply(
        convert_list_to_text
    )


clean_df = clean_df.rename(columns={
    "key": "book_key",
    "author_name": "authors",
    "first_publish_year": "first_publication_year",
    "subject": "subjects",
    "language": "languages",
    "publisher": "publishers",
    "edition_count": "total_editions",
    "cover_i": "cover_id",
    "publish_date": "publication_dates"
})

text_columns = [
    "book_key",
    "title",
    "authors",
    "subjects",
    "isbn",
    "languages",
    "publishers",
    "publication_dates"
]

for column in text_columns:

    clean_df[column] = (
        clean_df[column]
        .astype("string")
        .str.strip()
        .str.replace("  ", " ", regex=False)
    )

clean_df = clean_df.rename(columns={
    "key": "book_key",
    "author_name": "authors",
    "first_publish_year": "first_publication_year",
    "subject": "subjects",
    "language": "languages",
    "publisher": "publishers",
    "edition_count": "total_editions",
    "cover_i": "cover_id",
    "publish_date": "publication_dates"
})

clean_df["title"] = clean_df["title"].str.strip().str.title()

clean_df["authors"] = clean_df["authors"].str.strip()

clean_df["subjects"] = clean_df["subjects"].str.lower()

clean_df["languages"] = clean_df["languages"].str.lower()

clean_df["publishers"] = clean_df["publishers"].str.strip()

clean_df["isbn"] = clean_df["isbn"].str.strip()



clean_df["authors"] = clean_df["authors"].fillna("Unknown")

clean_df["subjects"] = clean_df["subjects"].fillna("Unknown")

clean_df["languages"] = clean_df["languages"].fillna("Unknown")

clean_df["publishers"] = clean_df["publishers"].fillna("Unknown")

clean_df["isbn"] = clean_df["isbn"].fillna("Not Available")

clean_df["publication_dates"] = (
    clean_df["publication_dates"].fillna("Unknown")
)

numeric_columns = [
    "first_publication_year",
    "total_editions",
    "cover_id"
]

for column in numeric_columns:

    if column not in clean_df.columns:
        clean_df[column] = np.nan

    clean_df[column] = pd.to_numeric(
        clean_df[column],
        errors="coerce"
    )



clean_df.loc[
    (clean_df["first_publication_year"] < 1000) |
    (clean_df["first_publication_year"] > 2026),
    "first_publication_year"
] = np.nan

clean_df["first_publication_year"] = (
    clean_df["first_publication_year"].astype("Int64")
)

clean_df.loc[
    clean_df["total_editions"] < 0,
    "total_editions"
] = np.nan

clean_df["total_editions"] = (
    clean_df["total_editions"].astype("Int64")
)

clean_df.loc[
    clean_df["cover_id"] <= 0,
    "cover_id"
] = np.nan

clean_df["cover_id"] = clean_df["cover_id"].astype("Int64")

clean_df["primary_author"] = clean_df["authors"].apply(
    lambda x: x.split(";")[0].strip()
    if x != "Unknown" else "Unknown"
)

clean_df["primary_subject"] = clean_df["subjects"].apply(
    lambda x: x.split(";")[0].strip()
    if x != "Unknown" else "Unknown"
)

clean_df["author_count"] = clean_df["authors"].apply(
    lambda x: len(x.split(";"))
    if x != "Unknown" else 0
)

clean_df["subject_count"] = clean_df["subjects"].apply(
    lambda x: len(x.split(";"))
    if x != "Unknown" else 0
)

clean_df["cover_url"] = clean_df["cover_id"].apply(
    lambda x: (
        f"https://covers.openlibrary.org/b/id/{int(x)}-L.jpg"
        if pd.notna(x) else None
    )
)

clean_df = clean_df.drop_duplicates()

clean_df = clean_df.reset_index(drop=True)

clean_df.to_csv(
    CLEANED_FILE,
    index=False,
    encoding="utf-8"
)

clean_df["publication_dates"] = pd.to_datetime(
    clean_df["publication_dates"],
    errors="coerce"
)

clean_df["publication_dates"] = clean_df["publication_dates"].dt.strftime(
    "%Y-%m-%d"
)

print("\n========== CLEANING REPORT ==========")

print("Original records:", len(df))
print("Cleaned records:", len(clean_df))
print("Total columns:", len(clean_df.columns))
print("\nMissing values:")
print(clean_df.isnull().sum())
print("\nData types:")
print(clean_df.dtypes)
print("\nCleaned data preview:")
print(clean_df.head())
print("\nCleaned dataset saved at:")
print(CLEANED_FILE)
print("\nDATA CLEANING COMPLETED SUCCESSFULLY!")

