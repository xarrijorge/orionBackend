import sys
import os

# Add the directory containing your Flask app to the Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))

# Import your Flask app
from app import app  # Replace 'app' with the actual name of your Flask application

# Define the application callable for WSGI server (Gunicorn, uWSGI, etc.)
application = app
