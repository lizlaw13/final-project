import datetime
import hashlib

# from flask_debugtoolbar import DebugToolbarExtension
from flask import Flask, render_template, redirect, request, flash, session, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, asc

# from jinja2 import StrictUndefined
import indicoio
import os

from database import connect_to_db, db
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
    """Registers new user"""

    # grab the email and password from the form
    new_user_email = request.form.get("new_email")
    new_user_password = request.form.get("new_password")

    hash_object = hashlib.md5(new_user_password.encode())

    password = hash_object.hexdigest()

    # creates new user in database
    new_user = User(email=new_user_email, password=password)

    # adds new user to database
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
    form_password = request.form.get("password")

    hash_object = hashlib.md5(form_password.encode())

    # querying by the password provided by the user
    user = User.query.filter_by(email=email).first()
    password = user.password

    if hash_object.hexdigest() == password:

        # created a session to store the user id
        session["user_id"] = user.user_id

        return redirect(f"/user/{user.user_id}")
    else:
        flash("Sorry, wrong password!")
        return redirect("/")


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

    time = datetime.datetime.now()
    compare_time = time.date()

    brain_dumps = User_Brain_Dump.query.filter_by(user_id=user.user_id).all()

    show_form = True
    entries = Entry.query.filter_by(user_id=user_id)
    for entry in entries:
        if entry.date_created.date() == compare_time:
            show_form = False

    return render_template(
        "user-homepage.html",
        user=user,
        moods=moods,
        activities=activities,
        now=now,
        brain_dumps=brain_dumps,
        show_form=show_form,
    )


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
    entries = Entry.query.filter_by(user_id=user_id).order_by("date_created").all()

    return render_template("all-entries.html", entries=entries, user=user)


@app.route("/brain-dump/<int:user_id>", methods=["POST", "GET"])
def show_brain_dump_form(user_id):

    # grab user in the session
    user_id = session.get("user_id")

    now = datetime.datetime.today().strftime("%A, %B %d, %Y")

    updated = request.args.get("updated")

    return render_template("brain-dump.html", user_id=user_id, now=now, updated=updated)


@app.route("/brain-dump", methods=["POST", "GET"])
def add_brain_dump():

    # grab user in the session
    user_id = session.get("user_id")

    # grab the user text from form
    user_brain_dump = request.form["brain_dump"]

    brain_dump = User_Brain_Dump(user_id=user_id, brain_dump_entry=user_brain_dump)

    db.session.add(brain_dump)
    db.session.commit()

    flash("You have successfully added a brain dump entry!")

    return redirect(f"/brain-dump/{user_id}")


@app.route("/update-brain-dump/<int:brain_dump_id>", methods=["POST", "GET"])
def update_brain_dump(brain_dump_id):

    entry_id = brain_dump_id

    # grab the user text from form
    user_brain_dump = request.form["brain_dump"]
    current_entry = User_Brain_Dump.query.get(entry_id)

    current_entry.brain_dump_entry = user_brain_dump
    db.session.commit()

    updated = "yes"

    flash("You have successfully updated your brain dump entry!")

    return redirect(
        url_for("show_brain_dump_details", user_brain_dump_id=entry_id, updated=updated)
    )


@app.route("/all-brain-dumps/<int:user_id>", methods=["POST", "GET"])
def show_all_brain_dumps(user_id):

    # grab user in the session
    user_id = session.get("user_id")

    brain_dumps = (
        User_Brain_Dump.query.filter_by(user_id=user_id).order_by("date_created").all()
    )

    return render_template(
        "all-brain-dumps.html", brain_dumps=brain_dumps, user_id=user_id
    )


@app.route("/brain-dump-details")
def brain_dump_entry(user_brain_dump_id):

    return redirect(f"/brain-dump-details/{user_brain_dump_id}")


