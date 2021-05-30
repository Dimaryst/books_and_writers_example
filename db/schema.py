from sqlalchemy import (
    Column, ForeignKey, Integer,
    String, MetaData, create_engine
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
username = 'user'
engine = create_engine(f"postgresql://{username}@localhost:5432/postgres")
meta = MetaData()
Base = declarative_base()


class Writer(Base):
    __tablename__ = 'writers'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)


class Book(Base):
    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey('writers.id'))
    name = Column(String, nullable=False)
    writer = relationship("Writer", back_populates="books")


def fill_db():
    Writer.books = relationship("Book", order_by=Book.id, back_populates="writer")
    Base.metadata.create_all(engine)

    dostoyevsky = Writer(name='Fyodor M. Dostoevsky')
    dostoyevsky.books = [Book(name='The Idiot'), Book(name='Notes from Underground')]

    salinger = Writer(name='Jerome D. Salinger')
    salinger.books = [Book(name='The Catcher in the Rye'), Book(name='Nine Stories')]

    bulgakov = Writer(name='Mikhail A. Bulgakov')
    bulgakov.books = [Book(name='The Master and Margarita'), Book(name='Heart of a Dog')]

    Session = sessionmaker(bind=engine)
    session = Session()
    session.add(dostoyevsky), session.add(salinger), session.add(bulgakov)
    session.commit()
