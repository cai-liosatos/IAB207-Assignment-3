#this will have the code for directing between the items listed/created (*cough cough* the destinations.py file in the tute *cough cough*)
from flask import Blueprint, flash, render_template, request, url_for, redirect 
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

#create a blueprint
# bp = Blueprint('item', __name__, url_prefix='/items')