@app.route("/brain-dump-details/<int:user_brain_dump_id>/", methods=["GET", "POST"])
def show_brain_dump_details(user_brain_dump_id):

    id = int(user_brain_dump_id)
    brain_dump = User_Brain_Dump.query.filter_by(user_brain_dump_id=id).first()

    positive = request.args.get("positive")
    negative = request.args.get("negative")
    value = request.args.get("value")
    confirmation = request.args.get("confirmation")
    updated = request.args.get("updated")

    return render_template(
        "/brain-dump-details.html",
        user_brain_dump_id=id,
        brain_dump=brain_dump,
        positive=positive,
        negative=negative,
        value=value,
        confirmation=confirmation,
    )


@app.route("/analyze-entry/<int:user_brain_dump_id>", methods=["GET", "POST"])
def analyze_entry(user_brain_dump_id):

    # ANALYZING ENTRY
    id = int(user_brain_dump_id)
    brain_dump = User_Brain_Dump.query.filter_by(user_brain_dump_id=id).first()

    text = brain_dump.brain_dump_entry

    KEY = os.getenv("I_KEY")
    indicoio.config.api_key = KEY

    # this function will return a number between 0 and 1. This number is a probability representing the likelihood that the analyzed text
    # is positive or negative. Values greater than 0.5 indicate positive sentiment, while values less than 0.5 indicate negative sentiment.

    sentiment_value = indicoio.sentiment([text])

    for value in sentiment_value:
        num_value = float(value)

    value = num_value

    positive = None
    negative = None
    if value > 0.5:
        positive = True
    elif value < 0.5:
        negative = True

    # UPDATING BRAIN DUMP ENTRY
    brain_dump.analysis = value
    confirmation = request.form.get("yesNo")

    if confirmation == "yes" and positive == True:
        brain_dump.analysis_confirmation = "yes"
        brain_dump.verbose_analysis = "positive"
    elif confirmation == "yes" and negative == True:
        brain_dump.analysis_confirmation = "yes"
        brain_dump.verbose_analysis = "negative"
    elif confirmation == "no":
        brain_dump.analysis_confirmation = "no"
        brain_dump.verbose_analysis = None
        brain_dump.analysis = None
        flash(
            """We are sorry your analysis does not reflect how you feel. Your analysis will not be saved. If you update your entry, 
            feel free to analyze again."""
        )

    db.session.commit()

    return redirect(
        url_for(
            "show_brain_dump_details",
            user_brain_dump_id=id,
            positive=positive,
            negative=negative,
            value=value,
            confirmation=confirmation,
        )
    )


@app.route("/reanalyze-entry/<int:brain_dump_id>")
def reanalyze_entry(brain_dump_id):

    # grabs the specific brain_dump id
    brain_dump = User_Brain_Dump.query.get(brain_dump_id)

    user_id = brain_dump.user_id

    brain_dump.analysis_confirmation = None
    brain_dump.verbose_analysis = None
    brain_dump.analysis = None

    db.session.commit()

    return redirect(f"all-brain-dumps/{user_id}")


@app.route("/delete-brain-dump/<int:brain_dump_id>")
def delete_brain_dump_entry(brain_dump_id):

    # grabs the specific brain_dump id
    brain_dump = User_Brain_Dump.query.get(brain_dump_id)

    user_id = brain_dump.user_id

    # removes a brain_dump_entry from the database
    db.session.delete(brain_dump)
    db.session.commit()

    # flash a message to show confirmation for the user
    flash("You have successfully deleted a brain dump entry!")

    return redirect(f"all-brain-dumps/{user_id}")


@app.route("/line-chart/<int:user_id>")
def line_chart(user_id):
    """"Shows line chart of user's mood over time"""

    # MOOD OVER TIME

    # grab user in the session
    user_id = session.get("user_id")

    user = User.query.get(user_id)

    # grab all the users entries
    entries = Entry.query.filter_by(user_id=user_id).order_by(Entry.date_created).all()

    values = [entry.mood.mood_id for entry in entries]
    sorted_dates = [entry.date_created.day for entry in entries]

    # create values to pass to the tempplate
    legend = "Mood Data"

    has_entries = True

    if len(user.moods) <= 1:
        has_entries = False

    return render_template(
        "line-chart.html",
        values=values,
        labels=sorted_dates,
        legend=legend,
        user=user,
        has_entries=has_entries,
    )


