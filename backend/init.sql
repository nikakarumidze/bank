-- Create a new SQLite database file
CREATE DATABASE IF NOT EXISTS bank_database;

-- Connect to the newly created database
ATTACH DATABASE 'bank_database.db' AS bank_database;

-- Create 'users' table
CREATE TABLE IF NOT EXISTS bank_database.users (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    password_hash TEXT,
    balance REAL
);

-- Create transactions table
CREATE TABLE IF NOT EXISTS bank_database.transactions (
    transaction_id INTEGER PRIMARY KEY,
    sender_id INTEGER,
    receiver_id INTEGER,
    amount REAL,
    date TEXT,
    FOREIGN KEY(sender_id) REFERENCES bank_database.users(user_id),
    FOREIGN KEY(receiver_id) REFERENCES bank_database.users(user_id)
);
