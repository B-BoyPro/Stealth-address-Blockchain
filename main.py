import utils
from wallet import *
from blockchain import *
from transazione import *
from announcement import *

Banner_login ="""
==============================================
1 - Login
2 - Register
3 - Exit

>"""

Banner_wallet ="""
======================================================
1 - See account information
2 - See all blockchain
3 - Send Transaction with public key
4 - Generate stealth meta address
5 - Send transasction with meta address
6 - See all announcement
7 - Check own stealth address from announcement 
8 - Log out

>"""

def login_data(user):
    wallet_user = Wallet(user)
    print(Banner_wallet, end=" ",flush=True)
    ch = int(input())
    
    if ch < 1 or ch > 8:
        print("Unrecognized command")

    elif ch == 8:
        return None

    elif ch == 1:
        print("Wallet information of",user,": ")
        print("Private_key =",wallet_user.private_key)
        print("Public_key =",wallet_user.public_key)
        print("Ethereum address =",wallet_user.ethereum_addr)
        print("Balance =",wallet_user.balance)
        print("Stealth meta address =",wallet_user.stealth_meta_address)


    elif ch == 2:
        bc = Blockchain()
        print(bc.to_string())

    elif ch == 3:
        sender_pub_key = wallet_user.public_key
        print("Recipient public key: ",end = " ", flush=True)
        recipient_pub_key = input().strip()
        print("amount: ",end = " ", flush=True)
        amount = int(input())
        send_money(sender_pub_key,recipient_pub_key,amount,user)
    elif ch == 4:
        stealth_meta_address = wallet_user.stealth_address_create()
        print(stealth_meta_address)

    elif ch == 5:
        sender_pub_key = wallet_user.public_key
        print("Recipient meta address: ",end = " ", flush=True)
        recipient_meta_address = input().strip()
        print("amount: ",end = " ", flush=True)
        amount = int(input())
        send_money_with_meta_address(sender_pub_key,recipient_meta_address,amount,user)

    elif ch == 6:
        ann = Announcement()
        print(ann.to_string())

    elif ch == 7:
        wallet_user.check_stealth_address()
    return user


def login_menu():
    print(Banner_login,end=" ",flush=True)
    ch = int(input())

    if ch < 1 or ch > 4:
        print("Unrecognized command")

    elif ch == 3:
        raise SystemExit()

    else:
        username = input("Enter your username: ")
        password = input("Enter your password: ")
        if ch == 2:
            if utils.add_new_user(username, password):
                print(f"User {username} registered successfully!")
                return username
            else: 
                print("Registration failed.")
        else:
            if utils.login(username, password):
                print(f"Logged in as {username}")
                return username
            else:
                print("Login failed")
    return None


def main():
    user = None

    while True:
        try:
            if user is None:
                user = login_menu()
            else:
                user = login_data(user)
        except SystemExit:
            print("Bye!")
            exit()
        except:
            print(f"Something bad happened...")
            exit()

if __name__ == '__main__':
    main()