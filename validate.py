import warnings

import pandas as pd
from pandera.typing.pandas import Series, DataFrame
import pandera.pandas as pa


class GoodreadsSchema(pa.DataFrameModel):
    """Data model for the Goodreads dataframe"""
    id: int = pa.Field(unique=True, ge=0)
    title: str
    rating_count: int = pa.Field(ge=0)
    review_count: int = pa.Field(ge=0)
    average_rating: float = pa.Field(ge=0.00, le=5.00)
    number_of_pages: pd.Int64Dtype = pa.Field(nullable=True, ge=0)
    year_published: int = pa.Field(le=2026)
    publisher: str = pa.Field(nullable=True)
    settings: str = pa.Field(nullable=True)
    awards: list[str] = pa.Field(nullable=True)
    description: str = pa.Field(nullable=True)

    @pa.dataframe_check(raise_warning=True)
    def ratings_over_reviews(cls, df: DataFrame) -> Series[bool]:
        """Custom dataframe check that uses a manual warning to display only IDs of rows where rating count is
        higher than review count."""
        check = df["rating_count"] >= df["review_count"]

        if not check.all():
            failed_ids = df.loc[~check, "id"].tolist()
            print(f"[WARNING] rating_count < review count in some rows. Failed IDs: {failed_ids}")

        return check

    class Config:
        strict = True
        coerce = True
        unique_column_names = True


class GutenbergSchema(pa.DataFrameModel):
    """Data model for the Gutenberg dataframe"""
    id: int = pa.Field(unique=True, ge=0)
    title: str
    subjects: list[str] = pa.Field(nullable=True)
    languages: list[str]
    copyright: bool
    download_count: int = pa.Field(ge=0)

    @pa.check("languages")
    def lang_code_len(cls, languages: Series[str]) -> Series[bool]:
        return languages.apply(lambda langs: [l == 2 for l in langs])

    class Config:
        strict = True
        coerce = True
        unique_column_names = True


class AuthorSchema(pa.DataFrameModel):
    """Data model for authors dataframe."""
    author_id: int = pa.Field(unique=True, gt=0)
    source: str = pa.Field(isin=["gutenberg", "goodreads"])
    name: str
    birth_year: int = pa.Field(nullable=True, le=2026)
    death_year: int = pa.Field(nullable=True, le=2026)

    @pa.dataframe_check
    def valid_years(cls, df: DataFrame) -> Series[bool]:
        return df["birth_year"] < df["death_year"]


class LinkSchema(pa.DataFrameModel):
    """Data model for book-author link dataframes."""
    book_id: int = pa.Field(ge=0)
    author_id: int = pa.Field(gt=0)

    class Config:
        strict = True
        coerce = True
        unique_column_names = True


SCHEMAS = {
    "goodreads": GoodreadsSchema,
    "gutenberg": GutenbergSchema,
    "authors": AuthorSchema,
    "goodreads_links": LinkSchema,
    "gutenberg_links": LinkSchema
}


def validate_dfs(dfs: dict[str, DataFrame]):
    validated_dfs = []
    for name, df in dfs.items():
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", category=pa.errors.SchemaWarning)
                validated_dfs.append(SCHEMAS[name].validate(df, lazy=True))
        except pa.errors.SchemaError as exc:
            print("Schema errors and failure cases:")
            print(exc.failure_cases)
    return validated_dfs
