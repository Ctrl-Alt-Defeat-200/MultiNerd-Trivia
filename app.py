from flask import Flask, flash, render_template, redirect, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import login_required, current_user
import os
# from models import TriviaSet, Question

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Ctrl-Alt-Defeat-200'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///multinerd.db'
db = SQLAlchemy(app)


@app.route('/')
def index():
    return "Welcome to the Trivia App"

# Route to list all Trivia Sets
@app.route('/trivia_sets')
def list_trivia_sets():
    from models import TriviaSet
    trivia_sets = TriviaSet.query.all()
    return render_template('trivia_sets.html', trivia_sets=trivia_sets)

# Route to view a single Trivia Set
@app.route('/trivia_set/<int:set_id>')
def view_trivia_set(set_id):
    from models import TriviaSet
    trivia_set = TriviaSet.query.get_or_404(set_id)
    return render_template('trivia_set.html', trivia_set=trivia_set)

# Route to create a new Trivia Set
@app.route('/create_trivia_set', methods=['GET', 'POST'])
@login_required  # Ensure that only logged-in users can create trivia sets
def create_trivia_set():
    from models import TriviaSet, Question, Option
    if request.method == 'POST':
        # Handle form submission for creating a trivia set
        set_title = request.form['set_title']
        category = request.form['category']
        difficulty = request.form['difficulty']

        # Create a new TriviaSet instance and add it to the database
        new_set = TriviaSet(set_title=set_title, category=category, difficulty=difficulty, user_id=current_user.id)

        try:
            db.session.add(new_set)
            db.session.commit()
            flash('Trivia set created successfully!', 'success')

            # Now, let's add questions and options
            num_questions = int(request.form['num_questions'])

            for i in range(num_questions):
                question_text = request.form[f'question_{i+1}']
                question_type = 'multiple_choice'  # Assuming all questions are multiple-choice

                new_question = Question(question_text=question_text, question_type=question_type, trivia_set=new_set)
                db.session.add(new_question)
                db.session.commit()

                # Add options for each question
                num_options = int(request.form[f'num_options_{i+1}'])

                for j in range(num_options):
                    option_text = request.form[f'option_{i+1}_{j+1}']
                    is_correct = bool(request.form.get(f'is_correct_{i+1}_{j+1}', False))

                    new_option = Option(text=option_text, is_correct=is_correct, question=new_question)
                    db.session.add(new_option)
                    db.session.commit()

            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            flash('An error occurred while creating the trivia set. Please try again.', 'danger')

    return render_template('create_trivia_set.html')

# Route to play a Trivia Set
@app.route('/play_set/<int:set_id>')
def play_trivia_set(set_id):
    from models import TriviaSet
    trivia_set = TriviaSet.query.get_or_404(set_id)
    questions = trivia_set.questions
    return render_template('play_set.html', trivia_set=trivia_set, questions=questions)

if __name__ == '__main__':


    # database_file = 'test.db'  # Replace with your database file name
    # if os.path.exists(database_file):
    #     os.remove(database_file)
    # else:
    #     print(f"The database file '{database_file}' does not exist.")

    with app.app_context():
        db.create_all()
        app.run(debug=True)

    
