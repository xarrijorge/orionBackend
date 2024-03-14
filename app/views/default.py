from flask import jsonify,  request
from .. import app


@app.route('/units')
def units():
    try:
        unit_id = request.args.get('id')
        if unit_id:
            units_data = execute_query("SELECT u_id, u_name, u_type, u_status, u_description, u_p_id, u_f_id FROM maintenance.units WHERE u_id = %s", (unit_id,))
        else:
            units_data = execute_query("SELECT u_id, u_name, u_type, u_status, u_description, u_p_id FROM maintenance.units")
        return jsonify(units_data)
    except Exception as e:
        return f"Error: {e}"


@app.route('/leases')
def leases():
    try:
        lease_id = request.args.get('id')
        if lease_id:
            lease_data = execute_query("SELECT l_id, l_start_date, l_end_date, l_rent, l_u_id, tenant_name, l_code, l_email, l_phone, l_secondary_phone, l_national_id from maintenance.leases WHERE l_id = %s", (lease_id,))
        else:
            lease_data = execute_query("SELECT l_id, l_start_date, l_end_date, l_rent, l_u_id, tenant_name, l_code, l_email, l_phone, l_secondary_phone, l_national_id from maintenance.leases")
        return jsonify(lease_data)
    except Exception as e:
        return f"Error: {e}"



#post methods

@app.route('/add-properties', methods=['POST'])
def add_property():
    try:
        # Get JSON data from the request
        data = request.json

        # Extract property details from the JSON data
        name = data.get('p_name')
        num_units = data.get('p_num_units')

        # Validate the compulsory fields
        if not name or not num_units:
            return jsonify({'error': 'Name and number of units are required'}), 400

        # Prepare the SQL query
        query = "INSERT INTO maintenance.properties (p_name, p_num_units"
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
