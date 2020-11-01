#this will have the code for directing between the items listed/created (*cough cough* the destinations.py file in the tute *cough cough*)
from flask import Blueprint, flash, render_template, request, url_for, redirect 
from .models import Item, Watchlist, User, Bid
from . import db
from .forms import ItemForm
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from sqlalchemy.sql.expression import func
from sqlalchemy import and_
from sqlalchemy import desc

#create a blueprint
bp = Blueprint('item', __name__, url_prefix='/items')

# function to upload an image
def check_upload_file(form):
    fp=form.image.data
    filename=fp.filename
    BASE_PATH=os.path.dirname(__file__)

    upload_path=os.path.join(BASE_PATH,'static/image',secure_filename(filename))
    db_upload_path='/static/image/' + secure_filename(filename)
    fp.save(upload_path)
    return db_upload_path

# function to show the item (grabs a bunch of variable, passed through for dynamic information)
@bp.route('/<id>') 
def show(id):
    item = Item.query.filter_by(id=id).first()
    similar_items = Item.query.filter_by(category=item.category).order_by(func.random()).limit(4)
    if current_user.is_authenticated:
        if current_user.id == item.userID:
            bidList1 = Bid.query.filter_by(itemId=item.id).order_by(desc(Bid.amount))
            user_details = User.query.filter(and_(User.id == Bid.userID, Bid.itemId == item.id))
            bidList2 = zip(bidList1, user_details)
            return render_template('items/show.html', similar_items=similar_items, item=item, bidList=bidList2)
    else:
        return render_template('items/show.html', similar_items=similar_items, item=item)

# function to create an item, pulled info from form and adds a new row to the Items table
@bp.route('/create', methods = ['GET', 'POST'])
@login_required #decorator between route and view function
def create():
    form = ItemForm()
    if(form.validate_on_submit()==True):
        # print('good job', 'success')
        db_file_path=check_upload_file(form)
        item=Item(name=form.name.data, category=form.category.data, manufacturer=form.manufacturer.data, condition=form.condition.data, image=db_file_path, 
        finishDate=form.finishdate.data, deliveryTime=form.postagedate.data, currentPrice=form.startingprice.data, postagePrice=form.postageprice.data, 
        currency=form.currency.data, moreInfo=form.description.data, status="open")
        db.session.add(item)
        db.session.commit()
        return redirect(url_for('item.show', id=item.id))
    return render_template('items/create.html', form=form)

# function to allow a user to bid on an item (could be a bit less complicated, but it works perfectly)
@bp.route('/bid/<id>', methods = ['GET', 'POST'])
@login_required
def bid(id):
    item = Item.query.filter_by(id=id).first()
    # user it only allowed to bid on an "open" auction
    if item.status == "open":
        price = request.form.get("price")
        i1 = Item.query.filter(and_(Item.currentPrice > price, Item.id == id)).first()
        if i1:
            flash('Invalid amount', 'warning')
            return redirect(url_for('item.show', id=id))
        else:
            updatedPrice = Item.query.filter_by(id=id).first()
            updatedPrice.currentPrice = price
            db.session.commit()
            
            bid=Bid(userID=current_user.id, itemId=id, amount=price)
            db.session.add(bid)
            db.session.commit()
            flash('Bid successful', 'success')
            return redirect(url_for('item.show', id=id))
    else:
        flash('Sorry, this item has closed for bidding.', 'warning')
        return redirect(url_for('main.index'))

# function to "close" an auction
@bp.route('/close/<id>', methods=['GET', 'POST'])
@login_required
def close(id):
    item = Item.query.filter_by(id=id).first()
    if item.status == "open":
        updatedStatus = Item.query.filter_by(id=id).first()
        updatedStatus.status = "Closed"
        db.session.commit()
        flash('This auction is closed', 'success')
        return redirect(url_for('item.show', id=id))
    else:
        flash('Sorry, this auction is already closed', 'warning')
        return redirect(url_for('main.index'))

