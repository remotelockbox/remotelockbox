 #!/usr/bin/python3

from flask import Flask, flash, redirect, render_template, json, \
        request, url_for
from werkzeug import generate_password_hash, check_password_hash
import flask_login
from flask_login import login_required

from contextlib import closing
from db import db, lock_state


app = Flask(__name__)
app.secret_key = 'foobar'
app.secret_pin = generate_password_hash('1234')


# Log in and User logic
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User:

    @staticmethod
    def get(user_id):
        if user_id == 'primary':
            return User(user_id, 'primary')
        else:
            return User(user_id, 'sub')

    def __init__(self, user_id, role):
        self.user_id = user_id
        self.role = role

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.user_id

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# Routes

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def login():
    pin = request.form['inputPassword']
    if pin:
        if check_password_hash(app.secret_pin, pin):
            remember = 'remember' in request.form
            flask_login.login_user(User.get('primary'), remember=remember)
            return redirect("/config")
        else:
            error = "PIN Invalid"
    else:
        error = "You must fill in the PIN to log in"

    return render_template("index.html", error=error)
 
@app.route("/signOut")
def logout():
    flask_login.logout_user()
    return redirect("/")

@app.route("/config")
@login_required
def config_form():
    return render_template("config_form.html", lock=lock_state)

@app.route("/config", methods=["POST"])
@login_required
def save_config():
    return render_template("config_form.html", lock=lock_state)

@app.route("/lock", methods=["POST"])
@login_required
def lock():
    if lock_state.is_locked():
        lock_state.sync()
        flash("Already locked")
    else:
        lock_state.lock(flask_login.current_user.user_id)
    
    db.sync()

    return redirect("/config")

@app.route("/unlock", methods=["POST"])
@login_required
def unlock():
    if not lock_state.is_locked():
        lock_state.sync()
        flash("Already unlocked")
    else:
        lock_state.unlock(flask_login.current_user.user_id)

    db.sync()

    return redirect("/config")

if __name__ == "__main__":
    with closing(db):
        app.run()

