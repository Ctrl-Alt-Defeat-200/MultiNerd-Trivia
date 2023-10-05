from app import db
from flask_login import UserMixin
import bcrypt

# Models
class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(length=120), nullable=False)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = self.generate_password_hash(password)

    @staticmethod
    def get(user_id):
        return User.query.get(int(user_id))

    def generate_password_hash(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password)
    
class TriviaSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    set_title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    questions = db.relationship('Question', backref='trivia_set')
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, set_title, category, difficulty):
       self.set_title=set_title
       self.category=category
       self.difficulty=difficulty

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(255), nullable=False)
    question_type = db.Column(db.Enum('multiple_choice', 'open_ended'), nullable=False)
    
    # Define a one-to-many relationship for options if it's a multiple choice question
    options = db.relationship('Option', backref='question', lazy=True, uselist=True)
    trivia_set_id = db.Column(db.Integer, db.ForeignKey('trivia_set.id'), nullable=False)
    def __init__(self, question_text, question_type):
        self.question_text = question_text
        self.question_type = question_type

class Option(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    is_correct = db.Column(db.Boolean, default=False, nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)

    def __init__(self, text, is_correct=False):
        self.text = text
        self.is_correct = is_correct

class UserScore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    trivia_set_id = db.Column(db.Integer, db.ForeignKey('trivia_set.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    def __init__(self, id, trivia_set_id, score):
        self.id=id
        self.trivia_set_id=trivia_set_id
        self.score=score