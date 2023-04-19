from sqlalchemy import MetaData, Integer, String, \
    Column, Date, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

__all__ = ["Book", "Borrow", "Base"]

# PORT = 5432
Base = declarative_base()
metadata = MetaData()

class Book(Base):
    __tablename__ = 'books'
    book_id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    author = Column(String(200), nullable=False)
    published = Column(Integer, nullable=False)
    date_added = Column(Date(), nullable=False)
    date_deleted = Column(Date(), nullable=True)

class Borrow(Base):
    __tablename__ = 'borrows'
    borrow_id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("books.book_id"), nullable=False)
    date_start = Column(Date, nullable=False)
    date_end = Column(Date, nullable=True)
    user_id = Column(Integer)
    book = relationship("Book")




