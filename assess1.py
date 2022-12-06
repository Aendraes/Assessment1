import psycopg2

def psconnect():
    params = {
        'dbname': 'website_database',
        'user': 'postgres',
        'password': '',
        'host': 'localhost',
        'port': 5432
        }

    connection = psycopg2.connect(**params)
    return connection
