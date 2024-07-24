import tkinter as tk
from tkinter import ttk, messagebox
from home import main_page
import ast

window = tk.Tk()
window.title('LogIn')
window.geometry('280x140')

# add  bubble sort to the list


def on_account_creation(user_name_entry, password_entry):
    username = user_name_entry.get()
    password = password_entry.get()
    account_details = [username, password, 1, 0, 0]
    account_creation = True

    if password and username != "":
        with open("account_database.txt", 'r') as f:
            for line in f:
                stored_account_details = ast.literal_eval(line.strip())
                if account_details[:2] == stored_account_details[:2]:
                    account_creation = False
                    break

        if account_creation:
            with open("account_database.txt", 'a') as f:
                f.write(str(account_details) + '\n')
        else:
            messagebox.showerror(title='Error', message='Invalid Account Details')
    else:
        messagebox.showerror(title='Error', message='Please Enter Username and Password')


def on_login(user_name_entry, password_entry):
    username = user_name_entry.get()
    password = password_entry.get()
    account_details = [username, password]
    account_login = False

    with open("account_database.txt", 'r') as f:
        for line in f:
            stored_account_details = ast.literal_eval(line.strip())
            if account_details[0] == stored_account_details[0] and account_details[1] == stored_account_details[1]:
                account_login = True
                break

    if account_login:
        # Load the second page
        main_page(username, password)
    else:
        messagebox.showerror(title='Login', message='Invalid Account Details')


user_name_label = ttk.Label(window, text='Username')
user_name_entry = ttk.Entry(window)
password_label = ttk.Label(window, text='Password')
password_entry = ttk.Entry(window, show='*')
account_creation_button = ttk.Button(window, text='Create Account',
                                     command=lambda: on_account_creation(user_name_entry, password_entry))
login_button = ttk.Button(window, text='LogIn',
                          command=lambda: on_login(user_name_entry, password_entry))

user_name_label.grid(column=0, row=0, padx=5, pady=5)
user_name_entry.grid(column=1, row=0, padx=5, pady=5)
password_label.grid(column=0, row=1, padx=5, pady=5)
password_entry.grid(column=1, row=1, padx=5, pady=5)
account_creation_button.grid(column=0, row=2, columnspan=2, padx=5, pady=2, sticky='ew')
login_button.grid(column=0, row=3, columnspan=2, padx=5, pady=2, sticky='ew')

window.mainloop()
