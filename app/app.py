import streamlit as st
import matplotlib.pyplot as plt

conn = st.connection("book_data_db", type="sql")

st.set_page_config(
    page_title="Book Data Dashboard",
    page_icon=":bar_chart"
)

st.title("Book Data Dashboard :books:")

with st.expander("About the Data"):
    st.header("Goodreads and Gutenberg")

    st.write("""**Goodreads** is an online platform where readers can track their reading and review/recommend
    books. The Goodreads data here contains 50,000 books scraped from a Goodreads list titled "Best Books Ever
     and published by Austin Reese on Kaggle. The original dataset contains 31 book features, many of which
     have been removed for streamlining purposes.""")

    st.write("""**Project Gutenberg** is an online library of over 75,000 free eBooks. The data here
    is extracted using the unofficial Gutendex API, which provides metadata on authors and books
    available there.""")

st.header("Most Popular Books (Gutenberg)")

# Use parameterized queries to handle different centuries
most_popular_books = conn.query(f"""SELECT
                                        gutenberg.id,
                                        gutenberg.title,
                                        authors.name AS author,
                                        gutenberg.download_count
                                    FROM gutenberg
                                    INNER JOIN gutenberg_links 
                                        ON gutenberg.id = gutenberg_links.book_id
                                    INNER JOIN authors
                                        ON gutenberg_links.author_id = authors.author_id
                                    LIMIT 10;""")

most_popular_books.index += 1

st.dataframe(most_popular_books)

# Display different languages in Gutendex
st.header("Book Languages (Gutenberg)")

languages = conn.query("""SELECT 
                            lang,
                            COUNT(DISTINCT id) AS book_count
                          FROM gutenberg
                          CROSS JOIN UNNEST(languages) as t(lang)
                          GROUP BY lang
                          ORDER BY book_count DESC""")
st.dataframe(languages)

st.header("Longest-Lived Authors")

author_age = conn.query("""SELECT 
                            author_id, 
                            name, 
                            birth_year,
                            death_year,
                            (death_year - birth_year) AS age
                           FROM authors
                           ORDER BY age DESC
                           LIMIT 25;""")
st.dataframe(author_age)

# Graph book ratings in Goodreads compared to publication year (scatter)

st.header("Book Ratings Distribution Across Time (Goodreads)")

ratings = conn.query("SELECT year_published, average_rating FROM goodreads")

plt.style.use("dark_background")
fig, ax = plt.subplots()
ax.scatter(ratings["year_published"], ratings["average_rating"], s=1)

ax.set_xlim(1000, 2026)
ax.set_xlabel("Year")
ax.set_ylabel("Rating")

st.pyplot(fig)
