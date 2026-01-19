import streamlit as st

conn = st.connection("book_data_db", type="sql")

st.set_page_config(
    page_title="Book Data Dashboard",
    page_icon=":bar_chart"
)

st.title("Book Data Dashboard :books:")

authors = conn.query("SELECT * FROM authors ORDER BY birth_year DESC")
st.dataframe(authors)
