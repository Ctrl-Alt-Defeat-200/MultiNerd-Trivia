from flask import Flask, flash, render_template, redirect, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
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
@app.route('/create_set', methods=['GET', 'POST'])
def create_trivia_set():
    from models import TriviaSet
    if request.method == 'POST':
        set_title = request.form.get('set_title')
        category = request.form.get('category')
        difficulty = request.form.get('difficulty')

        new_set = TriviaSet(set_title=set_title, category=category, difficulty=difficulty)
        db.session.add(new_set)
        db.session.commit()

        flash('Trivia Set created successfully', 'success')
        return redirect(url_for('list_trivia_sets'))

    return render_template('create_set.html')

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

    
