import sqlite3
from datetime import datetime
import os

DB_NAME = "budget_tracker.db"

def initialize_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS transactions (
                        id INTEGER PRIMARY KEY,
                        date TEXT,
                        type TEXT,
                        amount REAL,
                        category TEXT,
                        description TEXT
                     )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS cards (
                        id INTEGER PRIMARY KEY,
                        card_name TEXT,
                        card_number TEXT,
                        expiry_date TEXT,
                        cvv TEXT
                     )''')
    conn.commit()
    conn.close()

def add_transaction(transaction_type, amount, category, description):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    cursor.execute("INSERT INTO transactions (date, type, amount, category, description) VALUES (?, ?, ?, ?, ?)",
                   (date, transaction_type, amount, category, description))
    conn.commit()
    conn.close()

def add_card(card_name, card_number, expiry_date, cvv):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    card_number = "".join(chr(ord(c) + 2) for c in card_number)
    cvv = "".join(chr(ord(c) + 2) for c in cvv)
    cursor.execute("INSERT INTO cards (card_name, card_number, expiry_date, cvv) VALUES (?, ?, ?, ?)",
                   (card_name, card_number, expiry_date, cvv))
    conn.commit()
    conn.close()

# View monthly summary
def view_monthly_summary():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT type, SUM(amount) FROM transactions GROUP BY type")
    summary = cursor.fetchall()
    conn.close()
    income = sum(amount for t, amount in summary if t == 'income')
    expenses = sum(amount for t, amount in summary if t == 'expense')
    print(f"Total Income: {income:.2f} | Total Expenses: {expenses:.2f} | Net Balance: {income - expenses:.2f}")

# Main Menu
def main_menu():
    print("\n--- Budget Tracker ---")
    print("1. Add Income")
    print("2. Add Expense")
    print("3. Add Card")
    print("4. View Monthly Summary")
    print("5. Exit")

def main():
    initialize_db()
    while True:
        main_menu()
        choice = input("Select an option: ")
        if choice == '1':
            amount = float(input("Enter income amount: "))
            category = input("Enter income category: ")
            description = input("Enter income description: ")
            add_transaction('income', amount, category, description)
            print("Income added successfully.")
        elif choice == '2':
            amount = float(input("Enter expense amount: "))
            category = input("Enter expense category: ")
            description = input("Enter expense description: ")
            add_transaction('expense', amount, category, description)
            print("Expense added successfully.")
        elif choice == '3':
            card_name = input("Enter card name: ")
            card_number = input("Enter card number: ")
            expiry_date = input("Enter expiry date (MM/YY): ")
            cvv = input("Enter CVV: ")
            add_card(card_name, card_number, expiry_date, cvv)
            print("Card added successfully.")
        elif choice == '4':
            view_monthly_summary()
        elif choice == '5':
            print("Exiting Budget Tracker. Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
