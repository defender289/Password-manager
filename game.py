import sqlite3

'''
Things to add:
1. password generator
1. check if R U D has no errors if table has nothing
'''

#connects the file 'shooter.conf' to sqlite3
db = sqlite3.connect('shooter.conf')

def db_adder(category, encrypted_user, encrypted_pass):
    '''
Credentials creator. This function adds new passwords and usernames into said category. 
If category does not exist, then a new section is added into category.
It writes the encrypted password, encypted username and category into the table of the db file, disguised as 'shooter.conf'

Parameters: 
    category (str): user inputted category
    encrypted_user (str): takes in encrypted username as a string
    encrypted_pass (str): Takes in encrypted password, as a string

Returns:
    None
    
    '''
    db.execute("INSERT INTO credentials (category, username, password) VALUES (?, ?, ?)", (category, encrypted_user, encrypted_pass))
    db.commit()

    return None

def db_deleter(category):
    '''
Credentials deleter. This function alone purely deletes the whole row of credentials, including category, password, and username

Parameters:
    category (str): the category which the user wants to delete

Returns:
    None
    '''
    db.execute("DELETE FROM credentials WHERE category = ?", (category,))
    db.commit()

    return None

def db_getter(category):
    '''
Password retriever. This function takes already existing ecrypted passwords and usernames from a user defined category in the database. 
If user inputted category does not exist, then it returns an error

Parameters: 
    category (str): user inputted category

Returns:
    encrypted_pass (str) - the encrypted password which would not make sense without decryption
    
    '''
    password = db.execute("SELECT username, password FROM credentials WHERE category = ?", (category, ))
    result = password.fetchall()

    #unpacks the list into two values
    encrypted_pass, username = result[0]

    return encrypted_pass, username

def db_updater(category, encrypted_pass, encrypted_user):
    '''
Password updater. This function updates already existing passwords, changing them to whatever user wants. 
It writes the new encrypted password into the db file, disguised as 'shooter.conf'

Parameters: 
    category (str): user inputted category
    encrypted_pass (str): Takes in encrypted password, as a string
    encrypted_user (str): takes in encrypted username as a string

Returns:
    None
    
    '''
    db.execute("UPDATE credentials SET password = ?, username = ? WHERE category = ?", (encrypted_pass, encrypted_user, category))
    db.commit()

    return None

def xor_encryption(text, key):
    encrypted_text = ""
    for i in range(len(text)):
        encrypted_text += chr(ord(text[i]) ^ ord(key[i % len(key)]))

    return encrypted_text

def available_cat():
    '''
A function that shows all available categories, making it easier for the user to know which category to call

Parameters:
    None

Returns:
    a list of categories available, indicated by a '->' in each line

    '''
    #displays available categories
    result = db.execute("SELECT category FROM credentials")
    categories = result.fetchall()
    for i in range(len(categories)):
        tuple = categories[i]
        str_cat = ''.join(tuple)
        print('-> ' + str_cat)

def check_db_content():
    result = db.execute("SELECT COUNT(*) FROM credentials")
    check = result.fetchall()
    if check:
        pass
    else:
        print("Error, no entries in database.")

def main():
    #creates a table in the db file if it doesn't already exist, to store categories and passwords
    db.execute("CREATE TABLE IF NOT EXISTS credentials (category TEXT, username TEXT, password TEXT)")
    while True:
        key = str(input("Please enter your master key: "))
        user = str(input('''Welcome! What would you like to do?:  
-> Create new password (C)
-> Input credentials (I) 
-> Retrieve credentials (R) 
-> Update exisiting credentials (U) 
-> Delete existing credentials (D) 
-> Quit (Q) \n'''
        ))
        
        #inputting credentials
        if user == 'C':
            pass

        elif user == 'I':
            category = str(input("What category would it be called?: "))
            new_username = str(input("What is your username?: "))
            confirmation_u = str(input("Please confirm your username: "))
            newpass = str(input("What is your password?: "))
            confirmation_p = str(input("Please confirm your password: "))
            
            #checking the new passwords match
            if newpass == confirmation_p and new_username == confirmation_u:
                encrypted_pass = xor_encryption(newpass, key)
                encrypted_user = xor_encryption(new_username, key)
                db_adder(category, encrypted_user, encrypted_pass)
                print("All done! Your new password is now stored :)")
            
            elif newpass != confirmation_p or new_username != confirmation_u:
                print("Error! Your password does not match :(")
            
            else:
                print("Error, something went wrong on our end...")
            
        #retrieving credentials
        elif user == 'R':
            check_db_content()
            print("The categories available are: ")
            available_cat()

            category = str(input("What category are you retrieving?: "))
            encrypted_user, encrypted_pass = db_getter(category)
            password = xor_encryption(encrypted_pass, key)
            username = xor_encryption(encrypted_user, key)
            print("Your username for " + category + " is: " + username)
            print("Your password for " + category + " is: " + password)

        #updating credentials
        elif user == 'U':
            check_db_content()
            print("The categories available are: ")
            available_cat()
            
            category = str(input("What category are you updating?: "))
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
            
            elif updated_pass != confirmation_p or updated_user != confirmation_u:
                print("Error! Your password does not match :(")
            
            else:
                print("Error, something went wrong on our end...")

        #deleting existing credentials
        elif user == 'D':
            check_db_content()
            print("The categories available are: ")
            available_cat()

            category = str(input("Which category do you want to delete?: "))

            #checks that categories aren't being deleted without permission
            username = str(input("Please enter the username for " + category + ":"))
            password = str(input("Please enter the password for " + category + ":"))
            security_user, security_pass = db_getter(category)
            check_user = xor_encryption(security_user, key)
            check_pass = xor_encryption(security_pass, key)

            if check_user == username and check_pass == password:
                db_deleter(category)
                print("Success!, " + category + " has been deleted.")

            elif check_user != username or check_pass != password:
                print("Error, username or password entered does not match the credentials in our database.")

            else:
                print("Something went wrong on our end...")

        #quitting program
        elif user == 'Q':
            print("Exiting the program. Bye!")
            break
            
        else:
            print("Something went wrong...")
        
        #restart program
        restart = input("Would you like to use this program again? (y/n): ")
        if restart != 'y':
            print("Exiting the program. Bye!")
            break

main()
