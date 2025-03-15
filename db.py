from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    projects = db.relationship('Project', backref='creator_ref', lazy=True)

class Project(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    creator = db.Column(db.Integer, db.ForeignKey('user.ID'), nullable=False)
    createdat = db.Column(db.DateTime, default=datetime.utcnow)
    
class Task(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    details = db.Column(db.Text, nullable=True)
    state = db.Column(db.String(20), default='pending', nullable=False)
    createdat = db.Column(db.DateTime, default=datetime.utcnow)
    changedat = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ProjectUsers(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.ID'), nullable=False)
    projectID = db.Column(db.Integer, db.ForeignKey('project.ID'), nullable=False)
    db.UniqueConstraint(userID, projectID)

class LastOpened(db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.ID'), nullable=False)
    projectID = db.Column(db.Integer, db.ForeignKey('project.ID'), nullable=False)
    opendat = db.Column(db.DateTime, default=datetime.utcnow)

def init_db(app):
    """Initialize the database."""
    db.init_app(app)
    with app.app_context():
        db.create_all()
        print("Database tables created!")
