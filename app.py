# Personal Budget Tracker -> v1.0
# Python Console App
# Tech Stack > PYTHON, GIT, GITHUB
# By GRP 1 > Afiya Chrissy Tiana Chrison Silveston Owais Cephas

#------------------->
#import module
import os

# File paths to store user data and transaction records
USER_DATA_FILE = 'users.txt'
TRANSACTION_DATA_FILE = 'transactions.txt'

# --- Utility Functions ---

# Load user credentials from file
def load_user_data():
    user_data = {}
    if os.path.exists(USER_DATA_FILE):
        with open(USER_DATA_FILE, 'r') as file:
            for line in file:
                username, password = line.strip().split(',')
                user_data[username] = password
    return user_data

# Save user credentials to file
def save_user_data(username, password):
    with open(USER_DATA_FILE, 'a') as file:
        file.write(f'{username},{password}\n')

# Save transaction data to file
def save_transaction_data(username, transaction_type, amount, sender, receiver, date):
    with open(TRANSACTION_DATA_FILE, 'a') as file:
        file.write(f'{username},{transaction_type},{amount},{sender},{receiver},{date}\n')

# Load transaction data for a specific user
def load_transaction_data(username):
    transactions = []
    if os.path.exists(TRANSACTION_DATA_FILE):
        with open(TRANSACTION_DATA_FILE, 'r') as file:
            for line in file:
                u_name, transaction_type, amount, sender, receiver, date = line.strip().split(',')
                if u_name == username:
                    transactions.append({
                        'transaction_type': transaction_type,
                        'amount': float(amount),
                        'sender': sender,
                        'receiver': receiver,
                        'date': date
                    })
    return transactions

# --- User Registration/Login Functions ---

# User registration
def register(user_data):
    print("\n--- Register ---")
    username = input("Enter a username: ")
    
    if username in user_data:
        print("Username already exists. Try a different username.")
        return None
    
    password = input("Enter a password: ")
    confirm_password = input("Confirm password: ")
    
    if password != confirm_password:
        print("Passwords do not match. Try again.")
        return None
    
    user_data[username] = password
    save_user_data(username, password)
    print("Registration successful! You can now log in.\n")
    return username

# User login
def login(user_data):
    print("\n--- Login ---")
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    
    if username in user_data and user_data[username] == password:
        print(f"Welcome, {username}! You are now logged in.\n")
        return username
    else:
        print("Invalid username or password. Please try again.\n")
        return None

# --- Budget Management Functions ---

# Add cash to the account
def add_cash(username):
    print("\n--- Add Cash ---")
    amount = float(input("Enter amount to add: "))
    sender = input("Who sent the money? (Enter sender's name): ")
    date = input("Enter the date of transaction (DD-MM-YYYY): ")
    
    save_transaction_data(username, 'add', amount, sender, 'You', date)
    print(f"${amount} added to your account from {sender} on {date}.\n")

# Remove cash from the account
def remove_cash(username):
    print("\n--- Remove Cash ---")
    amount = float(input("Enter amount to remove: "))
    receiver = input("Who received the money? (Enter receiver's name): ")
    date = input("Enter the date of transaction (DD-MM-YYYY): ")
    
    save_transaction_data(username, 'remove', amount, 'You', receiver, date)
    print(f"${amount} removed from your account. Sent to {receiver} on {date}.\n")

# View budget summary
def view_summary(username):
    print("\n--- Budget Summary ---")
    transactions = load_transaction_data(username)
    
    total_added = 0
    total_removed = 0
    current_balance = 0
    inflow = []
    outflow = []
    
    for transaction in transactions:
        if transaction['transaction_type'] == 'add':
            total_added += transaction['amount']
            inflow.append(transaction['amount'])
        elif transaction['transaction_type'] == 'remove':
            total_removed += transaction['amount']
            outflow.append(transaction['amount'])
    
    current_balance = total_added - total_removed
    
    print(f"Total Money Added: ${total_added}")
    print(f"Total Money Removed: ${total_removed}")
    print(f"Current Balance: ${current_balance}\n")
    
    # Show simple bar graphs for inflow and outflow
    print("--- Cash Inflow Graph (Money Added) ---")
    show_bar_graph(inflow, 'inflow')
    print("--- Cash Outflow Graph (Money Removed) ---")
    show_bar_graph(outflow, 'outflow')

# Show simple bar graph
def show_bar_graph(data, label):
    if not data:
        print(f"No {label} transactions.")
    else:
        for i, amount in enumerate(data, 1):
            bars = '█' * int(amount / 100)  # For each $100, add a block
            print(f"{i}: ${amount} | {bars}")

# Main menu for logged-in users
def user_menu(username):
    while True:
        print("\n1. Add Cash")
        print("2. Remove Cash")
        print("3. View Budget Summary (with Graphs)")
        print("4. Logout")
        choice = input("Choose an option (1/2/3/4): ")
        
        if choice == '1':
            add_cash(username)
        elif choice == '2':
            remove_cash(username)
        elif choice == '3':
            view_summary(username)
        elif choice == '4':
            print("Logging out...")
            break
        else:
            print("Invalid option. Please try again.")

# --- Main Application ---

def main():
    print("=== Personal Budget Tracker ===")
    
    # Load existing user data from file
    user_data = load_user_data()
    
    while True:
        print("\n1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Choose an option (1/2/3): ")
        
        if choice == '1':
            username = register(user_data)
            if username:
                user_menu(username)
        elif choice == '2':
            username = login(user_data)
            if username:
                user_menu(username)
        elif choice == '3':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please try again.")

# Run the main function
if __name__ == "__main__":
    main()
