import sqlite3

# This class is a simple handler for all of our SQL database actions
# Practicing a good separation of concerns, we should only ever call 
# These functions from our models

# If you notice anything out of place here, consider it to your advantage and don't spoil the surprise

class SQLDatabase():
    '''
        Our SQL Database

    '''

    # Get the database running
    def __init__(self, database_arg=":memory:"):
        self.conn = sqlite3.connect(database_arg, check_same_thread=False)
        self.cur = self.conn.cursor()

    # SQLite 3 does not natively support multiple commands in a single statement
    # Using this handler restores this functionality
    # This only returns the output of the last command
    def execute(self, sql_string):
        out = None
        data = None
        for string in sql_string.split(";"):
            try:
                out = self.cur.execute(string)
                data = self.cur.fetchone()
            except:
                pass
        return data

    # Commit changes to the database
    def commit(self):
        self.conn.commit()

    #-----------------------------------------------------------------------------
    
    # Sets up the database
    # Default admin password
    def database_setup(self, admin_password='admin'):

        # Clear the database if needed
        self.execute("DROP TABLE IF EXISTS Users")
        self.commit()

        # Create the users table
        self.execute("""CREATE TABLE Users(
            username TEXT,
            password TEXT,
            friend TEXT,
            admin INTEGER DEFAULT 0
        )""")

        self.commit()

        # Add our admin user
        self.add_user('admin', admin_password, friend=None, admin=1,)

    #-----------------------------------------------------------------------------
    # User handling
    #-----------------------------------------------------------------------------

    # Add a user to the database
    def add_user(self, username, password, friend, admin=0):
        sql_cmd = """
                INSERT INTO Users(username, password, friend, admin)
                VALUES('{username}', '{password}', {admin}, '{friend}')
            """

        sql_cmd = sql_cmd.format(username=username, password=password, friend=friend, admin=admin)

        self.execute(sql_cmd)
        self.commit()
        return True

    # Add a user to the database
    def add_friend(self, username, friend):
        sql_cmd = """
                INSERT INTO Users(username, friend)
                VALUES('{username}', '{friend}')
            """

        sql_cmd = sql_cmd.format(username=username, friend=friend)

        self.execute(sql_cmd)
        self.commit()
        return True
    #-----------------------------------------------------------------------------

    # Check login credentials
    def check_username(self, username):
        sql_query = """
                SELECT 1 
                FROM Users
                WHERE username = '{username}'
            """

        sql_query = sql_query.format(username=username)
        data = self.execute(sql_query)
        #data = self.cur.fetchone()[0]
        print(data)

        # If our query returns
        if not data is None:
            return False
        else:
            return True


    # Check login credentials
    def check_credentials(self, username, password):
        sql_query = """
                SELECT username
                FROM Users
                WHERE username = '{username}' AND password = '{password}'
            """

        sql_query = sql_query.format(username=username, password=password)
        #data = self.cur.fetchone()[0]
        data = self.execute(sql_query)
        print(data)
        # If our query returns
        if not data is None:
            return True
        else:
            return False
    
    def get_friend(self, username):
        sql_query = """
                SELECT friend
                FROM Users
                WHERE username = '{username}'
            """
        sql_query = sql_query.format(username=username)
        #data = self.cur.fetchone()[0]
        data = self.execute(sql_query)
        if not data is None:
            return True
        else:
            return False