import sqlite3

"""

# creaating database
connection = sqlite3.connect('user.db') #setting connector
cursor = connection.cursor() # setting cursor
#creating the table
cursor.execute('''CREATE TABLE accounts(
    account_number text,
    users_name text,
    pin text,
    main_balance real,
    loan_balance real
)''')
print("Database Created")
connection.commit()  # commiting changes to database
connection.close() # closing the database connection

"""

# creating an account
def create(user, pin, acc_num):
    con = sqlite3.connect('user.db')
    c = con.cursor()
    data = [(acc_num), (user), (pin)]
    c.execute("INSERT INTO accounts VALUES (?, ?, ?, 0, 0)", data)
    print("Your acount has been created, your account number is: ", acc_num)
    print("Proceed to login")
    con.commit()
    con.close()

# logining in
def login():
    run = True
    tries = 3
    while run:
        acc_num = input("Enter Account number: ")
        pin = input("Enter password: ")
        con = sqlite3.connect('user.db')
        c = con.cursor()
        find = "SELECT account_number FROM accounts WHERE account_number = ? AND pin = ?"
        c.execute(find, [acc_num, pin])
        results = c.fetchone()
        con.commit()
        con.close()

        if results:
            for i in results:
                print("Login Success")
            return acc_num

        else:
            tries -= 1
            print("Either account number or pin is incorrect. Tries left: " + str(tries))
            if tries == 0:
                print("Tries finished, goodbye")
                run = False

            else:
                run = True

# showing balances
def show_balance(ref):
    con = sqlite3.connect('user.db')
    c = con.cursor()
    find = "SELECT main_balance, loan_balance FROM accounts WHERE account_number = {}".format(ref)
    c.execute(find)
    result = c.fetchone()

    print("Your main balance is $", str(result[0]))
    print("Your loan balance is $", str(result[1]))


#function to get value from table
def get_current_main_balance(ref):
    con = sqlite3.connect('user.db')
    c = con.cursor()
    find = "SELECT main_balance FROM accounts WHERE account_number = {}".format(ref)
    c.execute(find)
    result = c.fetchone()
    
    return result[0]

#function to get loan_balance current value
def get_current_loan_balance(ref):
    con = sqlite3.connect('user.db')
    c = con.cursor()
    find = "SELECT loan_balance FROM accounts WHERE account_number = {}".format(ref)
    c.execute(find)
    result = c.fetchone()
    
    return result[0]

# depositing
def deposit(ref, amount):
    con = sqlite3.connect('user.db')
    c = con.cursor()
    current_balance = get_current_main_balance(ref)
    new_balance = current_balance + amount
    update = "UPDATE accounts SET main_balance = {0} WHERE account_number = {1}".format(new_balance, ref)
    c.execute(update)
    input("Press enter to continue......")
    print("Amount has been deposited. Current balance is $", str(new_balance))
    con.commit()
    con.close()


# withdrawing
def withdraw(ref, amount):
    con = sqlite3.connect('user.db')
    c = con.cursor()
    current_balance = get_current_main_balance(ref)
    if current_balance > 0 and amount < current_balance:
        new_balance = current_balance - amount
        update = "UPDATE accounts SET main_balance = {0} WHERE account_number = {1}".format(new_balance, ref)
        c.execute(update)
        input("Press enter to continue......")
        print("Amount has been withdrawn. Current balance is $", str(new_balance))
    else:
        print("Amount exceeds current balance.")
    con.commit()
    con.close()

def take_out_loan(ref, amount):
    con = sqlite3.connect('user.db')
    c = con.cursor()
    current_balance = get_current_loan_balance(ref)
    if current_balance == 0:
        new_balance = current_balance + amount
        update = "UPDATE accounts SET loan_balance = {0} WHERE account_number = {1}".format(new_balance, ref)
        c.execute(update)
        input("Press enter to continue.....")
        print("Loan of amount $", str(amount) , " . You owe the bank $", str(new_balance))
    else:
        print("Please pay back exsiting loan of $", str(current_balance))
    con.commit()
    con.close()

def payback_loan(ref, amount):
    con = sqlite3.connect('user.db')
    c = con.cursor()
    current_balance = get_current_loan_balance(ref)
    if current_balance == 0:
        print("Loan already paid in full")

    elif amount > current_balance:
        remainder = amount - current_balance
        to_loan_balance = 0.0
        deposit(ref, remainder)
        payback_loan(ref, current_balance)
        print("Loan has been fully paid and $", str(remainder), " has been deposited into your main account")

    elif amount < current_balance:
        new_balance = current_balance - amount
        update = "UPDATE accounts SET loan_balance = {0} WHERE account_number = {1}".format(new_balance, ref)
        c.execute(update)
        print("Amount has been paid, you still owe $", str(new_balance))

    elif current_balance == amount:
        new_balance = 0.0
        update = "UPDATE accounts SET loan_balance = {0} WHERE account_number = {1}".format(new_balance, ref)
        c.execute(update)
        print("Loan has been fully paid")

        con.commit()
        con.close()