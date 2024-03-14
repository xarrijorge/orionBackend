from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)


from .views import auth, properties

app.register_blueprint(auth.bp)
app.register_blueprint(properties.bp)