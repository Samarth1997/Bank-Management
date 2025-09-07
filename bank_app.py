import json
import random
import string
import re
from pathlib import Path


class Bank:
    database = 'bank_data.json'
    data = []

    # Load existing data from file if available
    try:
        if Path(database).exists():
            with open(database) as fs:
                data = json.load(fs)
        else:
            print("No such file exists")
    except Exception as err:
        print(f"Error occurred: {err}")

    @staticmethod
    def update():
        with open(Bank.database, 'w') as fs:
            json.dump(Bank.data, fs, indent=4)

    @classmethod
    def __accountgen(cls):
        alpha = random.choices(string.ascii_letters, k=4)
        num = random.choices(string.digits, k=2)
        spechar = random.choices("@#$%&*", k=1)
        account_id = alpha + num + spechar
        random.shuffle(account_id)
        return "".join(account_id)

    @staticmethod
    def is_valid_email(email):
        pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        return re.match(pattern, email) is not None

    def create_account(self):
        print("Create Bank Account")

        info = {
            "name": input("Enter your name: "),
            "age": int(input("Enter your age: ")),
            "email": input("Enter your email: "),
            "pin": int(input("Enter a 4-digit PIN: ")),
            "phone_no": int(input("Enter a 10-digit phone number: ")),
            "Account_no": Bank.__accountgen(),
            "Balance": 0
        }

        if (
            info["age"] < 18
            or len(str(info['pin'])) != 4
            or len(str(info["phone_no"])) != 10
            or not self.is_valid_email(info["email"])
        ):
            print("❌ You cannot create an account. Invalid input.")
        else:
            print("✅ Account created successfully!")
            for key, value in info.items():
                print(f"{key}: {value}")
            print("Please note your account number.")
            Bank.data.append(info)
            Bank.update()

    def deposit_money(self):
        acc_no = input("Enter your account number: ")
        pin_no = int(input("Enter your PIN: "))

        user_data = [i for i in Bank.data if i['Account_no'] == acc_no and i['pin'] == pin_no]

        if not user_data:
            print("❌ No such user exists.")
        else:
            amount = int(input("Enter amount to deposit (0–10000): "))
            if 0 < amount <= 10000:
                user_data[0]['Balance'] += amount
                Bank.update()
                print("✅ Amount deposited successfully.")
            else:
                print("❌ Invalid deposit amount.")

    def withdraw_money(self):
        acc_no = input("Enter your account number: ")
        pin_no = int(input("Enter your PIN: "))

        user_data = [i for i in Bank.data if i['Account_no'] == acc_no and i['pin'] == pin_no]

        if not user_data:
            print("❌ Invalid account or PIN.")
        else:
            amount = int(input("Enter withdrawal amount: "))
            if 0 < amount <= user_data[0]['Balance']:
                user_data[0]['Balance'] -= amount
                Bank.update()
                print("✅ Withdrawal successful.")
            else:
                print("❌ Insufficient balance or invalid amount.")

    def view_account(self):
        acc_no = input("Enter your account number: ")
        pin_no = int(input("Enter your PIN: "))

        user_data = [i for i in Bank.data if i["Account_no"] == acc_no and i['pin'] == pin_no]

        if not user_data:
            print("❌ Account not found.")
        else:
            print("📄 Your Account Details:")
            for key, value in user_data[0].items():
                print(f"{key}: {value}")

    def update_account(self):
        acc_no = input("Enter your account number: ")
        pin_no = int(input("Enter your PIN: "))

        user_data = [i for i in Bank.data if i["Account_no"] == acc_no and i['pin'] == pin_no]

        if not user_data:
            print("❌ No such account found.")
        else:
            print("You cannot change Age, Balance, Account Number, or Phone number.")
            print("Fill the details or press Enter to skip:")

            new_data = {
                "name": input("New Name: ") or user_data[0]['name'],
                "pin": input("New PIN: ") or str(user_data[0]['pin']),
                "email": input("New Email: ") or user_data[0]['email'],
                "age": user_data[0]['age'],
                "Balance": user_data[0]['Balance'],
                "Account_no": user_data[0]['Account_no'],
                "phone_no": user_data[0]['phone_no']
            }

            new_data['pin'] = int(new_data['pin']) if new_data['pin'].isdigit() else user_data[0]['pin']

            user_data[0].update(new_data)
            Bank.update()
            print("✅ Account updated successfully.")
            for key, value in user_data[0].items():
                print(f"{key}: {value}")

    def delete_account(self):
        acc_no = input("Enter your account number: ")
        pin_no = int(input("Enter your PIN: "))

        user_data = [i for i in Bank.data if i["Account_no"] == acc_no and i["pin"] == pin_no]

        if not user_data:
            print("❌ No such account exists.")
        else:
            confirm = input("Press Y to delete or N to cancel: ").lower()
            if confirm == 'y':
                Bank.data.remove(user_data[0])
                Bank.update()
                print("✅ Your account has been deleted.")
            else:
                print("Account deletion canceled.")


