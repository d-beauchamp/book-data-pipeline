import requests
import json
import os

# TODO: Implement check where files are deleted if they already exist
# TODO: requirements.txt -- look into pyproject.toml


def download_kaggle_dataset(dataset_dir, dataset_identifier):
    os.makedirs(dataset_dir, exist_ok=True)
    os.system(f"kaggle datasets download -d {dataset_identifier} -p {dataset_dir} --unzip")


# Extract book data from Gutendex API using a given query, storing in JSON file
def extract_book_data(url, filename="guten_books.json"):
    book_data = []  # dictionary to accumulate data
    page = 1

    # If the file already exists, resume extraction from the last page
    if os.path.exists(filename):
        print(f"Loading data from {filename}")
        with open(filename, "r") as file:
            book_data = json.load(file)

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


def main():
    new_dir = "data"
    dataset_id = "austinreese/goodreads-books"
    download_kaggle_dataset(new_dir, dataset_id)
    print("Downloaded Kaggle Goodreads dataset")

    query = "https://gutendex.com/books"
    gutendata = extract_book_data(query)
    print(f"Total books fetched: {len(gutendata)}")


if __name__ == "__main__":
    main()
