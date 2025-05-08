#  Setup Instructions - Inventory Control System

---

## 1. Requirements

Before running the application, make sure you have the following installed:

* **Python** (version 3.8 or higher recommended)
* **Kivy** library
* **SQLite3** (comes built-in with Python)

---

## 2. Install Required Python Packages

Open your terminal or command prompt and run:

```bash
 pip install kivy
```

(You may also install other optional packages for better UI performance.)

---

## 3. Clone or Download the Project

If using Git, clone the repository:

```bash
   git clone <repository-link>
```

Otherwise, manually download and extract the ZIP file.

---

## 4. Project Structure

The project contains the following important files:

| File Name                 | Description                           |
| ------------------------- | ------------------------------------- |
| `main_kivy.py`            | Main file for running the application |
| `INVENTORY.py`            | File containing database operations   |
| `angel_store.db`          | SQLite database storing book records  |
| `README.md`               | Basic project information (optional)  |
| `USER_MANUAL.md`          | Instructions on how to use the app    |
| `SETUP_INSTRUCTIONS.docx` | This setup guide                      |

---

## 5. Setting Up the Database

The database `angel_store.db` will be created automatically when you first run the program.

If not, you can manually run:

```bash
  python INVENTORY.py
```

to initialize and populate the database with sample books.

---

## 6. Running the Application

From the terminal, navigate to the project folder and run:

```bash
  python main_kivy.py
```

This will open the Inventory Control System window.

---

## 7. Common Problems & Solutions

| Problem                    | Solution                                                     |
| -------------------------- | ------------------------------------------------------------ |
| App does not open          | Make sure Python and Kivy are properly installed             |
| Database errors            | Delete `angel_store.db` and rerun `INVENTORY.py`             |
| Screen layout looks broken | Resize the app window or check for missing Kivy dependencies |

---
