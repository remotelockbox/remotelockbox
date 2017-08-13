from flask import Flask, flash, redirect, render_template, json, \
        request, url_for
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_pin = generate_password_hash('1234')

@app.route("/")
def main():
    return render_template("index.html")

@app.route("/", methods=["POST"])
def signIn():
    pin = request.form['inputPassword']
    if pin:
        if check_password_hash(app.secret_pin, pin):
            # TODO create login session
            return redirect("/config")
        else:
            error = "PIN Invalid"
    else:
        error = "You must fill in the PIN to log in"

    return render_template("index.html", error=error)
 
@app.route("/signOut")
def signOut():
    # TODO delete and invalidate session
    return redirect("/")

@app.route("/config")
def config_form():
    # TODO check authorization
    return render_template("config_form.html")

@app.route("/config", methods=["POST"])
def save_config():
    return render_template("config_form.html")
    

if __name__ == "__main__":
    app.run()

