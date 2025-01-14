from . import db
from flask_login import UserMixin 
from datetime import datetime

class User(db.Model, UserMixin): 
	__tablename__= 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(100), index=True, unique=True, nullable=False)
	email = db.Column(db.String(100), index=True, unique=True, nullable=False)
	password_hash = db.Column(db.String(255), nullable=False)
	contact_number = db.Column(db.Integer, nullable=False)
	address = db.Column(db.String(255), nullable=False)
	watchlist = db.relationship('Watchlist', backref='user')
	bid = db.relationship('Bid', backref='user')
	item = db.relationship('Item', backref='user')


class Item(db.Model):
	__tablename__= 'items'
	id = db.Column(db.Integer, primary_key=True)
	userID = db.Column(db.Integer, db.ForeignKey('users.id'))
	name = db.Column(db.String(100), unique=False, nullable=False)
	category = db.Column(db.String(100), index=True, unique=False, nullable=False)
	manufacturer = db.Column(db.String(100), unique=False, nullable=True)
	condition = db.Column(db.String(100), unique=False, nullable=True)
	image = db.Column(db.String(400), nullable=False)
	finishDate = db.Column(db.DateTime, unique=False, nullable=False)
	deliveryTime = db.Column(db.DateTime, unique=False, nullable=False)
	currentPrice = db.Column(db.Integer, unique=False, nullable=False)
	postagePrice = db.Column(db.Integer, unique=False, nullable=False)
	currency = db.Column(db.String(3), unique=False, nullable=False)
	moreInfo = db.Column(db.String(100), unique=False, nullable=True)
	status = db.Column(db.String(100), unique=False, nullable=False)
	watchlist = db.relationship('Watchlist', backref='item')
	bid = db.relationship('Bid', backref='item')

class Bid(db.Model):
	__tablename__= 'bid'
	id = db.Column(db.Integer, primary_key=True)
	userID = db.Column(db.Integer, db.ForeignKey('users.id'))
	itemId = db.Column(db.Integer, db.ForeignKey('items.id'))
	amount = db.Column(db.Integer, unique=False, nullable=False)
	time = db.Column(db.DateTime, default=datetime.now())

class Watchlist(db.Model):
	__tablename__= 'watchlist'
	id = db.Column(db.Integer, primary_key=True)
	userID = db.Column(db.Integer, db.ForeignKey('users.id'))
	itemId = db.Column(db.Integer, db.ForeignKey('items.id'))
	addedDate = db.Column(db.DateTime, default=datetime.now())

