import tkinter as tk
from tkinter import ttk, messagebox
from stock_managment import stock_management_dashboard
from account_managment import on_account_creation, on_login
from store_management import store_management_dashboard

class SystemHub(tk.Tk):
    def __init__(self, username):
        super().__init__()
        self.title = 'Home'
        self.geometry('1225x500')

        # Initially show the home page
        self.login_page(username)

    def clear_window(self):
        """Clear all widgets in the window."""
        for widget in self.winfo_children():
            widget.destroy()

    def show_home(self, username):
        self.clear_window()
        # Create a menu bar
        menu_bar = tk.Menu(self)

        # create the File menu and add an item
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label='Stock', command=lambda: stock_management_dashboard(self, username))
        menu_bar.add_cascade(label='Functions', menu=file_menu)

        self.config(menu=menu_bar)

        # Creating the frame for other widgets
        controls_frame = tk.Frame(self, width=300, height=300)
        controls_frame.grid(row=0, column=0)

        # Creating a temp label displaying the users name
        # home_label = tk.Label(sales_frame, text=username, font=('Arial', 40))
        # home_label.grid(row=0, column=1)

        # Go Stock Page
        stock_page_button = ttk.Button(controls_frame, text="Stock Data", command=lambda: stock_management_dashboard(self, username))
        stock_page_button.grid(row=0, column=0, padx=5, pady=5)

        # Store - Used to test stock graph interaction
        store_page_button = ttk.Button(controls_frame, text="Store", command=lambda: store_management_dashboard(self, username))
        store_page_button.grid(row=1, column=0, padx=5, pady=5)

        # Return to Login page
        back_to_login_page_button = tk.Button(controls_frame, text="Back to Login", command=lambda: self.login_page(username))
        back_to_login_page_button.grid(row=2, column=0, padx=5, pady=5)

    def login_page(self, username):
        self.clear_window()

        username_label = ttk.Label(self, text='Username')
        username_entry = ttk.Entry(self)
        password_label = ttk.Label(self, text='Password')
        password_entry = ttk.Entry(self, show='*')
        account_creation_button = ttk.Button(self, text='Create Account',
                                             command=lambda: on_account_creation(username_entry, password_entry))
        login_button = ttk.Button(self, text='LogIn',
                                  command=lambda: on_login(username_entry, password_entry, self))

        username_label.grid(column=0, row=0, padx=5, pady=5)
        username_entry.grid(column=1, row=0, padx=5, pady=5)
        password_label.grid(column=0, row=1, padx=5, pady=5)
        password_entry.grid(column=1, row=1, padx=5, pady=5)
        account_creation_button.grid(column=0, row=2, columnspan=2, padx=5, pady=2, sticky='ew')
        login_button.grid(column=0, row=3, columnspan=2, padx=5, pady=2, sticky='ew')


def SystemHub_runtime(username):
    app = SystemHub(username)
    app.mainloop()


if __name__ == '__main__':
    # The username in this example is for test purposes
    username = 'root'
    app = SystemHub(username)
    app.mainloop()
