import os
import sqlite3

class DB:
    db = "test.db"
    table = 'wordlist'
    p_db = '.DB'

    def __init__(self):
        if(not os.path.isdir(self.p_db)):
            os.makedirs(self.p_db, exist_ok=True)
        self.conn = sqlite3.connect(os.path.join(self.p_db, self.db))
        self.__create()        

    def __create(self):
        c = self.conn.cursor()
        # Create table
        c.execute(f'''CREATE TABLE IF NOT EXISTS {self.table}
            (ID INTEGER PRIMARY KEY AUTOINCREMENT, Type text, Tr text, En text)''')
        # Save (commit) the changes
        self.conn.commit()

    def fetch(self):
        c = self.conn.cursor()
        # Create table
        c.execute(f'''SELECT * FROM {self.table}''')
        return c.fetchall()
        

    def delete(self, id=None):
        c = self.conn.cursor()
        q = f"DELETE FROM {self.table}"
        if id is not None:
            q += f" WHERE id={id}"
        c.execute(q)
        self.conn.commit()
    
    def append(self, Type, Tr, En):
        c = self.conn.cursor()
        c.execute(f"INSERT INTO {self.table} ('Type', 'Tr', 'En') VALUES ('{Type}', '{Tr}', '{En}')")
        self.conn.commit()

    def resetID(self):
        c = self.conn.cursor()
        q = f"""UPDATE SQLITE_SEQUENCE SET seq = 0 WHERE name = '{self.table}'"""
        c.execute(q)
        self.conn.commit()

    def close(self):
        # We can also close the connection if we are done with it.
        # Just be sure any changes have been committed or they will be lost.
        self.conn.close()


if __name__ == '__main__':
    db = DB()

    db.delete()
    db.resetID()

    for i in range(25):
        db.append(f"type-{i}", f"tr-{i}", f"en-{i}")

    for i in db.fetch():
        print(*i)
    