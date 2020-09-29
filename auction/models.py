from . import db
from flask_login import UserMixin 
from datetime import datetime

class User(db.Model, UserMixin): 
	__tablename__='users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(100), index=True, unique=True, nullable=False)
	email = db.Column(db.String(100), index=True, unique=True, nullable=False)
	password_hash = db.Column(db.String(255), nullable=False)

class Item(db.Model):
	__tablename__='items'
	id = db.Column(db.Integer, primary_key=True)
	itemName = db.Column(db.String(100), index=True, unique=False, nullable=False, backref='watchlist')
	category = db.Column(db.String(100), index=True, unique=False, nullable=False)
	manufacturer = db.Column(db.String(100), index=True, unique=False, nullable=True)
	condition = db.Column(db.String(100), index=True, unique=False, nullable=True)
	image = db.Column(db.String(400))
	finishDate = db.Column(db.Date(), index=True, unique=False, nullable=False)
	deliveryTime = db.Column(db.Integer, index=True, unique=False, nullable=False)
	currentPrice = db.Column(db.Integer, index=True, unique=False, nullable=False)
	postagePrice = db.Column(db.Integer, index=True, unique=False, nullable=False)
	currency = db.Column(db.String(3), index=True, unique=False, nullable=False)
	moreInfo = db.Column(db.String(100), index=True, unique=False, nullable=True)
	status = db.Column(db.String(100), index=True, unique=False, nullable=False)

class Watchlist(db.Model):
	__tablename__='watchlist'
	id = db.Column(db.Integer)
	userID = db.Column(db.Integer, db.ForeignKey('users.id'))
	itemName = db.Column(db.String(100), db.ForeignKey('items.itemName'), index=True, unique=False)
	addedDate = db.Column(db.Date(), index=True, unique=False)