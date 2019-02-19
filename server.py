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

@app.route("/")
def index():
    """Homepage"""

    return render_template("index.html")

@app.route("/register", methods=["GET"])
def register_form():
    """Show new user registeration form"""

    return render_template("register-form.html")

@app.route("/register", methods=["POST"])
def register_new_user():

    # grab the email and password from the form
    new_user_email = request.form.get("new_email")
    new_user_password = request.form.get("new_password")

    new_user = User(email=new_user_email, password=new_user_password)

    db.session.add(new_user)
    db.session.commit()

    return redirect("/")

@app.route("/login", methods=["GET"])
def login():
    """Show login form."""

    return render_template("login.html")

@app.route("/login", methods=["POST"])
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

@app.route("/logout")
def logout():
    """Log out."""

    # removing the user id from the session
    del session["user_id"]
    return redirect("/")

@app.route("/user/<int:user_id>")
def user_homepage(user_id):
    """Show user specific homepage."""

    # prevents the public for accessing user specific information
    if not session.get("user_id") or session["user_id"] != user_id:
        return redirect("/")
    # if session.get("user_id") == None or session["user_id"] is not user_id: 
    #     return redirect("/")

    # retreiving user id and all moods and activities to be able to use in a form
    user = User.query.get(user_id)
    moods = Mood.query.all()
    activities = Activity_Category.query.all()

    # generating today's date
    now = datetime.datetime.today().strftime("%A, %B %d, %Y")

    return render_template("user-homepage.html", user=user, moods=moods,
                           activities= activities, now=now)

@app.route("/all-entries")
def generate_all_entries():
    """Generate user specific URL"""

    # retrieve logged in user_id from the database
    user_id = session.get("user_id")

    # querying by user_id from the session
    user = User.query.filter_by(user_id=user_id).first()

    return redirect("/all-entries/{}".format(user.user_id))


@app.route("/all-entries/<int:user_id>")
def show_all_entries(user_id):
    """Show all entries for a specific user """

    # prevents the public for accessing user specific information
    # if session["user_id"] is not user_id:
    #     return redirect("/")
    if session["user_id"] != user_id:
        return redirect("/")

    # grab all the users entries
    user = User.query.get(user_id)
    entries = Entry.query.filter_by(user_id=user_id).order_by('date_created').all()


    return render_template("all-entries.html", entries=entries, user=user)

@app.route("/delete-entry/<int:entry_id>")
def delete_entry(entry_id):
    """Confirmation that a user deleted an entry"""
    
    # grabs the specific entry id 
    entry = Entry.query.get(entry_id)

    # grabs the user id in the session 
    user_id = session.get("user_id")

    # prevents the public for accessing user specific information
    if session["user_id"] is not user_id:
        return redirect("/")
    # if session["user_id"] != user_id:
    #     return redirect("/")

    # removes an entry from the database
    db.session.delete(entry)
    db.session.commit()


    return render_template("delete-entry.html")

@app.route("/modified-entry/<int:entry_id>",  methods=["POST", "GET"])
def modify_activitiy(entry_id):
    """Deletes selected activities from an entry"""

    # grabs user id in the session
    user_id = session.get("user_id")

    # grabs information for the form
    user_activities = request.form.getlist("activity_category")

    # grabs the specifc entry to delete from
    entry = Entry.query.get(entry_id)

    # appends each acitivity to a list from the form
    form_activities = []
    for activity_id in user_activities:
        form_activities.append(Activity_Category.query.get(int(activity_id)))

    # deletes each activitiy from the entry one by one
    for activity in form_activities:
        entry.activities.remove(activity)


    db.session.commit()

    return render_template("modified-entry.html")

@app.route("/delete-note-entry/<int:entry_id>", methods= ["POST", "GET"])
def delete_note(entry_id):

    entry = Entry.query.get(entry_id)
    entry.description = None

    db.session.commit()

    return render_template("delete-note-entry.html")


