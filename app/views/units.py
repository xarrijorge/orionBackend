from flask import (
    Blueprint,  jsonify
)
from app.views.db import get_db

bp = Blueprint('units', __name__)


@bp.route('/units')
def units():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'select u_id, u_name, u_type, u_status, u_description, u_p_id, u_f_id, u_code '
        ' from maintenance.units'
    )
    unit_data = cursor.fetchall()
    db.close()
    return jsonify(unit_data)