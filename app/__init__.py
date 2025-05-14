from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # Load all config values (SECRET_KEY, DATABASE_URI, etc.) from config.py
    app.config.from_object('config.Config')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Set the login view for Flask-Login
    login_manager.login_view = 'auth.login'

    # User loader function for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))

    # Create tables if not exist
    with app.app_context():
        from app import models
        db.create_all()

    # Import and register blueprints
    from app.routes.auth import auth_bp
    from app.routes.home import home_bp
    from app.routes.progress import progress_bp
    from app.routes.leaderboard import leaderboard_bp
    # from app.routes.past_tasks import past_tasks_bp
    # from app.routes.chats import chat_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(home_bp)
    app.register_blueprint(progress_bp)
    app.register_blueprint(leaderboard_bp)
    # app.register_blueprint(past_tasks_bp)
    # app.register_blueprint(chat_bp)

    from flask import send_from_directory

    @app.route('/sitemap.xml')
    def sitemap():
        return send_from_directory(app.static_folder, 'sitemap.xml')

    @app.route('/robots.txt')
    def robots():
        return send_from_directory(app.static_folder, 'robots.txt') 
    
    return app