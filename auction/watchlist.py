from flask import Blueprint, flash, render_template, request, url_for, redirect 
from .models import User, Item, Watchlist, Bid
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

bp = Blueprint('watchlist', __name__)
from flask import session

@bp.route('/add')
def add_to_watchlist():
    watchlist_item = Watchlist()
    db.session.add(watchlist_item)
    db.session.commit()
    return redirect(url_for('main.index'))

@bp.route('/watchlist', methods=['GET', 'POST'])
def watchlist():
    watchlist = Watchlist.query.filter_by(id=id).first()
    db.session.add(item)
    db.session.commit()
    return render_template('watchlist.html', watchlist=watchlist)

@bp.route('/watchlist', methods=['GET', 'POST'])
def watchlist():
    watchlist = Watchlist.query.filter_by(id=id).first()
    return render_template('watchlist.html', watchlist=watchlist)



