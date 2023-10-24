import sqlite3 as db

# Create the database connection and tables
obj = db.connect("Jpdocs.db")
cur = obj.cursor()
cur.execute("""
    CREATE TABLE IF NOT EXISTS customer (
        acc_no INTEGER PRIMARY KEY,
        f_name VARCHAR(15),
        l_name VARCHAR(15),
        pin INTEGER,
        bal FLOAT,
        address VARCHAR(40),
        contact VARCHAR(12)
    )
    """)
cur.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        tid INTEGER PRIMARY KEY,
        t_time DATETIME,
        tamount INTEGER,
        updated_balance REAL,
        sender INTEGER,
        receiver INTEGER,
        FOREIGN KEY(sender) REFERENCES customer(acc_no),
        FOREIGN KEY(receiver) REFERENCES customer(acc_no)
    )
    """)
obj.commit()


def createAccount():
    f_name = input("Enter your firstname-> ")
    l_name = input("Enter your lastname-> ")
    pin = int(input("Enter your pin-> "))
    address = input("Enter your address-> ")
    bal = float(input("Enter your initial amount-> "))
    contact = input("Enter your contact number-> ")
    cur.execute("""INSERT INTO customer (f_name, l_name, pin, bal, address, contact)VALUES (?, ?, ?, ?, ?, ?)""",
                (f_name, l_name, pin, bal, address, contact))
    obj.commit()
    print("Congratulations..! Your account is successfully created")


def seeDetails():
    acc_no = input("Enter your acc_no-> ")
    cur.execute("select * from customer where acc_no=? ", (acc_no,))
    row = cur.fetchone()
    if row is not None:
        print(f"Account number: {row[0]}")
        print(f"First number: {row[1]}")
        print(f"Last Name: {row[2]}")
        print(f"Balance: {row[4]}")
        print(f"Address: {row[5]}")
        print(f"Contact: {row[6]}")
    else:
        print("Please enter valid account number")


def depositBalance():
    acc_no = int(input("Enter your account number-> "))
    pin = int(input("Enter your pin-> "))
    cur.execute("SELECT pin FROM customer WHERE acc_no = ?", (acc_no,))
    row = cur.fetchone()
    if row is not None and pin == row[0]:
        dep = float(input("Enter amount to deposit-> "))
        cur.execute("SELECT bal FROM customer WHERE acc_no = ?", (acc_no,))
        row = cur.fetchone()
        balance = row[0] + dep
        cur.execute("UPDATE customer SET bal = ? WHERE acc_no = ?", (balance, acc_no))
        print("Thanks for using our services")
    else:
        print("Please enter a valid account number or PIN")


def withdraw():
    acc_no = int(input("Enter your account number-> "))
    pin = int(input("Enter your pin-> "))
    cur.execute("SELECT pin FROM customer WHERE acc_no = ?", (acc_no,))
    row = cur.fetchone()
    if row is not None and pin == row[0]:
        withdrawal = float(input("Enter amount to withdraw-> "))
        cur.execute("SELECT bal FROM customer WHERE acc_no = ?", (acc_no,))
        row = cur.fetchone()

        if row[0] >= withdrawal:
            balance = row[0] - withdrawal
            cur.execute("UPDATE customer SET bal = ? WHERE acc_no = ?", (balance, acc_no))
            print("Thanks for using our services")
        else:
            print("Insufficient balance")
    else:
        print("Please enter a valid account number or PIN")


def closeAccount():
    acc_no = int(input("Enter your account number-> "))
    cur.execute("DELETE FROM customer WHERE acc_no = ?", (acc_no,))
    print("Your account has been deleted")


def checkBalance():
    acc_no = int(input("Enter your account number-> "))
    cur.execute("SELECT bal FROM customer WHERE acc_no = ?", (acc_no,))
    row = cur.fetchone()
    if row is not None:
        print(f"Your current balance is: {row[0]}")
    else:
        print("Please enter a valid account number")


def main():
    while True:
        var = """   _ ____  ____   ___   ____ ____  
     | |  _ \|  _ \ / _ \ / ___/ ___| 
  _  | | |_) | | | | | | | |   \___ \ 
 | |_| |  __/| |_| | |_| | |___ ___) |
  \___/|_|   |____/ \___/ \____|____/ 
                                      """
        print(var)
        print("------Services-------")
        print("1. Create account")
        print("2.See Details")
        print("3. Deposit balance")
        print("4. Withdraw Cash")
        print("5. Check Balance")
        print("6. Close Account")
        print("7. exit")
        c = int(input("Enter your choice-> "))
        if c == 1:
            createAccount()
        elif c == 2:
            seeDetails()
        elif c == 3:
            depositBalance()
        elif c == 4:
            withdraw()
        elif c == 5:
            checkBalance()
        elif c == 6:
            closeAccount()
        elif c == 7:
            print("Thanks for using our service")
            break


if __name__ == "__main__":
    main()

