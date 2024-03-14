from flask import (
    Blueprint, flash, g, redirect, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from app.views.auth import login_required

from app.views.db import get_db

from .. import app

bp = Blueprint('properties', __name__)
@bp.route('/properties')
def properties():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'SELECT p_id, p_name, p_num_units, p_manager_id, p_country, p_city, p_address, p_zipcode, p_state, p_latitude, p_longitude, p_elevation, p_f_id'
        ' FROM maintenance.properties'
    )
    property_data = cursor.fetchall()
    db.close()
    return jsonify(property_data)

@bp.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':
        data = request.json
        name = data.get('p_name')
        num_units = data.get('p_num_units')
        error = None

        if not name:
            error = 'Name is required.'

        if error is not None:
            return jsonify({'error': error}), 400  # Return error response
        else:
            try:
                db = get_db()
                cursor = db.cursor()
                cursor.execute(
                    'INSERT INTO maintenance.properties (p_name, p_num_units)'
                    ' VALUES (%s, %s)',
                    (name, num_units)
                    
                )
                db.commit()
            except Exception as e:
                return jsonify({'error': str(e)}), 500  # Return error response
            finally:
                cursor.close()  # Close the cursor
                db.close()  # Close the database connection

        return jsonify({'message': 'Property added successfully'}), 201

    return jsonify({'error': 'Method not allowed'}), 405


# def get_post(id, check_author=True):
#     post = get_db().execute(
#         'SELECT p.id, title, body, created, author_id, username'
#         ' FROM post p JOIN user u ON p.author_id = u.id'
#         ' WHERE p.id = ?',
#         (id,)
#     ).fetchone()

#     if post is None:
#         abort(404, f"Post id {id} doesn't exist.")

#     if check_author and post['author_id'] != g.user['id']:
#         abort(403)

#     return post


# @bp.route('/<int:id>/update', methods=('GET', 'POST'))
# @login_required
# def update(id):
#     post = get_post(id)

#     if request.method == 'POST':
#         title = request.form['title']
#         body = request.form['body']
#         error = None

#         if not title:
#             error = 'Title is required.'

#         if error is not None:
#             flash(error)
#         else:
#             db = get_db()
#             db.execute(
#                 'UPDATE post SET title = ?, body = ?'
#                 ' WHERE id = ?',
#                 (title, body, id)
#             )
#             db.commit()
#             return redirect(url_for('blog.index'))

#     return render_template('blog/update.html', post=post)



# @bp.route('/<int:id>/delete', methods=('POST',))
# @login_required
# def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))