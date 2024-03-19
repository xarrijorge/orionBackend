from flask import (
    Blueprint, redirect, request, url_for, jsonify
)
from psycopg2.extras import DictCursor
from werkzeug.exceptions import abort
from app.views.auth import login_required

from app.views.db import get_db


bp = Blueprint('work_orders', __name__, url_prefix='/work_orders')


@bp.route('/')
def work_orders():
    db = get_db()
    cursor = db.cursor()

    wo_id = request.args.get('wo_id')
    wo_assigned_by = request.args.get('wo_assigned_by')
    wo_assigned_to = request.args.get('wo_assigned_to')

    if wo_id:
        query = (
         'SELECT wo_id, wo_pm_description, wo_l_id, wo_u_id, wo_created_time, '
         'wo_assigned_to, wo_assigned_by, wo_status, wo_due_date, wo_r_id, '
         'r_id, r_type, r_description, r_img_url, r_img_url1, r_img_url2, '
         'r_l_id, r_u_id, r_created_time, r_phone '
         ' FROM maintenance.work_order, maintenance.report '
         ' WHERE wo_r_id = r_id AND wo_id = %s '
         ' ORDER BY wo_created_time, r_created_time DESC'
        )
        cursor.execute(query, (wo_id,))
    elif wo_assigned_by:
        query = (
         'SELECT wo_id, wo_pm_description, wo_l_id, wo_u_id, wo_created_time,'
         ' wo_assigned_to, wo_assigned_by, wo_status, wo_due_date, wo_r_id,'
         ' r_id, r_type, r_description,r_img_url, r_img_url1, r_img_url2,'
         ' r_l_id, r_u_id, r_created_time, r_phone'
         ' from maintenance.work_order, maintenance.report'
         ' where wo_r_id=r_id and wo_assigned_by = %s'
         ' order by wo_created_time,r_created_time desc'
        )
        cursor.execute(query, (wo_assigned_by,))
    elif wo_assigned_to:
        query = (
         'SELECT wo_id, wo_pm_description, wo_l_id, wo_u_id, wo_created_time,'
         'wo_assigned_to, wo_assigned_by, wo_status, wo_due_date, wo_r_id,'
         ' r_id, r_type, r_description,r_img_url, r_img_url1, r_img_url2,'
         'r_l_id, r_u_id, r_created_time, r_phone'
         ' from maintenance.work_order, maintenance.report'
         ' where wo_r_id=r_id and wo_assigned_to = %s'
         'order by wo_created_time,r_created_time desc'
        )
        cursor.execute(query, (wo_assigned_to,))
    else:
        cursor.execute(
         'SELECT wo_id, wo_pm_description, wo_l_id, wo_u_id, wo_created_time,'
         'wo_assigned_to, wo_assigned_by, wo_status, wo_due_date, wo_r_id,'
         ' r_id, r_type, r_description,r_img_url, r_img_url1, r_img_url2,'
         'r_l_id, r_u_id, r_created_time, r_phone'
         ' from maintenance.work_order, maintenance.report where wo_r_id=r_id'
         ' order by wo_created_time,r_created_time desc'
        )
    wo_data = cursor.fetchall()
    db.close()
    return jsonify(wo_data)