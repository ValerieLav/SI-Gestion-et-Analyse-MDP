
import sys
import os

# Add parent directory to Python search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import json
import tkinter as tk
from tkinter import messagebox, simpledialog
from PIL import Image, ImageTk
from transformers import pipeline
from backend.encryption import encrypt_password, decrypt_password, generate_key
from backend.password_strength import generate_password, is_secure_password, is_password_safe
import sqlite3

# Import functions from password_manager.py
from password_manager import save_password, display_passwords, is_strong_password

# Configure the Hugging Face API
chatbot = pipeline('text-generation', model='microsoft/DialoGPT-medium')

# Initialize the database
def initialize_db():
    db_path = 'passwords.db'
    if os.path.exists(db_path):
        try:
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute('SELECT name FROM sqlite_master WHERE type="table"')
            conn.close()
        except sqlite3.DatabaseError:
            os.remove(db_path)
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS passwords (
                    site TEXT NOT NULL,
                    username TEXT NOT NULL,
                    encrypted_password TEXT NOT NULL,
                    PRIMARY KEY (site, username)
                )
            ''')
            conn.commit()
            conn.close()
    else:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                site TEXT NOT NULL,
                username TEXT NOT NULL,
                encrypted_password TEXT NOT NULL,
                PRIMARY KEY (site, username)
            )
        ''')
        conn.commit()
        conn.close()

# Function to store a password
def store_password(site, username, encrypted_password):
    # Vérifier si encrypted_password est de type bytes
    if isinstance(encrypted_password, bytes):
        encrypted_password = encrypted_password.decode()

    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute('''
        INSERT OR REPLACE INTO passwords (site, username, encrypted_password)
        VALUES (?, ?, ?)
    ''', (site, username, encrypted_password))
    conn.commit()
    conn.close()

# Function to retrieve a password
def retrieve_password(site, username):
    conn = sqlite3.connect('passwords.db')
    c = conn.cursor()
    c.execute('''
        SELECT encrypted_password FROM passwords
        WHERE site = ? AND username = ?
    ''', (site, username))
    result = c.fetchone()
    conn.close()
    if result:
        return result[0]
    return None

# Function to generate a random password
def generate_password_ui():
    password = generate_password()
    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)
    strength = check_password_strength(password)
    strength_label.config(text=f"Strength of password: {strength}")

# Function to check the strength of the password
def check_password_strength(password):
    if is_secure_password(password) and is_password_safe(password):
        return "Strong"
    elif is_secure_password(password):
        return "Medium"
    return "Weak"

# Function to save a password
def save_password_ui():
    site = site_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    if site and username and password:
        if not is_strong_password(password):
            messagebox.showwarning("Error", "Le mot de passe n'est pas assez fort. Veuillez choisir un mot de passe plus fort.")
            return
        encrypted_password = encrypt_password(key, password)
        store_password(site, username, encrypted_password)
        password_listbox.insert(tk.END, f"{site} ({username})")
        messagebox.showinfo("Success", f"Password for {site} saved.")
    else:
        messagebox.showwarning("Error", "Please enter a site, username, and password.")

# Function to search for a password
def search_password():
    site = site_entry.get()
    username = username_entry.get()
    if site and username:
        encrypted_password = retrieve_password(site, username)
        if encrypted_password:
            password = decrypt_password(key, encrypted_password)
            password_entry.delete(0, tk.END)
            password_entry.insert(0, password)
            messagebox.showinfo("Success", f"Password for {site} found.")
        else:
            messagebox.showwarning("Error", f"No password for {site} and {username}.")
    else:
        messagebox.showwarning("Error", "Please enter a site and username.")

# Function to export passwords
def export_passwords():
    file_name = simpledialog.askstring("Export", "Name of the file to export:")
    if file_name:
        conn = sqlite3.connect('passwords.db')
        c = conn.cursor()
        c.execute('SELECT * FROM passwords')
        passwords = c.fetchall()
        conn.close()
        with open(file_name + '.json', 'w') as f:
            json.dump(passwords, f)
        messagebox.showinfo("Success", "Passwords successfully exported.")

# Function to import passwords
def import_passwords():
    file_name = simpledialog.askstring("Import", "Name of the file to import:")
    if file_name:
        try:
            with open(file_name + '.json', 'r') as f:
                imported_passwords = json.load(f)
                conn = sqlite3.connect('passwords.db')
                c = conn.cursor()
                for site, username, encrypted_password in imported_passwords:
                    c.execute('''
                        INSERT OR REPLACE INTO passwords (site, username, encrypted_password)
                        VALUES (?, ?, ?)
                    ''', (site, username, encrypted_password))
                conn.commit()
                conn.close()
                password_listbox.delete(0, tk.END)
                for site, username, _ in imported_passwords:
                    password_listbox.insert(tk.END, f"{site} ({username})")
                messagebox.showinfo("Success", "Passwords successfully imported.")
        except Exception as e:
            messagebox.showerror("Error", f"Error during import: {str(e)}")

# Function to send a message in the chatbox
def send_message():
    message = chat_entry.get()
    if message:
        chatbox.config(state=tk.NORMAL)
        chatbox.insert(tk.END, f"You: {message}\n")
        chatbox.config(state=tk.DISABLED)
        chat_entry.delete(0, tk.END)
        print(f"Sending message: {message}")  # Debug print
        get_ai_response(message)

