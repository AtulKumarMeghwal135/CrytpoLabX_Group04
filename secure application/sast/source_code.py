import sqlite3


DATABASE = "library.db"


def initialize_database():
    """Create the database and required tables."""

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS members (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            issued INTEGER DEFAULT 0
        )
    """)

    connection.commit()
    connection.close()


def register_member():
    """Register a new library member."""

    print("\n--- Member Registration ---")

    name = input("Enter member name: ")
    email = input("Enter member email: ")

    # VULNERABILITY 2:
    # IMPROPER INPUT VALIDATION
    #
    # The application does not properly validate the
    # member name or email address.

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO members (name, email) VALUES (?, ?)",
        (name, email)
    )

    connection.commit()
    connection.close()

    print("Member registered successfully.")


def add_book():
    """Add a new book to the library."""

    print("\n--- Add Book ---")

    title = input("Enter book title: ")
    author = input("Enter author: ")

    # VULNERABILITY 2:
    # IMPROPER INPUT VALIDATION
    #
    # Empty/invalid values are not properly validated.

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO books (title, author) VALUES (?, ?)",
        (title, author)
    )

    connection.commit()
    connection.close()

    print("Book added successfully.")


def search_book():
    """Search books by title."""

    print("\n--- Search Book ---")

    title = input("Enter book title to search: ")

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    # VULNERABILITY 1:
    # SQL INJECTION
    #
    # User input is directly concatenated with
    # the SQL query instead of using a parameterized query.

    query = (
        "SELECT id, title, author, issued "
        "FROM books WHERE title LIKE '%"
        + title
        + "%'"
    )

    try:
        cursor.execute(query)

        results = cursor.fetchall()

        if results:
            print("\nSearch Results:")

            for book in results:

                if book[3] == 1:
                    status = "Issued"
                else:
                    status = "Available"

                print(
                    "ID:", book[0],
                    "| Title:", book[1],
                    "| Author:", book[2],
                    "| Status:", status
                )

        else:
            print("No books found.")

    except sqlite3.Error as error:
        print("Database error:", error)

    connection.close()


def issue_book():
    """Issue a book to a member."""

    print("\n--- Issue Book ---")

    book_id = input("Enter book ID: ")
    member_id = input("Enter member ID: ")

    try:
        book_id = int(book_id)
        member_id = int(member_id)

        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        cursor.execute(
            "SELECT issued FROM books WHERE id = ?",
            (book_id,)
        )

        book = cursor.fetchone()

        if book is None:
            print("Book not found.")
            connection.close()
            return

        if book[0] == 1:
            print("Book is already issued.")
            connection.close()
            return

        cursor.execute(
            "SELECT id FROM members WHERE id = ?",
            (member_id,)
        )

        member = cursor.fetchone()

        if member is None:
            print("Member not found.")
            connection.close()
            return

        cursor.execute(
            "UPDATE books SET issued = 1 WHERE id = ?",
            (book_id,)
        )

        connection.commit()
        connection.close()

        print("Book issued successfully.")

    except ValueError:
        print("Invalid ID. Please enter a number.")


def return_book():
    """Return a book and calculate the fine."""

    print("\n--- Return Book ---")

    book_id = input("Enter book ID: ")
    late_days = input("Enter number of late days: ")

    try:
        book_id = int(book_id)
        late_days = int(late_days)

        # VULNERABILITY 2:
        # IMPROPER INPUT VALIDATION
        #
        # Negative late days are accepted.
        #
        # Example:
        # late_days = -10
        # fine = -50

        fine = late_days * 5

        connection = sqlite3.connect(DATABASE)
        cursor = connection.cursor()

        cursor.execute(
            "UPDATE books SET issued = 0 WHERE id = ?",
            (book_id,)
        )

        connection.commit()
        connection.close()

        print("Book returned successfully.")
        print("Fine: Rs.", fine)

    except ValueError:
        print("Invalid input.")


def display_menu():
    """Display the application menu."""

    print("\n======================================")
    print("      LIBRARY MANAGEMENT SYSTEM")
    print("======================================")
    print("1. Register Member")
    print("2. Add Book")
    print("3. Search Book")
    print("4. Issue Book")
    print("5. Return Book")
    print("6. Exit")
    print("======================================")


def main():
    """
    Start the Library Management System.

    VULNERABILITY 3:
    MISSING AUTHENTICATION

    There is no username/password authentication
    before accessing the application.

    Any person who starts the program can directly
    access library operations.
    """

    initialize_database()

    # VULNERABILITY 3:
    # No login/authentication is performed here.

    print("\nWelcome to the Library Management System.")
    print("No authentication is required.")

    while True:

        display_menu()

        choice = input("Enter your choice: ")

        if choice == "1":
            register_member()

        elif choice == "2":
            add_book()

        elif choice == "3":
            search_book()

        elif choice == "4":
            issue_book()

        elif choice == "5":
            return_book()

        elif choice == "6":
            print("Thank you for using the Library Management System.")
            break

        else:
            print("Invalid menu choice.")


if __name__ == "__main__":
    main()
