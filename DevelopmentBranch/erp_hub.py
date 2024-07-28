import tkinter as tk
from tkinter import ttk, messagebox
from stock_managment import stock_management_dashboard

class SystemHub(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title = 'Home'
        self.geometry('500x500')

        # Initially show the home page
        self.show_home()

    def clear_window(self):
        """Clear all widgets in the window."""
        for widget in self.winfo_children():
            widget.destroy()

    def show_home(self):
        self.clear_window()
        # Create a menu bar
        menu_bar = tk.Menu(self)

        # create the File menu and add an item
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label='Stock', command=lambda: stock_management_dashboard(self))
        menu_bar.add_cascade(label='Functions', menu=file_menu)

        self.config(menu=menu_bar)

        # Creating the frame for other widgets
        sales_frame = tk.Frame(self, width=300, height=300)
        sales_frame.grid(row=0, column=0)

        # Creating a temp label displaying the users name
        # home_label = tk.Label(sales_frame, text=username, font=('Arial', 40))
        # home_label.grid(row=0, column=1)

        sale_page_button = ttk.Button(sales_frame, text="Stock Data", command=lambda: stock_management_dashboard(self))
        sale_page_button.grid(row=0, column=2)


def SystemHub_runtime():
    app = SystemHub()
    app.mainloop()


if __name__ == '__main__':
    app = SystemHub()
    app.mainloop()
