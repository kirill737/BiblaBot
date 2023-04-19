from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, MetaData, Table, func, select, desc, func, insert
import json, psycopg2
from datetime import datetime
from database.models import *

__all__ = ["DatabaseConnector"]

PORT =  5432
class DatabaseConnector():
    
    connection_string = f"postgresql+psycopg2://:@localhost:{PORT}/biblabot"

    def __init__(self, dbname, host, port):
        self.dbname = dbname
        self.host = host
        self.port = port

    def add(self, title, author, published):
        conn = psycopg2.connect(dbname=self.dbname, host=self.host, port=self.port)
        cur = conn.cursor()
        date_added = datetime.strftime(datetime.now(), '%Y-%m-%d')
        cur.execute("INSERT INTO Books (title, author, published, date_added) VALUES (%s, %s, %s, %s) RETURNING book_id", (title, author, published, date_added))
        # cur.execute(f"INSERT INTO Books (title, author, published, date_added) VALUES ({title}, {author}, {published}, {date_added}) RETURNING book_id")
        # book_id = cur.fetchone()[0]
        conn.commit()
        
        cur.close()
        conn.close()
        
        # if book_id:
        #     return book_id
        # else:
        #     return False

    def delete(self, title, author, published):
        try:
            conn = psycopg2.connect(dbname=self.dbname,  host=self.host, port=self.port)
            cur = conn.cursor()
            date_deleted = datetime.strftime(datetime.now(), '%Y-%m-%d')
            cur.execute("UPDATE Books SET date_deleted = %s WHERE lower(title) = lower(%s) AND lower(author) = lower(%s) AND published = %s AND date_deleted IS NULL", (date_deleted, str(title), str(author), published))
            # book_id = cur.fetchone()[0]
            conn.commit()

            cur.close()
            conn.close()

            return True            
        except:
            return False

    def borrow(self, book_id, user_id):
        date_start = datetime.strftime(datetime.now(), '%Y-%m-%d')
        conn = psycopg2.connect(dbname=self.dbname, host=self.host, port=self.port)
        cur = conn.cursor()

        cur.execute("SELECT borrow_id FROM Borrows WHERE book_id = %s AND date_end IS NULL", (book_id,))
        already_borrowed = cur.fetchone()

        if already_borrowed:
            cur.close()
            conn.close()
            return False        
        cur.execute("SELECT borrow_id FROM Borrows WHERE user_id = %s AND date_end IS NULL", (user_id,))
        has_borrowed_book = cur.fetchone()

        if has_borrowed_book:
            cur.close()
            conn.close()
            return False        
        cur.execute("INSERT INTO Borrows (book_id, date_start, user_id) VALUES (%s, %s, %s) RETURNING borrow_id", (book_id, date_start, user_id))
        borrow_id = cur.fetchone()[0]
        conn.commit()

        cur.close()
        conn.close()

        return borrow_id

    def list_books(self):
        try:
            conn = psycopg2.connect(dbname=self.dbname, host=self.host, port=self.port)
            cur = conn.cursor()
            
            cur.execute("SELECT title, author, published, date_deleted FROM Books")
            books = cur.fetchall()
            
            cur.close()
            conn.close()
            return books
        
        except:
            return []

    def get_book(self, title, author, published):
        conn = psycopg2.connect(dbname=self.dbname, host=self.host, port=self.port)
        cur = conn.cursor()

        cur.execute("SELECT book_id FROM Books WHERE lower(title) = lower(%s) AND lower(author) = lower(%s) AND published = %s AND date_deleted IS NULL", (str(title), str(author), published))
        book_id = cur.fetchone()

        cur.close()
        conn.close()

        if book_id:
            return book_id[0]
        else:
            return None    

    def retrieve (self, borrow_id):
        date_end = datetime.strftime(datetime.now(), '%Y-%m-%d')
        conn = psycopg2.connect(dbname=self.dbname, host=self.host, port=self.port)
        cur = conn.cursor()

        cur.execute("UPDATE Borrows SET date_end = %s WHERE borrow_id = %s", (date_end, borrow_id))
        conn.commit()

        cur.close()
        conn.close()
    def get_borrow(self, user_id):
        conn = psycopg2.connect(dbname=self.dbname, host=self.host, port=self.port)
        cur = conn.cursor()

        cur.execute(f"SELECT borrow_id FROM Borrows WHERE user_id = {user_id} AND date_end IS NULL")
        borrow_id = cur.fetchone()

        cur.close()
        conn.close()


        if borrow_id:
            return borrow_id[0]
        else:
            return None
    def get_book_borrow(self, borrow_id):
        conn = psycopg2.connect(dbname=self.dbname, host=self.host, port=self.port)
        cur = conn.cursor()

        cur.execute(f'SELECT b.title, b.author, b.published FROM Books AS b JOIN Borrows AS br ON b.book_id = br.book_id WHERE br.borrow_id = {borrow_id}')
        book = cur.fetchone()

        cur.close()
        conn.close()

        if book:
            return book
        else:
            return None


# a = DatabaseConnector('biblabot', 'ticklera', 'localhost', 5433)
# # print(a.get_borrow(859301521))
# a.retrieve(1)
# # a.borrow(1, 100)
# t = a.get_book_borrow(1)
# print(t[0], t[1], t[2])
# print(a.get_book_borrow(1))
# print(a.get_book(1, 1, 5))
# a.add(1, 1, 6)
# a.delete(1, 1, 6)
# a.list_books()

