# app.py

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

from INVENTORY import add_book, delete_book, update_book_details, show_all_books, get_book_by_title

# Initialize database on app start
#initialize_db()

class MainMenuScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)

        add_button = Button(text="Add Book")
        add_button.bind(on_press=lambda x: self.change_screen('add_book'))
        layout.add_widget(add_button)

        delete_button = Button(text="Delete Book")
        delete_button.bind(on_press=lambda x: self.change_screen('delete_book'))
        layout.add_widget(delete_button)

        update_button = Button(text="Update Book")
        update_button.bind(on_press=lambda x: self.change_screen('update_book'))
        layout.add_widget(update_button)

        view_button = Button(text="View Books")
        view_button.bind(on_press=lambda x: self.change_screen('view_books'))
        layout.add_widget(view_button)

        self.add_widget(layout)

    def change_screen(self, screen_name):
        self.manager.current = screen_name

class AddBookScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)

        self.name_input = TextInput(hint_text='Enter Book Name')
        layout.add_widget(self.name_input)

        self.price_input = TextInput(hint_text='Enter Book Price', input_filter='float')
        layout.add_widget(self.price_input)

        add_button = Button(text="Add Book")
        add_button.bind(on_press=self.add_book)
        layout.add_widget(add_button)

        self.status_label = Label(text="")
        layout.add_widget(self.status_label)

        back_button = Button(text="Back to Main Menu")
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def add_book(self, instance):
        name = self.name_input.text
        price = self.price_input.text

        if name and price:
            try:
                add_book(name, float(price))
                self.status_label.text = "Book added successfully!"
                self.name_input.text = ""
                self.price_input.text = ""
            except ValueError:
                self.status_label.text = "Invalid price!"
        else:
            self.status_label.text = "Please fill all fields."

    def go_back(self, instance):
        self.manager.current = "main_menu"

class DeleteBookScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)

        self.book_id_input = TextInput(hint_text='Enter Book ID to Delete')
        layout.add_widget(self.book_id_input)

        delete_button = Button(text="Delete Book")
        delete_button.bind(on_press=self.delete_book)
        layout.add_widget(delete_button)

        self.delete_status = Label(text="")
        layout.add_widget(self.delete_status)

        back_button = Button(text="Back to Main Menu")
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def delete_book(self, instance):
        book_id = self.book_id_input.text
        if book_id:
            try:
                delete_book(int(book_id))
                self.delete_status.text = "Book deleted successfully!"
                self.book_id_input.text = ""
            except ValueError:
                self.delete_status.text = "Invalid Book ID!"
        else:
            self.delete_status.text = "Please enter a Book ID."

    def go_back(self, instance):
        self.manager.current = "main_menu"

class UpdateBookScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)

        self.book_id_input = TextInput(hint_text='Enter Book ID')
        layout.add_widget(self.book_id_input)

        self.new_name_input = TextInput(hint_text='New Name (leave blank if no change)')
        layout.add_widget(self.new_name_input)

        self.new_price_input = TextInput(hint_text='New Price (leave blank if no change)', input_filter='float')
        layout.add_widget(self.new_price_input)

        update_button = Button(text="Update Book")
        update_button.bind(on_press=self.update_book)
        layout.add_widget(update_button)

        self.update_status = Label(text="")
        layout.add_widget(self.update_status)

        back_button = Button(text="Back to Main Menu")
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)

    def update_book(self, instance):
        book_id = self.book_id_input.text
        name = self.new_name_input.text
        price = self.new_price_input.text

        if book_id:
            try:
                update_book_details(int(book_id), name=name if name else None, price=float(price) if price else None)
                self.update_status.text = "Book updated successfully!"
            except ValueError:
                self.update_status.text = "Invalid input!"
        else:
            self.update_status.text = "Please enter Book ID."

    def go_back(self, instance):
        self.manager.current = "main_menu"

class ViewBooksScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=50, spacing=20)

        self.books_label = Label(text="Books will be displayed here")
        self.layout.add_widget(self.books_label)

        refresh_button = Button(text="Refresh List")
        refresh_button.bind(on_press=self.refresh_books)
        self.layout.add_widget(refresh_button)

        back_button = Button(text="Back to Main Menu")
        back_button.bind(on_press=self.go_back)
        self.layout.add_widget(back_button)

        self.add_widget(self.layout)

    def refresh_books(self, instance):
        books = show_all_books()
        if books:
            books_text = "\n".join([f"ID: {book[0]}, Name: {book[1]}, Price: {book[2]}" for book in books])
            self.books_label.text = books_text
        else:
            self.books_label.text = "No books available."

    def go_back(self, instance):
        self.manager.current = "main_menu"

class InventoryApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenuScreen(name='main_menu'))
        sm.add_widget(AddBookScreen(name='add_book'))
        sm.add_widget(DeleteBookScreen(name='delete_book'))
        sm.add_widget(UpdateBookScreen(name='update_book'))
        sm.add_widget(ViewBooksScreen(name='view_books'))
        return sm

if __name__ == "__main__":
    InventoryApp().run()