@app.route("/donut-chart/<int:user_id>")
def doughnut_chart(user_id):

    # TOTAL MOOD COUNT

    # grab user in the session
    user_id = session.get("user_id")

    user = User.query.get(user_id)

    # grab all the users entries
    entries = Entry.query.filter_by(user_id=user_id).all()

    # grab a list of all the moods for the user
    all_moods = []
    for entry in entries:
        all_moods.append(entry.mood.verbose_mood)

    # create a dictionary with keys being the mood and values being their count
    mood_dictionary = {}
    for mood in all_moods:
        if mood == "Fantastic":
            mood_dictionary["Fantastic"] = mood_dictionary.get("Fantastic", 0) + 1
        elif mood == "Good":
            mood_dictionary["Good"] = mood_dictionary.get("Good", 0) + 1
        elif mood == "Neutral":
            mood_dictionary["Neutral"] = mood_dictionary.get("Neutral", 0) + 1
        elif mood == "Sad/Bad":
            mood_dictionary["Sad/Bad"] = mood_dictionary.get("Sad/Bad", 0) + 1
        elif mood == "Terrible":
            mood_dictionary["Terrible"] = mood_dictionary.get("Terrible", 0) + 1

    # seperate the keys from the values
    json_moods = []
    moods = mood_dictionary.keys()
    json_count = []
    for mood in moods:
        json_moods.append(mood)

    count = mood_dictionary.values()
    for number in count:
        json_count.append(number)

    legend = "Total Mood Count"

    has_entries = True
    if len(user.moods) <= 1:
        has_entries = False

    return render_template(
        "/donut-chart.html",
        labels=json_moods,
        user=user,
        values=json_count,
        legend=legend,
        has_entries=has_entries,
    )


@app.route("/delete-entry/<int:entry_id>")
def delete_entry(entry_id):
    """Deletes a selected entry"""

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

    # flash a message to show confirmation for the user
    flash("You have successfully deleted an entry!")

    return redirect(f"all-entries/{user_id}")


@app.route("/modified-entry/<int:entry_id>", methods=["POST", "GET"])
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

    return redirect(f"/update-entry/{entry.entry_id}")


@app.route("/delete-note-entry/<int:entry_id>", methods=["POST", "GET"])
def delete_note(entry_id):
    """Deletes note for users entry"""

    entry = Entry.query.get(entry_id)

    entry.description = None

    db.session.commit()

    return redirect(f"/update-entry/{entry.entry_id}")


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
    print(entry.activities)

    return render_template(
        "update-entry.html", entry=entry, user=user, moods=moods, activities=activities
    )


@app.route("/updated-entry/<int:entry_id>", methods=["POST", "GET"])
def update_entry(entry_id):
    """Confirmation that a user has added an activity or updated their mood on their entry"""

    # grabs user id in the session

    # prevents the public from accessing user specific information
    # if session["user_id"] is not entry.user.user_id:
    #     return redirect("/")

    # grabs entry id
    entry = Entry.query.get(entry_id)
    user_id = session["user_id"]
    if user_id != entry.user.user_id:
        return redirect("/")

    # grabs information for the form
    user_mood = request.form.get("mood")
    if user_mood is None:
        pass
    else:
        mood = Mood.query.get(int(user_mood))
        entry.mood = mood

    user_activities = request.form.getlist("activity_category")

    description = request.form.get("description")
    if description is None and entry.description is None:
        pass
    elif description is None and entry.description is None:
        entry.description = description
    elif description is None and entry.description is None:
        entry.description += ", " + description

    # appends each acitivity to a list
    form_activities = []
    for activity_id in user_activities:
        form_activities.append(Activity_Category.query.get(int(activity_id)))

    activities = entry.activities

    entry.activities.extend(form_activities)

    db.session.commit()

    flash("You have successfully updated an entry!")

    return redirect(f"/all-entries/{user_id}")


