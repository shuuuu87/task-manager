from datetime import datetime
from . import db, login_manager
from flask_login import UserMixin

# Load user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    score = db.Column(db.Integer, default=0)
    tasks = db.relationship('Task', backref='owner', lazy=True)
    messages = db.relationship('ChatMessage', backref='author', lazy=True)

    def __repr__(self):
        return f'<User {self.username}>'

# Task model
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    is_completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    time_taken = db.Column(db.Integer)
    completed_at = db.Column(db.DateTime)
    date_created = db.Column(db.Date, default=lambda: datetime.utcnow().date(), nullable=False)
    work_time = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f'<Task {self.title}>'

# Chat message model
class ChatMessage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<ChatMessage {self.message[:20]}...>'
