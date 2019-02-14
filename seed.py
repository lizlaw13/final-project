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
# 
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

db.session.add(Liz)
db.session.add(Ashley)
db.session.add(Jess)
db.session.add(Sarah)
db.session.add(Eric)

db.session.commit()

# Add entries for users

Entry_One = Entry(mood_id= 1, user_id= 1, date_created='2019-02-1 20:31:05.974887')
Entry_One.activities.append(Leisure_Relaxation)
# Entry_Two = Entry(mood_id= 1, user_id= 1, date_created='2019-02-2 20:31:05.974887')
# Entry_Three = Entry(mood_id= 3, user_id= 1, date_created='2019-02-3 20:31:05.974887')
# Entry_Four = Entry(mood_id= 2, user_id= 1, date_created='2019-02-4 20:31:05.974887')
# Entry_Five = Entry(mood_id= 4, user_id= 1, date_created='2019-02-5 20:31:05.974887')
# Entry_Six = Entry(mood_id= 5, user_id= 1, date_created='2019-02-6 20:31:05.974887')
# Entry_Seven = Entry(mood_id= 3, user_id= 1, date_created='2019-02-7 20:31:05.974887')
# Entry_Seven = Entry(mood_id= 4, user_id= 1, date_created='2019-02-8 20:31:05.974887')
# Entry_Eight = Entry(mood_id= 1, user_id= 1, date_created='2019-02-9 20:31:05.974887')
# Entry_Nine = Entry(mood_id= 2, user_id= 1, date_created='2019-02-10 20:31:05.974887')
# Entry_Ten = Entry(mood_id= 2, user_id= 1, date_created='2019-02-11 20:31:05.974887')
# Entry_Eleven = Entry(mood_id= 1, user_id= 1, date_created='2019-02-12 20:31:05.974887')
# Entry_Twelve =Entry(mood_id=1, user_id= 1,date_created='2019-02-13 20:31:05.974887')

db.session.add(Entry_One)
# db.session.add(Entry_Two)
# db.session.add(Entry_Three)
# db.session.add(Entry_Four)
# db.session.add(Entry_Five)
# db.session.add(Entry_Six)
# db.session.add(Entry_Seven)
# db.session.add(Entry_Eight)
# db.session.add(Entry_Nine)
# db.session.add(Entry_Ten)
# db.session.add(Entry_Eleven)
# db.session.add(Entry_Twelve)


db.session.commit()

# Add activities for one user

# Activity_One = Entry_Activity(entry_id=1, activity_category_id=4)
# Activity_Two = Entry_Activity(entry_id=2, activity_category_id=2)
# Activity_Three = Entry_Activity(entry_id=3, activity_category_id=1)
# Activity_Four = Entry_Activity(entry_id=4, activity_category_id=4)
# Activity_Five = Entry_Activity(entry_id=5, activity_category_id=2)
# Activity_Six = Entry_Activity(entry_id=6, activity_category_id=3)
# Activity_Seven = Entry_Activity(entry_id=7, activity_category_id=3)
# Activity_Eight = Entry_Activity(entry_id=8, activity_category_id=3)
# Activity_Nine = Entry_Activity(entry_id=9, activity_category_id=4)
# Activity_Ten = Entry_Activity(entry_id=10, activity_category_id=4)
# Activity_Eleven = Entry_Activity(entry_id=11, activity_category_id=1)
# Activity_Twelve = Entry_Activity(entry_id=12, activity_category_id=2)

# db.session.add(Activity_One)
# db.session.add(Activity_Two)
# db.session.add(Activity_Three)
# db.session.add(Activity_Four)
# db.session.add(Activity_Five)
# db.session.add(Activity_Six)
# db.session.add(Activity_Seven)
# db.session.add(Activity_Eight)
# db.session.add(Activity_Nine)
# db.session.add(Activity_Ten)
# db.session.add(Activity_Eleven)
# db.session.add(Activity_Twelve)

# db.session.commit()

    