import csv


class Book:
    def __init__(self, title, author, pages, finished=False):
        # store the core attributes of a book when a new object is created
        self.title = title
        self.author = author
        self.pages = pages
        self.finished = finished   # defaults to False unless specified

    def mark_finished(self):
        # updates the book's status to finished — used once you complete reading it
        self.finished = True

    def __str__(self):
        # defines how a Book prints when passed to print() — instead of the
        # default "<Book object at 0x...>", we get a readable summary line
        status = "Finished" if self.finished else "Not finished"
        return f"{self.title} by {self.author} ({self.pages} pages) — {status}"


def save_books_to_csv(books, filename):
    # write the list of Book objects out to a CSV file, one row per book
    with open(filename, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["title", "author", "pages", "finished"])
        writer.writeheader()   # writes the column names as the first row
        for book in books:
            # convert each Book object's attributes into a plain dictionary,
            # since csv.DictWriter expects rows in dict form
            writer.writerow({
                "title": book.title,
                "author": book.author,
                "pages": book.pages,
                "finished": book.finished,
            })


def load_books_from_csv(filename):
    # read the CSV back in and rebuild a list of Book objects from it
    loaded_books = []
    with open(filename, "r") as f:
        reader = csv.DictReader(f)   # each row comes back as a dictionary
        for row in reader:
            # CSV values are always strings, so we convert "pages" to int
            # and compare "finished" against the string "True" to get a real bool
            book = Book(
                row["title"],
                row["author"],
                int(row["pages"]),
                finished=(row["finished"] == "True"),
            )
            loaded_books.append(book)
    return loaded_books


def main():
    # create the initial list of Book objects to work with
    books = [
        Book("Atomic Habits", "James Clear", 320, finished=True),
        Book("Deep Work", "Cal Newport", 296),
        Book("The Name of the Wind", "Patrick Rothfuss", 662, finished=True),
        Book("Mistborn: The Final Empire", "Brandon Sanderson", 541),
        Book("The Way of Kings", "Brandon Sanderson", 1007, finished=True),
    ]

    # save all books to a CSV file
    save_books_to_csv(books, "library.csv")

    # load the books back from that same file into a brand-new list —
    # this confirms the round trip (save then load) works correctly
    loaded_books = load_books_from_csv("library.csv")

    # print each loaded book using __str__ to verify everything matches
    for book in loaded_books:
        print(book)


# this block only runs when the file is executed directly (not when imported
# as a module elsewhere) — standard entry point pattern for Python scripts
if __name__ == "__main__":
    main()