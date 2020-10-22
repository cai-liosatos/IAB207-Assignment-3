from flask import Blueprint, render_template, request, session, redirect, url_for
from .models import Item, Watchlist
from . import db
from sqlalchemy.sql.expression import func

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    items = Item.query.all()
    featured_items =  Item.query.order_by(func.random()).limit(4).all()
    CPUCategory = Item.query.order_by(func.random()).filter_by(category='CPU').limit(4)
    GPUCategory = Item.query.order_by(func.random()).filter_by(category='GPU').limit(4)
    MoboCategory = Item.query.order_by(func.random()).filter_by(category='Motherboard').limit(4)
    RAMCategory = Item.query.order_by(func.random()).filter_by(category='RAM').limit(4)
    PSUCategory = Item.query.order_by(func.random()).filter_by(category='Power Supply Unit').limit(4)
    FanCategory = Item.query.order_by(func.random()).filter_by(category='Cooling Fan').limit(4)
    return render_template('index.html', items=items, featured_items=featured_items, CPUCategory=CPUCategory, GPUCategory=GPUCategory, MoboCategory=MoboCategory, RAMCategory=RAMCategory, PSUCategory=PSUCategory, FanCategory=FanCategory)

@bp.route('/search')
def search():
    if request.args['search']:
        ite = "%" + request.args['search'] + "%"
        items = Item.query.filter(Item.name.like(ite)).all()
        return render_template('index.html', items=items)
    else:
        return redirect(url_for('main.index'))

@bp.route('/add')
def add_to_watchlist():
    watchlist_item = Watchlist()
    db.session.add(watchlist_item)
    db.session.commit()
    return redirect(url_for('main.index'))
    
