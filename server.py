# from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session, url_for)
from flask_sqlalchemy import SQLAlchemy
# from flask_debugtoolbar import DebugToolbarExtension

from model import *


app = Flask(__name__)

app.secret_key = "ZILWAL"

# app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """Homepage"""

    return render_template("index.html")

@app.route('/login', methods=['GET'])
def login():
    """Show login form."""

    return render_template("login.html")

@app.route('/login', methods=["POST"])
def login_form():
    """Allow users to login"""

    # retrieving email and password from user
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(password=password).first()

    session["user_id"] = user.user_id

    return redirect(f"/user/{user.user_id}")


@app.route("/user/<int:user_id>")
def user_homepage(user_id):
    """Show user specific homepage."""

    user = User.query.get(user_id)
    return render_template("user-homepage.html", user=user)


@app.route('/add-entry', methods=["POST"])
def add_entry():

    # query to get the values of the moods from database
    moods = Mood.query.all()

    # retrieving mood and activities from the user
    mood = request.form.get("mood")
    print(mood)
    activities = request.form.get("activity_category")
    print(activities)

    return render_template("add-entry.html", moods=moods)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')