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
def pslist(query):
    connection = psconnect()
    cursor = connection.cursor()
    cursor.execute(query)
    list_for_printing = cursor.fetchall()
    for item in list_for_printing:
        print(item)

    return None

if __name__ == '__main__':
    query = """
    SELECT * FROM CONTACTS;
    """
    pslist(query)