import datetime
import hashlib

from flask_debugtoolbar import DebugToolbarExtension
from flask import (
    Flask,
    render_template,
    redirect,
    request,
    flash,
    session,
    url_for,
    jsonify,
)
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_paginate import Pagination, get_page_args
from jinja2 import StrictUndefined
from sqlalchemy import func, asc

import indicoio
import os

from database import connect_to_db, db
from model import *

app = Flask(__name__)
CORS(app)

app.secret_key = "ZILWAL"

app.jinja_env.undefined = StrictUndefined


@app.context_processor
def get_user():
    user_id = None
    if session.get("user_id"):
        user_id = session.get("user_id")
    return dict(user_id=user_id)

@app.route("/", methods=["POST", "GET"])
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
    new_user_email = request.form.get("inputEmail4")
    new_user_password = request.form.get("inputPassword4")
    if not new_user_email or not new_user_password:
            flash("Please resubmit your information correctly.")
            return redirect("/")

    # hash the password
    hash_object = hashlib.md5(new_user_password.encode())

    # grab the hashed password
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

    if not email or not form_password:
        flash("Please resubmit your information correctly.")
        return redirect("/")


    # hash the password provided
    hash_object = hashlib.md5(form_password.encode())

    # querying by the password provided by the user
    user = User.query.filter_by(email=email).first()
    password = user.password

    # if the hash password matches the password in the database then
    # log user in and create a session
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

    # retreiving user id and all moods and activities to be able to use in a form
    user = User.query.get(user_id)
    moods = Mood.query.all()
    activities = Activity_Category.query.all()

    # generating today's date to display on the page
    now = datetime.datetime.today().strftime("%A, %B %d, %Y")

    # if a user has already entered an entry for today's date- do not let then add another entry
    # >>
    # generate today's date to use as a compare date
    time = datetime.datetime.now()
    compare_time = time.date()

    # query to find all brain dumps
    brain_dumps = User_Brain_Dump.query.filter_by(user_id=user.user_id).all()

    # if there is an entry that exists with todays date set show_form to false
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
    if not session.get("user_id") or session["user_id"] != user_id:
        return redirect("/")

    # grab all the users entries
    user = User.query.get(user_id)
    entries = Entry.query.filter_by(user_id=user_id).order_by("date_created").all()

    page, per_page, offset = get_page_args(
        page_parameter="page", per_page_parameter="per_page"
    )

    per_page = 5

    offset = (page - 1) * per_page
    total = len(entries)

    pagination_entries = entries[offset : offset + per_page]
    pagination = Pagination(
        page=page, per_page=per_page, total=total, css_framework="bootstrap4"
    )

    return render_template(
        "all-entries.html",
        entries=pagination_entries,
        user=user,
        page=page,
        per_page=per_page,
        pagination=pagination,
    )


@app.route("/brain-dump/<int:user_id>", methods=["POST", "GET"])
def show_brain_dump_form(user_id):
    """Show brain dump form to add a brain dump entry"""

    # grab user in the session
    user_id = session.get("user_id")

    # generate today's date
    now = datetime.datetime.today().strftime("%A, %B %d, %Y")

    # grab infomration from params to check if a user is updating or created a new entry
    updated = request.args.get("updated")

    return render_template("brain-dump.html", user_id=user_id, now=now, updated=updated)


@app.route("/brain-dump", methods=["POST", "GET"])
def add_brain_dump():
    """Adds a brain dump to the database"""

    # grab user in the session
    user_id = session.get("user_id")

    # grab the user text from form
    user_brain_dump = request.form["brain_dump"]

    if not user_brain_dump:
        flash("Please resubmit your information correctly.")
        return redirect(f"/brain-dump/{user_id}")

    # add brain dump to database
    brain_dump = User_Brain_Dump(user_id=user_id, brain_dump_entry=user_brain_dump)

    db.session.add(brain_dump)
    db.session.commit()

    flash("You have successfully added a brain dump entry!")

    return redirect(f"/brain-dump/{user_id}")


@app.route("/update-brain-dump/<int:brain_dump_id>", methods=["POST", "GET"])
def update_brain_dump(brain_dump_id):
    """Shows the brain dump form to update a brain dump entry"""

    # grab brain dump entry id
    entry_id = brain_dump_id

    # grab the user text from form
    user_brain_dump = request.form["brain_dump"]
    current_entry = User_Brain_Dump.query.get(entry_id)

    # udpate the current entry
    current_entry.brain_dump_entry = user_brain_dump
    db.session.commit()

    # set variable to pass to method show_brain_dump_details()
    updated = "yes"

    flash("You have successfully updated your brain dump entry!")

    return redirect(
        url_for("show_brain_dump_details", user_brain_dump_id=entry_id, updated=updated)
    )


