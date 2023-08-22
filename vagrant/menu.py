from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBsession = sessionmaker(bind = engine)
session = DBsession()

myFirstRestaurant = Restaurant(name = "Pizza Palace")
session.add(myFirstRestaurant)
session.commit()
session.query(Restaurant).all()


cheesepizza = MenuItem (
    name = "Pizza Place", 
    description = "Made with all natural ingridients and fresh mozarella",
    course = "Entree",
    price = "$8.99",
    restaurant = myFirstRestaurant
    )
session.add(cheesepizza)
session.commit()
session.query(MenuItem).all()

firstResult = session.query(Restaurant).first()
firstResult.name

session.query(Restaurant).all()

items = session.query(MenuItem).all()
for item in items:
    print(item.name)

veggieBurgers = session.query(MenuItem).filter_by(name = "Veggie Burger")
for veggieBurger in veggieBurgers:
    print(veggieBurger.id)
    print(veggieBurger.price)
    print(veggieBurger.restaurant.name)
    print("\n")

urbanVeggieBurgers = session.query(MenuItem).filter_by(id = 8).one()
print(urbanVeggieBurgers.price)

urbanVeggieBurgers.price = "$2.99"
session.add(urbanVeggieBurgers)
session.commit()

veggieBurgers = session.query(MenuItem).filter_by(name = "Veggie Burger")
for veggieBurger in veggieBurgers:
    print(veggieBurger.id)
    print(veggieBurger.price)
    print(veggieBurger.restaurant.name)
    print("\n")

for veggieBurger in veggieBurgers:
    if veggieBurger.price != "$2.99":
        veggieBurger.price = "$2.99"
        session.add(veggieBurger)
        session.commit()

veggieBurgers = session.query(MenuItem).filter_by(name = "Veggie Burger")
for veggieBurger in veggieBurgers:
    print(veggieBurger.id)
    print(veggieBurger.price)
    print(veggieBurger.restaurant.name)
    print("\n")

spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()
print(spinach.restaurant.name)

session.delete(spinach)
session.commit()

# spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()


