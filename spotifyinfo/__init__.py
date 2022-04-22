from flask import Flask
from flask_session import Session

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

from spotifyinfo.searchify.views import searchify
from spotifyinfo.auth.views import auth
from spotifyinfo.errors.views import errors

app.register_blueprint(searchify)
app.register_blueprint(auth)
app.register_blueprint(errors)