from flask import Blueprint, render_template, request, session, redirect, url_for
from .models import Item, Watchlist
from . import db

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    items = Item.query.all()
    return render_template('index.html', items=items)

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
    
