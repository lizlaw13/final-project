"""Models and database functions for final project."""
# from SQLAlchemy import timestamp
import datetime

# from database import *

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Model definitions


class User(db.Model):
    """"User of website"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    first_name = db.Column(db.String(200), nullable=True)
    last_name = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(200))
    password = db.Column(db.String(100))

    # many to many relationship
    moods = db.relationship("Mood", backref="users", secondary="entries")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User user_id={self.user_id} email={self.email}>"


class Mood(db.Model):
    """Moods users can select from"""

    __tablename__ = "moods"

    mood_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    mood = db.Column(db.String(30))
    verbose_mood = db.Column(db.String(30))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Mood mood_id={self.mood_id} mood={self.mood} verbose_mood={self.verbose_mood}>"


class Activity_Category(db.Model):
    """"Activties users can select from"""

    __tablename__ = "activities"

    activity_category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category = db.Column(db.String(30))
    verbose_category = db.Column(db.String(30))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Activity activity_category_id={self.activity_category_id} category={self.category}>"


class Entry_Activity(db.Model):

    __tablename__ = "entry_activities"

    entry_activity_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    entry_id = db.Column(db.Integer, db.ForeignKey("entries.entry_id"))
    activity_category_id = db.Column(
        db.Integer, db.ForeignKey("activities.activity_category_id")
    )

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Entry_Activity entry_id={self.entry_id} activity_category_id={self.activity_category_id}>"


class Entry(db.Model):
    """Daily entries for each user"""

    __tablename__ = "entries"

    entry_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    mood_id = db.Column(db.Integer, db.ForeignKey("moods.mood_id"))
    description = db.Column(db.Text, nullable=True)

    # one to many relationship
    user = db.relationship("User", backref="entries")
    mood = db.relationship("Mood", backref="entries")

    # many to many
    activities = db.relationship(
        "Activity_Category", backref="entries", secondary="entry_activities"
    )

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<Entry entry_id={self.entry_id} date_created={self.date_created} user_id={self.user_id} mood_id={self.mood_id} description={self.description}>"


class Mood_Enhancer(db.Model):
    """Optional inputed description from user to enhance mood"""

    __tablename__ = "mood_enhancers"

    mood_enhancer_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    mood_enhancer = db.Column(db.Text, nullable=True)

    users = db.relationship("User", backref="mood_enhancers")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<Mood Enhancer mood_enhancer_id={self.mood_enhancer_id}
            user_id={self.user_id} mood_enhancer={self.mood_enhancer}>"""


class User_Brain_Dump(db.Model):
    """Optional inputed description from user as a diary entry """

    __tablename__ = "user_brain_dumps"

    user_brain_dump_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    brain_dump_entry = db.Column(db.Text, nullable=True)
    analysis_confirmation = db.Column(db.String(10), nullable=True)
    verbose_analysis = db.Column(db.String(10), nullable=True)
    analysis = db.Column(db.DECIMAL(18, 4), nullable=True)

    users = db.relationship("User", backref="user_brain_dumps")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<User Brain Dump user_brain_dump_id={self.user_brain_dump_id}
            user_id={self.user_id}>"""


################################################################################
# Helper functions


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///tracker"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    # Used to recreate my database if I need to drop
    db.create_all()


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app

    connect_to_db(app)
    print("Connected to DB.")

