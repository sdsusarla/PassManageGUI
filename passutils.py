import os
import encryptutils
'''
This module contains file utilities.
'''

def return_records(directory):
    '''
    This function iterates over the input directory and returns all of the password records as a list of name strings.
    '''
    
    passreccs = []
    #iterate over all password record folders
    for item in os.scandir(directory):
        if os.path.isdir(item): #checks if item is a folder
            passreccs.append(os.path.basename(item))
    
    return passreccs

def find_MASTERPASS(directory):
    '''
    This function iterates over the input directory and returns TRUE or FALSE depending on whether MASTERPASS.txt exists
    '''
    for item in os.scandir(directory):
        if os.path.basename(item) == "MASTERPASS.txt":
            return True
        
    return False #if MASTERPASS.txt is not found, False is returned

def clear_file(textfile):
    '''
    This function removes all text on the input .txt file
    '''
    with open(textfile, 'w') as file:
        file.write("") #unnecessary
        

    

            
        