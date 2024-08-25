import pandas as pd
import gzip

def process_openlib_dump():

filename = "open_lib_books.json"
books_df = pd.read_json(filename)

books_df.head(n=3)
books_df.tail(n=3)