from flask import Blueprint, flash, render_template, request, url_for, redirect 
from .models import User, Item, Watchlist
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from sqlalchemy import and_

bp = Blueprint('watchlist', __name__)
from flask import session

@bp.route('/watchlist')
@login_required
def show():
    watchlist_items = Watchlist.query.filter_by(user_id=current_user.id)
    item_details = Item.query.filter(and_(Item.id == Watchlist.itemId, Watchlist.userID == current_user.id))
    item_info = zip(watchlist_items, item_details)
    return render_template('watchlist.html', item_info=item_info)

@bp.route('/add/<id>', methods = ['GET', 'POST'])
@login_required
def add(id):
    item = Item.query.filter_by(id=id).first()  
    w1 = Watchlist.query.filter(and_(Watchlist.userID == current_user.id, Watchlist.itemId == id)).first()
    if w1:
        flash('Item is already in your watchlist', 'warning')
        return redirect(url_for('main.index'))  
    watchlist = Watchlist(itemId=id, userID=current_user.id)
    db.session.add(watchlist)
    db.session.commit()
    flash('Item has been added to your watchlist!', 'warning')
    return redirect(url_for('main.index'))

@bp.route('/remove/<id>', methods=['GET', 'POST'])
@login_required
def remove(id):
  item = Watchlist.query.filter(and_(Watchlist.userID == current_user.id, Watchlist.itemId == id)).first()
  db.session.delete(item)
  db.session.commit()
  return redirect(url_for('watchlist.show'))