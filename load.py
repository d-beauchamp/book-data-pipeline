import duckdb
from transform import main

# TODO: implement foreign key for more traditional structure (create author_id or use title)

# Import cleaned dataframes from transform file
cleaned_goodreads_df, cleaned_gutendex_df = main()

# Database connection
con = duckdb.connect("book_data.ddb")

# Create tables from the dataframes
con.execute("CREATE TABLE IF NOT EXISTS goodreads AS SELECT * FROM cleaned_goodreads_df")
con.execute("CREATE TABLE IF NOT EXISTS gutenberg AS SELECT * FROM cleaned_gutendex_df")

# Code to check that tables look right
df = con.sql("SELECT * FROM goodreads").df()
df2 = con.sql("SELECT * FROM gutenberg").df()

print(df.head())
print(df2.head())