@app.route("/add-entry", methods=["POST", "GET"])
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

    int_user_mood = int(user_mood)

    prompt_mood_enhancer = False
    if int_user_mood == 4 or int_user_mood == 5:
        prompt_mood_enhancer = True

    # genereate today's date in object form
    now = datetime.datetime.today().strftime("%A, %B %d, %Y")

    entries = Entry.query.filter_by(user_id=user_id).all()

    return render_template(
        "add-entry.html",
        user=user,
        entry=entry,
        activities=activities,
        mood=mood,
        prompt_mood_enhancer=prompt_mood_enhancer,
        user_id=user_id,
        now=now,
        entries=entries,
    )


@app.route("/mood-enhancers", methods=["POST", "GET"])
def mood_enhancer_input():

    user_id = session.get("user_id")

    user = User.query.get(user_id)

    entry = Entry.query.filter_by(user_id=user_id)


    # make form reactive such that you only show one text back and you enter one and it adds a new one 
    user_mood_enhancer_1 = request.form.get("mood_enhancer_1")
    user_mood_enhancer_2 = request.form.get("mood_enhancer_2")
    user_mood_enhancer_3 = request.form.get("mood_enhancer_3")

    # TODO
    # write a function to add mood enhancer to database

    if user_mood_enhancer_1:
        mood_enhancer_entry_1 = Mood_Enhancer(
            user_id=user_id, mood_enhancer=user_mood_enhancer_1
        )
        db.session.add(mood_enhancer_entry_1)
        db.session.commit()
    if user_mood_enhancer_2:
        mood_enhancer_entry_2 = Mood_Enhancer(
            user_id=user_id, mood_enhancer=user_mood_enhancer_2
        )
        db.session.add(mood_enhancer_entry_2)
        db.session.commit()

    if user_mood_enhancer_3:
        mood_enhancer_entry_3 = Mood_Enhancer(
            user_id=user_id, mood_enhancer=user_mood_enhancer_3
        )
        db.session.add(mood_enhancer_entry_3)

        db.session.commit()

    mood_enhancers = user.mood_enhancers

    return redirect(f"update-mood-enhancers/{user_id}")


@app.route("/update-mood-enhancers/<int:user_id>", methods=["POST", "GET"])
def show_mood_enhancers(user_id):

    user = User.query.get(user_id)
    mood_enhancers = user.mood_enhancers

    user = User.query.get(user_id)

    return render_template(
        "update-mood-enhancers.html", mood_enhancers=mood_enhancers, user=user
    )


@app.route("/update-mood-enhancer/<int:user_id>", methods=["POST", "GET"])
def update_mood_enhancer(user_id):

    user = User.query.get(user_id)

    delete_enhancer = request.form.getlist("delete_mood_enhancer")

    to_delete = []
    for enhancer in delete_enhancer:
        to_delete.append(int(enhancer))

    for mood_enhancer_id in to_delete:
        mood_enhancer = Mood_Enhancer.query.get(mood_enhancer_id)
        db.session.delete(mood_enhancer)

    db.session.commit()

    return redirect("/update-mood-enhancers/{}".format(user.user_id))


@app.route("/associated-moods/<int:user_id>")
def show_associated_moods_form(user_id):

    # grabs all moods and activities
    moods = Mood.query.all()

    return render_template("associated-moods.html", moods=moods)


@app.route("/associated-moods", methods=["GET", "POST"])
def redirect_associated_mood():

    # grab the mood_id from the form
    user_mood_id = request.form.get("mood")

    # set the mood_id to id grabbed from the form
    mood_id = user_mood_id

    return redirect("/moods/{}/entries".format(mood_id))


@app.route("/moods/<int:mood_id>/entries", methods=["GET", "POST"])
def show_mood(mood_id):

    user_id = session.get("user_id")
    user = User.query.get(user_id)

    entries = (
        Entry.query.filter_by(mood_id=mood_id, user_id=session["user_id"])
        .limit(10)
        .all()
    )
    mood = Mood.query.get(mood_id)
    verbose_mood = mood.verbose_mood

    activities = []
    for entry in entries:
        for activity in entry.activities:
            activities.append(activity.verbose_category)

    return render_template(
        "show-mood.html",
        verbose_mood=verbose_mood,
        activities=set(activities),
        user=user,
    )


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.autoreload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(port=5000, host="0.0.0.0")

