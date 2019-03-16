from sqlalchemy import func


from model import *
from server import app

import hashlib

connect_to_db(app)

"""Seed default moods and activities to  database"""

# Add moods
fantastic = Mood(mood="fantastic", verbose_mood="Fantastic", mood_id=5)
good = Mood(mood="good", verbose_mood="Good", mood_id=4)
neutral = Mood(mood="neutral", verbose_mood="Neutral", mood_id=3)
bad = Mood(mood="sad_bad", verbose_mood="Sad/Bad", mood_id=2)
terrible = Mood(mood="terrible", verbose_mood="Terrible", mood_id=1)

db.session.add(fantastic)
db.session.add(good)
db.session.add(neutral)
db.session.add(bad)
db.session.add(terrible)

db.session.commit()

# Add activity categories
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

# Add user and hash user passwords
liz_password = "abc123"
hash_object = hashlib.md5(liz_password.encode())
liz_password = hash_object.hexdigest()
liz = User(email="liz@gmail.com", password=liz_password)
db.session.add(liz)

db.session.commit()

# Add entries for user

entryOne = Entry(mood_id=5, user_id=1, date_created="2019-02-16 14:33:54.99179+00")
entryOne.activities.append(leisureRelaxation)
entryOne.activities.append(exercise)

entryTwo = Entry(mood_id=3, user_id=1, date_created="2019-02-17 10:33:54.99179+00")
entryTwo.activities.append(houseWork)
entryTwo.activities.append(exercise)

entryThree = Entry(
    mood_id=4,
    user_id=1,
    date_created="2019-02-18 22:33:54.99179+00",
    description="""I took a two hour spin class in the morning and in the evening I went downtown to 
                grab drinks with a couple of friends.""",
)
entryThree.activities.append(social)
entryThree.activities.append(leisureRelaxation)
entryThree.activities.append(exercise)

entryFour = Entry(
    mood_id=2,
    user_id=1,
    date_created="2019-02-19 17:33:54.99179+00",
    description="""
                I spent most of my day at Starbucks tweaking my resume. I also spent
                a little time solving some coding challengings and prepped for my behavoiral interview.""",
)
entryFour.activities.append(schoolWork)
entryFour.activities.append(work)


entryFive = Entry(
    mood_id=1,
    user_id=1,
    date_created="2019-02-19 10:33:54.99179+00",
    description="""
                All I have gotten done today was some major house work. I ended up cleaning
                my entire room and bathroom. I  also did three loads of laundry and went to
                Pet Express to give my dog a much needed bath.""",
)
entryFive.activities.append(houseWork)

entrySix = Entry(
    mood_id=5,
    user_id=1,
    date_created="2019-02-21 18:33:54.99179+00",
    description="""
                I went to get brunch with my best friend at a café called Home in the Sunset. After we
                decided to go window shopping in the Marina. I then came home and applied for jobs.""",
)
entrySix.activities.append(leisureRelaxation)
entrySix.activities.append(work)
entrySix.activities.append(social)


entrySeven = Entry(mood_id=3, user_id=1, date_created="2019-02-22 19:33:54.99179+00")
entrySeven.activities.append(houseWork)
entrySeven.activities.append(exercise)


entryEight = Entry(
    mood_id=2,
    user_id=1,
    date_created="2019-02-23 12:33:54.99179+00",
    description="""Today I went on a hike with my dog but my dog somehow got out of her harness and
                I had to chase her all over the beach. She got so busy so I had to give her a bath.
                In an attempt to make myself feel better I ended up going to an evening spin class.""",
)
entryEight.activities.append(social)
entryEight.activities.append(exercise)


entryNine = Entry(mood_id=5, user_id=1, date_created="2019-02-24 22:33:54.99179+00")
entryNine.activities.append(social)
entryNine.activities.append(exercise)
entryNine.activities.append(schoolWork)


entryTen = Entry(mood_id=1, user_id=1, date_created="2019-02-25 23:33:54.99179+00")
entryTen.activities.append(houseWork)
entryTen.activities.append(work)


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

db.session.commit()

# # Added brain dumps

mood_entry_one = User_Brain_Dump(
    user_id=1,
    brain_dump_entry="""What a busy day today!  I never had a moment’s rest. The day started with my alarm clock blaring at 7am.  I had to be at the Smith’s house by 8am to baby-sit. I really didn’t want to wake up so early on a Saturday, but I’m saving money to buy a new laptop and couldn’t say no to an all-day babysitting job.""",
    date_created="2019-02-01 23:31:05.974887",
)
mood_entry_two = User_Brain_Dump(
    user_id=1,
    brain_dump_entry="""Today I am going to Disneyland for the first time. I am so excited- I am going with my niece, nephew, and cousin. They've also never been to Disneyland so we are not sure what to expect. But, they do love roller coasters and Star Wars so I expect it to be a good time no matter what. I heard they also have a fireworks show in the evening!""",
    date_created="2019-02-27 10:31:05.974887",
)

mood_entry_three = User_Brain_Dump(
    user_id=1,
    brain_dump_entry="""I am so upset because today is my last day at Disneyland with my family. We all had such a good time- there is so much to do. I think the next time we visit we need more than just two days. We could not get around to going on every ride or seeing every show. I think my favorite ride was Matterhorn or even Haunted Mansion. My poor niece was so scared on Haunted Mansion so we had to buy her some ice cream right after to cheer her up.""",
    date_created="2019-02-27 10:31:05.974887",
)
mood_entry_four = User_Brain_Dump(
    user_id=1,
    brain_dump_entry="""It is only 9am but I have already deemed today being the worst day of my life. I was planning on taking a flight to Oregon so I could visit my best friend but my flight ended up being cancelled- which is so upsetting because I haven't seen my best friend in over 6 months. We had a lot of thigns planned but now I can't go. Apparently there is a tornado which is so weird because tornados do not normally happed in California???""",
    date_created="2019-03-10 18:33:54.99179+00",
)
mood_entry_five = User_Brain_Dump(
    user_id=1,
    brain_dump_entry="""I got food poisoning today- or so I thought. I ate In N Out for lunch and some time after I was puking. It was embarassing because I had invited my friend over to watch a movie. But instead- I started puking from food poisoning. My friend ended up having to leave. I tried to take a nap but I was in too much pain. I ended up getting a call from my boss warning me that the the Noro Virus had been spreading around at work. So it looks like I contracted the Noro Virus......""",
    date_created="2019-03-14 21:33:54.99179+00",
)
mood_entry_six = User_Brain_Dump(
    user_id=1,
    brain_dump_entry="I am so happy I could die.",
    date_created="2019-03-15 23:33:54.99179+00",
)

db.session.add(mood_entry_one)
db.session.add(mood_entry_two)
db.session.add(mood_entry_three)
db.session.add(mood_entry_four)
db.session.add(mood_entry_five)
db.session.add(mood_entry_six)

db.session.commit()
