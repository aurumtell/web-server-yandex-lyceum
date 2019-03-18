class NewsModel:
    def __init__(self, connection):
        self.connection = connection

    def init_table(self):
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS news 
                                (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                                 date VARCHAR(100),
                                 content VARCHAR(1000),
                                 user_name varchar(100),
                                 user_avatar varchar (50)
                                 )''')
        cursor.close()
        self.connection.commit()

    def insert(self, time, content, uname, avatar):
        cursor = self.connection.cursor()
        cursor.execute('''INSERT INTO news 
                          (date, content, user_name, user_avatar) 
                          VALUES (?,?,?,?)''''''''''', (time, content, uname, avatar))
        cursor.close()
        self.connection.commit()

    def get(self, news_id):
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM news WHERE id = ?", (str(news_id),))
        row = cursor.fetchone()
        return row

    def get_all(self, username=None):
        cursor = self.connection.cursor()
        if username:
            cursor.execute("SELECT * FROM news WHERE user_name = ?", (username,))
        else:
            cursor.execute("SELECT * FROM news")
        rows = cursor.fetchall()
        return rows

    def get_likes(self, news_id):
        pass

    def delete(self, news_id):
        cursor = self.connection.cursor()
        cursor.execute('''DELETE FROM news WHERE id = ?''', (str(news_id),))
        cursor.close()
        self.connection.commit()

    def delete_all(self, user_id=None):
        cursor = self.connection.cursor()
        if user_id:
            cursor.execute('''DELETE FROM news WHERE id = ?''', (user_id,))
        else:
            cursor.execute("DELETE FROM news")
        cursor.close()
        self.connection.commit()
