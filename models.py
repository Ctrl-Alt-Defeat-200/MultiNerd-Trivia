from app import db

# Models

class TriviaSet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    set_title = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    difficulty = db.Column(db.String(50), nullable=False)
    questions = db.relationship('Question', backref='trivia_set')
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


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

# class UserScore(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     trivia_set_id = db.Column(db.Integer, db.ForeignKey('trivia_set.id'), nullable=False)
#     score = db.Column(db.Integer, nullable=False)

