import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
import json
from dotenv import load_dotenv

load_dotenv() 

# For Heroku: Use DATABASE_URL if available, otherwise use local settings
DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    # Heroku environment - use their database URL
    # Fix the URL format for SQLAlchemy
    if DATABASE_URL.startswith('postgres://'):
        database_path = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
    elif DATABASE_URL.startswith('sqlite://'):
        database_path = DATABASE_URL
    else:
        database_path = DATABASE_URL
else:
    # Local environment - use SQLite for easier setup
    database_path = "sqlite:///trivia.db"

db = SQLAlchemy()

"""
setup_db(app)
    binds a flask application and a SQLAlchemy service
"""
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

"""
Question

"""
class Question(db.Model):
    __tablename__ = 'questions'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)
    category = Column(String)
    difficulty = Column(Integer)

    def __init__(self, question, answer, category, difficulty):
        self.question = question
        self.answer = answer
        self.category = category
        self.difficulty = difficulty

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category,
            'difficulty': self.difficulty
            }

"""
Category

"""
class Category(db.Model):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    type = Column(String)

    def __init__(self, type):
        self.type = type

    def format(self):
        return {
            'id': self.id,
            'type': self.type
            }