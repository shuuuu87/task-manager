import os

basedir = os.path.abspath(os.path.dirname(__file__))  # ✅ correct

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    
    # On Render, use DATABASE_URL from environment
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'task_manager.db')

    SQLALCHEMY_TRACK_MODIFICATIONS = False