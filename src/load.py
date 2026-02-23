import duckdb
from src.transform import transform_dfs

# Import cleaned dataframes from transform file
goodreads_df, gutenberg_df, authors_df, goodreads_link_df, gutenberg_link_df = transform_dfs()

# Database connection
con = duckdb.connect("../data/book_data.ddb")

# Create book and author tables directly from the dataframes
con.execute("CREATE TABLE IF NOT EXISTS goodreads AS SELECT * FROM goodreads_df")
con.execute("ALTER TABLE goodreads ADD PRIMARY KEY (id)")

con.execute("CREATE TABLE IF NOT EXISTS gutenberg AS SELECT * FROM gutenberg_df")
con.execute("ALTER TABLE gutenberg ADD PRIMARY KEY (id)")

con.execute("CREATE TABLE IF NOT EXISTS authors AS SELECT * FROM authors_df")
con.execute("ALTER TABLE authors ADD PRIMARY KEY (author_id)")

# Manually create link tables and import data from Pandas
# This is because these tables require foreign keys, which cannot be added via ALTER TABLE
con.execute("""CREATE TABLE IF NOT EXISTS goodreads_links (
                    book_id BIGINT REFERENCES goodreads(id),
                    author_id BIGINT REFERENCES authors(author_id)
                );""")
con.execute("INSERT INTO goodreads_links SELECT * FROM goodreads_link_df")

con.execute("""CREATE TABLE IF NOT EXISTS gutenberg_links (
                    book_id BIGINT REFERENCES gutenberg(id),
                    author_id BIGINT REFERENCES authors(author_id)
                );""")
con.execute("INSERT INTO gutenberg_links SELECT * FROM gutenberg_link_df")

con.close()
