from flask import Flask
from .db import migrate

app = Flask(__name__, template_folder='templates')
API_URL = 'http://localhost:8000'

from . import utils, routers