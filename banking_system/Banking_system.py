import random
import json
from datetime import datetime

# File where account details will be stored
DATA_FILE = "accounts.json"


# Load existing accounts from the file
def load_accounts():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


# Save accounts to the file
def save_accounts(accounts):
    with open(DATA_FILE, "w") as file:
        json.dump(accounts, file, indent=4)


# Generate a unique 8-digit account number
def generate_account_number(accounts):
    while True:
        account_number = str(random.randint(10000000, 99999999))

        if account_number not in accounts:
            return account_number


# Create a new bank account
def create_account(accounts):
    print("\n========== CREATE ACCOUNT ==========")

    name = input("Enter your name: ").strip()

    while name == "":
        print("Name cannot be empty.")
        name = input("Enter your name: ").strip()

    phone = input("Enter your phone number: ").strip()

    while not phone.isdigit() or len(phone) != 10:
        print("Please enter a valid 10-digit phone number.")
        phone = input("Enter your phone number: ").strip()

    pin = input("Create a 4-digit PIN: ").strip()

    while not pin.isdigit() or len(pin) != 4:
        print("PIN must contain exactly 4 digits.")
        pin = input("Create a 4-digit PIN: ").strip()

    confirm_pin = input("Confirm your PIN: ").strip()

    while pin != confirm_pin:
        print("PINs do not match.")
        pin = input("Create a 4-digit PIN: ").strip()
        confirm_pin = input("Confirm your PIN: ").strip()

    # Generate account number
    account_number = generate_account_number(accounts)

    # Store account information
    accounts[account_number] = {
        "name": name,
        "phone": phone,
        "pin": pin,
        "balance": 0.0,
        "transactions": []
    }

    save_accounts(accounts)

    print("\nAccount created successfully!")
    print("Your Account Number is:", account_number)
    print("Please remember your Account Number and PIN.")


# Login to an existing account
def login(accounts):
    print("\n========== LOGIN ==========")

    account_number = input("Enter Account Number: ").strip()
    pin = input("Enter PIN: ").strip()

    if account_number not in accounts:
        print("Account not found.")
        return None

    if accounts[account_number]["pin"] != pin:
        print("Incorrect PIN.")
        return None

    print("\nLogin successful!")
    print("Welcome,", accounts[account_number]["name"])

    return account_number


# Check account balance
def check_balance(account):
    print("\n========== ACCOUNT BALANCE ==========")
    print("Account Holder :", account["name"])
    print("Current Balance: ₹{:.2f}".format(account["balance"]))


# Add a transaction to transaction history
def add_transaction(account, transaction_type, amount, details):
    transaction = {
        "type": transaction_type,
        "amount": amount,
        "details": details,
        "date": datetime.now().strftime("%d-%m-%Y %I:%M:%S %p")
    }

    account["transactions"].append(transaction)


# Deposit money
def deposit_money(account):
    print("\n========== DEPOSIT MONEY ==========")

    try:
        amount = float(input("Enter amount to deposit: ₹"))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        account["balance"] += amount

        add_transaction(
            account,
            "Deposit",
            amount,
            "Money deposited"
        )

        print("\nDeposit successful!")
        print("Amount Deposited: ₹{:.2f}".format(amount))
        print("New Balance: ₹{:.2f}".format(account["balance"]))

    except ValueError:
        print("Please enter a valid amount.")


# Withdraw money
def withdraw_money(account):
    print("\n========== WITHDRAW MONEY ==========")

    try:
        amount = float(input("Enter amount to withdraw: ₹"))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        # Check balance before withdrawing
        if amount > account["balance"]:
            print("Insufficient balance.")
            print(
                "Available Balance: ₹{:.2f}".format(
                    account["balance"]
                )
            )
            return

        account["balance"] -= amount

        add_transaction(
            account,
            "Withdrawal",
            amount,
            "Money withdrawn"
        )

        print("\nWithdrawal successful!")
        print("Amount Withdrawn: ₹{:.2f}".format(amount))
        print("Remaining Balance: ₹{:.2f}".format(account["balance"]))

    except ValueError:
        print("Please enter a valid amount.")


