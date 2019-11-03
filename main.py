# main.py

from . import db
from .models import User
from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from flask_cors import CORS

# blueprint object
main = Blueprint('main', __name__)

CORS(main) # enable CORS on the main blue print

""" DEFAULT ROUTES BLOCK """

@main.route('/')
def index():
    return render_template('index.html')
