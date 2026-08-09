import os
import passutils
import encryptutils
'''
This module creates a master password
'''

#Check if MASTERPASS.txt exists, and create one if not 
if passutils.find_MASTERPASS("VAULT") == False:
    print("Master password not found. Let's make one.")
    masterpass = encryptutils.hash_(input("Enter master password: "))
    with open("VAULT/MASTERPASS.txt", 'a') as masterpassfile:
        masterpassfile.write(str(masterpass))
        print("MASTERPASS.txt created. You now have a master password.")
        
#If MASTERPASS.txt is empty, create one anyways
with open("VAULT/MASTERPASS.txt", 'r+') as masterpassfile:
    if masterpassfile.read() == "":
            print("Master password file empty. Let's make one.")
            masterpass = encryptutils.hash_(input("Enter master password: "))
            with open("VAULT/MASTERPASS.txt", 'w') as masterpassfile:
                masterpassfile.write(str(masterpass))
                print("MASTERPASS.txt created. You now have a master password.")
    else:  
        print("Master password is found.")
        #Modify the master password if the user agrees to. Otherwise quit
        modify = input("Modify master password? All saved passwords will become irrecoverable. (y/n): ")
        if modify == "y":
            if encryptutils.authenticate_user():
                masterpass = encryptutils.hash_(input("Enter new master password: "))
                passutils.clear_file("VAULT/MASTERPASS.txt")
                with open("VAULT/MASTERPASS.txt", 'a') as masterpassfile:
                    masterpassfile.write(str(masterpass))
                    print("MASTERPASS.txt modified. You now have a new master password.")
        else:
            quit()
        
    


