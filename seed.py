"""Seed default moods and activities to  database"""

from sqlalchemy import func


from model import *
from server import app

connect_to_db(app)
 # add functions

# Add moods
fantastic = Mood(mood="fantastic", verbose_mood="Fantastic")
good = Mood(mood="good", verbose_mood="Good")
neutral = Mood(mood="neutral", verbose_mood="Neutral")
bad = Mood(mood="sad_bad", verbose_mood="Sad/Bad")
terrible = Mood(mood="terrible", verbose_mood="Terrible")

db.session.add(fantastic)
db.session.add(good)
db.session.add(neutral)
db.session.add(bad)
db.session.add(terrible)
# 
db.session.commit()

# Add categories
work = Activity_Category(category="work", verbose_category="Work")
schoolWork = Activity_Category(category="school_work", verbose_category="School Work")
social = Activity_Category(category="social", verbose_category="Social")
leisureRelaxation = Activity_Category(category="leisure_social", verbose_category="Leisure/Relaxation")
exercise = Activity_Category(category="exercise", verbose_category="Exercise")
houseWork = Activity_Category(category="house_work", verbose_category="House Work")

db.session.add(work)
db.session.add(schoolWork)
db.session.add(leisureRelaxation)
db.session.add(exercise)
db.session.add(houseWork)

db.session.commit()

# Add users
liz = User(email="liz@gmail.com", password="abc123")
ashley = User(email="ash@gmail.com", password="corg123")
jess = User(email="jess@gmail.com", password="hm123")

db.session.add(liz)
db.session.add(ashley)
db.session.add(jess)

db.session.commit()

# Add entries for users

entryOne = Entry(mood_id= 1, user_id= 1, date_created='2019-02-1 20:31:05.974887')
entryOne.activities.append(leisureRelaxation)
entryOne.activities.append(exercise)
entryTwo = Entry(mood_id= 4, user_id= 1, date_created='2019-02-2 20:31:05.974887')
entryTwo.activities.append(houseWork)
entryTwo.activities.append(exercise)
entryThree = Entry(mood_id= 3, user_id= 1, date_created='2019-02-3 20:31:05.974887')
entryThree.activities.append(social)
entryThree.activities.append(leisureRelaxation)
entryThree.activities.append(exercise)
entryFour = Entry(mood_id= 2, user_id= 1, date_created='2019-02-4 20:31:05.974887')
entryFour.activities.append(schoolWork)
entryFive = Entry(mood_id= 4, user_id= 1, date_created='2019-02-5 20:31:05.974887')
entryFive.activities.append(exercise)
# Entry_Six = Entry(mood_id= 5, user_id= 1, date_created='2019-02-6 20:31:05.974887')
# Entry_Seven = Entry(mood_id= 3, user_id= 1, date_created='2019-02-7 20:31:05.974887')
# Entry_Seven = Entry(mood_id= 4, user_id= 1, date_created='2019-02-8 20:31:05.974887')
# Entry_Eight = Entry(mood_id= 1, user_id= 1, date_created='2019-02-9 20:31:05.974887')
# Entry_Nine = Entry(mood_id= 2, user_id= 1, date_created='2019-02-10 20:31:05.974887')
# Entry_Ten = Entry(mood_id= 2, user_id= 1, date_created='2019-02-11 20:31:05.974887')
# Entry_Eleven = Entry(mood_id= 1, user_id= 1, date_created='2019-02-12 20:31:05.974887')
# Entry_Twelve =Entry(mood_id=1, user_id= 1,date_created='2019-02-13 20:31:05.974887')

db.session.add(entryTwo)
db.session.add(entryOne)
db.session.add(entryThree)
db.session.add(entryFour)
db.session.add(entryFive)





db.session.commit()

    