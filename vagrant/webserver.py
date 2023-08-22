from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = "<html><body>"
                output += "<h1>Make a New Restaurant</h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
                output += "<input name='newRestaurantName' type='text' placeholder='New Restaurant Name'>"
                output += "<input type='submit' value='Create'>"
                output += "</form></body></html>"
                self.wfile.write(output.encode('utf-8'))
                return

            if self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>{}</h1>".format(myRestaurantQuery.name)
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/{}/edit'>".format(restaurantIDPath)
                    output += "<input name='newRestaurantName' type='text' placeholder='{}'>".format(myRestaurantQuery.name)
                    output += "<input type='submit' value='Rename'>"
                    output += "</form></body></html>"
                    self.wfile.write(output.encode('utf-8'))

            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>Are you sure you want to delete {}?</h1>".format(myRestaurantQuery.name)
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/{}/delete'>".format(restaurantIDPath)
                    output += "<input type='submit' value='Delete'>"
                    output += "</form></body></html>"
                    self.wfile.write(output.encode('utf-8'))

            if self.path.endswith("/restaurants"):
                restaurants = session.query(Restaurant).all()
                output = "<html><body>"
                output += "<a href='/restaurants/new'>Make a New Restaurant Here</a><br><br>"
                for restaurant in restaurants:
                    output += "{}<br>".format(restaurant.name)
                    output += "<a href='/restaurants/{}/edit'>Edit</a><br>".format(restaurant.id)
                    output += "<a href='/restaurants/{}/delete'>Delete</a><br><br>".format(restaurant.id)
                output += "</body></html>"
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(output.encode('utf-8'))
                return
        except IOError:
            self.send_error(404, 'File Not Found: {}'.format(self.path))

    def do_POST(self):
        try:
            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if myRestaurantQuery:
                    session.delete(myRestaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()

            if self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
                if ctype == 'multipart/form-data':
                    content_length = int(self.headers.get('content-length'))
                    pdict['CONTENT-LENGTH'] = content_length
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')
                    restaurantIDPath = self.path.split("/")[2]

                    myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                    if myRestaurantQuery:
                        myRestaurantQuery.name = messagecontent[0].decode('utf-8')
                        session.add(myRestaurantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurants')
                        self.end_headers()
                    if self.path.endswith("/restaurants/new"):
                        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
                        if ctype == 'multipart/form-data':
                            content_length = int(self.headers.get('content-length'))
                            pdict['CONTENT-LENGTH'] = content_length
                            fields = cgi.parse_multipart(self.rfile, pdict)
                            messagecontent = fields.get('newRestaurantName')

                            # Create new Restaurant Object
                            newRestaurant = Restaurant(name=messagecontent[0].decode('utf-8'))
                            session.add(newRestaurant)
                            session.commit()

                            self.send_response(301)
                            self.send_header('Content-type', 'text/html')
                            self.send_header('Location', '/restaurants')
                            self.end_headers()
        except:
            pass
def main():
    try:
        server = HTTPServer(('localhost', 8080), WebServerHandler)
        print('Web server running... Open http://localhost:8080/restaurants in your browser')
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down server')
        server.socket.close()
        
if __name__ == '__main__':
    main()

                    