from flask import Flask
from config import Config
from Flask-SQLAlchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from app.models import *

# Import routes after creating the Flask app to avoid circular imports
from app.routes import *

if __name__ == '__main__':
    app.run(debug=True)