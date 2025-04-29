from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
# from kivy.tools.report import title
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import sqlite3

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)

        manage_button = Button(text="Manage Books", size_hint=(1, 0.5)) #creating manage books button
        manage_button.bind(on_press=self.go_to_books)
        layout.add_widget(manage_button)

        exit_button = Button(text="Exit", size_hint=(1, 0.5)) #for exit button
        exit_button.bind(on_press=self.exit_app)
        layout.add_widget(exit_button)

        self.add_widget(layout)

    def go_to_books(self, instance):
        self.manager.current = "book_inventory"

    def exit_app(self, instance):
        App.get_running_app().stop()

class BookInventoryScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation= 'vertical')
        self.inventory = BookInventory()  # BookInventory is the existing form
        layout.add_widget(self.inventory)

        back_button = Button(text="Back to Main Menu", size_hint=(1, 0.1))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.add_widget(layout)
    def go_back(self,instance):
        self.manager.current = "main_menu"

# here is where i create buttons
class BookInventory(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)

        self.conn = sqlite3.connect('angel_store.db')
        self.cursor = self.conn.cursor()

        self.add_widget(Label(text='Book Title'))
        self.title_input = TextInput()
        self.add_widget(self.title_input)

        self.add_widget(Label(text='Genre'))
        self.genre_input = TextInput()
        self.add_widget(self.genre_input)

        self.add_widget(Label(text='Price'))
        self.price_input = TextInput()
        self.add_widget(self.price_input)

        self.add_widget(Label(text='Quantity'))
        self.quantity_input = TextInput()
        self.add_widget(self.quantity_input)

        self.add_button = Button(text='Add Book')
        self.add_button.bind(on_press=self.add_book)
        self.add_widget(self.add_button)

        self.show_button = Button(text='Show All Books')
        self.show_button.bind(on_press=self.show_books)
        self.add_widget(self.show_button)

        self.output = Label(text='')
        self.add_widget(self.output)

#enables me to add books here
    def add_book(self, instance):
        title = self.title_input.text
        genre = self.genre_input.text
        price = self.price_input.text
        quantity = self.quantity_input.text

        # Checks if any field is empty
        if not title or not genre or not price or not quantity:
            self.output.text = "Please fill all fields!"
            return

        try:
            self.cursor.execute("INSERT INTO books (book_title, genre, price, quantity) VALUES (?, ?, ?, ?)",
                                (title, genre, float(price), int(quantity)))
            self.conn.commit()
            self.output.text = f"Book '{title}' added successfully!"
        except Exception as e:
            self.output.text = f"Error: {e}"

            # Clear fields after adding
            self.title_input.text = ""
            self.genre_input.text = ""
            self.price_input.text = ""
            self.quantity_input.text = ""

    def show_books(self, instance):
        self.cursor.execute("SELECT * FROM books")
        books = self.cursor.fetchall()

        if books:
            # Creating a layout for the popup
            layout = GridLayout(cols=5, spacing=10, size_hint_y=None, padding=[10,10])
            layout.bind(minimum_height=layout.setter('height'))

            # Add Header Titles
            headers = ["ID", "Title", "Genre", "Price", "Quantity"]
            for header in headers:
                layout.add_widget(Label(
                    text=header, bold=True, halign="center", valign="middle",
                    size_hint_y=None, height=20, text_size=(150, None)
                ))

            # Adding each book as a Label
            for book in books:
                layout.add_widget(Label(text=str(book[0]), halign="center", valign="middle", size_hint_y=None, height=40))
                layout.add_widget(Label(text=book[1], halign="left", valign="middle", size_hint_y=None, height=40, text_size=(261, None)))
                layout.add_widget(Label(text=book[2], halign="left", valign="middle", size_hint_y=None, height=40, text_size=(150, None)))
                layout.add_widget(Label(text=str(book[3]), halign="center", valign="middle", size_hint_y=None, height=40))
                layout.add_widget(Label(text=str(book[4]), halign="center", valign="middle", size_hint_y=None, height=40))

            # Putting layout inside a scroll view
            scroll = ScrollView(size_hint=(1, 1))
            scroll.add_widget(layout)

            #boxlayout for scroll-view + close button
            popup_layout = BoxLayout(orientation='vertical')
            popup_layout.add_widget(scroll)
            close_button = Button(text="Close", size_hint=(1, 0.1))
            popup_layout.add_widget(close_button)
            popup = Popup(title= "Books in Inventory", content=popup_layout,
                          size_hint=(0.95, 0.9))
            close_button.bind(on_press=popup.dismiss)
            popup.open()

        else:
            self.output.text = "No books found in the inventory."

class InventoryApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainMenu(name="main_menu"))
        sm.add_widget(BookInventoryScreen(name="book_inventory"))
        return sm

if __name__ == '__main__':
    InventoryApp().run()
