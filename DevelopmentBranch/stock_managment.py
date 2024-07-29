import tkinter as tk
import webbrowser
from tkinter import ttk, messagebox
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
import sqlite3
import datetime

current_canvas = None

url = "http://localhost:63342/ERP/DevelopmentBranch/webDashboardStockCentre.html?_ijt=dondhqa48ugujgf1q9kj8te80q&_ij_reload=RELOAD_ON_SAVE"

def on_update_graph_data(stock_entry, reorder_level_entry, username, graph_frame):
    # Connect to the SQLite database
    conn = sqlite3.connect('erp_system.db')

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    new_stock_level = stock_entry.get()
    new_reorder_level = reorder_level_entry.get()
    current_date = datetime.datetime.now().strftime("%d-%m-%y")

    if new_stock_level.strip() != "":
        # Defining the update statement - Stock history
        insert_stock_history = """
        INSERT INTO stock_history(username, date, stock)
        VALUES (?, ?, ?)
        """

        cursor.execute(insert_stock_history, (username, current_date, new_stock_level))

    if new_reorder_level.strip() != "":
        # Defining the update statements
        reorder_level_update_statement = """
        UPDATE users
        SET reorder_level = ?
        WHERE username = ?
        """

        # Execute the updates with the new reorder level and username
        cursor.execute(reorder_level_update_statement, (new_reorder_level, username))

    # Commit the changes
    conn.commit()

    # Close the connection
    conn.close()

    load_graph_data(username, graph_frame, reorder_level_entry)


def load_graph_data(username: str, graph_frame, reorder_level_entry):
    # Connect to the SQLite database
    conn = sqlite3.connect('erp_system.db')

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Fetch the reorder level from users table
    cursor.execute("SELECT reorder_level FROM users WHERE username = ?", (username,))
    reorder_level = cursor.fetchone()[0]

    # Fetch stock history data
    cursor.execute("SELECT date, stock FROM stock_history WHERE username = ?", (username,))
    stock_data = cursor.fetchall()

    # Close the connection
    conn.close()

    # Prepare data for the graph
    # MAKE SURE I UNDERSTAND THIS FUNCTION
    dates = [datetime.datetime.strptime(row[0], "%d-%m-%y") for row in stock_data]
    stock_values = [row[1] for row in stock_data]

    # Insert the reorder level into the entry
    reorder_level_entry.delete(0, tk.END)
    reorder_level_entry.insert(0, reorder_level)

    # use this data within the graphs generation
    stock_graph_generator(dates, stock_values, reorder_level, graph_frame)


def stock_graph_generator(dates: list, stock_values: list, reorder_level: int, graph_frame):
    global current_canvas

    # Plots the graph
    fig, ax = plt.subplots()
    ax.plot(dates, stock_values, label="Stock Level")
    ax.axhline(y=reorder_level, color='r', linestyle='--', label='Reorder Level')

    # Format the date on the x-axis
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%y'))
    fig.autofmt_xdate()  # Rotate date labels

    # Adding the labels
    ax.set_xlabel("Time (Date)")
    ax.set_ylabel("Stock (units)")
    ax.legend()

    # Clear the old canvas if it exists
    if current_canvas is not None:
        current_canvas.get_tk_widget().destroy()

    # Drawing the canvas
    current_canvas = FigureCanvasTkAgg(fig, graph_frame)
    current_canvas.draw()
    current_canvas.get_tk_widget().grid(row=0, column=0)

    # Every time the graph is generated, the image will be updated
    # This image is used within webDashboard.html - the ERP website.
    plt.savefig('plot.png')


def clear_window(self):
    """Clear all widgets in the window."""
    for widget in self.winfo_children():
        widget.destroy()

def on_web_dashboard():
    webbrowser.open(url)

def stock_management_dashboard(self, username):
    self.clear_window()

    # All other frames are kept within this
    dashboard_frame = tk.Frame(self)
    dashboard_frame.grid(row=0, column=0)

    # Control Frame for stock
    control_frame = tk.Frame(dashboard_frame)
    control_frame.grid(row=0, column=0, padx=5, pady=5)

    # Graph Frame
    graph_frame = tk.Frame(dashboard_frame)
    graph_frame.grid(row=0, column=1, padx=5, pady=5)

    # Record Frame of changes made - log
    record_frame = tk.Frame(dashboard_frame)
    record_frame.grid(row=0, column=2, padx=5, pady=5)

    # controls ----
    # Stock Entry - Data Entry
    stock_entry_label = tk.Label(control_frame, text="Stock Entry")
    stock_entry_label.grid(row=0, column=0)
    stock_entry = tk.Entry(control_frame)
    stock_entry.grid(row=0, column=1, padx=5, pady=5)

    # Reorder level Entry - Data Entry
    reorder_entry_label = tk.Label(control_frame, text="Reorder Entry")
    reorder_entry_label.grid(row=1, column=0)
    reorder_level_entry = tk.Entry(control_frame)
    reorder_level_entry.grid(row=1, column=1, padx=5, pady=5)

    # Collects data for graph generation
    submit_button = tk.Button(control_frame, text="Submit",
                              command=lambda: on_update_graph_data(stock_entry, reorder_level_entry, username,
                                                                   graph_frame))
    submit_button.grid(row=2, column=0, padx=5, pady=5)

    button = tk.Button(control_frame, text="Go to Home Page", command=lambda: self.show_home(username))
    button.grid(row=3, column=0, padx=5, pady=5)

    # Loads up the Webpage
    web_dashboard_button = tk.Button(control_frame, text="Web Dashboard", command=on_web_dashboard)
    web_dashboard_button.grid(row=4, column=0, padx=5, pady=5)

    # graph
    reference_graph = tk.Label(graph_frame, text="Reference Graph")
    reference_graph.grid(row=0, column=0)

    # Fetches the data from the database
    load_graph_data(username, graph_frame, reorder_level_entry)

    # records
    reference_record = tk.Label(record_frame, text="Reference Record")
    reference_record.grid(row=0, column=0)
