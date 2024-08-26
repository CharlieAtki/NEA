import tkinter as tk
import webbrowser
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.dates import DateFormatter
import sqlite3
import datetime

current_canvas = None

url = "http://localhost:63342/ERP/DevelopmentBranch/webDashboardStockCentre.html?_ijt=dondhqa48ugujgf1q9kj8te80q&_ij_reload=RELOAD_ON_SAVE"

def on_update_graph_data(stock_entry, reorder_level_entry, username, graph_frame, stock_record_frame, graph_data_range_scale):
    # Connect to the SQLite database
    conn = sqlite3.connect('../database/erp_system.db')

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    new_stock_level = stock_entry.get()
    new_reorder_level = reorder_level_entry.get()
    current_date = datetime.datetime.now().strftime("%d-%m-%y %H:%M:%S")

    # The range of data shown on the graph
    graph_data_range_scale = graph_data_range_scale.get()

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

    load_graph_data(username, graph_frame, reorder_level_entry, graph_data_range_scale)

    stock_records = fetch_stock_records(username)
    update_ui_with_stock_records(stock_records, stock_record_frame)


def fetch_stock_records(username: str):
    conn = sqlite3.connect('../database/erp_system.db')

    cursor = conn.cursor()

    cursor.execute("SELECT date, stock FROM stock_history WHERE username = ?", (username,))

    stock_record = cursor.fetchall()

    print(f" Total stock records: {len(stock_record)}")

    # Only includes the 12 most recent stock records - stack
    if len(stock_record) > 12:
        stock_record = stock_record[(len(stock_record) - 12):]
    # Else - there is not yet 12 records

    print(f" Stack: total stock records: {len(stock_record)}")

    conn.close()

    return stock_record

def update_ui_with_stock_records(stock_records, stock_record_frame):
    # Clear previous records
    for widget in stock_record_frame.winfo_children():
        widget.destroy()

    # Flipping the list - so that the newest record is at the top
    stock_records.reverse()

    # Creating a label for each line
    for record in stock_records:
        record_label = tk.Label(stock_record_frame, text=f"Date: {record[0]}, Stock: {record[1]}", font=("Helvetica", 10))
        record_label.pack()

def load_graph_data(username: str, graph_frame, reorder_level_entry, graph_data_range_scale):
    # Connect to the SQLite database
    conn = sqlite3.connect('../database/erp_system.db')

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    # Fetch the reorder level from users table
    cursor.execute("SELECT reorder_level FROM users WHERE username = ?", (username,))
    reorder_level = cursor.fetchone()[0]

    # Fetch stock history data
    cursor.execute("SELECT date, stock FROM stock_history WHERE username = ?", (username,))
    stock_data = cursor.fetchall()

    print(f" before stack: {len(stock_data)}")

    # Only includes the 12 most recent stock records - stack
    if len(stock_data) > graph_data_range_scale:
        stock_data = stock_data[(len(stock_data) - graph_data_range_scale):]
    # Else - there is not yet 12 records

    print(f" After stack: {len(stock_data)}")

    # Close the connection
    conn.close()

    # Sort stock data by date
    stock_data.sort(key=lambda x: datetime.datetime.strptime(x[0], "%d-%m-%y %H:%M:%S"))

    # Prepare data for the graph
    dates = [row[0] for row in stock_data]
    stock_values = [row[1] for row in stock_data]

    # Insert the reorder level into the entry
    reorder_level_entry.delete(0, tk.END)
    reorder_level_entry.insert(0, reorder_level)

    # use this data within the graphs generation
    stock_graph_generator(dates, stock_values, reorder_level, graph_frame)


def stock_graph_generator(dates: list, stock_values: list, reorder_level: int, graph_frame):
    global current_canvas

    # Convert string dates to datetime objects
    dates = [datetime.datetime.strptime(date, "%d-%m-%y %H:%M:%S") for date in dates]

    # Plots the graph
    fig, ax = plt.subplots()
    ax.plot(dates, stock_values, label="Stock Level")
    ax.axhline(y=reorder_level, color='r', linestyle='--', label='Reorder Level')

    # Adding the labels
    ax.set_xlabel("Time (Date)")
    ax.set_ylabel("Stock (units)")
    ax.legend()

    # Formatting the date to show hours and minutes
    ax.xaxis.set_major_formatter(DateFormatter('%d-%m-%y'))
    fig.autofmt_xdate()  # Rotate date labels

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
    username_display_label = tk.Label(control_frame, text=f"User: {username}", font="Helvetica 18 bold", fg="darkblue")
    username_display_label.grid(row=0, column=0, padx=5, pady=50)

    # Stock Entry - Data Entry
    stock_entry_label = tk.Label(control_frame, text="Stock Entry")
    stock_entry_label.grid(row=1, column=0)
    stock_entry = tk.Entry(control_frame)
    stock_entry.grid(row=1, column=1, padx=5, pady=5)

    # Reorder level Entry - Data Entry
    reorder_entry_label = tk.Label(control_frame, text="Reorder Entry")
    reorder_entry_label.grid(row=2, column=0)
    reorder_level_entry = tk.Entry(control_frame)
    reorder_level_entry.grid(row=2, column=1, padx=5, pady=5)

    graph_data_range_label = tk.Label(control_frame, text="Graph Data Range")
    graph_data_range_label.grid(row=3, column=0)
    graph_data_range_scale = tk.Scale(control_frame, from_=12, to=100, orient="horizontal")
    graph_data_range_scale.grid(row=3, column=1, padx=5, pady=5)

    # Collects data for graph generation
    submit_button = tk.Button(control_frame, text="Submit",
                              command=lambda: on_update_graph_data(stock_entry, reorder_level_entry, username,
                                                                   graph_frame, stock_record_frame, graph_data_range_scale))
    submit_button.grid(row=4, column=0, padx=5, pady=5)

    back_to_home_page_button = tk.Button(control_frame, text="Go to Home Page", command=lambda: self.show_home(username))
    back_to_home_page_button.grid(row=5, column=0, padx=5, pady=5)

    # Loads up the Webpage
    web_dashboard_button = tk.Button(control_frame, text="Web Dashboard", command=on_web_dashboard)
    web_dashboard_button.grid(row=6, column=0, padx=5, pady=5)

    # graph
    reference_graph = tk.Label(graph_frame, text="Reference Graph")
    reference_graph.grid(row=0, column=0)

    # Fetches the data from the database
    load_graph_data(username, graph_frame, reorder_level_entry, graph_data_range_scale=12)

    # records
    stock_record_title_label = tk.Label(record_frame, text="Stock Records:", font=("Helvetica", 20))
    stock_record_title_label.grid(row=0, column=0)

    stock_record_description_label = tk.Label(record_frame, text="Latest Stock Addition:\nOrganised from Top to Bottom", font=("Helvetica", 10), fg="darkblue")
    stock_record_description_label.grid(row=1, column=0)

    stock_record_frame = tk.Frame(record_frame)
    stock_record_frame.grid(row=2, column=0, padx=5, pady=5)

    stock_records = fetch_stock_records(username)
    update_ui_with_stock_records(stock_records, stock_record_frame)