from flask import jsonify
from app import app  # Import the app instance
import psycopg2

@app.route('/users')
def users():
    try:
        # Connect to the database using app configuration
        conn = psycopg2.connect(
            dbname=app.config['SQLALCHEMY_DATABASE_URI'].split('/')[-1],
            user=app.config['SQLALCHEMY_DATABASE_URI'].split('://')[1].split(':')[0],
            password=app.config['SQLALCHEMY_DATABASE_URI'].split(':')[2].split('@')[0],
            host=app.config['SQLALCHEMY_DATABASE_URI'].split('@')[1].split(':')[0],
            port=app.config['SQLALCHEMY_DATABASE_URI'].split(':')[3].split('/')[0]
       
        )
        cur = conn.cursor()

        # Execute SQL query
        cur.execute("SELECT id, created_at, username, email FROM users")
        users = cur.fetchall()

        # Close the cursor and connections
        cur.close()
        conn.close()

        # Return data as JSON
        return jsonify(users)
    except Exception as e:
        # Handle any exceptions
        return f"Error: {e}"


@app.route('/test')
def test():
    return 'Hello, World!'