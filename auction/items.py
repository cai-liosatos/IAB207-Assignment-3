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

def check_upload_file(form):
    fp=form.image.data
    filename=fp.filename
    BASE_PATH=os.path.dirname(__file__)

    upload_path=os.path.join(BASE_PATH,'static/image',secure_filename(filename))
    db_upload_path='/static/image/' + secure_filename(filename)
    fp.save(upload_path)
    return db_upload_path

@bp.route('/<id>') 
def show(id):
  item = Item.query.filter_by(id=id).first()
  similar_items = Item.query.filter_by(category=item.category).order_by(func.random()).limit(4)
  if current_user.id == item.userID:
    bidList = Bid.query.filter_by(itemId=item.id).order_by(desc(Bid.amount))
    return render_template('items/show.html', similar_items=similar_items, item=item, bidList=bidList)
  else:
    return render_template('items/show.html', similar_items=similar_items, item=item)

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

@bp.route('/bid/<id>', methods = ['GET', 'POST'])
@login_required
def bid(id):
    statusCheck = Item.query.filter(and_(Item.status == "Open", Item.id == id))
    if statusCheck:
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

@bp.route('/close/<id>', methods=['GET', 'POST'])
def close(id):
    statusCheck3 = Item.query.filter(and_(Item.status == "Open", Item.id == id))
    if statusCheck3:
        updatedStatus = Item.query.filter(id=id).first()
        updatedStatus.status = "Closed"
        db.session.commit()
        flash('This auction is closed', 'success')
        return redirect(url_for('item.show', id=id))
    else:
        flash('Sorry, this auction is already closed', 'warning')
        return redirect(url_for('item.show', id=id))