@app.route("/all-brain-dumps/<int:user_id>", methods=["POST", "GET"])
def show_all_brain_dumps(user_id):
    """Show all user brain dumps"""

    # grab user in the session
    user_id = session.get("user_id")

    # grabs all the brain dumps from the user and order them by date created
    brain_dumps = (
        User_Brain_Dump.query.filter_by(user_id=user_id).order_by("date_created").all()
    )

    page, per_page, offset = get_page_args(
        page_parameter="page", per_page_parameter="per_page"
    )

    per_page = 5

    offset = (page - 1) * per_page
    total = len(brain_dumps)

    pagination_brain_dumps = brain_dumps[offset : offset + per_page]
    pagination = Pagination(
        page=page, per_page=per_page, total=total, css_framework="bootstrap4"
    )

    return render_template(
        "all-brain-dumps.html",
        brain_dumps=pagination_brain_dumps,
        user_id=user_id,
        per_page=per_page,
        pagination=pagination,
    )


@app.route("/brain-dump-details")
def brain_dump_entry(user_brain_dump_id):
    """Generate URL for brain dump details"""

    return redirect(f"/brain-dump-details/{user_brain_dump_id}")


@app.route("/brain-dump-details/<int:user_brain_dump_id>/", methods=["GET", "POST"])
def show_brain_dump_details(user_brain_dump_id):
    """Shows brain dump details for specific entry for a user"""

    # converting id entry id to an integer and querying to grab specific entry
    id = int(user_brain_dump_id)
    brain_dump = User_Brain_Dump.query.filter_by(user_brain_dump_id=id).first()

    # grabs all the necessary params passed in
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
    # >>
    # converting id entry id to an integer and querying to grab specific entry
    id = int(user_brain_dump_id)
    brain_dump = User_Brain_Dump.query.filter_by(user_brain_dump_id=id).first()

    # grabbing text from entry
    text = brain_dump.brain_dump_entry

    # passing API key
    KEY = os.getenv("I_KEY")
    indicoio.config.api_key = KEY

    # this  will return a number between 0 and 1. This number is a probability representing the
    # likelihood that the analyzed text is positive or negative. Values greater than 0.5 indicate
    #  positive sentiment, while values less than 0.5 indicate negative sentiment.
    sentiment_value = indicoio.sentiment([text])

    # converts from int to float
    for value in sentiment_value:
        num_value = float(value)

    value = num_value

    # setting positive and negative depending on the score
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
        return redirect(f"brain-dump-details/{id}")


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
    """Allows users to reanalyze their entry"""

    # grabs the specific brain_dump id
    brain_dump = User_Brain_Dump.query.get(brain_dump_id)

    # grabs the entry's user id
    user_id = brain_dump.user_id

    # empty's all analysis columns from database
    brain_dump.analysis_confirmation = None
    brain_dump.verbose_analysis = None
    brain_dump.analysis = None

    db.session.commit()

    return redirect(f"brain-dump-details/{brain_dump_id}")


@app.route("/delete-brain-dump/<int:brain_dump_id>")
def delete_brain_dump_entry(brain_dump_id):
    """Deletes brain dump entries"""

    # grabs the specific brain_dump id
    brain_dump = User_Brain_Dump.query.get(brain_dump_id)

    # grabs the entry's user id
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

    sorted_dates = [entry.date_created.strftime("%m-%d") for entry in entries]

    # create values to pass to the tempplate
    legend = "Mood Data"

    has_entries = True
    print("hello:", sorted_dates)

    # if a user only has one entry do not display chart
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
    """"Shows donut chart of user's mood over time"""

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

    # if a user only has one entry do not display chart
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
    if not session.get("user_id") or session["user_id"] != user_id:
        return redirect("/")

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

    # prevents the public for accessing user specific information
    # if not session.get("user_id") or session["user_id"] != user_id:
    #     return redirect("/")

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


@app.route("/update-entry/<int:entry_id>", methods=["GET"])
def update_form(entry_id):
    id = entry_id
    print("testing")

    return render_template("update-entry.html", entry_id=id)


@app.route("/update/<int:entry_id>", methods=["GET"])
def show_update_form(entry_id):
    print("hi")
    """Displays the update form for a user"""

    # grabs the specific entry id
    entry = Entry.query.get(entry_id)
    mood_id = entry.mood_id

    # prevents the public for accessing user specific information
    # if not session.get("user_id") or session["user_id"] != user_id:
    #     return redirect("/")

    # grabs the user's information
    user = User.query.get(entry.user.user_id)

    # grabs all moods and activities
    moods = Mood.query.all()
    activities = Activity_Category.query.all()

    user_mood_info = Mood.query.filter_by(mood_id=mood_id).first()
    entry_mood = user_mood_info.verbose_mood

    entry_date = entry.date_created.strftime("%B %d, %Y")

    entry_activities = entry.activities

    entry_description = entry.description
    return jsonify(
        {
            "moods": [
                {"mood_id": mood.mood_id, "verbose_mood": mood.verbose_mood}
                for mood in moods
            ],
            "activities": [
                {
                    "activity_category_id": activity.activity_category_id,
                    "verbose_category": activity.verbose_category,
                }
                for activity in activities
            ],
            "entry": {
                "entry_mood": entry_mood,
                "entry_date": entry_date,
                "entry_description": entry_description,
                "entry_id": entry_id,
                "user_id": user.user_id,
            },
            "entry_activities": [
                {
                    "activity": activity.verbose_category,
                    "activity_id": activity.activity_category_id,
                }
                for activity in entry.activities
            ],
        }
    )

    # return render_template(
    #     "update-entry.html", entry=entry, user=user, moods=moods, activities=activities
    # )


