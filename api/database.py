"""Database queries"""
import psycopg2
from flask import current_app as app

class Database:
    """class that holds all the queries"""

    def __init__(self, url='postgresql://postgres:0000@localhost:5432/stackoverflow'):
        """initializes the connection to the db"""
        self.connection = psycopg2.connect(
            database="stackoverflow", user="postgres", host="localhost", password="0000", port="5432"
        )
        #for pointing/connecting to the db
        self.cursor = self.connection.cursor()

    def create_tables(self):
        """creates all the tables for the db"""
        create_table = "CREATE TABLE IF NOT EXISTS users\
        ( user_id SERIAL PRIMARY KEY, username VARCHAR(15), email VARCHAR(100), password VARCHAR(100))"
        self.cursor.execute(create_table)

        create_table = "CREATE TABLE IF NOT EXISTS questions\
        (question_id SERIAL PRIMARY KEY, user_id INTEGER NOT NULL, \
        FOREIGN KEY (user_id) REFERENCES users (user_id) ON UPDATE CASCADE ON DELETE CASCADE,\
        title VARCHAR(255), description VARCHAR(255), date TIMESTAMP NOT NULL)"
        self.cursor.execute(create_table)

        create_table = "CREATE TABLE IF NOT EXISTS answers\
        (answer_id SERIAL PRIMARY KEY, question_id INTEGER NOT NULL, \
        FOREIGN KEY (question_id) REFERENCES questions (question_id) ON UPDATE CASCADE ON DELETE CASCADE,\
        reply VARCHAR(255), user_id INTEGER NOT NULL, \
        FOREIGN KEY (user_id) REFERENCES users (user_id) ON UPDATE CASCADE ON DELETE CASCADE,\
        preffered VARCHAR(255) DEFAULT 'False')"
        self.cursor.execute(create_table)
        self.connection.commit()
        # self.connection.close()

    def insert_user_data(self,username, email, password ):
        """inserting data"""
        user_query = "INSERT INTO users (username, email, password) VALUES\
         ('{}', '{}', '{}');".format(username, email, password)
        self.cursor.execute(user_query)
        self.connection.commit()
        # self.connection.close()

    def get_by_argument(self, table, column_name,argument):
        query = "SELECT * FROM {} WHERE {} = '{}';".format(table, column_name, argument)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        return result
    
    def insert_question_data(self, user_id, title, description, date):
        """Insert a new question to the database"""
        query = "INSERT INTO questions (user_id, title, description, date)\
         VALUES('{}','{}', '{}','{}' );".format(user_id, title, description, date)
        self.cursor.execute(query)
        self.connection.commit()

    def fetch_all(self):
        """ Fetches all questions from the database"""
        self.cursor.execute("SELECT * FROM questions ")
        rows = self.cursor.fetchall()
        questions = []
        for row in rows:
            row = {'question_id': row[0], 'user_id': row[1],
                   'title': row[2],
                   'description': row[3]
                   }
            questions.append(row)
        return questions

    def query_all_where_id(self, table_name, table_column, item_id):
        """method selects all records from a database matching a value
        select * from table_name where table_column = item_id"""
        self.cursor.execute("(SELECT * FROM {} WHERE {} = '{}');".format(
            table_name, table_column, item_id))
        items = self.cursor.fetchall()
        return items

    def insert_answer_data(self, question_id, reply, user_id):
        """Insert a new question to the database"""
        query = "INSERT INTO answers (question_id, reply, user_id)\
         VALUES('{}','{}', '{}' );".format(question_id, reply, user_id)
        self.cursor.execute(query)
        self.connection.commit()

    def delete_question(self, question_id):
        """method deletes question from database"""
        delete_answers = "DELETE FROM answers WHERE question_id = {}".format(
            question_id)
        self.cursor.execute(delete_answers)
        delete_query = "DELETE FROM questions WHERE question_id = {}" .format(
            question_id)
        self.cursor.execute(delete_query)

    def update_answer_record(self, table_name, set_column, new_value, where_column, item_id):
        """method updates record. i.e UPDATE table_name SET set_column = new_value, where
        where_colum = item_id"""
        update_command = "Update {} SET {} = '{}' WHERE {} = '{}'".format(table_name,
                                                                      set_column, new_value, where_column, item_id)
        self.cursor.execute(update_command)
        self.connection.commit()

    def drop(self, table):
        query = "DROP TABLE IF EXISTS {} CASCADE;".format(table)
        self.cursor.execute(query)