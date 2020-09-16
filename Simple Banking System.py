import random
import sqlite3


class Bank:
    db = sqlite3.connect("card.db")  # connect or create data base
    cr = db.cursor()  # Setting up the cursor

    cr.execute(
        'CREATE TABLE if not exists card(id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)')

    def __init__(self):
        self.option = ""
        self.card_number = ""
        self.pin_number = ""
        self.balance = 0

    def close_db(self):
        """Saving and closing the Database"""

        self.db.commit()
        self.db.close()

    def luhn_algorithm(self, card):
        """USing the Luhn Algorithm to identify the correct card number"""
        self.step_number = dict()
        for step, number in enumerate(card[:15]):
            if (step + 1) % 2 != 0:
                self.step_number[step + 1] = int(number) * 2
                if self.step_number[step + 1] > 9:
                    self.step_number[step + 1] = (int(number) * 2) - 9
            else:
                self.step_number[step + 1] = int(number)
        self.total_identifier = sum(self.step_number.values()) + int(card[15])
        return self.total_identifier % 10

    def generator(self):
        """Generating card number if they are completing the Luhn Algo conditions"""
        while True:
            self.card_number = "400000" + str(random.randrange(0, int("9" * 10))).zfill(10)
            self.cr.execute(f"SELECT number FROM card WHERE number = '{self.card_number}'")
            check_available = self.cr.fetchone()  # Assign the value we get back from the SELECT
            if self.luhn_algorithm(self.card_number) == 0 and check_available is None:
                self.pin_number = str(random.randrange(0, int("9" * 4))).zfill(4)
                self.cr.execute(
                    f"INSERT INTO card VALUES({self.card_number} , '{self.card_number}', '{self.pin_number}', {self.balance})")
                self.db.commit()
                return False

    def create_account(self):
        """Creating the User account"""
        self.generator()
        print("Your card has been created")
        print("Your card number:")
        print(self.card_number)
        print("Your card PIN:")
        print(self.pin_number)

    def log_account(self):
        """Logging to the user account"""
        self.qst_card_num = input("Enter your card number:\n")
        self.cr.execute(f"SELECT number, pin FROM card WHERE number = '{self.qst_card_num}'")
        self.check_account = self.cr.fetchone()
        if self.check_account != None:
            self.card_num = self.check_account[0]
            self.pin_num = self.check_account[1]
            if self.qst_card_num == self.card_num:
                self.qst_pin_num = input("Enter your PIN:\n")
                if self.qst_pin_num == self.pin_num:
                    print("You have successfully logged in!")
                    self.ask = ""
                    while True:
                        self.ask = input("1. Balance\n2. Add income\n3. Do transfer\n4. Close account\n5. Log out\n0. Exit\n")
                        self.cr.execute(f"SELECT number, balance FROM card WHERE number = '{self.card_num}'")
                        self.balance_number = self.cr.fetchone()
                        if self.balance_number != None:
                            self.user_balance = int(self.balance_number[1])
                            if self.ask == "1":
                                self.balance = self.balance_number[1]
                                print(f"Balance: {self.balance}")
                            elif self.ask == "2":
                                self.balance = self.balance_number[1]
                                self.income = int(input("Enter income:\n"))
                                self.cr.execute(f"UPDATE card set balance = {self.income + self.balance} WHERE number = {self.card_num}")
                                print("Income was added!")
                                Bank.db.commit()
                            elif self.ask == "3":
                                self.transfer = input("Transfer\nEnter card number:\n")
                                if len(self.transfer) == 16:
                                    self.check_card = self.luhn_algorithm(self.transfer)
                                    if self.check_card == 0:
                                        self.cr.execute(f"SELECT number, pin, balance FROM card WHERE number = '{self.transfer}'")
                                        self.trasfer_num = self.cr.fetchone()
                                        if self.trasfer_num != None:
                                            self.trasfer_num = self.trasfer_num[0]
                                            self.ask_money = int(input("Enter how much money you want to transfer:\n"))
                                            if self.user_balance >= self.ask_money :
                                                self.cr.execute(f"UPDATE card set balance = balance + {self.ask_money} WHERE number = '{self.trasfer_num}'") # Receiver
                                                self.cr.execute(f"UPDATE card set balance = balance - {self.ask_money} WHERE number = '{self.card_num}'") # Donner
                                                Bank.db.commit()
                                                print("Success!")                                    
                                            else:
                                                print("Not enough money!")
                                        else:
                                            print("Such a card does not exist.")    
                                    else:
                                        print("Probably you made a mistake in the card number. Please try again!")
                                else:
                                        print("Probably you made a mistake in the card number. Please try again!")
                            elif self.ask == "4":
                                self.cr.execute(f"DELETE FROM card WHERE number = '{self.card_num}'")
                                self.db.commit()
                                print("The account has been closed!")
                                return False
                            elif self.ask == "5":
                                print("You have successfully logged out!")
                                return False
                            elif self.ask == "0":
                                print("Bye!")
                                quit()
                else:
                    print("Wrong card number or PIN!")
            else:
                print("Wrong card number or PIN!")
        else:
                print("Wrong card number or PIN!")

    def show(self):
        """Collecting all the Methods in this one to make the Class run by it self"""
        while self.option != "0":
            self.option = input("1. Create an account\n2. Log into account\n0. Exit\n")
            if self.option == "1":
                self.create_account()
            elif self.option == "2":
                self.log_account()
            elif self.option == "0":
                print("Bye!")
                self.close_db()
                quit()
            else:
                print("Please Choose an option from the above!")

Bank().show()  # Write your code here
