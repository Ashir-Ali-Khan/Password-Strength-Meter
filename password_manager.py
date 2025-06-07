import re
import streamlit as st
import random
import string 
import bcrypt
import json
import os
import sqlite3

# Constants
HISTORY_FILE = "password_history.json"
DATABASE_FILE = "users.db"

# Database setup
def setup_database():
    """Sets up the SQLite database and users table."""
    try:
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute('PRAGMA integrity_check')
        result = cursor.fetchone()
        if result[0] != 'ok':
            raise sqlite3.DatabaseError("Database is malformed")
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
        ''')
        conn.commit()
    except sqlite3.DatabaseError:
        # Handle the malformed database by recreating it
        conn.close()
        os.remove(DATABASE_FILE)  # Remove the corrupted database file
        conn = sqlite3.connect(DATABASE_FILE)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
        ''')
        conn.commit()
    return conn, cursor

def hash_password(password):
    """Hashes a password using bcrypt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt)

def store_user(cursor, conn, username, password):
    """Stores a new user with a hashed password in the database."""
    hashed_pwd = hash_password(password).decode()
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, hashed_pwd))
        conn.commit()
        st.write("User stored successfully.")
    except sqlite3.IntegrityError:
        st.write("Username already exists.")

def save_password(password):
    """Stores hashed password in a JSON file."""
    hashed_pwd = hash_password(password).decode()
    try:
        with open(HISTORY_FILE, "r") as file:
            data = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        data = []

    data.append(hashed_pwd)

    with open(HISTORY_FILE, "w") as file:
        json.dump(data, file, indent=4)

def check_password_strength(password, username):
    score = 0
    feedback = []
    
    # Length Check
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("❌ Password should be at least 8 characters long.")
    
    # Upper & Lowercase Check
    if re.search(r"[A-Z]", password) and re.search(r"[a-z]", password):
        score += 1
    else:
        feedback.append("❌ Include both uppercase and lowercase letters.")
    
    # Digit Check
    if re.search(r"\d", password):
        score += 1
    else:
        feedback.append("❌ Add at least one number (0-9).")
    
    # Special Character Check
    if re.search(r"[!@#$%^&*]", password):
        score += 1
    else:
        feedback.append("❌ Include at least one special character (!@#$%^&*).")
    
    # Username Check
    if username.lower() not in password.lower():
        score += 1
    else:
        feedback.append("❌ Password should not contain your username.")
    
    # Common Password Check
    common_passwords = ["password", "123456", "123456789", "qwerty", "abc123"]
    if password.lower() not in common_passwords:
        score += 1
    else:
        feedback.append("❌ Avoid using common passwords.")
    
    # Strength Rating
    if score == 6:
        feedback.append("✅ Very Strong Password!")
    elif score >= 4:
        feedback.append("✅ Strong Password!")
    elif score == 3:
        feedback.append("⚠️ Moderate Password - Consider adding more security features.")
    else:
        feedback.append("❌ Weak Password - Improve it using the suggestions above.")
    
    return feedback

def generate_strong_password(length=12):
    characters = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(random.choice(characters) for i in range(length))
    return password

# Streamlit app
st.title("Password Strength Checker")
st.markdown("Check your password strength and get security insights.")
username = st.text_input("Enter your username:")
password = st.text_input("Enter your password:", type="password")

# Setup database connection
conn, cursor = setup_database()

if password:
    feedback = check_password_strength(password, username)
    for message in feedback:
        st.write(message)
    if "✅ Very Strong Password!" in feedback or "✅ Strong Password!" in feedback:
        store_user(cursor, conn, username, password)
        save_password(password)
        st.write("🔒 Your password has been securely stored.")

if st.button("Generate Strong Password"):
    st.write("Suggested Password: ", generate_strong_password())

# Close the database connection when the script ends
conn.close()