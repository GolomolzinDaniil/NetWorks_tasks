from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

from parser import parse


app = Flask(__name__)

DBASE_URL = 'postgresql://danya:123@golom_dbase_cont:5432/dbase'

engine = create_engine(DBASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class Book(Base):

    __tablename__ = 'books'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(String)
    availability = Column(String)
    url = Column(String)

Base.metadata.create_all(bind=engine)


def save_to_db(data):

    with SessionLocal() as session:
        try:
            for item in data:
                book = Book(
                    name=item['name'],
                    price=item['price'],
                    availability=item['availability'],
                    url=item['url']
                )
                session.add(book)
            session.commit()
            return 'success'
        except:
            return 'error'

    
@app.route('/parse')
def parsing():
    
    url = request.args.get('url', r'http://books.toscrape.com/')
    num_page = request.args.get('page', 3, type=int)

    data = parse(num_page, url)
    if not data:
        return jsonify({'status': 'error', 'source': 'parser'})

    status_save_to_db = save_to_db(data)
    return jsonify({'status': f'{status_save_to_db}', 'source': 'save_to_db'})


@app.route('/get_data')
def get_all_data():
    with SessionLocal() as session:
        try:
            books = session.query(Book).all()
            result = []
            for book in books:
                result.append(
                    {
                        'id': book.id,
                        'name': book.name,
                        'availability': book.availability,
                        'url': book.url
                    }
                )
            return result
        except:
            return jsonify({'status': 'error', 'source': 'get_data'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8008, debug=True)