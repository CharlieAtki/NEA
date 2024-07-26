import tkinter as tk
from tkinter import ttk, messagebox
# This is the sales page - where the sales are displayed.
from sale import sale_main_page


def main_page(username, password):
    window = tk.Tk()
    window.title('Home')
    window.geometry('500x450')

    # Create a menu bar
    menu_bar = tk.Menu(window)

    # create the File menu and add an item
    file_menu = tk.Menu(menu_bar, tearoff=0)
    file_menu.add_command(label='Sales', command=lambda: sale_main_page(username, password))
    menu_bar.add_cascade(label='Functions', menu=file_menu)

    window.config(menu=menu_bar)

    # Creating the frame for other widgets
    sales_frame = tk.Frame(window, width=300, height=300)
    sales_frame.grid(row=0, column=0)

    # Creating a temp label displaying the users name
    home_label = tk.Label(sales_frame, text=username, font=('Arial', 40))
    home_label.grid(row=0, column=1)

    sale_page_button = ttk.Button(sales_frame, text="Sales Data", command=lambda: sale_main_page(username, password))
    sale_page_button.grid(row=0, column=2)

    window.mainloop()


