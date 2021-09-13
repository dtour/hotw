from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from tempfile import mkdtemp

# Configure application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'cf43cc3cd14c6194695d8bbc492db6c5'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hotw.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

from application import routes