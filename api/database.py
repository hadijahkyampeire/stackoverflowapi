"""Database queries"""
import psycopg2

class Database:
    """class that holds all the queries"""

    def __init__(self):
        """initializes the connection to the db"""
        self.connection = psycopg2.connect(
            database="stackoverflow", user="postgres", host="localhost", password="0000", port="5432"
        )
        #for pointing/connecting to the db
        self.cursor = self.connection.cursor()

    def create_tables(self):
        """creates all the tables for the db"""
        create_table = "CREATE TABLE IF NOT EXISTS users\
        ( user_id SERIAL PRIMARY KEY, username VARCHAR(15), email VARCHAR(100), password VARCHAR(25))"
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
        FOREIGN KEY (user_id) REFERENCES users (user_id) ON UPDATE CASCADE ON DELETE CASCADE)"
        self.cursor.execute(create_table)
        self.connection.commit()
        self.connection.close()

    def insert_user_data(self,username, email, password ):
        """inserting data"""
        user_query = "INSERT INTO users (username, email, password) VALUES\
         ('{}', '{}', '{}');".format(username, email, password)
        self.cursor.execute(user_query)
        self.connection.commit()
        self.connection.close()

    def get_by_argument(self, table, column_name,argument):
        query = "SELECT * FROM {} WHERE {} = '{}';".format(table, column_name, argument)
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        print(result)
        return result


    
    
