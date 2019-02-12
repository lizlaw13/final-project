"""Seed default moods and activities to  database"""

from sqlalchemy import func


from model import *
from server import app

def load_moods():
    """Load moods into database."""

    Fantastic = Mood(mood="fantastic")
    Good = Mood(mood="good")
    Neutral = Mood(mood="neutral")
    Sad_Bad = Mood(mood="sad_bad")
    Terrible = Mood(mood="terrible")

    db.session.add(Fantastic)
    db.session.add(Good)
    db.session.add(Neutral)
    db.session.add(Sad_Bad)
    db.session.add(Terrible)

    db.session.commit()

def load_cateogories():
    """Load categories into database."""


    Work = Activity_Category(category="work")
    School_Work = Activity_Category(category="school_work")
    Social = Activity_Category(category="social")
    Leisure_Relaxation = Activity_Category(category="leisure_social")
    Exercise = Activity_Category(category="exercise")
    House_Work = Activity_Category(category="house_work")

    db.session.add(Work)
    db.session.add(School_Work)
    db.session.add(Leisure_Relaxation)
    db.session.add(Exercise)
    db.session.add(House_Work)

    db.session.commit()

def load_users():
    """Load categories into database."""

    Liz = User(email="liz@gmail.com", password="abc123")
    Ashley = User(email="ash@gmail.com", password="corg123")
    Jess = User(email="jess@gmail.com", password="hm123")
    Sarah = User(email="sarah@gmail.com", password="mentor122")
    Eric = User(email="eric@gmail.com", password="mentor123")

    db.session.add(Liz)
    db.session.add(Ashley)
    db.session.add(Jess)
    db.session.add(Sarah)
    db.session.add(Eric)

    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    # db.create_all()

    # db.session.rollback()

    # Import  data
    load_moods()
    load_cateogories()
    load_users()