from app import db  # Import your Flask app's db instance
from models import TriviaSet, Question  # Import the models

def test_create_trivia_set():
    trivia_set = TriviaSet(set_title="Set 1", category="General", difficulty="Easy")
    db.session.add(trivia_set)
    db.session.commit()
    assert trivia_set.id is not None

def test_create_question():
    trivia_set = TriviaSet(set_title="Set 2", category="Science", difficulty="Medium")
    question = Question(
        content="What is the capital of France?",
        option1="Madrid",
        option2="Berlin",
        option3="Rome",
        option4="Paris",
        correct_option=4,
        trivia_set=trivia_set
    )
    db.session.add(trivia_set)
    db.session.add(question)
    db.session.commit()
    assert question.id is not None

def test_query_trivia_set():
    trivia_set = TriviaSet.query.filter_by(set_title="Set 1").first()
    assert trivia_set is not None
    assert trivia_set.category == "General"
    assert trivia_set.difficulty == "Easy"

def test_query_question():
    question = Question.query.filter_by(content="What is the capital of France?").first()
    assert question is not None
    assert question.correct_option == 4
    assert question.trivia_set.set_title == "Set 2"



# import pytest
# from app import db  # Import your Flask application's db instance
# from models import TriviaSet  # Import the TriviaSet model

# @pytest.fixture
# def sample_trivia_set():
#     """Create a sample TriviaSet object for testing."""
#     return TriviaSet(title="Sample Trivia Set", category="Movies", difficulty="Easy")

# def test_create_trivia_set(sample_trivia_set):
#     """Test creating a TriviaSet object."""
#     assert sample_trivia_set.id is None
#     assert sample_trivia_set.title == "Sample Trivia Set"
#     assert sample_trivia_set.category == "Movies"
#     assert sample_trivia_set.difficulty == "Easy"

# def test_save_trivia_set(sample_trivia_set):
#     """Test saving a TriviaSet object to the database."""
#     db.session.add(sample_trivia_set)
#     db.session.commit()

#     assert sample_trivia_set.id is not None

# def test_query_trivia_set_by_title(sample_trivia_set):
#     """Test querying a TriviaSet object by title."""
#     db.session.add(sample_trivia_set)
#     db.session.commit()

#     queried_trivia_set = TriviaSet.query.filter_by(title="Sample Trivia Set").first()
#     assert queried_trivia_set is not None
#     assert queried_trivia_set.title == "Sample Trivia Set"

# def test_update_trivia_set_category(sample_trivia_set):
#     """Test updating the category of a TriviaSet object."""
#     db.session.add(sample_trivia_set)
#     db.session.commit()

#     sample_trivia_set.category = "Updated category"
#     db.session.commit()

#     updated_trivia_set = TriviaSet.query.filter_by(title="Sample Trivia Set").first()
#     assert updated_trivia_set.category == "Updated category"

# def test_delete_trivia_set(sample_trivia_set):
#     """Test deleting a TriviaSet object."""
#     db.session.add(sample_trivia_set)
#     db.session.commit()

#     TriviaSet.query.filter_by(title="Sample Trivia Set").delete()
#     db.session.commit()

#     deleted_trivia_set = TriviaSet.query.filter_by(title="Sample Trivia Set").first()
#     assert deleted_trivia_set is None
