import random
from datetime import datetime

accounts = {}

print("================================")
print("       BANKING SYSTEM")
print("================================")


# 1. CREATE ACCOUNT
def create_account():
    print("\n===== CREATE ACCOUNT =====")

    name = input("Enter your name: ")
    phone = input("Enter your phone number: ")
    pin = input("Create a 4-digit PIN: ")

    account_number = random.randint(100000, 999999)

    accounts[account_number] = {
        "name": name,
        "phone": phone,
        "pin": pin,
        "balance": 0,
        "transactions": []
    }

    print("\nAccount created successfully!")
    print("Your Account Number:", account_number)


# LOGIN
def login():
    print("\n===== LOGIN =====")

    account_number = int(input("Enter your account number: "))
    pin = input("Enter your PIN: ")

    if account_number in accounts:
        if accounts[account_number]["pin"] == pin:
            print("\nLogin successful!")
            print("Welcome,", accounts[account_number]["name"])
            return account_number
        else:
            print("\nIncorrect PIN!")
    else:
        print("\nAccount not found!")

    return None


# 1. CHECK BALANCE
def check_balance(account_number):
    print("\n===== ACCOUNT BALANCE =====")

    balance = accounts[account_number]["balance"]

    print("Current Balance: ₹", balance)


# 2. DEPOSIT
def deposit(account_number):
    print("\n===== DEPOSIT MONEY =====")

    amount = float(input("Enter amount to deposit: "))

    if amount <= 0:
        print("Please enter a valid amount.")
        return

    accounts[account_number]["balance"] += amount

    transaction_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    transaction = {
        "type": "Deposit",
        "amount": amount,
        "date_time": transaction_time
    }

    accounts[account_number]["transactions"].append(transaction)

    print("\nDeposit successful!")
    print("Deposited Amount: ₹", amount)
    print("Current Balance: ₹", accounts[account_number]["balance"])


# 3. WITHDRAW
def withdraw(account_number):
    print("\n===== WITHDRAW MONEY =====")

    amount = float(input("Enter amount to withdraw: "))

    if amount <= 0:
        print("Please enter a valid amount.")
        return

    if amount > accounts[account_number]["balance"]:
        print("\nInsufficient balance!")
        return

    accounts[account_number]["balance"] -= amount

    transaction_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    transaction = {
        "type": "Withdrawal",
        "amount": amount,
        "date_time": transaction_time
    }

    accounts[account_number]["transactions"].append(transaction)

    print("\nWithdrawal successful!")
    print("Withdrawn Amount: ₹", amount)
    print("Current Balance: ₹", accounts[account_number]["balance"])


# 4. TRANSFER
def transfer(account_number):
    print("\n===== TRANSFER MONEY =====")

    receiver = int(input("Enter receiver account number: "))
    amount = float(input("Enter amount to transfer: "))

    if receiver not in accounts:
        print("\nReceiver account not found!")
        return

    if receiver == account_number:
        print("\nYou cannot transfer money to your own account!")
        return

    if amount <= 0:
        print("\nPlease enter a valid amount.")
        return

    if amount > accounts[account_number]["balance"]:
        print("\nInsufficient balance!")
        return

    accounts[account_number]["balance"] -= amount
    accounts[receiver]["balance"] += amount

    transaction_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    sender_transaction = {
        "type": "Transfer",
        "amount": amount,
        "to": receiver,
        "date_time": transaction_time
    }

    receiver_transaction = {
        "type": "Received",
        "amount": amount,
        "from": account_number,
        "date_time": transaction_time
    }

    accounts[account_number]["transactions"].append(sender_transaction)
    accounts[receiver]["transactions"].append(receiver_transaction)

    print("\nTransfer successful!")
    print("Transferred Amount: ₹", amount)
    print("Current Balance: ₹", accounts[account_number]["balance"])


# 5. TRANSACTION HISTORY
def transaction_history(account_number):
    print("\n===== TRANSACTION HISTORY =====")

    transactions = accounts[account_number]["transactions"]

    if len(transactions) == 0:
        print("No transactions found.")
        return

    for i, transaction in enumerate(transactions, start=1):
        print("\nTransaction", i)
        print("Type:", transaction["type"])
        print("Amount: ₹", transaction["amount"])

        if "to" in transaction:
            print("To Account:", transaction["to"])

        if "from" in transaction:
            print("From Account:", transaction["from"])

        print("Date & Time:", transaction["date_time"])


# 6. CHANGE PIN
def change_pin(account_number):
    print("\n===== CHANGE PIN =====")

    old_pin = input("Enter your old PIN: ")

    if old_pin != accounts[account_number]["pin"]:
        print("\nIncorrect old PIN!")
        return

    new_pin = input("Enter your new PIN: ")
    confirm_pin = input("Confirm your new PIN: ")

    if new_pin != confirm_pin:
        print("\nPINs do not match!")
        return

    if len(new_pin) != 4 or not new_pin.isdigit():
        print("\nPIN must contain exactly 4 digits!")
        return

    accounts[account_number]["pin"] = new_pin

    print("\nPIN changed successfully!")


# ACCOUNT MENU
def account_menu(account_number):

    while True:

        print("\n========== ACCOUNT MENU ==========")
        print("1. Check Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Transaction History")
        print("6. Change PIN")
        print("7. Logout")
        print("==================================")

        choice = input("Enter your choice: ")

        if choice == "1":
            check_balance(account_number)

        elif choice == "2":
            deposit(account_number)

        elif choice == "3":
            withdraw(account_number)

        elif choice == "4":
            transfer(account_number)

        elif choice == "5":
            transaction_history(account_number)

        elif choice == "6":
            change_pin(account_number)

        elif choice == "7":
            print("\nLogged out successfully!")
            break

        else:
            print("\nInvalid choice! Please select 1-7.")


# MAIN PROGRAM
create_account()

logged_in_account = login()

if logged_in_account is not None:
    account_menu(logged_in_account)