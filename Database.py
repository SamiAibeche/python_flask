import mysql.connector
import os
from dotenv import load_dotenv
from mysql.connector import Error

load_dotenv()  # Load environment variables from .env file


class Database:
    def __init__(self):

        self.DB_HOST = os.getenv("DB_HOST")
        self.DB_USER = os.getenv("DB_USER")
        self.DB_PASSWORD = os.getenv("DB_PASSWORD")
        self.DB_NAME = os.getenv("DB_NAME")

    def connect_db(self):

        # MySQL CONNECT
        config = {
            'user': self.DB_USER,
            'password': self.DB_PASSWORD,
            'database': self.DB_NAME,
            'host': self.DB_HOST,
            'unix_socket': '/Applications/MAMP/tmp/mysql/mysql.sock',
            'raise_on_warnings': True
        }

        try:
            cnx = mysql.connector.connect(**config)
            # cursor = cnx.cursor(dictionary=True)

        except Error as e:
            print(f"Error: {e}")

        finally:
            # Close the connection and cursor
            if cnx.is_connected():
                # cursor.close()
                # cnx.close()
                print("MySQL connection is closed.")

        return cnx

    def fetch_all(self):

        myDb = Database()

        cnx = myDb.connect_db()

        cursor = cnx.cursor(dictionary=True)

        cursor.execute('SELECT `id`, `lastname`, `firstname`, `gender`, `email`, `message`, `subjects` FROM `users`')

        return cursor.fetchall()

    def fetch_one_by(self, id):

        myDb = Database()

        connection = myDb.connect_db()
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            query = "SELECT gender, firstname, lastname, email, message, subjects, country FROM users WHERE id=%s"
            args = (id,)  # Correctly form a single-element tuple
            cursor.execute(query, args)

            result = cursor.fetchone()  # Use fetchone() instead of fetchall() for a single result
            cursor.close()
            connection.close()
            return result

    def delete_one_by(self, id):

        myDb = Database()

        connection = myDb.connect_db()
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            query = "DELETE FROM users WHERE id=%s"
            args = (id,)  # Correctly form a single-element tuple
            cursor.execute(query, args)

            connection.commit()
            cursor.close()
            connection.close()

    def insert_datas(self, gender, firstname, lastname, email, message, subjects, country='Be'):

        myDb = Database()

        connection = myDb.connect_db()

        if connection.is_connected():
            # PREVENT SQL INJECTION BY PREPARING THE SQL QUERY
            query = "INSERT INTO users (gender, firstname, lastname, email, message, subjects, country) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            args = (gender, firstname, lastname, email, message, subjects, country)

            # Create a cursor and execute the SQL statement
            cursor = connection.cursor()

            cursor.execute(query, args)
            # Commit the transaction
            connection.commit()
            print("Session data inserted successfully.")

    def update_datas(self, gender, firstname, lastname, email, message, subjects, id, country='Be'):

        myDb = Database()

        connection = myDb.connect_db()

        if connection.is_connected():
            # PREVENT SQL INJECTION BY PREPARING THE SQL QUERY
            query = "UPDATE users SET `gender` = %s, `firstname` = %s, `lastname` = %s, `email` = %s, `message` = %s, `subjects` = %s, `country` = %s WHERE  `id` = %s"
            args = (gender, firstname, lastname, email, message, subjects, id, country)

            # Create a cursor and execute the SQL statement
            cursor = connection.cursor()

            cursor.execute(query, args)
            # Commit the transaction
            connection.commit()
            print("Session data inserted successfully.")
