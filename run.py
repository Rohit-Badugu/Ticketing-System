from flask import Flask
from routes import configure_routes

#Creating an instance of Flask object
app = Flask(__name__)

#Setting the configuation from config file
app.config.from_object("config.TestingConfig")

#Load the app routes
configure_routes(app)

#Start the app
if __name__ == "__main__":
    app.run()