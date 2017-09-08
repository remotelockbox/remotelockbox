from contextlib import closing
import datetime
import logging
import argparse

from flask import Flask, flash, redirect, render_template, json, \
    request, url_for
import flask_login
from flask_login import login_required

import db
from db import get_user
import forms
import worker

app = Flask(__name__)
app.secret_key = 'foobar'

# Log in and User logic
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


def current_user_id():
    return flask_login.current_user.get_id()


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
        for user in db.users:
            if user.check_pin(pin):
                remember = 'remember' in request.form
                flask_login.login_user(User.get(user.id), remember=remember)
                return redirect("/config")
        else:
            error = "PIN Invalid"
    else:
        error = "You must fill in the PIN to log in"

    return render_template("index.html", error=error)


@app.route("/logout")
def logout():
    flask_login.logout_user()
    return redirect("/")


@app.route("/config")
@login_required
def show_config():
    form_data = None
    if 'schedule_form' in db.shelf:
        form_data = db.shelf['schedule_form']

    return render_template("config_form.html",
                           now=datetime.datetime.now(),
                           lock=db.lock_state,
                           schedule_form=forms.ScheduleForm(form_data)
                           )


@app.route("/config", methods=["POST"])
@login_required
def save_config():
    schedule_form = forms.ScheduleForm(request.form)
    if not schedule_form.validate():
        return render_template("config_form.html",
                               now=datetime.datetime.now(),
                               lock=db.lock_state,
                               schedule_form=schedule_form
                               )
    try:
        if current_user_id() != 'primary' and 'schedule_form' in db.shelf:
            flash("You can't change the schedule once it is set")
            return show_config()
    except KeyError:
        pass

    if request.form['unlock_date'] != '':
        db.lock_state.lock(current_user_id())

    db.shelf['schedule_form'] = request.form
    db.shelf['schedule_user_id'] = current_user_id()
    db.shelf.sync()
    logging.info('schedule updated to %s', list(db.shelf['schedule_form'].items()))
    return show_config()


@app.route("/lock", methods=["POST"])
@login_required
def lock():
    if db.lock_state.is_locked():
        db.lock_state.sync()
        flash("Already locked")
    else:
        db.lock_state.lock(current_user_id())

    db.shelf.sync()

    return redirect("/config")


@app.route("/unlock", methods=["POST"])
@login_required
def unlock():
    if not db.lock_state.can_unlock(current_user_id()):
        flash("You can't unlock the box because it was locked by someone else.")
        return redirect("/config")

    if not db.lock_state.is_locked():
        db.lock_state.sync()
        flash("Already unlocked")
    else:
        db.lock_state.unlock(current_user_id())

    db.shelf.sync()

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
        user = get_user(current_user_id())
        if user.check_pin(old_pin):
            user.set_pin(new_pin)
            flash("PIN changed")
        else:
            error = "PIN Invalid"
    else:
        error = "You must fill in the old and new PIN"

    return render_template("profile.html", error=error)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog='remotelockbox',
                                     description='Remote Lock Box')
    parser.add_argument("-H", "--host", default='127.0.0.1')
    parser.add_argument("-P", "--port", type=int, default='5000')
    parser.add_argument("-d", "--debug", action="store_true")

    options = parser.parse_args()

    loglevel = logging.DEBUG if options.debug else logging.WARN
    logging.basicConfig(format='%(asctime)s %(message)s', level=loglevel)

    db.init()

    with closing(db.shelf):
        try:
            worker.start()
            app.run(
                debug=options.debug,
                host=options.host,
                port=options.port)
        finally:
            worker.stop()
