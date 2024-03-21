import functools
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,
    jsonify, json,
)
from werkzeug.security import check_password_hash, generate_password_hash
from .db import get_db
from .user import User
from .. import app
from config import GOOGLE_CLIENT_ID, GOOGLE_DISCOVERY_URL, GOOGLE_CLIENT_SECRET
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from oauthlib.oauth2 import WebApplicationClient
import requests


# User session management setup
# https://flask-login.readthedocs.io/en/latest
login_manager = LoginManager()
login_manager.init_app(app)


# OAuth 2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)


# Flask-Login helper to retrieve a user from our db
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()


@app.route("/login")
def login():
    # Find out what URL to hit for Google login
    google_provider_cfg = get_google_provider_cfg()
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]

    # Use library to construct the request for Google login and provide
    # scopes that let you retrieve user's profile from Google
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)


@app.route("/login/callback")
def callback():
    # Get authorization code Google sent back to you
    code = request.args.get("code")
    # Find out what URL to hit to get tokens that allow you to ask for
# things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]
    # Prepare and send a request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
     token_endpoint, authorization_response=request.url,
     redirect_url=request.base_url,
     code=code
    )
    token_response = requests.post(
     token_url,
     headers=headers,
     data=body,
     auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

# Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))
# Now that you have tokens (yay) let's find and hit the URL
# from Google that gives you the user's profile information,
# including their Google profile image and email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)
    # You want to make sure their email is verified.
# The user authenticated with Google, authorized your
# app, and now you've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        picture = userinfo_response.json()["picture"]
        users_name = userinfo_response.json()["given_name"]  
    else:
        return "User email not available or not verified by Google.", 400
    # Create a user in your db with the information provided
# by Google
    user = User(
     id_=unique_id, name=users_name, email=users_email, profile_pic=picture
    )

# Doesn't exist? Add it to the database.
    if not User.get(unique_id):
        User.create(unique_id, users_name, users_email, picture)

# Begin user session by logging the user in
    login_user(user)

# Send user back to homepage
    return redirect(url_for("index"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/")
def index():
    if current_user.is_authenticated:
        db = get_db()
        cursor = db.cursor()
        user_email = current_user.email

        if user_email:
            cursor.execute(
                'SELECT * '
                ' FROM users.user WHERE email = %s', (user_email,)
            )
        user_details = cursor.fetchall()
        db.close()
        return jsonify(user_details)

        # (
        #     "<p>Hello, {}! You're logged in! Email: {}</p>"
        #     "<div><p>Google Profile Picture:</p>"
        #     '<img src="{}" alt="Google profile pic"></img></div>'
        #     '<a class="button" href="/logout">Logout</a>'.format(
        #         current_user.name, current_user.email, current_user.profile_pic
        #     )
        # )
    else:
        return ( 
           ' <p>  Resiix By Orion </p> '
           '<br> </br> <br> </br>'
           '<a class="button" href="/login">Google with Login</a>'
           )


bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/users')
def users():
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'SELECT id, created_at, update_at, username, email '
        'FROM users.users'
    )
    user_data = cursor.fetchall()
    db.close()
    return jsonify(user_data)


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)
    return "User created successfully", 201


@bp.route('/oldlogin', methods=('GET', 'POST'))
def oldlogin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')
