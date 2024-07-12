import sqlite3

db = sqlite3.connect('shooter.conf')

def db_adder(category, encrypted_pass):
    db.execute("INSERT INTO credentials (category, passwords) VALUES (?, ?)", (category, encrypted_pass))
    db.commit()

    return None

def db_getter(category):
    query = db.execute("SELECT passwords FROM credentials WHERE category = ?", (category, ))
    result = query.fetchall()
    tuple = result[0]
    password = ''.join(tuple)

    return password

def db_updater(category, encrypted_pass):
    db.execute("UPDATE credentials SET passwords = ? WHERE category = ?", (encrypted_pass, category))
    db.commit()

    return None

def xor_encryption(text, key):
    encrypted_text = ""
    for i in range(len(text)):
        encrypted_text += chr(ord(text[i]) ^ ord(key[i % len(key)]))

    return encrypted_text

def main():
    db.execute("CREATE TABLE IF NOT EXISTS credentials (category TEXT, passwords TEXT)")
    while True:
        key = str(input("Please enter your master key: "))
        category = str(input("What category are you targetting?: "))
        user = str(input("Welcome! What would you like to do?: \n Create a new password (C) \n Retrieve a password (R) \n Update exisiting password (U) \n Quit (Q) \n"))
        
        if user == 'C':
            newpass = str(input("What is your new password?: "))
            confirmation = str(input("Please confirm your new password: "))
            
            if newpass == confirmation:
                encrypted_pass = xor_encryption(newpass, key)
                db_adder(category, encrypted_pass)
                print("All done! Your new password is now stored :)")
            
            elif newpass != confirmation:
                print("Error! Your password does not match :(")
            
            else:
                print("Error, something went wrong on our end...")
        
        elif user == 'R':
            encrypted_pass = db_getter(category)
            password = xor_encryption(encrypted_pass, key)

            result = print("Your password for " + category + " is: " + password)
            return result

        elif user == 'U':
            updated_pass = str(input("What would your new password be in " + category + "?: "))
            encrypted_pass = xor_encryption(updated_pass, key)
            db_updater(category, encrypted_pass)
            print("Updated successfully!")

        elif user == 'Q':
            print("Exiting the program. Bye!")
            
        else:
            print("Something went wrong...")
        
        restart = input("Would you like to use this program again? (y/n): ")
        if restart != 'y':
            print("Exiting the program. Bye!")
            break

main()
