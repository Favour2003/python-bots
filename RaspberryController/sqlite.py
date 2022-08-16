import sqlite3
from dbGestione import admins

conn = sqlite3.connect('users.db', check_same_thread=False)

c = conn.cursor()

class db:
    @staticmethod
    def insert_admin(admin):
        with conn:
            c.execute("INSERT INTO admins VALUES (?, ?, ?)", (admin.id, admin.username, admin.password))
    @staticmethod
    def get_admin(uname, password):
        with conn:
            c.execute("SELECT * FROM admins WHERE username=:username AND password=:password", {'username':uname, 'password':password})
            admin = c.fetchone()
            return admin
    @staticmethod
    def remove_admin(uname):
        with conn:
            c.execute("DELETE FROM admins WHERE username=:username", {'username':uname})
    @staticmethod
    def get_last_id():
        with conn:
            c.execute("SELECT id FROM admins ORDER BY id desc")
            last_id = c.fetchone()
            return last_id[0] 

# c.execute("""CREATE TABLE admins (
#    id INTEGER PRIMARY KEY AUTOINCREMENT,
#    username TEXT NOT NULL,
#    password TEXT NOT NULL
# #     )""")
#yo = admins('2', 'ye', 'ye')

# insert_admin(yo)

with conn:    
    boo = db()
    gay = boo.get_admin('pippo', 'pippo')
    c.execute("SELECT * FROM admins WHERE username='pippo' AND password='pippo'")
    print(gay)

#conn.close()