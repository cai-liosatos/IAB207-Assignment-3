from . import db
from flask_login import UserMixin 
from datetime import datetime



class User(db.Model, UserMixin):
    __tablename__='users' # good practice to specify table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
	#password is never stored in the DB, an encrypted password is stored
	# the storage should be at least 255 chars long
    password_hash = db.Column(db.String(255), nullable=False)

    # relation to call user.comments and comment.created_by
    comments = db.relationship('Comment', backref='user')
# class User(db.Model, UserMixin): 
# 	__tablename__= 'users'
# 	id = db.Column(db.Integer, primary_key=True)
# 	username = db.Column(db.String(100), index=True, unique=True, nullable=False)
# 	email = db.Column(db.String(100), index=True, unique=True, nullable=False)
# 	password_hash = db.Column(db.String(255), nullable=True)
# 	watchlist = db.relationship('Watchlist', backref='user')
# 	bid = db.relationship('Bid', backref='user')

# 	def __repr__(self):
# 		return "<Name: {}>".format(self.username)


class Item(db.Model):
	__tablename__= 'items'
	id = db.Column(db.Integer, primary_key=True)
	Name = db.Column(db.String(100), unique=False, nullable=False, backref='watchlist')
	category = db.Column(db.String(100), index=True, unique=False, nullable=False)
	manufacturer = db.Column(db.String(100), unique=False, nullable=True)
	condition = db.Column(db.String(100), unique=False, nullable=True)
	image = db.Column(db.String(400), nullable=False)
	finishDate = db.Column(db.DateTime, default=datetime.now(), unique=False, nullable=False)
	deliveryTime = db.Column(db.DateTime, unique=False, nullable=False)
	currentPrice = db.Column(db.Integer, unique=False, nullable=False)
	postagePrice = db.Column(db.Integer, unique=False, nullable=False)
	currency = db.Column(db.String(3), unique=False, nullable=False)
	moreInfo = db.Column(db.String(100), unique=False, nullable=True)
	status = db.Column(db.String(100), unique=False, nullable=False)
	watchlist = db.relationship('Watchlist', backref='item')
	bid = db.relationship('Bid', backref='item')

	def __repr__(self): #string print method
		return "<Name: {}>".format(self.name)



class Bid(db.Model):
	__tablename__= 'bid'
	id = db.Column(db.Integer, primary_key=True)
	userID = db.Column(db.Integer, db.Foreign('users.id'))
	itemId = db.Column(db.Integer, db.Foreign('items.itemId'))
	amount = db.Column(db.Integer, unique=False, nullable=False)
	time = db.Column(db.DateTime, default=datetime.now())

	def __repr__(self):
		return "<Bid: {}>".format(self.amount)

class Watchlist(db.Model):
	__tablename__= 'watchlist'
	id = db.Column(db.Integer, primary_key=True)
	userID = db.Column(db.Integer, db.ForeignKey('users.id'))
	itemName = db.Column(db.String(100), db.ForeignKey('items.itemName'), unique=False)
	addedDate = db.Column(db.DateTime, default=datetime.now())

