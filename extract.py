import requests
import json
import os

# Todo: add case where files are deleted if they already exist
# Todo: fix main function

def download_kaggle_dataset(dataset_dir, dataset_identifier):
    os.makedirs(dataset_dir, exist_ok=True)
    os.system(f"kaggle datasets download -d {dataset_identifier} -p {dataset_dir} --unzip")

# Extract book data from Gutendex API using a given query, storing in JSON file
def extract_book_data(url, filename="guten_books.json"):
    book_data = []  # dictionary to accumulate data
    page = 1

    '''# If the file already exists, resume extraction from the last page
    if os.path.exists(filename):
        print(f"Loading data from {filename}")
        with open(filename, "r") as file:
            book_data = json.load(file)'''

    # maybe break this into separate function
    while True:
        params = {
            "page": page
        }

        response = requests.get(url, params)
        if response.status_code != 200:
            print(f"Failed to retrieve data: {response.status_code}")
            break

        # load request data as a dict and store the book objects from 'results'
        data = response.json()
        books = data.get("results", [])

        # break out of the loop if no books available
        if not books:
            break

        # add current page results to overall collection of books
        book_data.extend(books)

        if page % 50 == 0:
            print(books[0]["title"])
            with open(filename, "w") as file:
                json.dump(book_data, file, indent=4)

        page += 1

    with open(filename, "w") as file:
        json.dump(book_data, file, indent=4)

    return book_data


if __name__ == "__main__":
    '''url = "https://openlibrary.org/data/ol_dump_works_latest.txt.gz"
    local_file = "ol_dump_works_latest.txt.gz"
    open_lib_dump = download_file(url, local_file)
    print(f"Downloaded {local_file}")'''

    new_dir = "kaggle_datasets"
    dataset_id = "austinreese/goodreads-books"
    download_kaggle_dataset(new_dir, dataset_id)
    print("Downloaded dataset")

    '''query = "https://gutendex.com/books"
    gutendata = extract_book_data(query)
    print(f"Total books fetched: {len(gutendata)}")'''


'''def download_file(url, local_filename):
    with requests.get(url, stream=True) as response:
        response.raise_for_status()  # check for errors
        with open(local_filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=64*1024):
                file.write(chunk)
                print("Chunk processed")
    return local_filename'''

'''# Extract book data from OpenLibrary API using a given query, storing in JSON file
def extract_lib_data(query, limit, filename="open_lib_books.json"):
    book_data = [] # dictionary to accumulate data
    url = https://openlibrary.org/search.json
    page = 1

    if os.path.exists(filename): # potential variable for filename if made function
        print(f"Loading data from {filename}")
        with open(filename, "r") as file:
            book_data = json.load(file)
        page = (len(book_data) // limit) + 1

    # maybe break this into separate function
    while True:
        params = {
            "q": query,
            "fields": "title, author_name, edition_count, first_publish year, contributor, first_sentence, \
                     subject, language, publisher, number_of_pages_median, place, time, readinglog_count, \
                     ratings_average, ratings_count",
            "page": page,
            "limit": limit
        }
        headers = {
            "User-Agent": "ETL Pipeline/1.0 (dbeauchamp@vassar.edu)"
        }
        response = requests.get(url, params=params, headers=headers)
        if response.status_code != 200:
            print(f"Failed to retrieve data: {response.status_code}")
            break

        data = response.json()
        books = data.get("docs", [])

        if not books:
            break

        book_data.extend(books)
        page += 1

        if len(book_data) % 10000 == 0:
            print(books[0]["title"])
            with open(filename, "w") as file:
                json.dump(book_data, file, indent=4)

    with open(filename, "w") as file:
        json.dump(book_data, file, indent=4)

    return book_data
'''
