#from kivy.app import App
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
from kivy.app import App
#from INVENTORY import delete_book
from INVENTORY import delete_book, search_book_by_title, search_book_by_genre
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle, Color
from kivy.core.window import Window


# Gradient background
class GradientBackground(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(0.5, 0.2, 0.7, 1)  # Deep purple
            self.rect = Rectangle(size=Window.size, pos=self.pos)
        self.bind(size=self.update_rect, pos=self.update_rect)
        Window.bind(size=self.update_rect)

    def update_rect(self, *args):
        self.rect.size = Window.size
        self.rect.pos = self.pos

class MainMenu(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)

        # Common button style
        def create_button(text, bg_color, text_color):
            return Button(
                text=text,
                background_color=bg_color,
                color=text_color,
                font_size=22,
                bold=True,
                size_hint=(1, 0.2),
                background_normal='',
                background_down=''
            )

        manage_button = create_button("Manage Books", (1, 0.75, 0.8, 1), (0, 0, 0, 1))  # pink bg, black text
        manage_button.bind(on_press=self.go_to_books)
        layout.add_widget(manage_button)

        update_button = create_button("Update Book", (1, 0.75, 0.8, 1), (0, 0, 0, 1))
        update_button.bind(on_press=lambda x: setattr(self.manager, 'current', 'update'))
        layout.add_widget(update_button)

        delete_button = create_button("Delete Book", (0.8, 0, 0.2, 1), (1, 1, 1, 1))  # red bg, white text
        delete_button.bind(on_press=lambda x: setattr(self.manager, 'current', 'delete'))
        layout.add_widget(delete_button)

        search_button = create_button("Search Book", (1, 0.75, 0.8, 1), (0, 0, 0, 1))
        search_button.bind(on_press=lambda x: setattr(self.manager, 'current', 'search'))
        layout.add_widget(search_button)

        exit_button = create_button("Exit", (0, 0, 0, 1), (1, 0.8, 0.9, 1))  # black bg, pink text
        exit_button.bind(on_press=lambda x: App.get_running_app().stop())
        layout.add_widget(exit_button)

        self.add_widget(layout)

    def go_to_books(self, instance):
        self.manager.current = "book_inventory"

    def exit_app(self, instance):
        App.get_running_app().stop()


class UpdateBookScreen(Screen):
    def __init__(self, **kwargs):
        super(UpdateBookScreen, self).__init__(**kwargs) #update book class constructor

        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        self.book_id_input = TextInput(hint_text="Enter Book ID to update", multiline=False)
        self.new_book_name_input = TextInput(hint_text="Enter New Book Name", multiline=False)
        self.new_book_price_input = TextInput(hint_text="Enter New Book Price", multiline=False)
        self.new_genre_input = TextInput(hint_text="Enter genre", multiline=False)

        save_button = Button(
            text="Save Changes",
            background_color=(0.4, 0.2, 0.6, 1),
            color=(1, 1, 1, 1),
            font_size=20,
            bold=True,
            background_normal='',
            background_down=''
        )
        save_button.bind(on_press=self.save_changes)

        cancel_button = Button(
            text="Cancel",
            background_color=(0, 0, 0, 1),
            color=(1, 0.8, 0.9, 1),
            font_size=20,
            bold=True,
            background_normal='',
            background_down=''
        )
        cancel_button.bind(on_press=self.go_back)

        layout.add_widget(Label(text="Update Book Details", font_size=24))
        layout.add_widget(self.book_id_input)
        layout.add_widget(self.new_book_name_input)
        layout.add_widget(self.new_book_price_input)
        layout.add_widget(self.new_genre_input)
        layout.add_widget(save_button)
        layout.add_widget(cancel_button)

        self.add_widget(layout)

    def save_changes(self, instance):
        from INVENTORY import update_book_details  # import inventory file
        book_id = self.book_id_input.text
        book_name = self.new_book_name_input.text
        book_price = self.new_book_price_input.text
        genre = self.new_genre_input.text

        if book_id:
            update_book_details(
                int(book_id),
                book_name if book_name else None,
                float(book_price) if book_price else None,
                genre if genre else None
            )

        self.manager.current = 'main_menu'  # After saving, go back to main screen

    def go_back(self, instance):
        self.manager.current = 'main_menu'  # Just go back without saving


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

# here is where I create buttons
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

         # Clear fields after adding /trying (success/error
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
                    text=f"[b]{header}[/b]", markup=True, halign="center", valign="middle",
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

class DeleteBookScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        self.book_id_input = TextInput(hint_text='Enter Book ID to Delete', multiline=False)
        layout.add_widget(self.book_id_input)

        delete_button = Button(
            text="Delete Book",
            background_color=(0.8, 0.0, 0.2, 1),  # Cherry Red
            color=(1, 1, 1, 1),
            font_size=20,
            bold=True
        )
        delete_button.bind(on_press=self.delete_selected_book)
        layout.add_widget(delete_button)

        back_button = Button(text="Back to Main Menu")
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.result_label = Label(text='')
        layout.add_widget(self.result_label)

        self.add_widget(layout)

    def delete_selected_book(self, instance):
        book_id = self.book_id_input.text.strip()
        if book_id.isdigit():
            delete_book(int(book_id))
            self.result_label.text = f"Book ID {book_id} deleted successfully."
        else:
            self.result_label.text = "Invalid Book ID. Please enter a valid number."

    def go_back(self, instance):
        self.manager.current = 'main_menu'

#this is for searching
class SearchBookScreen(Screen):
    def __init__(self, **kwargs):
        super(SearchBookScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical', padding=20, spacing=20)

        self.search_input = TextInput(hint_text="Enter Title or Genre to search", multiline=False)
        layout.add_widget(self.search_input)

        search_button = Button(
            text="Search",
            background_color=(1, 0.6, 0.8, 1),  # Soft Pink
            color=(0, 0, 0, 1),
            font_size=20,
            bold=True
        )
        search_button.bind(on_press=self.search_books)
        layout.add_widget(search_button)

        back_button = Button(text="Back to Main Menu", size_hint=(1, 0.3))
        back_button.bind(on_press=self.go_back)
        layout.add_widget(back_button)

        self.result_label = Label(text='')
        layout.add_widget(self.result_label)

        self.add_widget(layout)

    def search_books(self, instance):
        search_text = self.search_input.text.strip()
        if not search_text:
            self.show_popup("No Input", "Please enter a title or genre to search.")
            return

        title_matches = search_book_by_title(search_text)
        genre_matches = search_book_by_genre(search_text)
        results = title_matches + genre_matches

        if results:
            layout = GridLayout(cols=5, spacing=10, size_hint_y=None, padding=[10, 10])
            layout.bind(minimum_height=layout.setter('height'))

            # Add Headers
            headers = ["ID", "Title", "Genre", "Price", "Quantity"]
            for header in headers:
                layout.add_widget(Label(
                    text=f"[b]{header}[/b]", markup=True, halign="center", valign="middle",
                    size_hint_y=None, height=30, text_size=(150, None)
                ))

            # Add Book Details
            for book in results:
                layout.add_widget(
                    Label(text=str(book[0]), halign="center", valign="middle", size_hint_y=None, height=40))
                layout.add_widget(Label(text=book[1], halign="left", valign="middle", size_hint_y=None, height=40,
                                        text_size=(261, None)))
                layout.add_widget(Label(text=book[2], halign="left", valign="middle", size_hint_y=None, height=40,
                                        text_size=(150, None)))
                layout.add_widget(
                    Label(text=str(book[3]), halign="center", valign="middle", size_hint_y=None, height=40))
                layout.add_widget(
                    Label(text=str(book[4]), halign="center", valign="middle", size_hint_y=None, height=40))

            # ScrollView to make it scrollable
            scroll = ScrollView(size_hint=(1, 1))
            scroll.add_widget(layout)

            popup_layout = BoxLayout(orientation='vertical')
            popup_layout.add_widget(scroll)

            close_button = Button(text="Close", size_hint=(1, 0.1))
            popup_layout.add_widget(close_button)

            popup = Popup(title="Search Results", content=popup_layout,
                          size_hint=(0.95, 0.9))
            close_button.bind(on_press=popup.dismiss)
            popup.open()

        else:
            self.show_popup("No Results", "No matching books found.")

    def show_popup(self, title, message):
        popup_content = BoxLayout(orientation='vertical', padding=50, spacing=50)
        popup_content.add_widget(Label(text=message))

        close_button = Button(text="Close", size_hint=(1, 0.2))
        popup_content.add_widget(close_button)

        popup = Popup(title=title, content=popup_content, size_hint=(0.9, 0.4))
        close_button.bind(on_press=popup.dismiss)
        popup.open()

    def go_back(self, instance):
        self.manager.current = 'main_menu'


class InventoryApp(App):
    def build(self):
        root = BoxLayout(orientation='vertical')

        # Add gradient background first
        bg = GradientBackground()
        root.add_widget(bg)

        self.sm = ScreenManager()
        self.sm.add_widget(MainMenu(name="main_menu"))
        self.sm.add_widget(BookInventoryScreen(name="book_inventory"))
        self.sm.add_widget(UpdateBookScreen(name='update'))
        self.sm.add_widget(DeleteBookScreen(name="delete"))
        self.sm.add_widget(SearchBookScreen(name="search"))

        screen_layout = BoxLayout(orientation='vertical')
        screen_layout.add_widget(self.sm)

        root.add_widget(screen_layout)

        return root

if __name__ == '__main__':
    InventoryApp().run()
