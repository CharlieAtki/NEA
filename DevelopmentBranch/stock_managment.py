import tkinter as tk
import webbrowser
from tkinter import ttk, messagebox
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import bcrypt


def clear_window(self):
    """Clear all widgets in the window."""
    for widget in self.winfo_children():
        widget.destroy()

def stock_management_dashboard(self):
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

    button = tk.Button(control_frame, text="Go to Home Page", command=self.show_home)
    button.grid(row=1, column=0, padx=5, pady=5)

    # graph
    reference_graph = tk.Label(graph_frame, text="Reference Graph")
    reference_graph.grid(row=0, column=0)

    # records
    reference_record = tk.Label(record_frame, text="Reference Record")
    reference_record.grid(row=0, column=0)



