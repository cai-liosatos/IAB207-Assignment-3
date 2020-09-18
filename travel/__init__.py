#import flask - from the package import class
from flask import Flask 
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

#create a function that creates a web application
# a web server will run this web application
def create_app():
  
    app=Flask(__name__)  # this is the name of the module/package that is calling this app
    app.debug=True
    app.secret_key='utroutoru'
    #set the app configuration data 
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///travel123.sqlite'
    #initialize db with flask app
    db.init_app(app)

    bootstrap = Bootstrap(app)
    
    #the folder to store images
    UPLOAD_FOLDER = '/static/image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


    #importing views module here to avoid circular references
    # a commonly used practice.
    from . import views
    app.register_blueprint(views.mainbp)

    from . import destinations
    app.register_blueprint(destinations.bp)
    
    return app