# Function to get a response from the AI
def get_ai_response(message):
    try:
        response = chatbot(message, max_length=50, num_return_sequences=1, truncation=True)
        ai_message = response[0]['generated_text'].strip()
        print(f"Received AI response: {ai_message}")  # Debug print
        chatbox.config(state=tk.NORMAL)
        chatbox.insert(tk.END, f"AI: {ai_message}\n")
        chatbox.config(state=tk.DISABLED)
        chatbox.see(tk.END)  # Scroll to the end of the chatbox
    except Exception as e:
        print(f"Error: {e}")  # Debug print
        messagebox.showerror("Error", f"Failed to get response from AI: {e}")

# Load or generate the encryption key
key_filename = "secret.key"
if os.path.exists(key_filename):
    with open(key_filename, 'rb') as f:
        key = f.read()
else:
    key = generate_key()
    with open(key_filename, 'wb') as f:
        f.write(key)

# Initialize the database
initialize_db()

# Create the main window
root = tk.Tk()
root.title("Intelligent Password Management and Analysis System")
root.geometry("800x600")

# Load the background image
background_image_path = os.path.join(os.path.dirname(__file__), '..', 'assets', 'background.jpg')
background_image = Image.open(background_image_path)
background_photo = ImageTk.PhotoImage(background_image)

# Create a label for the background image
background_label = tk.Label(root, image=background_photo)
background_label.place(relwidth=1, relheight=1)

# Create a frame for the widgets
frame = tk.Frame(root, bg='#80c1ff', bd=3)
frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

# Entry field for the site
site_entry = tk.Entry(frame, font=('Oswald', 12))
site_entry.place(relwidth=0.2, relheight=1)
site_entry.insert(0, "Site")

# Entry field for the username
username_entry = tk.Entry(frame, font=('Oswald', 12))
username_entry.place(relx=0.25, relwidth=0.2, relheight=1)
username_entry.insert(0, "Username")

# Entry field for the password
password_entry = tk.Entry(frame, font=('Oswald', 12))
password_entry.place(relx=0.5, relwidth=0.2, relheight=1)
password_entry.insert(0, "Password")

# Button to add a password
add_button = tk.Button(frame, text="Add", font=('Oswald', 12), command=save_password_ui)
add_button.place(relx=0.75, relheight=1, relwidth=0.2)

# Password strength indicator
strength_label = tk.Label(root, text="Password strength: ", font=('Oswald', 12), bg='#80c1ff')
strength_label.place(relx=0.5, rely=0.2, anchor='n')

# Button to generate a password
generate_button = tk.Button(root, text="Generate password", font=('Oswald', 12), command=generate_password_ui)
generate_button.place(relx=0.5, rely=0.3, anchor='n')

# Frame for the password listbox and scrollbar
password_frame = tk.Frame(root)
password_frame.place(relx=0.5, rely=0.5, relwidth=0.75, relheight=0.3, anchor='n')

# List of saved passwords
password_listbox = tk.Listbox(password_frame, font=('Oswald', 12))
password_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Scrollbar for the password listbox
password_scrollbar = tk.Scrollbar(password_frame, orient=tk.VERTICAL)
password_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Attach the scrollbar to the listbox
password_listbox.config(yscrollcommand=password_scrollbar.set)
password_scrollbar.config(command=password_listbox.yview)

# Entry field for password search
search_entry = tk.Entry(root, font=('Oswald', 12))
search_entry.place(relx=0.5, rely=0.85, relwidth=0.65, anchor='n')

# Button to search for a password
search_button = tk.Button(root, text="Search", font=('Oswald', 12), command=search_password)
search_button.place(relx=0.85, rely=0.85, anchor='n')

# Frame for the chatbox and scrollbar
chat_frame = tk.Frame(root)
chat_frame.place(relx=0.5, rely=0.7, relwidth=0.75, relheight=0.1, anchor='n')

# Chatbox
chatbox = tk.Text(chat_frame, font=('Oswald', 12), state=tk.DISABLED, wrap=tk.WORD)
chatbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Scrollbar for the chatbox
chat_scrollbar = tk.Scrollbar(chat_frame, orient=tk.VERTICAL)
chat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Attach the scrollbar to the chatbox
chatbox.config(yscrollcommand=chat_scrollbar.set)
chat_scrollbar.config(command=chatbox.yview)

# Entry field for chat messages
chat_entry = tk.Entry(root, font=('Oswald', 12))
chat_entry.place(relx=0.5, rely=0.82, relwidth=0.65, anchor='n')

# Button to send chat messages
send_button = tk.Button(root, text="Send", font=('Oswald', 12), command=send_message)
send_button.place(relx=0.85, rely=0.82, anchor='n')

# Navigation menu
menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Export", command=export_passwords)
file_menu.add_command(label="Import", command=import_passwords)
file_menu.add_command(label="Quit", command=root.quit)

# Load existing passwords into the list
conn = sqlite3.connect('passwords.db')
c = conn.cursor()
c.execute('SELECT site, username FROM passwords')
for site, username in c.fetchall():
    password_listbox.insert(tk.END, f"{site} ({username})")
conn.close()

# Run the application
root.mainloop()