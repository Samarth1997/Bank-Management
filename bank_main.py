import json
import random
import string
from pathlib import Path
import re



class Bank:

    database='bank_data.json'
    data= []

    try:
        if Path(database).exists():
            with open(database) as fs:
                data=json.loads(fs.read())
        else:
            print("No such file exist")
    except Exception as err:
        print("error occured due to {err}")
    
    
    @staticmethod
    def update():
       with open(Bank.database,'w') as fs:
           fs.write(json.dumps(Bank.data))
           
    
    @classmethod
    def __accountgen(cls):
        alpha =random.choices(string.ascii_letters, k=4)
        num = random.choices(string.digits,k=2)
        spechar = random.choices("@#$%&*",k=1)
        id= alpha+num+spechar
        random.shuffle(id)
        return "".join(id)

    def create_account(self):
        print("create bank account:")

        info={
                "name": input("Enter Your Name:"),
                "age":  int(input("Enter Your age:")),
                "email": input("Enter Your Email:"),
                "pin":  int(input("Enter Your pin of 4 digits:")),
                "phone_no": int(input("Enter your Phone no of 10 digits:")),
                "Account_no": Bank.__accountgen(),
                "Balance": 0
            }        


        def is_valid_email(email):
            pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
            return re.match(pattern, info["email"]) is not None

        # Example1
        print(is_valid_email("test@example.com"))  # True
        if info["age"]<18 or len(str(info['pin']))!=4 or len(str(info["phone_no"]))!=10:

            print("You cannot Create Account.")
        else:
            print("You Have create Account Successfully")
            for i in info:
                print(f"{i} : {info[i]}")
            print("please note your account Number:")

            Bank.data.append(info)
            Bank.update()


    
    def deposit_money(self):
        acc_no=input("please enter your account number:")
        pin_no=int(input("please enter your pin:"))
        # print(Bank.data)

        user_data = [i for i in Bank.data if i['Account_no']== acc_no and i['pin']== pin_no]
        print(user_data)

        if user_data==False:
            print("No Such user existed:")
        else:
            amount=int(input("enter amount you want to deposit:"))
            if amount>10000 or amount<0:
                print("you can deposit less than 0 and more than 10000")
            else:
                # print(user_data)
                user_data[0]['Balance']+=amount
                Bank.update()
                print(Bank.data)
                print("amount deposited successfully:")


    def withdraw_Money(self):

        acc_no=input("Enter your account number:")
        pin_no= int(input("Enter your  pin:"))
        user_data=[i for i in Bank.data if i['Account_no']==acc_no and i['pin']== pin_no]
        # print(user_data)

        if user_data== False:
            print("Data is Not Exists. Please Enter Valid Account number or Pin number")
        else:
            amount=int(input("Enter Withdrawl Amount:"))
            if (amount< 0 or amount > user_data[0]['Balance']):
                print("Enter Valid Amount:")
            else:
                user_data[0]['Balance']-=amount
                Bank.update()
                print(Bank.data)
                print("Withrawl Sucess:")


    def view_account(self):
        acc_no=input("Enter your Account no:")
        pin_no=int(input("Enter your Pin no:"))

        user_data=[i for i in Bank.data if i["Account_no"]==acc_no and i['pin']==pin_no]
        # print("Here is Your Account Details:",user_data)
        for i in user_data[0]:
            print(f"{i}: {user_data[0][i]} ")

    def update_account(self):
        acc_no=input("Enter your Account no:")
        pin_no=int(input("Enter Your Pin no:")) 

        user_data=[i for i in Bank.data if i["Account_no"]==acc_no and i['pin']==pin_no]

        if user_data== False:
            print("No Such Account Found:")
        
        else:
            print("You Cannot change Age, Balance, Account Number, Phone number:")
            print("Fill the details for change or leave it empty if no change")

            new_data={
                "name": input("Write your New Name or press enter to Skip"),
                "pin": input("Write your New Pin or press enter to Skip"),
                "email": input("Write your New Email or press enter to Skip"),
                 
            }

            
            if new_data["name"]== "":
                new_data["name"]=user_data[0]['name']
            if new_data['email']== "":
                new_data['email']= user_data[0]['email']

            new_data['age']=user_data[0]['age']
            new_data['Balance']=user_data[0]['Balance']
            new_data['Account_no']=user_data[0]['Account_no']
            new_data['phone_no']=user_data[0]['phone_no']


            if new_data['pin'].isdigit():
                new_data['pin'] = int(new_data['pin'])
            else:
                new_data['pin'] = user_data[0]['pin']  

            for i in new_data:
                if new_data[i]==user_data[0][i]:
                    continue
                else:
                    user_data[0][i]=new_data[i]
                    Bank.update()
                    print("Your Details are Updated Successfully:")
                    for i in user_data[0]:
                        print(f"{i}:{user_data[0][i]}")   
                    # print(user_data)
    def delete_account(self):
        
        acc_no=input("Enter your Account no:")
        pin_no=int(input("Enter Your Pin no:")) 

        user_data=[i for i in Bank.data if i["Account_no"]== acc_no and i["pin"]== pin_no]

        if user_data == False:
            print("No such account Exist")

        else:
            check1=input("press Y to Delete or press N to skip:")

            if check1== "N" or check1=="n":
                pass
            else:
                index= Bank.data.index(user_data[0])
                Bank.data.pop(index)
                print("your Account has been Deleted:")
                Bank.update()
        
       


User= Bank()
print("Press 1 for Creating Bank Account:")
print("Press 2 to Deposit Money:")
print("Press 3 to Withdraw Money:")
print("Press 4 to View Account Details:")
print("Press 5 to Change or Update Account Details:")
print("Press 6 to Delete Bank Account:")


check= int(input("Please Select any one Option:"))

if check==1:
    User.create_account()

if check==2:
    User.deposit_money()

if check==3:
    User.withdraw_Money()

if check==4:
    User.view_account()

if check==5:
    User.update_account()

if check==6:
    User.delete_account()

