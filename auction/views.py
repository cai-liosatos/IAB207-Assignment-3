# Importing relevant packages
from flask import Blueprint, render_template, request, session, redirect, url_for
from .models import Item, Watchlist, Bid
from . import db
from sqlalchemy.sql.expression import func
from sqlalchemy import desc

# blueprint
bp = Blueprint('main', __name__)

# Function for index page
@bp.route('/')
def index():
    func.count()
    items = Item.query.all() # grabs all items in db
    # Does a bunch of filtering based on items
    featured_items =  Item.query.order_by(func.random()).limit(4).all()
    CPUCategory = Item.query.order_by(func.random()).filter_by(category='CPU').limit(4)
    GPUCategory = Item.query.order_by(func.random()).filter_by(category='GPU').limit(4)
    MoboCategory = Item.query.order_by(func.random()).filter_by(category='Motherboard').limit(4)
    RAMCategory = Item.query.order_by(func.random()).filter_by(category='RAM').limit(4)
    PSUCategory = Item.query.order_by(func.random()).filter_by(category='Power Supply Unit').limit(4)
    FanCategory = Item.query.order_by(func.random()).filter_by(category='Cooling Fan').limit(4)
    # renders the page with variables
    return render_template('index.html', items=items, featured_items=featured_items, CPUCategory=CPUCategory, GPUCategory=GPUCategory, MoboCategory=MoboCategory, RAMCategory=RAMCategory, PSUCategory=PSUCategory, FanCategory=FanCategory)

# Function that allows the user to search for items by name
@bp.route('/search')
def search():
    # grabs the text inputted, then filters DB based on that
    if request.args['search']:
        ite = "%" + request.args['search'] + "%"
        items = Item.query.filter(Item.name.like(ite)).all()
        return render_template('index.html', search_items=items)
    else:
        return redirect(url_for('main.index'))




