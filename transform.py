import pandas as pd
import re

# Todo: see how to fix encoding in order to avoid strange characters in title/description
# Todo: Try to break down columns that are lists
# Todo: drop duplicates for id and title columns in BOTH tables (also dropna id)
# Todo: Check if import re is needed
# Todo: rename id columns to goodreads_id and gutendex_id for clarity

def split_values(col_vals):
    if isinstance(col_vals, str):
        split_vals = col_vals.split(',')
        stripped_vals = [item.strip() for item in split_vals]
        return stripped_vals
    else:
        return pd.NA

def clean_goodreads_data(df):
    return (df
            # See if there's a way to .apply to multiple columns at once
            .assign(date_published=df["date_published"].str.extract(r'(\d{4})', expand=False),
                    author=df["author"].apply(split_values),
                    books_in_series=df["books_in_series"].apply(split_values),
                    awards=df["awards"].apply(split_values)
                    )
            .rename(columns={"date_published": "year_published"})
            .astype({"year_published": "Int64"})
            .dropna(subset=["title", "year_published"])
            .convert_dtypes()
            )

def rearrange_author_names(authors):
    for author in authors:
        if "name" in author:
            parts = author["name"].split(", ")
            if len(parts) == 2:
                author["name"] = f"{parts[1]} {parts[0]}"
    return authors

def clean_gutendex_data(df):
    return (df
            .drop(columns='formats')
            .assign(authors=df["authors"].apply(rearrange_author_names))
            .drop_duplicates(subset="id")
            .dropna(subset=["title"])
            .convert_dtypes()
            )

def main():
    pd.set_option("display.max_columns", None)

    goodreads_cols = ["id", "title", "series", "author", "rating_count", "review_count",
                      "average_rating", "five_star_ratings", "four_star_ratings", "three_star_ratings",
                      "two_star_ratings", "one_star_ratings", "number_of_pages", "date_published", "publisher",
                      "settings", "awards", "books_in_series", "description"]
    goodreads_df = pd.read_csv("kaggle_datasets/goodreads_books.csv", usecols=goodreads_cols)
    gutendex_df = pd.read_json("guten_books.json")

    cleaned_goodreads_df = clean_goodreads_data(goodreads_df)
    cleaned_gutendex_df = clean_gutendex_data(gutendex_df)

    return cleaned_goodreads_df, cleaned_gutendex_df

if __name__ == "__main__":
    main()


