import duckdb
from transform import main

# TODO: foreign key as title? See about matching possibilities
# Create separate author table where author_id is foreign key

# Import cleaned dataframes from transform file
cleaned_goodreads_df, cleaned_gutendex_df = main()

# Database connection
con = duckdb.connect("book_data.ddb")

# Drop tables if they already exist (to refresh with new data) -- can delete once done testing
# con.execute("DROP TABLE IF EXISTS goodreads")
# con.execute("DROP TABLE IF EXISTS gutenberg")

# Create tables from the dataframes
con.execute("CREATE TABLE IF NOT EXISTS goodreads AS SELECT * FROM cleaned_goodreads_df")
con.execute("CREATE TABLE IF NOT EXISTS gutenberg AS SELECT * FROM cleaned_gutendex_df")

# Code to check that tables look right
"""df = con.sql("SELECT * FROM goodreads").df()
df2 = con.sql("SELECT * FROM gutenberg").df()

print(df.head())
print(df2.head())"""