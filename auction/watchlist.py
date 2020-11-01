from flask import Blueprint, flash, render_template, request, url_for, redirect 
from .models import User, Item, Watchlist
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from sqlalchemy import and_

bp = Blueprint('watchlist', __name__)
from flask import session

# function to view your watchlist, containing user-specific items
@bp.route('/watchlist')
@login_required
def show():
    watchlist_items = Watchlist.query.filter_by(userID=current_user.id)
    item_details = Item.query.filter(and_(Item.id == Watchlist.itemId, Watchlist.userID == current_user.id))
    item_info = zip(watchlist_items, item_details)
    return render_template('watchlist.html', item_info=item_info)

# function to add an item to your watchlist
@bp.route('/add/<id>', methods = ['GET', 'POST'])
@login_required
def add(id):
    item = Item.query.filter_by(id=id).first()
    # not allowed to add an item if the auction it "closed"
    if item.status == "open":
        item = Item.query.filter_by(id=id).first()
        w1 = Watchlist.query.filter(and_(Watchlist.userID == current_user.id, Watchlist.itemId == id)).first()
        if w1:
            flash('Item is already in your watchlist', 'warning')
            return redirect(url_for('main.index'))  
        watchlist = Watchlist(itemId=id, userID=current_user.id)
        db.session.add(watchlist)
        db.session.commit()
        flash('Item has been added to your watchlist!', 'success')
        return redirect(url_for('main.index'))
    else:
        flash('Sorry, this item has closed for bidding.', 'warning')
        return redirect(url_for('main.index'))

# function to remove an item from your watchlist
@bp.route('/remove/<id>', methods=['GET', 'POST'])
@login_required
def remove(id):
  item = Watchlist.query.filter(and_(Watchlist.userID == current_user.id, Watchlist.itemId == id)).first()
  db.session.delete(item)
  db.session.commit()
  flash('Item has been removed from your watchlist', 'danger')
  return redirect(url_for('watchlist.show'))