@app.route("/update-entry/<int:entry_id>")
def show_update_form(entry_id):
    """Displays the update form for a user"""

    # grabs the specific entry id 
    entry = Entry.query.get(entry_id)

    # prevents the public for accessing user specific information
    # if session["user_id"] is not entry.user.user_id:
    #     return redirect("/")

    # if session["user_id"] != entry.user.user_id:
    #     return redirect("/")

    # grabs the user's information 
    user = User.query.get(entry.user.user_id)

    # grabs all moods and activities 
    moods = Mood.query.all()
    activities = Activity_Category.query.all()


    return render_template("update-entry.html", entry=entry, user=user, moods=moods, activities=activities)

@app.route("/updated-entry/<int:entry_id>", methods=["POST", "GET"])
def update_entry(entry_id):
    """Confirmation that a user has added an activity or updated their mood on their entry"""

    # grabs user id in the session
    user_id = session.get("user_id")

    # prevents the public from accessing user specific information
    # if session["user_id"] is not entry.user.user_id:
    #     return redirect("/")
    if session["user_id"] != user_id:
        return redirect("/")

    # grabs entry id
    entry = Entry.query.get(entry_id)

    # grabs information for the form
    user_mood = request.form.get("mood")

    mood = Mood.query.get(int(user_mood))

    user_activities = request.form.getlist("activity_category")

    description = request.form.get("description")


    # appends each acitivity to a list
    form_activities = []
    for activity_id in user_activities:
        form_activities.append(Activity_Category.query.get(int(activity_id)))

    activities = entry.activities

    # update the existing entry's mood
    entry = Entry.query.get(entry_id)
    entry.mood = mood

    entry.activities.extend(form_activities)

    if entry.description == None:
        entry.description = description 
    else:
        entry.description += ', ' + description


    db.session.commit()


    return render_template("updated_entry.html", activities=activities)

@app.route('/add-entry', methods=["POST", "GET"])
def add_entry():
    """Adds a new entry for a user"""

    # retreive logged in user_id from the database
    user_id = session.get("user_id")

    # retrieving mood and activities from the user
    user_mood = request.form.get("mood")

    user_activities = request.form.getlist("activity_category")

    description = request.form.get("description")

    activities = []
    for activity_id in user_activities:
        activities.append(Activity_Category.query.get(int(activity_id)))

    # get user_id from the database
    user = User.query.get(user_id)

    # grab the mood and activities from the database
    mood = Mood.query.get(int(user_mood))

    # add an entry to the database for the user logged in
    entry = Entry(mood=mood, user=user, description=description)

    entry.activities.extend(activities)
    user.entries.append(entry)
    db.session.add(user)
    db.session.commit()

    # pass the information the user submitted to the template
    activities = entry.activities

    return render_template("add-entry.html", entry=entry, activities=activities, mood=mood)

@app.route("/mood-enhancers", methods=["POST", "GET"])
def mood_enhancer_input():

    user_id = session.get("user_id")



    user = User.query.get(user_id)

    entry = Entry.query.filter_by(user_id=user_id)

    user_mood_enhancer_1 = request.form.get("mood_enhancer_1")
    user_mood_enhancer_2 = request.form.get("mood_enhancer_2")
    user_mood_enhancer_3 = request.form.get("mood_enhancer_3")

    mood_enhancer_entry_1 = Mood_Enhancer(user_id=user_id, mood_enhancer=user_mood_enhancer_1)
    mood_enhancer_entry_2 = Mood_Enhancer(user_id=user_id, mood_enhancer=user_mood_enhancer_2)
    mood_enhancer_entry_3 = Mood_Enhancer(user_id=user_id, mood_enhancer=user_mood_enhancer_3)

    db.session.add(mood_enhancer_entry_1)
    db.session.add(mood_enhancer_entry_2)
    db.session.add(mood_enhancer_entry_3)


    # db.session.commit()

    enhancer = Mood_Enhancer.query.filter_by(user_id=1)
    print(enhancer)

    return render_template("mood-enhancers.html")

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