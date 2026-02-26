import json
import sqlite3

class UserStore:
    def __init__(self, db_path):
        self.db_path= db_path
        self.init_db()

    def _get_connection(self):
        conn= sqlite3.connect(self.db_path)
        conn.row_factory= sqlite3.Row
        return conn
    
    #create user table
    def init_db(self):
        with self._get_connection() as conn:
            cursor= conn.cursor()
            cursor.execute("""CREATE TABLE IF NOT EXISTS users
                           (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           name TEXT NOT NULL)""")
            conn.commit()

    #return list of user dicts from database
    def load(self):
        with self._get_connection() as conn:
            cursor= conn.cursor()
            cursor.execute("SELECT * FROM users")
            rows= cursor.fetchall()
            #conveert sqlite rows into stardard py dicts
            return [dict(row) for row in rows]
        
    #insert/update users in database
    def save(self, users):
        with self._get_connection() as conn:
            cursor= conn.cursor()
            for user in users:
                #insert or replace
                cursor.execute("""INSERT OR REPLACE INTO users (id, name)
                               VALUES (?, ?)""",
                               (user.get("id"), user.get("name")))
                conn.commit()

    #return user dict or none using sql query
    def find_by_id(self, user_id):
        with self._get_connection() as conn:
            cursor= conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row= cursor.fetchone()
            if row:
                return dict(row)
            return None
        
    ##Extension##

    #update user by id using sql UPDATE statement
    def update_user(self, user_id, updated_data):
        with self._get_connection() as conn:
            cursor= conn.cursor()
            if "name" in updated_data:
                cursor.execute("""UPDATE users SET name = ? WHERE id= ?""",
                               (updated_data["name"], user_id))
                conn.commit()
                #return True if at least one row is updated successfully
                return cursor.rowcount > 0
        return False
    
    #remove user by id using sql DELETE statement
    def delete_user(self, user_id):
        with self._get_connection() as conn:
            cursor= conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()

            return cursor.rowcount > 0
        
        
