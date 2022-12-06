import psycopg2



# 3.3 Add to the program a function that creates the connection to the database. 
# Commit to repo. (This is part of Task 2.3) 
def psconnect():
    params = {
        'dbname': 'assessmentcontacts',
        'user': 'postgres',
        'password': '',
        'host': 'localhost',
        'port': 5432
        }

    connection = psycopg2.connect(**params)
    return connection

# 3.4 Create a function that can fetch data from the database and print it to the 
# console. Commit to remote repo. 
# Can obviously make this more advanced and present the information prettier.
# But The assignment doesn't ask for that and I'm conserving time.
def pslist():
    query = """
    SELECT * FROM view_contacts
    ORDER BY first_name, last_name;"""
    connection = psconnect()
    cursor = connection.cursor()
    cursor.execute(query)
    list_for_printing = cursor.fetchall()
    for item in list_for_printing:
        print(item)
    cursor.close()
    connection.close()
    return None
# 3.6 Create a function that inserts a new contact into the contacts table. Commit 
# to remote repo. 
# STRETCH TASKS 
# If you have finished all the tasks and handed in to Canvas, you can try the following: 
# 3.8 STRETCH TASK! Add functions to the program in Task 3 that can add contact 
# type and category as well. Create new Commands to make this work. 
# 3.9 STRETCH TASK! Continue and add a function to add a new item using 
# contacts, contact_type, and contact_category. Add new command to 

# I made a mistake in 3.6. I will just copy the function and reduce it (Since it's almost the solution to 3.9) to fit 3.6
# My guess is that 3.9 expects a function that takes in type, category and contact info but nothing else?
# My function adds a contact with full info already.
# Since it is a 'Stretch' Task I'll leave it as it is because I need a break.

def addcontacttype(contact_type):
    connection=psconnect()
    cursor=connection.cursor()
    query = f"INSERT INTO CONTACT_TYPES (contact_type) VALUES ('{contact_type}')"
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()
    return True

def addcategory(category):
    connection=psconnect()
    cursor=connection.cursor()
    query = f"INSERT INTO contact_categories (contact_category) VALUES ('{category}')"
    cursor.execute(query)
    connection.commit()
    cursor.close()
    connection.close()
    return True

# Real function for 3.6

def insertcontact(first_name, last_name, title, organization):
    connection = psconnect()
    cursor = connection.cursor()
    insert_contacts = f"""
    INSERT INTO contacts (first_name, last_name, title, organization) VALUES
    ('{first_name}', '{last_name}','{title}','{organization}');
    """
    cursor.execute(insert_contacts)
    connection.commit()
    cursor.close()
    connection.close()
    return True


# My first attempt doing too much.
def insertcontact2(first_name, last_name, title, organization, contact_type, contact, contact_category):
    connection = psconnect()
    cursor = connection.cursor()
    insert_contacts = f"""
    INSERT INTO contacts (first_name, last_name, title, organization) VALUES
    ('{first_name}', '{last_name}','{title}','{organization}');
    """
    get_contact_id = f"""
    SELECT id from contacts
    order by id DESC LIMIT 1;
    """
    get_contact_type_id = f"""
    SELECT id FROM contact_types WHERE contact_type = '{contact_type}';
    """
    get_contact_category_id = f"""
    SELECT id FROM contact_categories WHERE contact_category = '{contact_category}';
    """
    cursor.execute(insert_contacts)
    connection.commit()
    cursor.execute(get_contact_id)
    contact_id = cursor.fetchone()[0]
    cursor.execute(get_contact_category_id)
    category_id = cursor.fetchone()[0]
    cursor.execute(get_contact_type_id)
    type_id = cursor.fetchone()[0]

    insert_items = f"""
    INSERT INTO items (contact, contact_id, contact_type_id, contact_category_id) VALUES
    ('{contact}', {contact_id},{type_id},{category_id});
    """
    cursor.execute(insert_items)
    connection.commit()
    cursor.close()
    connection.close()
    return True



# 3.7 Create a function that deletes a contact from the contacts table. Commit to 
# remote repo. 
def psdelete(first_name, last_name):
    connection = psconnect()
    cursor = connection.cursor()
    selectquery = f"""
    SELECT id from contacts where first_name = '{first_name}' AND last_name = '{last_name}';"""
    cursor.execute(selectquery)
    contact_id = cursor.fetchone()[0]
    deletequery = f"""
    DELETE FROM items where contact_id = {contact_id};
    DELETE FROM contacts where id = {contact_id}"""
    cursor.execute(deletequery)
    connection.commit()
    cursor.close()
    connection.close()
    return True


if __name__ == '__main__':
#     3.5 Add a loop that makes the program ask for input. The input is a command to 
#         select between different functions. Commands could be: LIST, INSERT, 
#         DELETE. Commit to remote repo. 
    print("Available commands: LIST, INSERT,INSERT2(Full insert), DELETE, QUIT, ADDTYPE, ADDCATEGORY")
    while True:
        
        command = input("Please enter a command: ")
            # Quit the program
        if command.upper() == 'QUIT':
            quit()

            # Insert items
        elif command.upper() == 'INSERT':
            first_name = input("Insert first name please\n")
            last_name = input("Insert last name please\n")
            title = input("Insert title please\n")
            organization = input("Insert organization please\n")
            try:
                insertcontact(first_name, last_name, title, organization)
                print(f"Contact with name {first_name} inserted successfully!")
            except:
                print("Error inserting contact.")

                #Insert 2 
        elif command.upper() == 'INSERT2':
            first_name = input("Insert first name please\n")
            last_name = input("Insert last name please\n")
            title = input("Insert title please\n")
            organization = input("Insert organization please\n")
            contact_type = input("Insert contact type please (Email, Phone, Skype, Instagram\n")
            contact = input("Insert contact information please\n")
            contact_category = input("Insert contact category please. (Home, Work, Fax)\n")
            try:
                insertcontact2(first_name, last_name, title, organization, contact_type, contact, contact_category)
                print(f"Contact with name {first_name} inserted successfully!")
            except:
                print("Error inserting contact.")


                # List items
        elif command.upper() == 'LIST':
            pslist()
                #Delete
        elif command.upper() == 'DELETE':
            first_name = input("Enter first name: \n")
            last_name = input("Enter last name: \n")
            try:
                psdelete(first_name,last_name)
                print(f"Delete successful!- {first_name} removed from database.")
            except:
                print("Delete not successful!")
                # Add Type
        elif command.upper() == 'ADDTYPE':
            contact_type = input("Enter type to insert: ")
            try:
                addcontacttype(contact_type)
                print("Added a new type",contact_type)
            except:
                print("Failed to add type")

                # Category
        elif command.upper() == 'ADDCATEGORY':
            category = input("Add new category: ")
            try:
                addcategory(category)
                print("Added new category, ", category)
            except:
                print("Failed to add category", category)
        