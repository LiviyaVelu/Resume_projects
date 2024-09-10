import tkinter as tk
from tkinter import messagebox
import mysql.connector
from datetime import date

# Establishing connection to the database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Livi@1908",
    database="library_db"
)

cursor = db.cursor()

# Function to add a new book
def add_book():
    title = title_entry.get()
    author = author_entry.get()
    if title and author:
        cursor.execute("INSERT INTO books (title, author) VALUES (%s, %s)", (title, author))
        db.commit()
        messagebox.showinfo("Success", "Book added successfully")
        title_entry.delete(0, tk.END)
        author_entry.delete(0, tk.END)
        display_books()
    else:
        messagebox.showwarning("Input Error", "Please fill all fields")

# Function to display all books
def display_books():
    cursor.execute("SELECT * FROM books")
    rows = cursor.fetchall()
    listbox.delete(0, tk.END)
    for row in rows:
        listbox.insert(tk.END, f"ID: {row[0]} | Title: {row[1]} | Author: {row[2]} | Status: {row[3]}")

# Function to search for a book by title
def search_book():
    search_title = search_entry.get()
    cursor.execute("SELECT * FROM books WHERE title LIKE %s", (f"%{search_title}%",))
    rows = cursor.fetchall()
    listbox.delete(0, tk.END)
    for row in rows:
        listbox.insert(tk.END, f"ID: {row[0]} | Title: {row[1]} | Author: {row[2]} | Status: {row[3]}")

# Function to add a new user
def add_user():
    name = name_entry.get()
    email = email_entry.get()
    if name and email:
        cursor.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
        db.commit()
        messagebox.showinfo("Success", "User added successfully")
        name_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)
    else:
        messagebox.showwarning("Input Error", "Please fill all fields")

# Function to issue a book to a user
def issue_book():
    book_id = int(issue_book_entry.get())
    user_id = int(issue_user_entry.get())

    cursor.execute("SELECT status FROM books WHERE book_id = %s", (book_id,))
    status = cursor.fetchone()[0]

    if status == "Available":
        issue_date = date.today()
        cursor.execute("INSERT INTO transactions (book_id, user_id, issue_date, status) VALUES (%s, %s, %s, %s)", 
                       (book_id, user_id, issue_date, "Issued"))
        cursor.execute("UPDATE books SET status = 'Issued' WHERE book_id = %s", (book_id,))
        db.commit()
        messagebox.showinfo("Success", "Book issued successfully")
    else:
        messagebox.showwarning("Error", "Book is not available")

# Function to return a book
def return_book():
    book_id = int(return_book_entry.get())
    cursor.execute("SELECT issue_date FROM transactions WHERE book_id = %s AND status = 'Issued'", (book_id,))
    issue_date = cursor.fetchone()[0]
    return_date = date.today()
    days_diff = (return_date - issue_date).days
    fine = 0
    if days_diff > 15:
        fine = (days_diff - 15) * 2

    cursor.execute("UPDATE transactions SET return_date = %s, fine = %s, status = 'Returned' WHERE book_id = %s AND status = 'Issued'", 
                   (return_date, fine, book_id))
    cursor.execute("UPDATE books SET status = 'Available' WHERE book_id = %s", (book_id,))
    db.commit()

    if fine > 0:
        messagebox.showinfo("Returned with Fine", f"Book returned with fine of ${fine}")
    else:
        messagebox.showinfo("Success", "Book returned successfully")

# Setting up the main Tkinter window
root = tk.Tk()
root.title("Library Management System")

# Setting window size to fit laptop display
root.geometry("800x600")

# Adding book section
tk.Label(root, text="Add a Book").grid(row=0, column=0, columnspan=2, pady=10)
tk.Label(root, text="Title:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
title_entry = tk.Entry(root)
title_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Author:").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
author_entry = tk.Entry(root)
author_entry.grid(row=2, column=1, padx=10, pady=5)

add_book_button = tk.Button(root, text="Add Book", command=add_book)
add_book_button.grid(row=3, column=0, columnspan=2, pady=10)

# Adding user section
tk.Label(root, text="Add a User").grid(row=4, column=0, columnspan=2, pady=10)
tk.Label(root, text="Name:").grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
name_entry = tk.Entry(root)
name_entry.grid(row=5, column=1, padx=10, pady=5)

tk.Label(root, text="Email:").grid(row=6, column=0, padx=10, pady=5, sticky=tk.W)
email_entry = tk.Entry(root)
email_entry.grid(row=6, column=1, padx=10, pady=5)

add_user_button = tk.Button(root, text="Add User", command=add_user)
add_user_button.grid(row=7, column=0, columnspan=2, pady=10)

# Book display section
tk.Label(root, text="Available Books").grid(row=8, column=0, columnspan=2, pady=10)
listbox = tk.Listbox(root, width=80, height=10)
listbox.grid(row=9, column=0, columnspan=2, padx=10, pady=10)

# Search book section
tk.Label(root, text="Search Book by Title:").grid(row=10, column=0, padx=10, pady=5, sticky=tk.W)
search_entry = tk.Entry(root)
search_entry.grid(row=10, column=1, padx=10, pady=5)

search_button = tk.Button(root, text="Search Book", command=search_book)
search_button.grid(row=11, column=0, columnspan=2, pady=10)

# Issue book section
tk.Label(root, text="Issue Book").grid(row=12, column=0, columnspan=2, pady=10)
tk.Label(root, text="Book ID:").grid(row=13, column=0, padx=10, pady=5, sticky=tk.W)
issue_book_entry = tk.Entry(root)
issue_book_entry.grid(row=13, column=1, padx=10, pady=5)

tk.Label(root, text="User ID:").grid(row=14, column=0, padx=10, pady=5, sticky=tk.W)
issue_user_entry = tk.Entry(root)
issue_user_entry.grid(row=14, column=1, padx=10, pady=5)

issue_book_button = tk.Button(root, text="Issue Book", command=issue_book)
issue_book_button.grid(row=15, column=0, columnspan=2, pady=10)

# Return book section
tk.Label(root, text="Return Book").grid(row=16, column=0, columnspan=2, pady=10)
tk.Label(root, text="Book ID:").grid(row=17, column=0, padx=10, pady=5, sticky=tk.W)
return_book_entry = tk.Entry(root)
return_book_entry.grid(row=17, column=1, padx=10, pady=5)

return_book_button = tk.Button(root, text="Return Book", command=return_book)
return_book_button.grid(row=18, column=0, columnspan=2, pady=10)

# Initial display of available books
display_books()

root.mainloop()
