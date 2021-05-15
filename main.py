import database #calling the database module
import random # module used to create account number

run = True

while run:
    print("Welcome to XYZ Bank")
    print("""
    create: Create a new account
    login: Login into already existing account
    quit: Exit application
    """)

    option = input(">> ")

    if option.lower() == "create":
        user = input("Enter full name: ")
        pin = input("Enter desired pin: ")
        rand = random.randint(10000000, 99999999)
        database.create(user, pin, rand)

    elif option.lower() == "login":
        ref = database.login()
        input("Press enter to continue")
        
        while True:

            print("""
            balance: Check balances
            deposit: Deposit money in to bank
            withdraw: Withdraw money from the bank
            take: Take out a loan
            pay: Pay back loan
            exit: log out of account
            """)

            choice = input(">> ")

            if choice.lower() == "balance":
                database.show_balance(ref)

            elif choice.lower() == "deposit":
                deposit_amount = eval(input("Enter amount to be deposited: $"))
                database.deposit(ref, deposit_amount)

            elif choice.lower() == "withdraw":
                withdraw_amount = eval(input("Enter amount to be withdrawn: $"))
                database.withdraw(ref, withdraw_amount)

            elif choice.lower() == "take":
                amount_to_be_taken_out = eval(input("Enter amount you want to be loaned: $"))
                database.take_out_loan(ref, amount_to_be_taken_out)

            elif choice.lower() == "pay":
                amount_to_be_paid = eval(input("Enter amount to paid: $"))
                database.payback_loan(ref, amount_to_be_paid)

            elif choice.lower() == "exit":
                break

            else:
                print("Select one of the given options.")
        

    elif option.lower() == "quit":
        print("Thank you for using XYZ Bank")
        run = False
    else:
        print("Invalid option. Select one of the give options.")
    