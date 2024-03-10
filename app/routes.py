from flask import jsonify,  request
from app import app  # Import the app instance
import psycopg2


def connect_to_database():
    # Connect to the database using app configuration
    conn = psycopg2.connect(
        dbname=app.config['SQLALCHEMY_DATABASE_URI'].split('/')[-1],
        user=app.config['SQLALCHEMY_DATABASE_URI'].split('://')[1].split(':')[0],
        password=app.config['SQLALCHEMY_DATABASE_URI'].split(':')[2].split('@')[0],
        host=app.config['SQLALCHEMY_DATABASE_URI'].split('@')[1].split(':')[0],
        port=app.config['SQLALCHEMY_DATABASE_URI'].split(':')[3].split('/')[0]
    )
    return conn


def execute_query(query, values=None):
    conn = connect_to_database()
    cur = conn.cursor()
    if values:
        cur.execute(query, values)
    else:
        cur.execute(query)
    result = cur.fetchall()
    conn.commit()  # Commit the transaction
    cur.close()
    conn.close()
    return result

@app.route('/users')
def users():
    try:
        # Execute SQL query
        users = execute_query("SELECT id, created_at, username, email FROM users")
        # Return data as JSON
        return jsonify(users)
    except Exception as e:
        # Handle any exceptions
        return f"Error: {e}"

@app.route('/properties')
def properties():
    try:
        # Execute SQL query
        properties = execute_query("SELECT id, name, num_units, manager_id, latitude, longitude  FROM maintenance.properties")
        # Return data as JSON
        return jsonify(properties)
    except Exception as e:
        # Handle any exceptions
        return f"Error: {e}"


@app.route('/add-properties', methods=['POST'])
def add_property():
    try:
        # Get JSON data from the request
        data = request.json

        # Extract property details from the JSON data
        name = data.get('name')
        num_units = data.get('num_units')

        # Validate the compulsory fields
        if not name or not num_units:
            return jsonify({'error': 'Name and number of units are required'}), 400

        # Prepare the SQL query
        query = "INSERT INTO maintenance.properties (name, num_units"
        values = [name, num_units]

        # Add optional fields to the query and values list
        optional_fields = ['country', 'city', 'address', 'zipcode', 'state', 'latitude', 'longitude', 'elevation', 'manager_id']
        for field in optional_fields:
            if field in data:
                query += f", {field}"
                values.append(data[field])

        # Complete the query string
        query += ") VALUES ("
        query += ', '.join(['%s'] * len(values))
        query += ") ON CONFLICT (id) DO UPDATE SET "

        # Add optional fields to the update part of the query
        fields_added = False
        for field in optional_fields:
            if field in data:
                query += f"{field}=EXCLUDED.{field}, "
                fields_added = True

        # Remove the last comma and space from the update query
        if fields_added:
            query = query[:-2]

        # Execute the query
        execute_query(query, tuple(values))

        return jsonify({'message': 'Property added successfully'}), 201
    except Exception as e:
        # Handle any exceptions
        return jsonify({'error': str(e)}), 500
    

@app.route('/test')
def test():
    return 'Hello, World!'
