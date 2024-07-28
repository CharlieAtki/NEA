import tkinter as tk
import webbrowser
from tkinter import ttk, messagebox
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import bcrypt
import sqlite3

current_canvas = None

def load_graph_data(username: str, graph_frame):
    # Connect to the SQLite database
    conn = sqlite3.connect('erp_system.db')

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))

    # Fetches the next row of the result set.
    # Appending the data to a list
    result = cursor.fetchone()
    result_list = [result]

    print(result_list)
    # Separating the values used within the graph
    days: int = result_list[0][3]
    stock: int = result_list[0][4]
    reorder_level: int = result_list[0][5]
    print(days, stock, reorder_level)

    # use this data within the graphs generation......
    stock_graph_generator(days, stock, reorder_level, graph_frame)

def stock_graph_generator(days: int, stock: int, reorder_level: int, graph_frame):
    global current_canvas

    # Plots the graph
    fig, ax = plt.subplots()
    ax.plot(days, stock, label="Sales")

    # Adding the labels
    ax.set_xlabel("Time (Days)")
    ax.set_ylabel("Stock (units)")
    ax.legend()

    # Clear the old canvas if it exists
    if current_canvas is not None:
        current_canvas.get_tk_widget().destroy()

    # Drawing the canvas
    canvas = FigureCanvasTkAgg(fig, graph_frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0)

    # Every time the graph is generated, the image will be updated
    # This image is used within webDashboard.html - the ERP website.
    plt.savefig('plot.png')

def clear_window(self):
    """Clear all widgets in the window."""
    for widget in self.winfo_children():
        widget.destroy()

def stock_management_dashboard(self, username):
    self.clear_window()

    # All other frames are kept within this
    dashboard_frame = tk.Frame(self)
    dashboard_frame.grid(row=0, column=0)

    # Control for stock
    control_frame = tk.Frame(dashboard_frame)
    control_frame.grid(row=0, column=0, padx=5, pady=5)

    # Graph
    graph_frame = tk.Frame(dashboard_frame)
    graph_frame.grid(row=0, column=1, padx=5, pady=5)

    # Record of changes made - log
    record_frame = tk.Frame(dashboard_frame)
    record_frame.grid(row=0, column=2, padx=5, pady=5)

    # controls ----
    reference_control = tk.Label(control_frame, text='Reference controls')
    reference_control.grid(row=0, column=0)

    button = tk.Button(control_frame, text="Go to Home Page", command=lambda: self.show_home(username))
    button.grid(row=1, column=0, padx=5, pady=5)

    # graph
    reference_graph = tk.Label(graph_frame, text="Reference Graph")
    reference_graph.grid(row=0, column=0)

    # Fetches the data from the database
    load_graph_data(username, graph_frame)

    # records
    reference_record = tk.Label(record_frame, text="Reference Record")
    reference_record.grid(row=0, column=0)



