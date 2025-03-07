# Password-Strength-Meter
Password Strength Checker
A Python-based web application built using Streamlit to check the strength of passwords, provide feedback, and securely store user information in a SQLite database.

Features
Password Strength Checker:

Checks if the password meets security criteria (length, uppercase, lowercase, digits, special characters, etc.).

Provides feedback on how to improve the password.

Secure User Storage:

Stores usernames and hashed passwords in a SQLite database.

Uses bcrypt for secure password hashing.

Password History:

Saves hashed passwords in a JSON file for history tracking.

Strong Password Generator:

Generates a random strong password with a mix of uppercase, lowercase, digits, and special characters.

Requirements
To run this project, you need the following Python libraries:

streamlit

bcrypt

sqlite3

re

random

string

json

os

You can install the required libraries using:

bash
Copy
pip install streamlit bcrypt
How to Run the Project
Clone the repository or download the code.

Open a terminal and navigate to the project directory.

Run the following command to start the Streamlit app:

bash
Copy
streamlit run app.py
The app will open in your web browser.

How to Use the App
Enter Username and Password:

Input your username and password in the provided fields.

Check Password Strength:

The app will analyze your password and provide feedback on its strength.

Store User:

If the password is strong, it will be securely stored in the database.

Generate Strong Password:

Click the "Generate Strong Password" button to get a random strong password.

File Structure
Copy
password-strength-checker/
├── app.py                # Main Python script
├── users.db              # SQLite database for storing user data
├── password_history.json # JSON file for storing password history
├── README.md             # This file
Code Overview
Key Functions
setup_database():

Sets up the SQLite database and creates a users table if it doesn’t exist.

bcrypt_password(password):

Hashes the password using bcrypt.

store_user(cursor, conn, username, password):

Stores the username and hashed password in the database.

check_password_strength(password, username):

Checks the strength of the password and provides feedback.

generate_strong_password(length=12):

Generates a random strong password.
