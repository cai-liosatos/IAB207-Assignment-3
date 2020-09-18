from flask import Blueprint, render_template, request, session



#Use of blue print to group routes, 
# name - first argument is the blue print name 
# import name - second argument - helps identify the root url for it 
mainbp = Blueprint('main', __name__)
from flask import session
@mainbp.route('/')
def index():
    return render_template('index.html')