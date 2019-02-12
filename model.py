"""Models and database functions for final project."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Model definitions 

class User(db.Model):
    """"User of website"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, 
        autoincrement=True, 
        primary_key=True)
    first_name = db.Column(db.String(200), 
        nullable=True)
    last_name = db.Column(db.String(200), 
        nullable=True)
    email = db.Column(db.String(200))
    password = db.Column(db.String(20))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"<User user_id={self.user_id} email={self.email}>"

class Mood(db.Model):
    """"Moods users can select from"""

    __tablename__ = "moods"

    mood_id = db.Column(db.Integer, 
        autoincrement=True, 
        primary_key=True)
    mood = db.Column(db.String(15))

    def __repr__(self):
        """Provide helpful representation when printed."""
       
        return f"<Mood mood_id={self.mood_id} mood={self.mood}>"

class Activity_Category(db.Model):
    """"Activties users can select from"""

    __tablename__ = "activities"

    activity_category_id = db.Column(db.Integer, 
        autoincrement=True, 
        primary_key=True)
    category = db.Column(db.String(15))

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<Activity Category activity_category_id={self.activity_category_id}
            category={self.category}"""

class Activity_Category_Description(db.Model):
    """"Optional activity description users can input"""

    __tablename__ = "descriptions"

    description_id = db.Column(db.Integer, 
        autoincrement=True, 
        primary_key=True)
    user_id = db.Column(db.Integer, 
        db.ForeignKey("users.user_id"))
    activity_category_id = db.Column(db.Integer, 
        db.ForeignKey("activities.activity_category_id"))
    description = db.Column(db.Text, 
        nullable=True)

    users = db.relationship('User', backref = "descriptions")
    categories = db.relationship('Activity_Category', backref = "descriptions")


    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<Activity Category Description description_id={self.description_id}
            user_id= {self.user_id}ctivity_category_id={self.activity_category_id}>"""


class User_Mood(db.Model):
    """Relationship table between user and their selected moods"""

    __tablename__ = "user_moods"

    user_mood_id = db.Column(db.Integer, 
        autoincrement=True, 
        primary_key=True)
    user_id = db.Column(db.Integer, 
        db.ForeignKey("users.user_id"))
    mood_id = db.Column(db.Integer, 
        db.ForeignKey("moods.mood_id"))

    users = db.relationship('User', backref = "user_moods")
    moods = db.relationship('Mood', backref = "user_moods")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<User Mood user_mood_id={self.user_mood_id}
            user_id={self.user_id} mood_id={self.mood_id}>"""


class User_Activity(db.Model):
    """Relationship table between user and their selected activities and optional 
    descriptions"""

    __tablename__ = "user_activities"

    user_activity_id = db.Column(db.Integer,  
        autoincrement=True, 
        primary_key=True)
    user_id = db.Column(db.Integer, 
        db.ForeignKey("users.user_id"))
    activity_category_id = db.Column(db.Integer, 
        db.ForeignKey("activities.activity_category_id"))

    users = db.relationship('User', backref ="user_activities")
    categories = db.relationship('Activity_Category', backref = "user_activities")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<User Activity user_activity_id={self.user_activity_id}
            user_id={self.user_id} activity_category_id={self.activity_category_i}>"""

class Mood_Enhancer(db.Model):
    """Optional inputed description from user to enhance mood"""

    __tablename__ = "mood_enhancers"

    mood_enhancer_id = db.Column(db.Integer, 
        autoincrement=True, 
        primary_key=True)
    user_id = db.Column(db.Integer, 
        db.ForeignKey("users.user_id"))
    mood_enhancer = db.Column(db.Text, 
        nullable=True)

    users = db.relationship('User', backref = "mood_enhancers")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<Mood Enhancer mood_enhancer_id={self.mood_enhancer_id}
            user_id={self.user_id}>"""

class User_Brain_Dump(db.Model):
    """Optional inputed description from user as a diary entry """

    __tablename__ = "user_brain_dumps"

    user_brain_dump_id = db.Column(db.Integer, 
        autoincrement=True, 
        primary_key=True)
    user_id = db.Column(db.Integer, 
        db.ForeignKey("users.user_id"))
    brain_dump_entry = db.Column(db.Text, 
        nullable=True)

    users = db.relationship('User', backref = "user_brain_dumps")

    def __repr__(self):
        """Provide helpful representation when printed."""

        return f"""<User Brain Dump user_brain_dump_id={self.user_brain_dump_id}
            user_id={self.user_id}>"""

################################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///tracker'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

    # Used to recreate my database if I need to drop
    # db.create_all()



if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print("Connected to DB.")