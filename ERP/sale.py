import tkinter as tk
import webbrowser
from tkinter import ttk, messagebox
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import ast

# Global variable to hold the canvas
current_canvas = None

# Global variables to hold the stock level
# These values are for reference during development
x = [1]
y = [0]

url = "http://localhost:63342/NEA/ERP/webDashboardStockCentre.html?_ijt=f1ln5hsftks9671o2jo68qr6ns&_ij_reload=RELOAD_ON_SAVE"


def load_data(username, password, x, y):
    account_details = [username, password]
    try:
        # This takes the values stored within the file to be loaded into the graph
        with open("account_database.txt", "r") as f:
            for line in f:
                stored_account_details = ast.literal_eval(line.strip())
                # This checks that account details are equal to the details within the line
                # [:x] is e method of extracting multiple index values - Head to tail
                # This example - [:2] - would take the username and password
                if account_details == stored_account_details[:2]:
                    temp_x = stored_account_details[2]
                    temp_y = stored_account_details[3]
                    # isinstance is checking whether temp_x and temp_y are lists (if it is true)
                    if isinstance(temp_x, list) and isinstance(temp_y, list):
                        # .clear removes all the values already stored within x and y
                        x.clear()
                        y.clear()
                        # extend adds multiple values to the list
                        x.extend(temp_x)
                        y.extend(temp_y)

                        # Takes the reorder level already set
                        reorder_level = stored_account_details[4]

                        print("Values returned")
                        return reorder_level
                    else:
                        print("Invalid data format in the database")
                        return None

    except FileNotFoundError:
        print("Data not found for the user.")
        return None


def save_data(username, password, reorder_level_entry, x, y):
    reorder_level = reorder_level_entry.get()
    graph_data = [username, password, x, y, reorder_level]
    updated = True
    lines = []

    try:
        with open("account_database.txt", "r") as f:
            for line in f:
                graph_data_string = ast.literal_eval(line.strip())
                # Making sure the correct account data is modified
                # This called slicing index
                if graph_data[:2] == graph_data_string[:2]:
                    # If correct account, append the original data
                    lines.append(str(graph_data) + '\n')
                    updated = True
                else:
                    # If not the correct account, append the original data
                    lines.append(line)

        if updated:
            # If the correct account is found, update the lines
            with open("account_database.txt", "w") as f:
                f.writelines(lines)
                print("Data updated successfully")
        else:
            # If the incorrect account is found, keep the same lines
            with open("account_database.txt", "a") as f:
                f.write(str(graph_data) + '\n')
                print("New data updated successfully")

    except FileNotFoundError:
        # if no account found, assume there is no duplicates - write anyway
        with open("account_database.txt", "w") as f:
            f.write(str(graph_data) + '\n')
            print("Data saved successfully")


def stack():
    global x, y
    # When the length of list x is greater than 12, it wil remove index[0] data from x and y
    while len(x) > 12:
        x.pop(0)
        y.pop(0)


def stock_adjustment(y_stock_entry):
    try:
        y_stock = float(y_stock_entry.get())
        return y_stock
    except ValueError:
        return None


def reorder_level_adjustment(reorder_level_entry, username, password):
    account_details = [username, password]

    try:
        # Convert the reorder level from string to float
        # If reorder_level has an input - change that element on the graph
        reorder_level = float(reorder_level_entry.get())
        return reorder_level
    except ValueError:
        # if nothing has been input into the reorder level entry
        with open("account_database.txt", "r") as f:
            for line in f:
                # finding the correct account details
                stored_account_details = ast.literal_eval(line.strip())
                if account_details[:2] == stored_account_details[:2]:
                    reorder_level = str(stored_account_details[4])
                    return reorder_level
                else:
                    return None


def graph_generation(stock_frame, reorder_level_entry, y_stock_entry, username, password):
    # Declare the global variable
    global current_canvas, x, y

    # Clear any existing plots
    plt.clf()

    # Checking to see if stock has been added
    y_stock = stock_adjustment(y_stock_entry)
    reorder_level = reorder_level_adjustment(reorder_level_entry, username, password)

    # Add new stock if valid
    if y_stock is not None:
        y.append(y_stock)
        # increment the last value of x by one for the new day
        x.append(x[-1] + 1)
        stack()

    # Plots the graph
    fig, ax = plt.subplots()
    ax.plot(x, y, label="Sales")

    # Add new_reorder level if valid
    if reorder_level is not None:
        ax.plot(x, [reorder_level] * len(x), linestyle='--', color='red', label="Reorder Level")

    # Adding the labels
    ax.set_xlabel("Time (Days)")
    ax.set_ylabel("Stock (units)")
    ax.legend()

    # Clear the old canvas if it exists
    if current_canvas is not None:
        current_canvas.get_tk_widget().destroy()

    # Drawing the canvas
    canvas = FigureCanvasTkAgg(fig, stock_frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=0, column=0)

    # Every time the graph is generated, the image will be updated
    # This image is used within webDashboard.html - the ERP website.
    plt.savefig('plot.png')


def on_web_dashboard():
    webbrowser.open(url)


def sale_main_page(username, password):
    account_details = account_details = [username, password]
    window = tk.Tk()
    window.title('Sale Centre')
    window.geometry('1225x500')

    # Creating the controls for the graph
    control_frame = tk.Frame(window)
    control_frame.grid(row=0, column=0, padx=10, pady=10)

    # This is where the sales graph will go within the GUI
    stock_frame = tk.Frame(window, width=300, height=300)
    stock_frame.grid(row=0, column=1)

    # This is where the record of changes will be displayed
    record_frame = tk.Frame(window)
    record_frame.grid(row=0, column=2)

    # Creating the UI to add stock levels
    y_stock_button = tk.Button(control_frame, text="Stock level",
                               command=lambda: graph_generation(stock_frame, reorder_level_entry, y_stock_entry,
                                                                username, password))
    y_stock_entry = tk.Entry(control_frame)

    y_stock_button.grid(row=0, column=0)
    y_stock_entry.grid(row=0, column=1)

    # This takes the re-order level the business would like to set
    # lambda is being used as there is more than 2 parameters being passed
    reorder_level_entry = tk.Entry(control_frame)
    reorder_level_button = tk.Button(control_frame, text='Reorder Level',
                                     command=lambda: graph_generation(stock_frame, reorder_level_entry, y_stock_entry,
                                                                      username, password))

    save_data_button = tk.Button(control_frame, text="Save Data",
                                 command=lambda: save_data(username, password, reorder_level_entry, x, y))

    # Loads up the Webpage
    web_dashboard_button = tk.Button(control_frame, text="Web Dashboard", command=on_web_dashboard)

    # Place of widgets within the control frame
    reorder_level_button.grid(row=1, column=0)
    reorder_level_entry.grid(row=1, column=1, padx=5, pady=5)
    save_data_button.grid(row=2, column=0, padx=5, pady=5)
    web_dashboard_button.grid(row=3, column=0, padx=5, pady=10)

    # Creating the record widgets
    record_label = tk.Label(record_frame, text="Stock record")

    # Placement of widgets
    record_label.grid(row=0, column=0, padx=10, pady=5)

    # This loads the data from past graph use - ensures this code is only ran once
    # This code is ran before the graph is generated
    runtime = 1
    while runtime == 1:
        runtime -= 1
        reorder_level = load_data(username, password, x, y)
        reorder_level_entry.insert(0, reorder_level)

    # This is calling the graph generation function
    # Ensures that a graph has been generated when ui is initially loaded
    graph_generation(stock_frame, reorder_level_entry, y_stock_entry, username, password)

    window.mainloop()
