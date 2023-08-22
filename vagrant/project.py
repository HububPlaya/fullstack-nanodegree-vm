from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Restaurant, MenuItem, Base

app = Flask(__name__)


engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

@app.route('/')
@app.route('/hello')
def hello_world():  # Changed function name to follow Flask naming convention
    restaurant = session.query(Restaurant).first()
    items = session.query(MenuItem).filter_by(id = restaurant.id)
    message= ''
    for item in items:
        message += item.name
        message += '<br>'
        return message
    
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
