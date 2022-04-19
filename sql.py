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
                data = self.cur.fetchall()
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
            friend JSON,
            admin INTEGER DEFAULT 0
        )""")

        self.commit()

        # Add our admin user
        self.add_user('admin', admin_password, friend=None, admin=1)

    #-----------------------------------------------------------------------------
    # User handling
    #-----------------------------------------------------------------------------

    # Add a user to the database
    def add_user(self, username, password, index=0, friend=None, admin=0):
        print("password: ")
        print(password)
        sql_cmd = """
                INSERT INTO Users(username, password, friend, admin)
                VALUES('{username}', '{password}', '{friend}', {admin})
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
        data = self.execute(sql_cmd)
        print("add_friend:")
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
        print("Check useraname:", data)
        print(len(data))
        # If our query returns
        if not len(data) == 0:
            return False
        else:
            print("Check_username:","true")
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
        print("check credentials:", data)
        # If our query returns
        if not len(data) == 0:
            return False
        else:
            return True
    
    def get_friend(self, username):
        sql_query = """
                SELECT friend
                FROM Users
                WHERE username = '{username}'
            """
        sql_query = sql_query.format(username=username)
        #data = self.cur.fetchone()[0]
        data = self.execute(sql_query)
        data = self.remove_none(data)
        print("get_friend:", data)
        return data
    
    def get_pwd(self, username):
        sql_query = """
                SELECT password
                FROM Users
                WHERE username = '{username}'
            """
        sql_query = sql_query.format(username=username)
        print(sql_query)
        data = self.execute(sql_query)
        data = self.remove_none(data)
        print("get_pwd:", data)
        # if not data is None:
        #     return True
        # else:
        #     return False
        return data
    
    def show_values(self):
        sql_query = """
                SELECT *
                FROM Users
            """
        sql_query = sql_query.format()
        data = self.execute(sql_query)
        print("show values:", data)
        # if not data is None:
        #     return True
        # else:
        #     return False
        return data
    
    def show_info(self, username):
        sql_query = """
                SELECT *
                FROM Users
                WHERE username = '{username}'
            """
        sql_query = sql_query.format(username=username)
        data = self.execute(sql_query)
        print("show values:", data)
        # if not data is None:
        #     return True
        # else:
        #     return False
        return data
    
    def remove_none(self, data):
        new_data = []
        if not data is None:
            for value in data:
                print("remove_none:", value)
                if not value[0] == 'None':
                    new_data.append(value)
        return new_data