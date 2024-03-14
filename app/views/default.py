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




