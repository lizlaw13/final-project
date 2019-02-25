"""Seed default moods and activities to  database"""

from sqlalchemy import func


from model import *
from server import app

import hashlib


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

db.session.commit()

# Add categories
work = Activity_Category(category="work", verbose_category="Work")
schoolWork = Activity_Category(category="school_work", verbose_category="School Work")
social = Activity_Category(category="social", verbose_category="Social")
leisureRelaxation = Activity_Category(
    category="leisure_social", verbose_category="Leisure/Relaxation"
)
exercise = Activity_Category(category="exercise", verbose_category="Exercise")
houseWork = Activity_Category(category="house_work", verbose_category="House Work")

db.session.add(work)
db.session.add(schoolWork)
db.session.add(leisureRelaxation)
db.session.add(exercise)
db.session.add(houseWork)

db.session.commit()

# Add users and hash user passwords
liz_password = "abc123"
hash_object = hashlib.md5(liz_password.encode())
liz_password = hash_object.hexdigest()
liz = User(email="liz@gmail.com", password=liz_password)
db.session.add(liz)

ash_password = "corg123"
hash_object = hashlib.md5(ash_password.encode())
ash_password = hash_object.hexdigest()
ashley = User(email="ashley@gmail.com", password=ash_password)
db.session.add(ashley)

jess_password = "hm123"
hash_object = hashlib.md5(jess_password.encode())
jess_password = hash_object.hexdigest()
jess = User(email="jess@gmail.com", password=jess_password)
db.session.add(jess)

db.session.commit()

# Add entries for users

entryOne = Entry(mood_id=1, user_id=1, date_created="2019-02-01 19:33:54.99179+00")
entryOne.activities.append(leisureRelaxation)
entryOne.activities.append(exercise)
entryTwo = Entry(mood_id=2, user_id=1, date_created="2019-02-02 19:33:54.99179+00")
entryTwo.activities.append(houseWork)
entryTwo.activities.append(exercise)
entryThree = Entry(
    mood_id=3,
    user_id=1,
    date_created="2019-02-03 19:33:54.99179+00",
    description="drinks with friends, 2 hour spin class",
)
entryThree.activities.append(social)
entryThree.activities.append(leisureRelaxation)
entryThree.activities.append(exercise)
entryFour = Entry(mood_id=2, user_id=1, date_created="2019-02-04 19:33:54.99179+00")
entryFour.activities.append(schoolWork)
entryFive = Entry(mood_id=3, user_id=1, date_created="2019-02-05 19:33:54.99179+00")
entryFive.activities.append(exercise)

entrySix = Entry(mood_id=1, user_id=1, date_created="2019-02-06 19:33:54.99179+00")
entrySix.activities.append(leisureRelaxation)
entrySix.activities.append(exercise)
entrySeven = Entry(mood_id=2, user_id=1, date_created="2019-02-07 19:33:54.99179+00")
entrySeven.activities.append(houseWork)
entrySeven.activities.append(exercise)
entryEight = Entry(
    mood_id=3,
    user_id=1,
    date_created="2019-02-08 19:33:54.99179+00",
    description="drinks with no one",
)
entryEight.activities.append(social)
entryEight.activities.append(leisureRelaxation)
entryEight.activities.append(exercise)
entryNine = Entry(mood_id=2, user_id=1, date_created="2019-02-09 19:33:54.99179+00")
entryNine.activities.append(schoolWork)
entryNine = Entry(
    mood_id=3,
    user_id=1,
    date_created="2019-02-10 19:33:54.99179+00",
    description="hiking with my me",
)
entryNine.activities.append(exercise)
entryNine.activities.append(social)
entryNine.activities.append(leisureRelaxation)
entryNine.activities.append(exercise)
entryTen = Entry(mood_id=2, user_id=1, date_created="2019-02-11 19:33:54.99179+00")
entryTen.activities.append(schoolWork)
entryEleven = Entry(
    mood_id=1,
    user_id=1,
    date_created="2019-02-12 19:33:54.99179+00",
    description="hiking with my dog",
)
entryEleven.activities.append(exercise)
entryTwelve = Entry(
    mood_id=1,
    user_id=1,
    date_created="2019-02-13 19:33:54.99179+00",
    description="hiking with my cat",
)
entryTwelve.activities.append(exercise)
entryThirteen = Entry(
    mood_id=2,
    user_id=1,
    date_created="2019-02-14 19:33:54.99179+00",
    description="hiking with maddie",
)
entryThirteen.activities.append(exercise)
entryFourteen = Entry(
    mood_id=4,
    user_id=1,
    date_created="2019-02-15 19:33:54.99179+00",
    description="hiking with myself",
)
entryFourteen.activities.append(exercise)


# entryOne = Entry(mood_id= 1, user_id= 1, date_created='2019-02-1 20:31:05.974887')
# entryOne.activities.append(leisureRelaxation)
# entryOne.activities.append(exercise)
# entryTwo = Entry(mood_id= 4, user_id= 1, date_created='2019-02-2 20:31:05.974887')
# entryTwo.activities.append(houseWork)
# entryTwo.activities.append(exercise)
# entryThree = Entry(mood_id= 3, user_id= 1, date_created='2019-02-3 20:31:05.974887')
# entryThree.activities.append(social)
# entryThree.activities.append(leisureRelaxation)
# entryThree.activities.append(exercise)
# entryFour = Entry(mood_id= 2, user_id= 1, date_created='2019-02-4 20:31:05.974887')
# entryFour.activities.append(schoolWork)
# entryFive = Entry(mood_id= 4, user_id= 1, date_created='2019-02-5 20:31:05.974887')
# entryFive.activities.append(exercise)
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
db.session.add(entrySix)
db.session.add(entrySeven)
db.session.add(entryEight)
db.session.add(entryNine)
db.session.add(entryTen)
db.session.add(entryEleven)
db.session.add(entryTwelve)
db.session.add(entryThirteen)
db.session.add(entryFourteen)


mood_enhancer_entry_1 = Mood_Enhancer(user_id=1, mood_enhancer="Go for a walk")
mood_enhancer_entry_2 = Mood_Enhancer(user_id=1, mood_enhancer="Call best friend")
mood_enhancer_entry_3 = Mood_Enhancer(user_id=1, mood_enhancer="Listen to music")

db.session.add(mood_enhancer_entry_1)
db.session.add(mood_enhancer_entry_2)
db.session.add(mood_enhancer_entry_3)


db.session.commit()


mood_entry_one = User_Brain_Dump(
    user_id=1,
    brain_dump_entry="today i am so happy i could die",
    date_created="2019-02-01 20:31:05.974887",
)
mood_entry_two = User_Brain_Dump(
    user_id=1,
    brain_dump_entry="today i am so sad",
    date_created="2019-02-02 20:31:05.974887",
)

mood_entry_three = User_Brain_Dump(
    user_id=1,
    brain_dump_entry="today i am feeling ok i am excited to go for a hike",
    date_created="2019-02-03 20:31:05.974887",
)


db.session.add(mood_entry_one)
db.session.add(mood_entry_two)
db.session.add(mood_entry_one)


db.session.commit()
