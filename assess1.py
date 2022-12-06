import psycopg2



# 3.3 Add to the program a function that creates the connection to the database. 
# Commit to repo. (This is part of Task 2.3) 
def psconnect():
    params = {
        'dbname': 'assessmentcontacts',
        'user': 'postgres',
        'password': 'Magnus725!',
        'host': 'localhost',
        'port': 5432
        }

    connection = psycopg2.connect(**params)
    return connection

# 3.4 Create a function that can fetch data from the database and print it to the 
# console. Commit to remote repo. 
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
def insertcontact(first_name, last_name, title, organization, contact_type, contact, contact_category):
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


if __name__ == '__main__':
#     3.5 Add a loop that makes the program ask for input. The input is a command to 
#         select between different functions. Commands could be: LIST, INSERT, 
#         DELETE. Commit to remote repo. 
    print("Available commands: LIST, INSERT, DELETE, QUIT")
    while True:
        
        command = input("Please enter a command: ")

        if command.upper() == 'QUIT':
            break
        elif command.upper() == 'INSERT':
            first_name = input("Insert first name please\n")
            last_name = input("Insert last name please\n")
            title = input("Insert title please\n")
            organization = input("Insert organization please\n")
            contact_type = input("Insert contact type please (Email, Phone, Skype, Instagram\n")
            contact = input("Insert contact information please\n")
            contact_category = input("Insert contact category please. (Home, Work, Fax)\n")
            if insertcontact(first_name, last_name, title, organization, contact_type, contact, contact_category):
                print(f"Contact with name {first_name} inserted successfully!")
            else:
                print("Error inserting contact.")
        elif command.upper() == 'LIST':
            pslist()
            
            