import os
import encryptutils
import passutils

'''
This module will prompt the user for the title of the password record, the username of the password record, and the password they want to save.
It will then create a folder in VAULT with a .txt file of encrypted text with this information.
'''

#Create MASTERPASS.txt if not found 
if passutils.find_MASTERPASS("VAULT") is False:
    print("Use createmasterpass.py to create a master password before creating password records.")
    quit()

#Authenticate user
print("Authenticate yourself before adding a password record.")
encryptutils.authenticate_user()


#Take input from user on title, username, and password
title = input("Title: ")

#Force user to not use spaces 
while " " in title:
    print("Sorry, please do not use spaces")
    title = input("Title: ")


#Take input for username and password
user = input("Username: ")
with open("VAULT/MASTERPASS.txt", 'r') as masterpassfile: 
    password = encryptutils.encrypt(masterpassfile.read(), input("Password: ")) #Encrypt the password on input


#Create folder in VAULT
os.makedirs(f"VAULT/{title}")

#Create textfile with encrypted password
with open(f"VAULT/{title}/{title}.txt", 'a') as newfile:
    newfile.write(
        f"Title: {title} \nUsername: {user}"
    )
    newfile.write(
        f"\nPassword: {password}"
        )
    
print("Saving password complete.")
    
