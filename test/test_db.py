import sqlite3 #Import the SQLite3 module
import os
def create_db():
    try:
        # Creates or opens a file called mydb with a SQLite3 DB
        db = sqlite3.connect('../src/database/testDB')
        # Get a cursor object
        cursor = db.cursor()
        # Check if table users does not exist and create it
        cursor.execute('''CREATE TABLE IF NOT EXISTS
                            locations(id INTEGER PRIMARY KEY, name TEXT)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS
                            ingredients(id INTEGER PRIMARY KEY, name TEXT, amount INTEGER, location_id INTEGER)''')
        
        cursor.execute('''INSERT INTO locations VALUES (1, 'Food1')''')
        cursor.execute('''INSERT INTO locations VALUES (2, 'Food3')''')
        cursor.execute('''INSERT INTO locations VALUES (3, 'Food3')''')
        
        cursor.execute('''INSERT INTO ingredients VALUES (1, 'Ham', 34, 1)''')
        cursor.execute('''INSERT INTO ingredients VALUES (2, 'Ham', 21, 2)''')
        cursor.execute('''INSERT INTO ingredients VALUES (3, 'Ham', 0, 3)''')
        cursor.execute('''INSERT INTO ingredients VALUES (4, 'Sauce', 24, 1)''')
        cursor.execute('''INSERT INTO ingredients VALUES (5, 'Sauce', 34, 3)''')



        # Commit the change
        db.commit()
        #Testing the input
        #cursor.execute('''SELECT name, amount, location_id FROM ingredients''')
        #for row in cursor:
        # row[0] returns the first column in the query (name), row[1] returns email column.
            #print('{0} : {1}, {2}'.format(row[0], row[1], row[2]))



    # Catch the exception
    except Exception as e:
        # Roll back any change if something goes wrong
        db.rollback()
        raise e
    finally:
        # Close the db connection
        db.close()

def delete_db():
    os.remove('../src/database/testDB')

#if __name__ == '__main__':
#    create_db()
#    delete_db()
