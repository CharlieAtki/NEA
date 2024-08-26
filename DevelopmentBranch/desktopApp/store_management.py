import tkinter as tk
import sqlite3
import datetime
from tkinter import messagebox


def fetch_stock_records(username: str):
    conn = sqlite3.connect('../database/erp_system.db')

    cursor = conn.cursor()

    cursor.execute("SELECT date, stock FROM stock_history WHERE username = ?", (username,))

    stock_record = cursor.fetchall()

    conn.close()

    if stock_record:
        latest_stock_record = stock_record[len(stock_record) - 1]
        return latest_stock_record[1]
    else:
        return 0

def on_purchase(username: str, purchase_number_entry: tk.Entry):

    try:
        purchase_number = int(purchase_number_entry.get())
        if purchase_number < 0:
            messagebox.showwarning(title='Warning', message='Purchase number must be positive')
            return

        stock_level = int(fetch_stock_records(username))
        if purchase_number > stock_level:
            messagebox.showerror("Stock Error", "Not enough stock available.")
            return

        stock_level -= purchase_number
        current_date = datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S")

        # Connect to the SQLite database
        conn = sqlite3.connect('../database/erp_system.db')
        # Create a cursor object to interact with the database
        cursor = conn.cursor()

        # Defining the update statement - Stock history
        insert_stock_history = """
            INSERT INTO stock_history(username, date, stock)
            VALUES (?, ?, ?)
            """

        cursor.execute(insert_stock_history, (username, current_date, stock_level))
        conn.commit()
        conn.close()

        messagebox.showinfo("success", f"Purchase of {purchase_number} items has been made.")
    except ValueError:
        messagebox.showwarning("Input Error", 'Please enter a valid number.')
    except Exception as e:
        messagebox.showwarning("Database Error", f"An Error occurred: {e}")

def clear_window(self):
    """Clear all widgets in the window."""
    for widget in self.winfo_children():
        widget.destroy()

def store_management_dashboard(self, username):
    self.clear_window()

    # Dashboard Frame
    dashboard_frame = tk.Frame(self)
    dashboard_frame.grid(row=0, column=0)

    # Title Frame
    dashboard_title_frame = tk.Frame(dashboard_frame)
    dashboard_title_frame.grid(row=0, column=0)

    # Control Frame
    control_frame = tk.Frame(dashboard_frame)
    control_frame.grid(row=1, column=0)

    # title frame widgets
    # Store title
    dashboard_title_label = tk.Label(dashboard_title_frame, text="Store!")
    dashboard_title_label.grid(row=0, column=0)

    # Control Frame Widgets
    purchase_number_label = tk.Label(control_frame, text="Num of Purchases:")
    purchase_number_label.grid(row=0, column=0)

    purchase_number_entry = tk.Entry(control_frame)
    purchase_number_entry.grid(row=0, column=1)

    # Purchase a good
    submit_purchase_button = tk.Button(control_frame, text="Purchase", command=lambda: on_purchase(username, purchase_number_entry))
    submit_purchase_button.grid(row=1, column=0, padx=5, pady=5)

    # Back home button
    back_to_home_page_button = tk.Button(control_frame, text="Go to Home Page",
                                         command=lambda: self.show_home(username))
    back_to_home_page_button.grid(row=2, column=0, padx=5, pady=5)
