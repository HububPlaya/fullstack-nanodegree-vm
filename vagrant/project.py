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
@app.route('/restaurants/<int:restaurant_id>/')
def restaurant_menu(restaurant_id=None):  # Make the parameter optional with default None
    if restaurant_id is None:
        return "Welcome to the restaurant menu!"
    
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).first()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    message = ''
    for item in items:
        message += item.name
        message += '<br>'
    return message

@app.route('/restaurants/<int:restaurant_id>/new/')
def newMenuItem(restaurant_id):
    return "page to create a new menu item. Task 1 complete!"

# Task 2: Create route for editMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
    return "page to edit a menu item. Task 2 complete!"

# Task 3: Create a route for deleteMenuItem function here

@app.route('/restaurants/<int:restaurant_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
    return "page to delete a menu item. Task 3 complete!"
if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)
