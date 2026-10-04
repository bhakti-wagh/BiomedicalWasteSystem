import mysql.connector


def get_db_connection():
    connection = mysql.connector.connect(
    host="localhost",
    port=3300,
    user="root",
    password="bhakti6000",
    database="biomedical_waste_db"
)
    return connection

connection = get_db_connection()

if connection.is_connected():
    print("MySQL Database Connected Successfully!")

connection.close()