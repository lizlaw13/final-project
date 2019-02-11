# from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash,
                   session, url_for)
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.secret_key = "ZILWAL"

# app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    """Homepage"""

    return render_template("index.html")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    # make sure templates, etc. are not cached in debug mode
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')