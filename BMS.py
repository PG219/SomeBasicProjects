import random
import string
import mysql.connector

# Database connection setup
mycon = mysql.connector.connect(host="localhost", user="root", password="123", database="Banking")
mycursor = mycon.cursor()

def create_table(table_name, columns):
    try:
        mycursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({columns});")
        print(f"Table '{table_name}' created successfully.")
    except Exception as e:
        print(f"Error creating table: {e}")

def create_database(database_name):
    try:
        mycursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name};")
        print(f"Database '{database_name}' created successfully.")
    except Exception as e:
        print(f"Error creating database: {e}")

def register_user():
    print("\t\t\t\t\t\t""Welcome to SAAP INTERNATIONAL BANK")
    print("\t\t\t\t\t""Please fill in the required details")

    while True:
        first_name = input("FIRST Name: ")
        last_name = input("LAST Name: ")
        if first_name.isalpha() and last_name.isalpha():
            break
        else:
            print("Invalid input! Both first name and last name should contain only alphabetic characters.")

    while True:
        house_no = input("Please enter house no.")
        city = input("Please input your city")
        state = input("Please input your State")
        if city.isalpha() and state.isalpha() and house_no.isdigit():
            break
        else:
            print("Invalid input! Please enter valid details.")

    while True:
        email = input("Please enter your email.")
        if "@" in email and "." in email:
            break
        else:
            print("Invalid input! Invalid email format.")

    signature = input("Please give your signature")

    # Generating account number
   
    remaining_digits = ''.join(random.choice(string.digits) for _ in range(6))
    account_number = remaining_digits


    # Save user details to the database
    try:
        mycursor.execute("INSERT INTO Customer_Details (Account_no, CustomerFirst_name, CoustomerLast_name, Customer_AdDress, Gmail_Id) VALUES (%s, %s, %s, %s, %s)",
                         (account_number, first_name, last_name, f"{house_no} {city} {state}", email))
        mycon.commit()
        print("User registered successfully.")
        print("your account no:",account_number)
    except Exception as e:
        print("Error registering user: ", e)

def modify():
    try:
       
        print("1. Update ADDRESS")
        print("2. Insert Mobile(10 digit)")

        choice = int(input("Enter your choice: "))
       
        if choice == 1:
            new_address = input("Enter new ADDRESS: ")
            account_number = input("Enter ACCOUNT number: ")
            mycursor.execute(f"UPDATE Customer_Details SET Customer_AdDress = '{new_address}' WHERE Account_no = '{account_number}'")
       
            return
        if choice == 2:
            if choice == 2:
             phone = int(input("Enter Mobile No.: "))
             account_number = int(input("Enter ACCOUNT number: "))
             mycursor.execute("UPDATE Customer_Details SET phone = {} WHERE Account_no = {}".format(phone, account_number))

             mycon.commit()
             print("Mobile number updated successfully.")

        else:
            print("Invalid choice")
            return

        mycon.commit()
        print("Data modified successfully.")
    except Exception as e:
        print("Error registering user: ", e)
       



def close():
    account_number = input("Enter ACCOUNT number: ")
    #first delete foreign key table then delete primary key table
    delete_query1 = "DELETE FROM cash WHERE Account_no = %s"
    mycursor.execute(delete_query1, (account_number,))

    # Use a placeholder for the account_number to avoid SQL injection
    delete_query = "DELETE FROM customer_details WHERE Account_no = %s"

    # Execute the query with the actual account_number value
    mycursor.execute(delete_query, (account_number,))

    # Commit the changes to the database
    mycon.commit()

def create_cash_table():
    try:
        mycursor.execute('''CREATE TABLE IF NOT EXISTS cash (
                            Account_no INT(10) PRIMARY KEY,
                            Money_Left DECIMAL(20, 2),
                            FOREIGN KEY (Account_no) REFERENCES Customer_Details(Account_no)
                            );''')
        print("Table 'cash' created successfully.")
    except Exception as e:
        print("Error creating 'cash' table:" ,e)

def link_cash_to_customer(account_number):
    try:
       
        mycursor.execute("INSERT INTO cash (Account_no, Money_Left) VALUES (%s, 0.0);", (account_number,))

        mycon.commit()
        print(f"Linked 'cash' to account {account_number}.")
    except Exception as e:
        print(f"Error linking 'cash' to account: {e}")



def deposit_money(account_number, amount):
    try:
        mycursor.execute("UPDATE cash SET Money_Left = Money_Left + {} WHERE Account_no = '{}'".format(amount, account_number))

        mycon.commit()
        print(f"Successfully deposited {amount} into account {account_number}.")
    except Exception as e:
        print("Error depositing money:", e)

def withdraw_money(account_number, amount):
    try:
        mycursor.execute(f"UPDATE cash SET Money_Left = Money_Left - {amount} WHERE Account_no = '{account_number}'")
        mycon.commit()
        print(f"Successfully withdrew {amount} from account {account_number}.")
    except Exception as e:
        print(f"Error withdrawing money:" ,e)

def show_account():
   a= int(input("enter your account_no."))
   
   mycursor.execute("SELECT * FROM Customer_details where Account_no='{}'".format(a))
   
   result = mycursor.fetchall()
   

   for row in result:
       print(row)
   mycursor.execute("select Money_left from cash where Account_no='{}'".format(a))
   money=mycursor.fetchall()
   for i in money:
       print("NET AMOUNT LEFT",i)




# Main Menu
while True:
    print("****************** Main Menu **************")
    print("1. To Register in SAAP Bank")
    print("2. To Modify Account Details")
    print("3. To Close Account")
    print("4. To Deposit Money and Withdraw money")
    print("5. Show account details")
     
    print("6. Exit")
   
    choice = int(input("Enter your choice: "))
   
    if choice == 1:
        register_user()
    elif choice == 2:
        modify()
    elif choice == 3:
       close()
       
    elif choice == 4:
       
      account_number_input = input("Enter your account number: ")

      create_cash_table()

      # Link 'cash' to the customer's account
      link_cash_to_customer(account_number_input)

      amount_to_deposit = float(input("Enter the amount to deposit: "))
      deposit_money(account_number_input, amount_to_deposit)

      amount_to_withdraw = float(input("Enter the amount to withdraw: "))
      withdraw_money(account_number_input, amount_to_withdraw)
    elif choice==5:
        show_account()
       
   
       
       
    elif choice == 6:
        break
    else:
        print("Invalid choice. Please enter a valid option.")
