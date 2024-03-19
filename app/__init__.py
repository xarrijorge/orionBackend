from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
CORS(app)


from .views import auth, properties, units, firms, leases, work_orders, db

app.register_blueprint(auth.bp)
app.register_blueprint(properties.bp)
app.register_blueprint(units.bp)
app.register_blueprint(db.bp)
app.register_blueprint(work_orders.bp)