# Transfer money from one account to another
def transfer_money(accounts, sender_account_number):
    print("\n========== TRANSFER MONEY ==========")

    receiver_account_number = input(
        "Enter receiver Account Number: "
    ).strip()

    # Check whether receiver exists
    if receiver_account_number not in accounts:
        print("Receiver account not found.")
        return

    # Prevent transferring to the same account
    if receiver_account_number == sender_account_number:
        print("You cannot transfer money to your own account.")
        return

    try:
        amount = float(input("Enter amount to transfer: ₹"))

        if amount <= 0:
            print("Amount must be greater than zero.")
            return

        sender = accounts[sender_account_number]
        receiver = accounts[receiver_account_number]

        # Check sender's balance
        if amount > sender["balance"]:
            print("Insufficient balance.")
            return

        # Deduct money from sender
        sender["balance"] -= amount

        # Add money to receiver
        receiver["balance"] += amount

        # Add transaction to sender's history
        add_transaction(
            sender,
            "Transfer",
            amount,
            "Transferred to Account " + receiver_account_number
        )

        # Add transaction to receiver's history
        add_transaction(
            receiver,
            "Transfer Received",
            amount,
            "Received from Account " + sender_account_number
        )

        print("\nTransfer successful!")
        print("Amount Transferred: ₹{:.2f}".format(amount))
        print("Your New Balance: ₹{:.2f}".format(sender["balance"]))

    except ValueError:
        print("Please enter a valid amount.")


# Display transaction history
def transaction_history(account):
    print("\n========== TRANSACTION HISTORY ==========")

    transactions = account["transactions"]

    if len(transactions) == 0:
        print("No transactions found.")
        return

    for i, transaction in enumerate(transactions, start=1):
        print("\nTransaction", i)
        print("Type    :", transaction["type"])
        print("Amount  : ₹{:.2f}".format(transaction["amount"]))
        print("Details :", transaction["details"])
        print("Date    :", transaction["date"])


# Change account PIN
def change_pin(account):
    print("\n========== CHANGE PIN ==========")

    old_pin = input("Enter old PIN: ").strip()

    if old_pin != account["pin"]:
        print("Incorrect old PIN.")
        return

    new_pin = input("Enter new 4-digit PIN: ").strip()

    while not new_pin.isdigit() or len(new_pin) != 4:
        print("PIN must contain exactly 4 digits.")
        new_pin = input("Enter new 4-digit PIN: ").strip()

    confirm_pin = input("Confirm new PIN: ").strip()

    if new_pin != confirm_pin:
        print("PINs do not match.")
        return

    account["pin"] = new_pin

    print("PIN changed successfully.")


# Account menu after successful login
def account_menu(accounts, account_number):

    while True:
        account = accounts[account_number]

        print("\n")
        print("======================================")
        print("           ACCOUNT MENU")
        print("======================================")
        print("1. Check Balance")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Transfer Money")
        print("5. Transaction History")
        print("6. Change PIN")
        print("7. Logout")
        print("======================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":

            check_balance(account)

        elif choice == "2":

            deposit_money(account)
            save_accounts(accounts)

        elif choice == "3":

            withdraw_money(account)
            save_accounts(accounts)

        elif choice == "4":

            transfer_money(accounts, account_number)
            save_accounts(accounts)

        elif choice == "5":

            transaction_history(account)

        elif choice == "6":

            change_pin(account)
            save_accounts(accounts)

        elif choice == "7":

            print("\nLogged out successfully.")
            print("Returning to main menu...")
            break

        else:

            print("Invalid choice.")
            print("Please enter a number from 1 to 7.")


# Main menu
def main():
    accounts = load_accounts()

    while True:

        print("\n")
        print("======================================")
        print("          PYTHON BANKING SYSTEM")
        print("======================================")
        print("1. Create Account")
        print("2. Login")
        print("3. Exit")
        print("======================================")

        choice = input("Enter your choice: ").strip()

        if choice == "1":

            create_account(accounts)

        elif choice == "2":

            account_number = login(accounts)

            if account_number is not None:
                account_menu(accounts, account_number)

        elif choice == "3":

            print("\nThank you for using the Banking System!")
            print("Goodbye!")
            break

        else:

            print("Invalid choice.")
            print("Please enter 1, 2, or 3.")


# Start the program
if __name__ == "__main__":
    main()
   
