import os
import encryptutils
import passutils

'''
This module will open the target password record from /VAULT and display it for the user. 
'''

#Load all password records
passreccs = passutils.return_records("VAULT")

#test
print(passreccs)

#Enter master password to authenticate user
encryptutils.authenticate_user()
    
endprogram = False
while endprogram == False:
    #Take input from user to find the target password record
    targettitle = input("Which password record do you want to access? ")
    while not(targettitle in passreccs):
        print("Target not found in VAULT. Try again.")
        targettitle = input("Which password record do you want to access? ")

     #Output the password record
    print(encryptutils.open_record(targettitle))
    
    #Ask if they want to open more records and end the program if not. 
    if input("\nOpening password record complete. Open another? (y/n): ") == 'n':
        quit()
    
