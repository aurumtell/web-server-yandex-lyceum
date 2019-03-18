class UsersModel:
    def __init__(self, connection):
        self.connection = connection

    def get_connection(self):
        return self.connection

    # def __del__(self):
    #     self.connection.close()

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                            (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                             email VARCHAR(50),
                             user_name VARCHAR(50),
                             password_hash VARCHAR(128),
                             img VARCHAR(128)
                             )''')
        # cursor.close()
        self.connection.commit()

    def insert(self, email, user_name, password_hash, img="twitter1.jpg"):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO users 
                          (email, user_name, password_hash, img) 
                          VALUES (?,?,?,?)''''''''', (email, user_name, password_hash, img))
        # cursor.close()
        self.connection.commit()

    def get_username(self, email):
        cursor = self.connection.cursor()
        cursor.execute("SELECT user_name FROM users WHERE email = ?", (email, ))
        row = cursor.fetchone()
        return row[0]

    def get_email(self, username):
        cursor = self.connection.cursor()
        cursor.execute("SELECT email FROM users WHERE user_name = ?", (username, ))
        row = cursor.fetchone()
        return row[0]

    def get_all(self):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
        return rows

    def exists(self, email, password_hash):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = ? AND password_hash = ?",
                       (email, password_hash))
        row = cursor.fetchone()
        return True if row else False

    def change_avatar(self, uname, img):
        cursor = self.connection.cursor()
        cursor.execute('''UPDATE users 
                            SET img = ?
                            WHERE user_name = ?;''', (img, uname))
        # cursor.close()
        self.connection.commit()

    def get_avatar(self, uname):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_name = ?",
                       (uname, ))
        row = cursor.fetchone()
        return row[4]

