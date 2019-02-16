# from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session, url_for)
from flask_sqlalchemy import SQLAlchemy
# from flask_debugtoolbar import DebugToolbarExtension

import datetime

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

@app.route('/logout')
def logout():
    """Log out."""

    del session["user_id"]
    return redirect("/")

@app.route("/user/<int:user_id>")
def user_homepage(user_id):
    """Show user specific homepage."""

    if session.get("user_id") == None or session["user_id"] is not user_id: 
        return redirect("/")
        
    user = User.query.get(user_id)
    moods = Mood.query.all()
    activities = Activity_Category.query.all()

    now = datetime.datetime.today().strftime('%Y-%m-%d')
    print (now)

    return render_template("user-homepage.html", user=user, moods=moods,
                           activities= activities, now=now)

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
    if session["user_id"] is not user_id:
        return redirect("/")

    # grab all the users entries
    user = User.query.get(user_id)
    entries = Entry.query.filter_by(user_id=user_id).order_by('date_created').all()


    return render_template("all-entries.html", entries=entries)

@app.route("/delete-entry/<int:entry_id>")
def delete_entry(entry_id):

    entry = Entry.query.get(entry_id)

    user_id = session.get("user_id")


    if session["user_id"] is not user_id:
        return redirect("/")

    db.session.delete(entry)
    db.session.commit()


    return render_template("delete-entry.html")

@app.route("/modified-entry/<int:entry_id>")
def modify_activitiy(entry_id):

    return render_template("modified-entry.html")

@app.route("/update-entry/<int:entry_id>")
def show_update_form(entry_id):
    entry = Entry.query.get(entry_id)

    if session["user_id"] is not entry.user.user_id:
        return redirect("/")

    user = User.query.get(entry.user.user_id)
    moods = Mood.query.all()
    activities = Activity_Category.query.all()

    for activity in entry.activities:
        print(activity.activity_category_id)


    return render_template("update-entry.html", entry=entry, user=user, moods=moods, activities=activities)

@app.route("/updated-entry/<int:entry_id>", methods=["POST", "GET"])
def update_entry(entry_id):

    entry = Entry.query.get(entry_id)

    user_id = session.get("user_id")

    user_mood = request.form.get("mood")

    mood = Mood.query.get(int(user_mood))

    user_activities = request.form.getlist("activity_category")

    form_activities = []
    for activity_id in user_activities:
        form_activities.append(Activity_Category.query.get(int(activity_id)))

    if session["user_id"] is not entry.user.user_id:
        return redirect("/")

    # update the existing entry's mood
    entry = Entry.query.get(entry_id)
    entry.mood = mood
    

    # for activity in entry.activities:
    #     for form_activity in form_activities:
    #         if activity != form_activity:
    #                 entry.activities.extend(form_activity)

    entry.activities.extend(form_activities)


    db.session.commit()


    return render_template("updated_entry.html")

@app.route('/add-entry', methods=["POST"])
def add_entry():
    # retreive logged in user_id from the database
    user_id = session.get("user_id")

    # retrieving mood and activities from the user
    user_mood = request.form.get("mood")
    # print(user_mood)

    user_activities = request.form.getlist("activity_category")
    # print('\n\n\n\n\n\n\n')
    # print(user_activities)

    activities = []
    for activity_id in user_activities:
        activities.append(Activity_Category.query.get(int(activity_id)))

    # get user_id from the database
    user = User.query.get(user_id)

    # grab the mood and activities from the database
    mood = Mood.query.get(int(user_mood))

    # add an entry to the database for the user logged in
    entry = Entry(mood=mood, user=user)


    entry.activities.extend(activities)

    user.entries.append(entry)


    db.session.add(user)


    db.session.commit()

    # pass the information the user submitted to the template
    entry = user.entries[-1]
    mood = entry.mood.mood
    print(mood)
    activities = entry.activities


    return render_template("add-entry.html", entry=entry, activities=activities)


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