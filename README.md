# book-data-pipeline

## :books: Book Data Pipeline and Dashboard

### Overview

This project builds an ETL pipeline integrating Goodreads and Project Gutenberg data into a relational DuckDB database, 
with by a Streamlit dashboard for analytics and visualization.

For ease of viewing, I've deployed the dashboard via Streamlit Cloud; it can be found
here: <https://book-data-pipeline.streamlit.app>.

### Tech Stack

* Python 
* Pandas
* DuckDB
* Streamlit
* SQL

### Pipeline Architecture

1. **Extract**: Load raw datasets from the APIs.
2. **Transform**: Clean and normalize data.
3. **Validate**: Enforce schemas and constraints.
4. **Load**: Create relational database with primary/foreign keys.
5. **Analyze**: Deploy a Streamlit dashboard with sample insights.

### How to Run

```bash
pip install -r requirements.txt
python src/extract.py
python src/load.py
```

### Future Improvements

* Introduce scheduling/orchestration for a more streamlined pipeline.
* Update extract.py to resume extraction from last page if file already exists.
* Fix encoding issues and authors with missing years that sometimes occur in the transform stage. 