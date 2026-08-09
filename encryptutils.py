#import cryptography.fernet as Fernet
import random
'''
This module contains all the functions used for anything related to encryption or hashing. 
'''
characters = [
    "a", "b", "c", "d", "e", "f", "g",
    "h", "i", "j", "k", "l", "m", "n",
    "o", "p", "q", "r", "s", "t", "u",
    "v", "w", "x", "y", "z",
    "A", "B", "C", "D", "E", "F", "G",
    "H", "I", "J", "K", "L", "M", "N",
    "O", "P", "Q", "R", "S", "T", "U",
    "V", "W", "X", "Y", "Z",
    "0", "1", "2", "3", "4",
    "5", "6", "7", "8", "9",
    " "
]

def encrypt(key, password):
    '''
    This function returns a 'encrypted' password string that is created from the key and password.
    This is not an effective encryption function, but is employed to simulate one. It is a Caesar Cipher.
    It is only deterministic because the seed is set by the key.
    '''
    random.seed(key)
    shift = random.randint(1, 25)
    encryptedpassword = ""
    for letter in password:
        trueletternum = characters.index(letter)
        shiftedletter = characters[(trueletternum + shift) % len(characters)]
        encryptedpassword = encryptedpassword + shiftedletter
    
    return encryptedpassword

def decrypt(key, encryptedtext):
    '''
    This function returns the decrypted password string that is created from the key and encrypted password.
    '''
    random.seed(key)
    shift = random.randint(1, 25)
    
    decryptedpass = ""
    #iterate over the encrypted text, deshift each letter, then add that letter to decryptedpass 
    for letter in encryptedtext.strip():
        #print(letter)
        falseletternum = characters.index(letter)
        unshiftedletter = characters[(falseletternum - shift) % len(characters)]
        decryptedpass = decryptedpass + unshiftedletter
    
    return decryptedpass

def hash_(string):
    '''
    This function returns a 10 character long number that originates from the input string.
    This is not a real hash function. It is only deterministic since the seed is set. 
    '''
    random.seed(string)
    hashreturn = ''
    while len(hashreturn) < 10:
        hashreturn = hashreturn + str(random.randint(0, 99))
    while len(hashreturn) > 10:
        hashreturn = hashreturn[:-1] #remove last character if hashreturn is greater than 10 characters
        
    return hashreturn
        
def authenticate_user():
    '''
    This function returns True when the user knows the master password. 
    '''
    
    #verifies that the user knows the password by comparing the hashed input with the saved hashed masterpassword
    with open("VAULT/MASTERPASS.txt", 'r') as file:
        savedpass = file.read()
        givenpass = hash_(input("Enter current master password: "))
        if givenpass == savedpass:
            return True
        while givenpass != savedpass:
            print("ERROR: Incorrect master password.")
            givenpass = hash_(input("Enter current master password: "))
        return True
    
def open_record(targettitle):
    '''
    This function prints the password record with the password decrypted.
    '''
    #Output the password record
    with open(f"VAULT/{targettitle}/{targettitle}.txt", 'r') as record:
        lines = record.readlines() #split the lines into a list 
        #take the last element, the password, and remove the text before the actual password string
        decryptedpasswordline = lines[-1].replace("Password: ", "")
        a = record.read()
        print(a)
        with open("VAULT/MASTERPASS.txt", 'r') as masterpassfile:
            decryptedpasswordline = "Password: " + decrypt(masterpassfile.read(), decryptedpasswordline)
    
    #collate the final record string
    finalrecord = lines[0]+ lines[1] + decryptedpasswordline
    return finalrecord
        