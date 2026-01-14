import pandera.pandas as pa


class GoodreadsSchema(pa.DataFrameModel):
    """Data model for the Goodreads dataframe"""
    ...


class GutenbergSchema(pa.DataFrameModel):
    """Data model for the Gutenberg dataframe"""
    ...


class AuthorSchema(pa.DataFrameModel):
    """Data model for authors dataframe."""
    author_id: int = pa.Field()
    name: str = pa.Field()
    birth_year: int = pa.Field(nullable=True)
    death_year: int = pa.Field(nullable=True)
    ...


# use alias parameter of field to handle different book_id names
class LinkSchema(pa.DataFrameModel):
    """Data model for book-author link dataframes."""
    book_id: int = pa.Field()
    author_id: int = pa.Field()


def validate_dfs():
    ...