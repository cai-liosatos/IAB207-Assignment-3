#this will have the code for directing between the items listed/created (*cough cough* the destinations.py file in the tute *cough cough*)
from flask import Blueprint, flash, render_template, request, url_for, redirect 
from .models import Item, Watchlist, User, Bid
from . import db
from .forms import ItemForm
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

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
  similar_items =  Item.query.filter_by(category=item.category).order_by(func.random()).limit(4)
  return render_template('items/show.html', item=item)


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
        return redirect(url_for('item.create'))
    return render_template('items/create.html', form=form)
    
    


# @bp.route('/create', methods = ['GET', 'POST'])
# @login_required #decorator between route and view function
# def create():
#   print('Method type: ', request.method)
#   form = DestinationForm()
#   if(form.validate_on_submit()):
#     db_file_path=check_upload_file(form)
#     #variables in the "form"
#     item=Item(name=form.name.data,description=form.description.data, 
#     image=db_file_path,currency=form.currency.data)
    
#     db.session.add(item)
#     db.session.commit()
#     return redirect('index.html')
#     # return redirect(url_for('item.show', id=item.id))
#   return render_template('items/create.html', form=form)