import sqlite3

def dict_factory(cursor, row):
    d ={}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


class showsDB:
    def __init__(self):
        self.connection = sqlite3.connect("shows_db.db")
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()

    def insertShow(self, name, genre, status, rating):
        data = [name, genre, status, rating]
        self.cursor.execute("INSERT INTO shows (name, genre, status, rating) VALUES (?, ?, ?, ?)", data)
        self.connection.commit()

    def getShows(self):
        self.cursor.execute("SELECT * FROM shows")
        result = self.cursor.fetchall()
        return result

    def getOneShow(self, shows_id):
        data = [shows_id]
        self.cursor.execute("SELECT * FROM shows WHERE id = ?", data)
        result = self.cursor.fetchone()
        return result

    def deleteShows(self, shows_id):
        data = [shows_id]
        self.cursor.execute("DELETE FROM shows WHERE id = ?", data)
        self.connection.commit()

    def editShows(self, shows_id, name, genre, status, rating):
        data = [name, genre, status, rating, shows_id]
        print(data)
        self.cursor.execute("UPDATE shows SET name = ?, genre = ?, status = ?, rating = ? WHERE id = ?" , data)
        self.connection.commit()
