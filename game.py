import sqlite3

#connects the file 'shooter.conf' to sqlite3
db = sqlite3.connect('shooter.conf')

def db_adder(category, username, encrypted_pass):
    '''
Password creator. This function adds new passwords into said category. 
If category does not exist, then a new section is added into category.
It writes the encrypted password and category into the table of the db file, disguised as 'shooter.conf'

Parameters: 
    category (str): user inputted category
    encrypted_pass (str): Takes in encrypted password, as a string

Returns:
    None
    
    '''
    db.execute("INSERT INTO credentials (category, username, passwords) VALUES (?, ?, ?)", (category, username, encrypted_pass))
    db.commit()

    return None

def db_getter(category):
    '''
Password retriever. This function takes already existing ecrypted passwords from a user defined category in the database. 
If user inputted category does not exist, then it returns an error

Parameters: 
    category (str): user inputted category

Returns:
    encrypted_pass (str) - the encrypted password which would not make sense without decryption
    
    '''
    password = db.execute("SELECT username, passwords FROM credentials WHERE category = ?", (category, ))
    result = password.fetchall()

    #since result returns as a tuple within a list, the following two lines converts them into a string
    encrypted_pass, username = result[0]

    return encrypted_pass, username

def db_updater(category, encrypted_pass, username):
    '''
Password updater. This function updates already existing passwords, changing them to whatever user wants. 
It writes the new encrypted password into the db file, disguised as 'shooter.conf'

Parameters: 
    category (str): user inputted category
    encrypted_pass (str): Takes in encrypted password, as a string

Returns:
    None
    
    '''
    db.execute("UPDATE credentials SET passwords = ?, username = ? WHERE category = ?", (encrypted_pass, username, category))
    db.commit()

    return None

def xor_encryption(text, key):
    encrypted_text = ""
    for i in range(len(text)):
        encrypted_text += chr(ord(text[i]) ^ ord(key[i % len(key)]))

    return encrypted_text

def main():
    #creates a table in the db file if it doesn't already exist, to store categories and passwords
    db.execute("CREATE TABLE IF NOT EXISTS credentials (category TEXT, username TEXT, passwords TEXT)")
    while True:
        key = str(input("Please enter your master key: "))
        category = str(input("What category are you targetting?: "))
        user = str(input("Welcome! What would you like to do?: \n Create a new password (C) \n Retrieve a password (R) \n Update exisiting password (U) \n Quit (Q) \n"))
        
        if user == 'C':
            new_username = str(input("What is your username?: "))
            newpass = str(input("What is your new password?: "))
            confirmation = str(input("Please confirm your new password: "))
            
            #checking the new passwords match
            if newpass == confirmation:
                encrypted_pass = xor_encryption(newpass, key)
                username = xor_encryption(new_username, key)
                db_adder(category, username, encrypted_pass)
                print("All done! Your new password is now stored :)")
            
            elif newpass != confirmation:
                print("Error! Your password does not match :(")
            
            else:
                print("Error, something went wrong on our end...")
            
        
        elif user == 'R':
            encrypted_user, encrypted_pass = db_getter(category)
            password = xor_encryption(encrypted_pass, key)
            username = xor_encryption(encrypted_user, key)
            print("Your username for " + category + " is: " + username)
            print("Your password for " + category + " is: " + password)

        elif user == 'U':
            updated_user = str(input("What is the username?: "))
            confirmation_u = str(input("Please confirm your username: "))
            updated_pass = str(input("What would your new password be in " + category + "?: "))
            confirmation_p = str(input("Please confirm your password: "))
            
            #checking updated password matches confirmation
            if updated_pass == confirmation_p and updated_user == confirmation_u:
                encrypted_pass = xor_encryption(updated_pass, key)
                encrypted_user = xor_encryption(updated_user, key)
                db_updater(category, encrypted_pass, encrypted_user)
                print("Updated successfully!")
                print("All done! Your new password is now stored :)")
            
            elif updated_pass != confirmation:
                print("Error! Your password does not match :(")
            
            else:
                print("Error, something went wrong on our end...")

        elif user == 'Q':
            print("Exiting the program. Bye!")
            break
            
        else:
            print("Something went wrong...")
        
        restart = input("Would you like to use this program again? (y/n): ")
        if restart != 'y':
            print("Exiting the program. Bye!")
            break

main()
