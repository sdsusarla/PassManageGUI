import os
import passutils
import encryptutils
'''
This module opens a password record and gives the user the ability to modify it. 
'''

def modify_user(record):
    '''
    This function modifies the user's chosen password record's username field.
    '''
    #Opens record and recieves user input on new username
    decryptedrecord = encryptutils.open_record(record)
    
    #test
    print("@@@@@@\n" + decryptedrecord + "\n@@@@@@@")
    
    #recieve input on new username
    newuser = input("What should the new username be? ")
    
    #save information from current record 
    with open(f"VAULT/{record}/{record}.txt", 'r') as recordfile:
        lines = recordfile.readlines()
        lines[1] = "Username: " + newuser + "\n"
    #clear file and write new information
    with open(f"VAULT/{record}/{record}.txt", 'w+') as recordfile: 
        for line in lines:
            recordfile.write(f"{line}")
    #print(encryptutils.open_record(record))
    print("Modification complete.")
        
def modify_pass(record):
    #Open record and recieves user input on new password
    decryptedrecord = encryptutils.open_record(record)
    print("@@@@@@\n" + decryptedrecord + "\n@@@@@@@")
    
    with open("VAULT/MASTERPASS.txt", 'r') as masterpassfile: 
        newpass = encryptutils.encrypt(masterpassfile.read(), input("What should the new password be? "))
        
    #save information from current record 
    with open(f"VAULT/{record}/{record}.txt", 'r') as recordfile:
        lines = recordfile.readlines()
        lines[2] = "Password: " + newpass + "\n"
        
    #clear file and write new information
    with open(f"VAULT/{record}/{record}.txt", 'w+') as recordfile: 
        for line in lines:
            recordfile.write(f"{line}")
            
    print("Modification complete.")
    
#load all password records
passreccs = passutils.return_records("VAULT")

#authenticate user
encryptutils.authenticate_user()

#have user make a choice on which record is being modified
print("Modify which password record?")
for index, record in enumerate(passreccs):
    print(record + f" {index}") 
recordchoice = int(input("Enter number of record: "))

#have user make a choice on what part of the record they want to modify
componentchoice = int(input("Modify username (1) or modify password (2)? "))

if componentchoice == 1:
    modify_user(passreccs[recordchoice])
else:
    modify_pass(passreccs[recordchoice])