from pandas import Series, DataFrame
import pandera.pandas as pa


class ConfigModel(pa.DataFrameModel):
    class Config:
        strict = True
        coerce = True
        unique_column_names = True


class GoodreadsSchema(pa.DataFrameModel, ConfigModel):
    """Data model for the Goodreads dataframe"""
    id: int = pa.Field(unique=True, ge=0)
    title: str
    rating_count: int = pa.Field(ge=0)
    review_count: int = pa.Field(ge=0)
    average_rating: float = pa.Field(between=(0.00, 5.00))
    number_of_pages: int = pa.Field(ge=0)
    year_published: int = pa.Field(le=2026)
    publisher: str = pa.Field(nullable=True)
    settings: str = pa.Field(nullable=True)
    awards: list[str] = pa.Field(nullable=True)
    description: str = pa.Field(nullable=True)

    @pa.dataframe_check
    def ratings_over_reviews(cls, df: DataFrame) -> Series[bool]:
        return df["rating_count"] >= df["review_count"]


class GutenbergSchema(pa.DataFrameModel, ConfigModel):
    """Data model for the Gutenberg dataframe"""
    id: int = pa.Field(unique=True, ge=0)
    title: str = pa.Field()
    subjects: list[str] = pa.Field(nullable=True)
    languages: list[str] = pa.Field()
    copyright: bool = pa.Field()
    download_count: int = pa.Field(ge=0)

    @pa.check("languages")
    def lang_code_len(cls, languages: Series[str]) -> Series[bool]:
        return languages.apply(lambda langs: [l == 2 for l in langs])


class AuthorSchema(pa.DataFrameModel, ConfigModel):
    """Data model for authors dataframe."""
    author_id: int = pa.Field(unique=True, gt=0)
    source: str = pa.Field(isin=["gutenberg", "goodreads"])
    name: str = pa.Field()
    birth_year: int = pa.Field(nullable=True, le=2026)
    death_year: int = pa.Field(nullable=True, le=2026)

    @pa.dataframe_check
    def valid_years(cls, df: DataFrame) -> Series[bool]:
        return df["birth_year"] < df["death_year"]


class LinkSchema(pa.DataFrameModel, ConfigModel):
    """Data model for book-author link dataframes."""
    book_id: int = pa.Field(ge=0)
    author_id: int = pa.Field(gt=0)


def validate_dfs():
    try:
        ...  # TODO: lazy validation
    except pa.errors.SchemaError as exc:
        print(exc)
