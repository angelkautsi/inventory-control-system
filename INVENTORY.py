import sqlite3

def create_table():
    conn = sqlite3.connect('angel_store.db')
    a = conn.cursor()

    # Create the table if it doesn't exist
    a.execute('''
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY,
            book_title TEXT NOT NULL,
            genre TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER DEFAULT 0
        )
    ''')

    conn.commit()
    conn.close()

# Call the function
create_table()

#adding items
def add_book(book_id, book_title, genre, price, quantity):
        conn = sqlite3.connect('angel_store.db')
        a = conn.cursor()

        try:
            a.execute("INSERT INTO books (book_id, book_title, genre, price, quantity) VALUES (?, ?, ?, ?, ?)",
                      (book_id, book_title, genre, price, quantity))
            conn.commit()
            print(f"Added book: {book_title}")
        except sqlite3.IntegrityError:
            print("This Book ID already exists. Try a different one.")

        conn.close()
        # --- Test Example (You can remove this after testing) ---
        # Uncomment and change values to test
add_book(1, "A Court of Thorns and Roses", "Fantasy", 550.0, 100)
add_book(2, "Twilight", "Dark Romance", 420.0, 55)
add_book(3, "Jack & Jill", "Suspence & crime", 600.0, 399)
add_book(4, "Better Than The Movies", "YA Romance", 590.0, 5)


create_table()

def show_all_books():
    conn = sqlite3.connect('angel_store.db')
    a = conn.cursor()

    # Query all books from the database
    a.execute("SELECT * FROM books") #we are selecting from the table
    books = a.fetchall()

    # Display the books using if-else condition statements
    if books:
        print("\n--- All Books in Inventory ---")
        for book in books:
            print(f"ID: {book[0]} | Title: {book[1]} | Genre: {book[2]} | Price: {book[3]} | Quantity: {book[4]}")
    else:
        print("No books found in the inventory.")

    conn.close()

show_all_books() # This function displays all the books in the database


#updating book details
def update_book_details(book_id, new_title=None, new_genre=None, new_price=None):
    conn = sqlite3.connect('angel_store.db')
    a = conn.cursor()

    # Build a dynamic update query
    if new_title:
        a.execute("UPDATE books SET book_title = ? WHERE book_id = ?", (new_title, book_id))
    if new_genre:
        a.execute("UPDATE books SET genre = ? WHERE book_id = ?", (new_genre, book_id))
    if new_price:
        a.execute("UPDATE books SET price = ? WHERE book_id = ?", (new_price, book_id))

    conn.commit()
    print(f"✅ Book ID {book_id} updated successfully.")
    conn.close()

update_book_details(2, new_title="Twilight Saga", new_price=450.0)

#delete_book() function

# Getting a book by its title
def get_book_by_title(title):
    conn = sqlite3.connect('angel_store.db')
    a = conn.cursor()

    a.execute("SELECT * FROM books WHERE book_title = ?", (title,))
    book = a.fetchone()

    if book:
        print(f"Found Book:\nID: {book[0]} | Title: {book[1]} | Genre: {book[2]} | Price: {book[3]} | Quantity: {book[4]}")
    else:
        print(f"\nNo book found with title '{title}'.")

    conn.close()
#get_book_by_title()


