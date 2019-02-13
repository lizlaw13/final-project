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

@app.route('/login', methods=["GET"])
def login():
    """Show login form."""

    return render_template("login.html")

@app.route('/login', methods=["POST"])
def login_form():
    """Allow users to login"""

    # retrieving email and password from user
    email = request.form.get("email")
    password = request.form.get("password")

    # querying by the password provided by the user
    user = User.query.filter_by(password=password).first()

    # created a session to store the user id
    session["user_id"] = user.user_id

    return redirect(f"/user/{user.user_id}")


@app.route("/user/<int:user_id>")
def user_homepage(user_id):
    """Show user specific homepage."""

    user = User.query.get(user_id)
    moods = Mood.query.all()
    activities = Activity_Category.query.all()


    return render_template("user-homepage.html", user=user, moods=moods,
                           activities= activities)

@app.route("/all-entries")
def generate_all_entries():
    """Generate user specific URL"""

    # retreive logged in user_id from the database
    user_id = session.get("user_id")

    # querying by user_id from the session
    user = User.query.filter_by(user_id=user_id).first()

    return redirect(f"/all-entries/{user.user_id}")


@app.route("/all-entries/<int:user_id>")
def show_all_entries(user_id):
    """Show all entries for a specific user """

    # grab all the users entries
    entries = Entry.query.filter_by(user_id=user_id).all()
    print(entries)

    return render_template("all-entries.html", entries=entries)



@app.route('/add-entry', methods=["POST"])
def add_entry():

    # retreive logged in user_id from the database
    user_id = session.get("user_id")

    # retrieving mood and activities from the user
    user_mood = request.form.get("mood")
    # print(user_mood)

    user_activities = request.form.get("activity_category")
    # print(user_activities)

    # get user_id from the database
    user = User.query.get(user_id)

    # grab the mood and activities from the database
    mood = Mood.query.filter_by(mood_id=user_mood).first()
    print(mood)

    activity = Activity_Category.query.filter_by(activity_category_id=user_activities).first()

    # add an entry to the database for the user logged in
    entry = Entry(mood=mood, activity_category=activity)

    user.entries.append(entry)

    db.session.add(user)

    db.session.commit()

    # pass the information the user submitted to the template
    # info = user.entries[0]
    info = entry
    print(info)


    return render_template("add-entry.html", info=info)



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