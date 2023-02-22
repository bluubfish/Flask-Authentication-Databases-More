from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME="database.db"

def create_app():
    # initialise flask
    app=Flask(__name__)
    app.config['SECRET_KEY'] = 'secret key'
    # sqlite db is located at db_name
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    # registering these blueprints
    from .views import views
    from .auth import auth
    

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    with app.app_context():
        db.create_all()
    
        login_manager = LoginManager()
    # where should flask redirect us if we're not logged in
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # telling flask how we load a user
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

# check if db exists already
def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all()
        print("Created DB!")


