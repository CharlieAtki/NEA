import sqlite3
import tkinter as tk
import bcrypt
from tkinter import ttk, messagebox

def password_check(username: str, password: str) -> bool:
    # pull the password from the database - check it matched the input password
    # Connect to the SQLite database
    conn = sqlite3.connect('erp_system.db')

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # Checks that the password stored in the database matches the input password
        cursor.execute("SELECT password_hash FROM users WHERE username = ?", (username,))

        # Fetches the next row of the result set. If there are no more rows, it returns None.
        result = cursor.fetchone()

        # if the row can be found
        if result:
            # assigning the password value
            stored_password_hash = (result[0])
            # if the stored password and input password are equal
            if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash.encode('utf-8')):
                return True
            else:
                messagebox.showerror("Error", "Password incorrect")
                return False
        else:
            return False
    except sqlite3.Error as e:
        messagebox.showinfo("Error", f"An Error Occurred: {e}")
        return False
    finally:
        conn.close()


# This function
def data_integrity(username: str) -> bool:
    # Connect to the SQLite database
    conn = sqlite3.connect('erp_system.db')

    # Create a cursor object to interact with the database
    cursor = conn.cursor()

    try:
        # 1 is the same as username, taking the colum
        cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))

        # checks whether the row matches my query conditions.
        # If the username exists in the database a row will return True
        # If the name does not exist, False will be returned.
        exists: bool = cursor.fetchone() is not None

        if exists:
            return False
        else:
            return True
    # If an error occurs, print the error and return false - don't create the account
    except Exception as e:
        messagebox.showinfo("Error", f"An Error Occurred: {e}")
        return False
    # Once all conditions are met, close the database
    finally:
        conn.close()


def on_account_creation(username_entry, password_entry, reorder_level):
    # All data used within the database
    username: str = username_entry.get().strip()
    password: str = password_entry.get().strip()

    if data_integrity(username):
        try:
            # Connect to the SQLite database
            conn = sqlite3.connect('erp_system.db')
            # Create a cursor object to interact with the database
            cursor = conn.cursor()

            # Hash the password
            # Make sure to check how the program interacts with the database
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            # Create the users table if it doesn't exist
            cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password_hash TEXT NOT NULL,
                reorder_level INTEGER NOT NULL             
            )
            ''')

            cursor.execute("INSERT INTO users (username, password_hash, reorder_level) VALUES (?, ?, ?)",
                           (username, password_hash, reorder_level))

            # Commit the changes
            conn.commit()

            # Query the database to verify the data was inserted
            # This is for test purposes - remove later
            cursor.execute("SELECT * FROM users")
            users = cursor.fetchall()
            print("Users:")
            for user in users:
                print(user)

            # Raised when trying to update a record that violates a uniqueness constraint.
            # Eg, primary key or unique index.
        except sqlite3.IntegrityError:
            # Handle unique constraint violation for username
            messagebox.showwarning("Error", "Username already exists.")
        except Exception as e:
            # Handle other exceptions
            messagebox.showerror("Error", f"An error occurred: {e}")
        finally:
            # Ensure the connection is closed
            conn.close()
    else:
        messagebox.showinfo("Username", "Username is already taken")


def on_login(username_entry, password_entry, self):
    username = username_entry.get()
    password = password_entry.get()

    # If the username is taken
    # and if Password check is True - pass matches the username, login
    if not data_integrity(username) and password_check(username, password):
        try:
            # load the homepage
            self.show_home(username)
        except Exception as e:
            messagebox.showinfo("Error", f"An Error Occurred: {e}")
    elif data_integrity(username):
        messagebox.showinfo("Error", "That username does not exist")