from flask import Flask, flash, render_template, redirect, request, jsonify, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.urls import url_decode
import bcrypt
# from models import TriviaSet, Question

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Ctrl-Alt-Defeat-200'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///multinerd.db'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    from models import User
    return User.get(user_id)

@app.route('/')
def index():
    return "Welcome to the Trivia App"

@app.route('/register', methods=['GET', 'POST'])
def register():
    from models import User

    if request.method == 'POST':
        # Get user registration data from the form
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if a user with the same username or email already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'danger')
        else:
            existing_email = User.query.filter_by(email=email).first()
            if existing_email:
                flash('Email address already registered.', 'danger')
            else:
                # Create a new User instance with the hashed password
                new_user = User(username=username, email=email, password=password)

                try:
                    # Add the new user to the database
                    db.session.add(new_user)
                    db.session.commit()
                    flash('Registration successful. You can now log in.', 'success')
                    return redirect(url_for('login'))
                except Exception as e:
                    db.session.rollback()
                    flash('An error occurred during registration. Please try again.', 'danger')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    from models import User
    if request.method == 'POST':
        # Check the user's credentials (e.g., username and password)
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.check_password(request.form['password']):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    from models import TriviaSet, UserScore
    # Retrieve user's top scores
    top_scores = UserScore.query.filter_by(user_id=current_user.id).order_by(UserScore.score.desc()).limit(10).all()

    # Retrieve most played categories
    category_counts = db.session.query(
        TriviaSet.category,
        func.count(TriviaSet.category).label('count')
    ).filter(TriviaSet.user_id == current_user.id).group_by(TriviaSet.category).order_by(func.count(TriviaSet.category).desc()).limit(5).all()

    most_played_categories = {category: count for category, count in category_counts}

    return render_template('dashboard.html', user=current_user, top_scores=top_scores, most_played_categories=most_played_categories)

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

    
