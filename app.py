 #!/usr/bin/python3

from contextlib import closing
import datetime

from flask import Flask, flash, redirect, render_template, json, \
        request, url_for
import flask_login
from flask_login import login_required

from db import db, lock_state, get_user, users


app = Flask(__name__)
app.secret_key = 'foobar'

# Log in and User logic
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User:
    @staticmethod
    def get(user_id):
        return User(user_id)

    def __init__(self, user_id):
        self.user_id = user_id

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
    if not flask_login.current_user.is_authenticated:
        return render_template("index.html")
    else:
        return redirect("/config")

@app.route("/", methods=["POST"])
def login():
    pin = request.form['inputPassword']
    if pin:
        for user in users:
            if user.check_pin(pin):
                remember = 'remember' in request.form
                flask_login.login_user(User.get(user.id), remember=remember)
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
    return render_template("config_form.html", now=datetime.datetime.now(), lock=lock_state)

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
        lock_state.lock(flask_login.current_user.get_id())
    
    db.sync()

    return redirect("/config")

@app.route("/unlock", methods=["POST"])
@login_required
def unlock():
    if not lock_state.is_locked():
        lock_state.sync()
        flash("Already unlocked")
    else:
        lock_state.unlock(flask_login.current_user.get_id())

    db.sync()

    return redirect("/config")

@app.route("/profile")
@login_required
def show_profile():
    return render_template("profile.html")

@app.route("/profile", methods=["POST"])
@login_required
def save_profile():
    error = None
    old_pin = request.form['oldPin']
    new_pin = request.form['newPin']

    if old_pin and new_pin:
        user = get_user(flask_login.current_user.get_id())
        if user.check_pin(old_pin):
            user.set_pin(new_pin)
            flash("PIN changed")
        else:
            error = "PIN Invalid"
    else:
        error = "You must fill in the old and new PIN"

    return render_template("profile.html", error=error)

if __name__ == "__main__":
    with closing(db):
        app.run()

