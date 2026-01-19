import pandas as pd
from validate import validate_dfs

# TODO: Handle encoding issues to clean strange characters in title/description
# TODO: authors that appear in both sources marked as being in only one and missing birth/death years
# e.g. shakespeare, steinbeck
# Add Gutenberg first, then goodreads?


def split_values(col_vals):
    if isinstance(col_vals, str):
        split_vals = col_vals.split(',')
        stripped_vals = [item.strip() for item in split_vals]
        return stripped_vals
    else:
        return pd.NA


def normalize_authors(authors):
    for author in authors:
        if "name" in author:
            parts = author["name"].split(", ")
            if len(parts) == 2:
                author["name"] = f"{parts[1]} {parts[0]}"
    return authors


def book_author_names_view(df):
    view = df[["id", "authors"]].copy()
    view["authors"] = view["authors"].apply(lambda authors: [a["name"] for a in authors])
    return view


def clean_goodreads_data(df):
    return (df
            .assign(date_published=df["date_published"].str.extract(r'(\d{4})', expand=False),
                    author=df["author"].apply(split_values),
                    awards=df["awards"].apply(split_values)
                    )
            .rename(columns={"date_published": "year_published", "author": "authors"})
            .astype({"year_published": "Int64"})
            .dropna(subset=["title", "year_published"])
            .drop_duplicates(subset="id")
            .convert_dtypes()
            )


def _goodreads_author_df(authors):
    cleaned_authors = (authors.to_frame(name="name"))
    cleaned_authors.insert(loc=0, column="source", value="goodreads")
    return cleaned_authors


def _gutenberg_author_df(authors):
    normalized_authors = pd.json_normalize(authors)
    cleaned_authors = normalized_authors.astype({"birth_year": "Int64", "death_year": "Int64"})
    cleaned_authors.insert(loc=0, column="source", value="gutenberg")
    return cleaned_authors


def create_author_df(author_dfs: list, sources: list[str]):
    cleaned_author_dfs = []
    for authors, source in zip(author_dfs, sources):
        cleaned_authors = (authors
                           .explode()
                           .dropna()
                           )
        if source == "gutenberg":
            cleaned_author_dfs.append(_gutenberg_author_df(cleaned_authors))
        elif source == "goodreads":
            cleaned_author_dfs.append(_goodreads_author_df(cleaned_authors))
        else:
            raise ValueError("Unknown source")

    merged_authors = pd.concat(cleaned_author_dfs, ignore_index=True)
    author_table = merged_authors.drop_duplicates(subset="name").reset_index(drop=True)
    author_table.insert(loc=0, column="author_id", value=author_table.index + 1)

    return author_table


def create_link_df(books, authors):
    """Create a dataframe linking book IDs to author IDs for each data source."""
    links = []

    # Lookup dict for faster processing (instead of using .loc)
    authors_lookup = dict(zip(authors["name"], authors["author_id"]))

    for book in books.itertuples():
        for author in book.authors:
            author_id = authors_lookup[author]
            links.append({"book_id": book.id, "author_id": author_id})

    return pd.DataFrame(links)


def clean_gutendex_data(df):
    return (df
            .drop(columns=["formats", "translators", "media_type", "bookshelves"])
            .assign(authors=df["authors"].apply(normalize_authors),
                    subjects=df["subjects"].apply(lambda x: x if x else pd.NA))
            .drop_duplicates(subset="id")
            .dropna(subset=["title"])
            .convert_dtypes()
            )


def transform_dfs():
    pd.set_option("display.max_columns", None)

    goodreads_cols = ["id", "title", "author", "rating_count", "review_count",
                      "average_rating", "number_of_pages", "date_published", "publisher",
                      "settings", "awards", "description"]
    goodreads_df = pd.read_csv("data/goodreads_books.csv", usecols=goodreads_cols)
    gutendex_df = pd.read_json("data/guten_books.json")

    cleaned_goodreads_df = clean_goodreads_data(goodreads_df)
    cleaned_gutendex_df = clean_gutendex_data(gutendex_df)

    author_list = [cleaned_goodreads_df["authors"], cleaned_gutendex_df["authors"]]
    authors = create_author_df(author_list, ["goodreads", "gutenberg"])

    goodreads_book_author_view = cleaned_goodreads_df[["id", "authors"]]
    gutenberg_book_author_view = book_author_names_view(cleaned_gutendex_df)

    goodreads_links = create_link_df(goodreads_book_author_view, authors)
    gutenberg_links = create_link_df(gutenberg_book_author_view, authors)

    goodreads_table = cleaned_goodreads_df.drop(columns=["authors"])
    gutenberg_table = cleaned_gutendex_df.drop(columns=["authors"])

    dfs = {
        "goodreads": goodreads_table,
        "gutenberg": gutenberg_table,
        "authors": authors,
        "goodreads_links": goodreads_links,
        "gutenberg_links": gutenberg_links
    }

    validated_dfs = validate_dfs(dfs)

    return validated_dfs


if __name__ == "__main__":
    transform_dfs()
