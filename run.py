from flask import Flask
from routes import configure_routes

app = Flask(__name__)
app.config.from_object("config.TestingConfig")

configure_routes(app)

if __name__ == "__main__":
    app.run()