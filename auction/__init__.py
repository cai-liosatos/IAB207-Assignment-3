#import flask - from the package import class
from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from werkzeug.exceptions import HTTPException

db=SQLAlchemy()

#create a function that creates a web application
# a web server will run this web application
def create_app():

    app=Flask(__name__)  # this is the name of the module/package that is calling this app
    app.debug=True
    app.secret_key='utroutoru'
    #set the app configuration data 
    app.config['SQLALCHEMY_DATABASE_URI']=os.environ['DATABASE_URL']
    #  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    #initialize db with flask app
    db.init_app(app)

    bootstrap = Bootstrap(app)

    #  error handlers
    @app.errorhandler(404)
    def page_not_found(e):
        error_code_404 = "yes"
        return render_template('error.html', error_code_404=error_code_404), 404

    @app.errorhandler(Exception)
    def handle_exception(e):
      if isinstance(e, HTTPException):
         return e
      return render_template("error.html", e=e), 500

    #the folder to store images
    UPLOAD_FOLDER = '/static/image'
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    
    #initialize the login manager
    login_manager = LoginManager()
    
    #set the name of the login function that lets user login
    # in our case it is auth.login (blueprintname.viewfunction name)
    login_manager.login_view='auth.login'
    login_manager.init_app(app)

    # create a user loader function takes userid and returns User
    from .models import User  # importing here to avoid circular references
    @login_manager.user_loader
    def load_user(user_id):
       return User.query.get(int(user_id))

    #importing views module here to avoid circular references
    # a commonly used practice.
    from . import views
    app.register_blueprint(views.bp)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import items
    app.register_blueprint(items.bp)

    from . import watchlist
    app.register_blueprint(watchlist.bp)

    # from . import watchlist
    # app.register_blueprint(watchlist.bp)
   
    return app