@app.route("/updated-entry/<int:entry_id>", methods=["POST", "GET"])
def update_entry(entry_id):
    """Confirmation that a user has added an activity or updated their mood on their entry"""

    entry = Entry.query.get(entry_id)
    user_id = session["user_id"]
    print(entry)
    # if user_id != entry.user.user_id:
    #     return redirect("/")

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
    elif description and entry.description:
        entry.description += ", " + description
    elif description and entry.description is None:
        entry.description = description

    form_activities = []
    for activity_id in user_activities:
        form_activities.append(Activity_Category.query.get(int(activity_id)))

    activities = entry.activities

    entry.activities.extend(form_activities)

    db.session.commit()

    flash("You have successfully updated an entry!")

    # return redirect(f"/all-entries/{user_id}")
    return redirect(f"/update-entry/{entry.entry_id}")


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
    if int_user_mood == 1 or int_user_mood == 2:
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
    """Allows users to add mood enhancers"""

    user_id = session.get("user_id")
    id = user_id

    user = User.query.get(user_id)

    entry = Entry.query.filter_by(user_id=user_id)

    # make form reactive such that you only show one text back and you enter one and it adds a new one
    user_mood_enhancer_1 = request.form.get("mood_enhancer_1")
    user_mood_enhancer_2 = request.form.get("mood_enhancer_2")
    user_mood_enhancer_3 = request.form.get("mood_enhancer_3")

    # function to add mood enhancer to database
    def add_mood_enhancer(user_mood_enhancer):
        mood_enhancer = Mood_Enhancer(user_id=user_id, mood_enhancer=user_mood_enhancer)
        db.session.add(mood_enhancer)
        db.session.commit()

    if user_mood_enhancer_1:
        add_mood_enhancer(user_mood_enhancer_1)
    if user_mood_enhancer_2:
        add_mood_enhancer(user_mood_enhancer_2)
    if user_mood_enhancer_3:
        add_mood_enhancer(user_mood_enhancer_3)

    mood_enhancers = user.mood_enhancers

    # return redirect(f"update-mood-enhancers/{user_id}")
    return render_template("update-mood-enhancers.html", user_id=user_id)


@app.route("/update-mood-enhancers/<int:user_id>", methods=["GET"])
def show_mood_enhancers(user_id):
    """Shows all user's mood enhancers"""

    user = User.query.get(user_id)
    mood_enhancers = user.mood_enhancers

    user = User.query.get(user_id)

    return jsonify(
        {
            "user": user.user_id,
            "mood_enhancers": [
                {
                    "mood_enhancer": mood_enhancer.mood_enhancer,
                    "mood_enhancer_id": mood_enhancer.mood_enhancer_id,
                }
                for mood_enhancer in mood_enhancers
            ],
        }
    )

    # return render_template(
    #     "update-mood-enhancers.html", mood_enhancers=mood_enhancers, user=user
    # )


@app.route("/delete-mood-enhancer/<int:user_id>", methods=["POST"])
def update_mood_enhancer(user_id):
    """Allows users to update their mood enhancers"""

    user = User.query.get(user_id)

    delete_enhancer = request.form.getlist("mood_enhancer")

    to_delete = []
    for enhancer in delete_enhancer:
        to_delete.append(int(enhancer))

    for mood_enhancer_id in to_delete:
        mood_enhancer = Mood_Enhancer.query.get(mood_enhancer_id)
        db.session.delete(mood_enhancer)

    db.session.commit()

    return render_template("update-mood-enhancers.html", user_id=user.user_id)


@app.route("/associated-moods/<int:user_id>")
def show_associated_moods_form(user_id):
    """Allows users to view all activities with a mood"""

    # grabs all moods and activities
    moods = Mood.query.all()

    return render_template("associated-moods.html", moods=moods)


@app.route("/associated-moods", methods=["GET", "POST"])
def redirect_associated_mood():
    """Grabs the mood inputted from the user"""

    # grab the mood_id from the form
    user_mood_id = request.form.get("mood")

    # set the mood_id to id grabbed from the form
    mood_id = user_mood_id

    return redirect("/moods/{}/entries".format(mood_id))


@app.route("/moods/<int:mood_id>/entries", methods=["GET", "POST"])
def show_mood(mood_id):
    """Shows all the associated activities depending on the mood"""

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

