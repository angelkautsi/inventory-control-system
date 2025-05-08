**Inventory Control System Documentation**

---

# 1. Setup Instructions

### Software Requirements:

* Python 3.11 or higher
* pip (Python package installer)
* Git (for version control)

### Required Python Libraries:

* Kivy
* SQLite3 (built into Python)

### Installation Steps:

1. **Clone the repository:**

```bash
   git clone <your-repository-link>
```

2. **Navigate into the project folder:**

```bash
   cd inventory-control-system
```

3. **Create and activate a virtual environment (optional but recommended):**

```bash
   python -m venv venv
   source venv/bin/activate  # For Linux/Mac
   venv\Scripts\activate     # For Windows
```

4. **Install Kivy:**

```bash
   pip install kivy
```

5. **Run the application:**

```bash
   python main_kivy.py
```

---

# 2. User Manual

### Main Menu:

* **Manage Books:** Add and view books.
* **Update Book:** Update an existing book's name or price.
* **Delete Book:** Remove a book using its ID.
* **Search Book:** Find books by title or genre.
* **Exit:** Close the application.

### Adding a Book:

* Fill in "Book Title," "Genre," "Price," and "Quantity".
* Click **Add Book**.

### Viewing All Books:

* Click **Show All Books** to see the list.

### Updating a Book:

* Enter the Book ID.
* Fill in the new title and/or genre and/or new price.
* Click **Save Changes**.

### Deleting a Book:

* Enter the Book ID to delete.
* Click **Delete Book**.

### Searching for a Book:

* Enter a Title or Genre.
* Click **Search**.

---

# 3. Code Overview

### Main Files:

* **main\_kivy.py**: The main Kivy application with screens for each functionality.
* **INVENTORY.py**: Handles database operations (add, delete, update, search).

### Main Components:

* **GradientBackground**: Adds a purple gradient to the app.
* **MainMenu**: Main screen for navigation.
* **BookInventory**: Adding and showing books.
* **UpdateBookScreen**: Updating a book.
* **DeleteBookScreen**: Deleting a book.
* **SearchBookScreen**: Searching for a book.

### Database:

* SQLite database: `angel_store.db`
* Table: `books`
* Columns: `book_id`, `book_title`, `genre`, `price`, `quantity`

---

# 4. Commenting Approach

* All classes and major functions are commented.
* Each section describes its purpose briefly.
* Inline comments explain critical lines.
* Logical division: screens and database operations are clearly separated.

### Example Comment:

```python
# This class handles the main menu screen
class MainMenu(Screen):
    ...

# Adds a new book to the database
 def add_book(self, instance):
     ...
```

---

# Final Notes

* Buttons have custom colors and round corners for better user experience.
* Gradient background ensures visual appeal.
* The app is kept simple, user-friendly, and lightweight.

---

**End of Documentation**

---
