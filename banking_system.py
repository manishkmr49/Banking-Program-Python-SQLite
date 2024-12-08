import sqlite3

class BankAccount:
    def __init__(self, account_holder, account_number=None, balance=0):
        self.account_holder = account_holder
        self.account_number = account_number
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            print(f"\n✅ Successfully Deposited: ${amount}")
            self.update_balance_in_db()
        else:
            print("\n❌ Deposit amount must be positive.")

    def withdraw(self, amount):
        if amount > 0:
            if amount <= self.balance:
                self.balance -= amount
                print(f"\n✅ Successfully Withdrew: ${amount}")
                self.update_balance_in_db()
            else:
                print("\n❌ Insufficient balance.")
        else:
            print("\n❌ Withdrawal amount must be positive.")

    def check_balance(self):
        print(f"\n💰 Account Balance: ${self.balance}")

    def display_account_info(self):
        print("\n🌟 Account Information 🌟")
        print(f"Account Holder: {self.account_holder}")
        print(f"Account Number: {self.account_number}")
        self.check_balance()

    def update_balance_in_db(self):
        conn = sqlite3.connect('banking.db')
        cursor = conn.cursor()
        cursor.execute('''UPDATE accounts SET balance = ? WHERE account_number = ?''', 
                       (self.balance, self.account_number))
        conn.commit()
        conn.close()

    @staticmethod
    def create_account(account_holder):
        conn = sqlite3.connect('banking.db')
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO accounts (account_holder, balance) 
                          VALUES (?, ?)''', (account_holder, 0))
        account_number = cursor.lastrowid  # Get the auto-generated account number
        conn.commit()
        conn.close()
        return account_number  # Return the account number to be displayed

    @staticmethod
    def get_account(account_number):
        conn = sqlite3.connect('banking.db')
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM accounts WHERE account_number = ?''', (account_number,))
        account_data = cursor.fetchone()
        conn.close()
        if account_data:
            return BankAccount(account_data[1], account_data[0], account_data[2])
        else:
            print("\n❌ Account not found!")
            return None

    @staticmethod
    def setup_database():
        conn = sqlite3.connect('banking.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS accounts (
                            account_number INTEGER PRIMARY KEY AUTOINCREMENT,
                            account_holder TEXT,
                            balance REAL)''')
        conn.commit()
        conn.close()

def main():
    BankAccount.setup_database()
    print( )
    print("*" * 5  + "       Welcome to AAA BANK    " + "*" * 5)

    name = input("\nEnter account holder's name: ")
    account_number = BankAccount.create_account(name)  # Capture the generated account number

    print(f"\n✅ Account successfully created for {name}!")
    print(f"🌟 Your account number is: {account_number} 🌟")  # Display the account number

    entered_account_number = int(input("\nEnter your account number: "))
    account = BankAccount.get_account(entered_account_number)

    if account:
        while True:
            print("\n📋 MENU 📋")
            print( )
            print("1️⃣  Deposit Money")
            print("2️⃣  Withdraw Money")
            print("3️⃣  Check Balance")
            print("4️⃣  View Account Info")
            print("5️⃣  Exit")

            choice = input("\nEnter your choice: ")

            if choice == "1":
                amount = float(input("\nEnter deposit amount: "))
                account.deposit(amount)

            elif choice == "2":
                amount = float(input("\nEnter withdrawal amount: "))
                account.withdraw(amount)

            elif choice == "3":
                account.check_balance()

            elif choice == "4":
                account.display_account_info()

            elif choice == "5":
                print("\n✨ Thank you for using AAA BANK. Goodbye! ✨")
                print( )
                break

            else:
                print("\n❌ Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
