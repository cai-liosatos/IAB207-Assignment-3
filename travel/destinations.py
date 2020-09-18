from flask import ( 
    Blueprint, flash, render_template, request, url_for, redirect
) 
from .models import Destination,Comment,User
from .forms import CommentForm, DestinationForm
from . import db
import os
from werkzeug.utils import secure_filename

#create a blueprint
bp = Blueprint('destination', __name__, url_prefix='/destinations')

 # a new function
def check_upload_file(form):
    fp=form.image.data
    filename=fp.filename
    BASE_PATH=os.path.dirname(__file__)

    upload_path=os.path.join(BASE_PATH,'static/image',secure_filename(filename))
    db_upload_path='/static/image/' + secure_filename(filename)
    fp.save(upload_path)
    return db_upload_path


#create a page that will show the details fo the destination
@bp.route('/<id>') 
def show(id): 
  destination = Destination.query.filter_by(id=id).first()  
  cform = CommentForm()
  return render_template('destinations/show.html', destination=destination, form=cform)


@bp.route('/create', methods = ['GET', 'POST'])
def create():
  print('Method type: ', request.method)
  form = DestinationForm()
  if(form.validate_on_submit()):
    db_file_path=check_upload_file(form)
    destination=Destination(name=form.name.data,description=form.description.data, 
    image=db_file_path,currency=form.currency.data)
    
    db.session.add(destination)
    db.session.commit()
    return redirect(url_for('destination.create'))
  return render_template('destinations/create.html', form=form)




@bp.route('/<destination>/comment', methods = ['GET', 'POST'])  
def comment(destination):  
    form = CommentForm()  
    #get the destination object associated to the page and the comment
    destination_obj = Destination.query.filter_by(id=destination).first()  
    if form.validate_on_submit():  
      #read the comment from the form
      comment = Comment(text=form.text.data,  
                        destination=destination_obj) 
      #here the back-referencing works - comment.destination is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit() 

      #flashing a message which needs to be handled by the html
      #flash('Your comment has been added', 'success')  
      print('Your comment has been added', 'success') 
    # using redirect sends a GET request to destination.show
    return redirect(url_for('destination.show', id=destination))