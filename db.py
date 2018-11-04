import sqlite3
from uuid import uuid4

DB_NAME = 'cyber_guild.db'

def drop_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        DROP TABLE IF EXISTS users;          
    ''')
    conn.commit()
    conn.close()


def create_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE users (
            id int,
            username varchar(255),
            password varchar(255),
            greeting varchar(255),
            realname varchar(255),
            banknumber varchar(16)
        );
    ''')

    users = [(1, "ncr", "password", "Welcome to the application", "John Smith", "0123456789abcdef"),
             (2, "admin", "reallysecurepassword", "You are the admin", "Jane Doe", "0123456789abcdef"),
             (3, "connections", "cxpassword", "Welcome to the Connections account", "Pam Beasely", "7438291756473222")]
    c.executemany('''
        INSERT INTO users VALUES (?,?,?,?,?,?)
    ''', users)
    conn.commit()
    conn.close()


def get_user(username, password):
    sql_stmt = "SELECT username, greeting, realname, banknumber FROM users WHERE username = '%s' AND password = '%s'" % (username, password)
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    try:
        c.execute(sql_stmt)
        row = c.fetchall()
        if row:
            return [ dict(zip(r.keys(), r)) for r in row ]
        else:
            return None
    except Exception as e:
        error = '''
            Error with statement: %s
        ''' % (sql_stmt)
        raise Exception(error)


if __name__ == '__main__':
    drop_db()
    create_db()
