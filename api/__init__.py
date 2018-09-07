from flask import Flask
from flask_cors import CORS
from instance.config import app_config


app = Flask(__name__, instance_relative_config=True)
CORS(app)
app.config.from_object(app_config["development"])

from api.auth import views
from api.questions import views
from api.answers import views