class Admin:
    admin_cred = {"Admin": "Admin123"}

    def __init__(self):
        self.bank_data = Bank.data

    @staticmethod
    def login():
        username = input("Enter admin username: ")
        password = input("Enter admin password: ")

        if username in Admin.admin_cred and Admin.admin_cred[username] == password:
            print("✅ Login successful. Welcome, Admin!")
            return True
        else:
            print("❌ Invalid credentials.")
            return False

    @classmethod
    def __accountgen(cls):
        alpha = random.choices(string.ascii_letters, k=4)
        num = random.choices(string.digits, k=2)
        spechar = random.choices("@#$%&*", k=1)
        account_id = alpha + num + spechar
        random.shuffle(account_id)
        return "".join(account_id)

    def view_all_accounts(self):
        print("📋 All Bank Accounts:")
        for account in self.bank_data:
            print(account)

    def create_account_admin(self):
        print("Create Account as Admin")

        info = {
            "name": input("Enter name: "),
            "age": int(input("Enter age: ")),
            "email": input("Enter email: "),
            "pin": int(input("Enter 4-digit PIN: ")),
            "phone_no": int(input("Enter 10-digit phone number: ")),
            "Account_no": Admin.__accountgen(),
            "Balance": 0
        }

        if (
            info["age"] < 18
            or len(str(info['pin'])) != 4
            or len(str(info["phone_no"])) != 10
            or not Bank.is_valid_email(info["email"])
        ):
            print("❌ Invalid account data.")
        else:
            Bank.data.append(info)
            Bank.update()
            print("✅ Account created successfully.")
            for k, v in info.items():
                print(f"{k}: {v}")

    def update_account_admin(self):
        acc_no = input("Enter account number: ")
        pin_no = int(input("Enter PIN: "))

        user_data = [i for i in Bank.data if i["Account_no"] == acc_no and i['pin'] == pin_no]

        if not user_data:
            print("❌ No such account found.")
            return

        print("You cannot change Age, Balance, Account Number, or Phone number.")
        print("Enter new details or press Enter to skip:")

        new_data = {
            "name": input("New Name: ") or user_data[0]['name'],
            "pin": input("New PIN: ") or str(user_data[0]['pin']),
            "email": input("New Email: ") or user_data[0]['email'],
            "age": user_data[0]['age'],
            "Balance": user_data[0]['Balance'],
            "Account_no": user_data[0]['Account_no'],
            "phone_no": user_data[0]['phone_no']
        }

        new_data['pin'] = int(new_data['pin']) if new_data['pin'].isdigit() else user_data[0]['pin']
        user_data[0].update(new_data)
        Bank.update()
        print("✅ Account updated successfully.")
        for k, v in user_data[0].items():
            print(f"{k}: {v}")

    def delete_any_account(self, acc_no):
        account = [i for i in self.bank_data if i["Account_no"] == acc_no]

        if account:
            self.bank_data.remove(account[0])
            Bank.update()
            print("✅ Account deleted by Admin.")
        else:
            print("❌ Account not found.")


# Main Program
if __name__ == "__main__":
    user_type = int(input("Press 1 for Admin, 2 for Customer: "))
    bank_user = Bank()

    if user_type == 2:
        print("""
        1. Create Bank Account
        2. Deposit Money
        3. Withdraw Money
        4. View Account Details
        5. Update Account
        6. Delete Account
        """)

        choice = int(input("Choose an option: "))

        if choice == 1:
            bank_user.create_account()
        elif choice == 2:
            bank_user.deposit_money()
        elif choice == 3:
            bank_user.withdraw_money()
        elif choice == 4:
            bank_user.view_account()
        elif choice == 5:
            bank_user.update_account()
        elif choice == 6:
            bank_user.delete_account()
        else:
            print("Invalid Option")

    elif user_type == 1:
        admin = Admin()
        if admin.login():
            print("""
            1. View All Accounts
            2. Create Account
            3. Update Account
            4. Delete Account
            """)
            admin_choice = int(input("Choose an option: "))

            if admin_choice == 1:
                admin.view_all_accounts()
            elif admin_choice == 2:
                admin.create_account_admin()
            elif admin_choice == 3:
                admin.update_account_admin()
            elif admin_choice == 4:
                acc_no = input("Enter account number to delete: ")
                admin.delete_any_account(acc_no)
            else:
                print("Invalid Option")
        else:
            print("Exiting admin panel.")
