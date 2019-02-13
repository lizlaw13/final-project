"""Seed default moods and activities to  database"""

from sqlalchemy import func


from model import *
from server import app

connect_to_db(app)


# Add moods
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

# Add categories
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

# Add users
Liz = User(email="liz@gmail.com", password="abc123")
Ashley = User(email="ash@gmail.com", password="corg123")
Jess = User(email="jess@gmail.com", password="hm123")
Sarah = User(email="sarah@gmail.com", password="mentor122")
Eric = User(email="eric@gmail.com", password="mentor123")


# Add entries for users
Jess.entries.append(Entry(date_created='2019-02-1 20:31:05.974887' ,mood=Fantastic, activity_category=Work))
Jess.entries.append(Entry(date_created='2019-02-2 20:31:05.974887' ,mood=Fantastic, activity_category=Work))
Jess.entries.append(Entry(date_created='2019-02-3 20:31:05.974887' ,mood=Neutral, activity_category=Work))
Jess.entries.append(Entry(date_created='2019-02-4 20:31:05.974887' ,mood=Terrible, activity_category=Work))
Jess.entries.append(Entry(date_created='2019-02-5 20:31:05.974887' ,mood=Fantastic, activity_category=Work))
Jess.entries.append(Entry(date_created='2019-02-6 20:31:05.974887' ,mood=Good, activity_category=Work))
Jess.entries.append(Entry(date_created='2019-02-7 20:31:05.974887' ,mood=Good, activity_category=Work))
Jess.entries.append(Entry(date_created='2019-02-8 20:31:05.974887' ,mood=Good, activity_category=Work))
Jess.entries.append(Entry(date_created='2019-02-9 20:31:05.974887' ,mood=Terrible, activity_category=Work))
Jess.entries.append(Entry(date_created='2019-02-10 20:31:05.974887' ,mood=Terrible, activity_category=Work))
Jess.entries.append(Entry(date_created='2019-02-11 20:31:05.974887' ,mood=Sad_Bad, activity_category=Work))
Jess.entries.append(Entry(date_created='2019-02-12 20:31:05.974887' ,mood=Sad_Bad, activity_category=Work))
Jess.entries.append(Entry(date_created='2019-02-13 20:31:05.974887' ,mood=Fantastic, activity_category=Work))




Liz.entries.append(Entry(mood=Terrible, activity_category=Social))

db.session.add(Liz)
db.session.add(Ashley)
db.session.add(Jess)
db.session.add(Sarah)
db.session.add(Eric)

db.session.commit()

    