import pytest
from model import Question

def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_add_choice_with_invalid_text():
    question = Question(title='q1')
    with pytest.raises(Exception, match='Text cannot be empty'):
        question.add_choice('')
    with pytest.raises(Exception, match='Text cannot be longer than 100 characters'):
        question.add_choice('a' * 101)

def test_create_question_with_invalid_points():
    with pytest.raises(Exception, match='Points must be between 1 and 100'):
        Question(title='q1', points=0)
    with pytest.raises(Exception, match='Points must be between 1 and 100'):
        Question(title='q1', points=101)

def test_add_multiple_choices_generates_sequential_ids():
    question = Question(title='q1')
    choice1 = question.add_choice('Opção A')
    choice2 = question.add_choice('Opção B')
    assert choice1.id == 1
    assert choice2.id == 2
    assert len(question.choices) == 2

def test_remove_choice_by_id_success():
    question = Question(title='q1')
    question.add_choice('Opção A')
    choice2 = question.add_choice('Opção B')
    
    question.remove_choice_by_id(choice2.id)
    
    assert len(question.choices) == 1
    assert question.choices[0].text == 'Opção A'

def test_remove_choice_by_invalid_id():
    question = Question(title='q1')
    question.add_choice('Opção A')
    
    with pytest.raises(Exception, match='Invalid choice id 999'):
        question.remove_choice_by_id(999)

def test_remove_all_choices():
    question = Question(title='q1')
    question.add_choice('Opção A')
    question.add_choice('Opção B')
    
    question.remove_all_choices()
    
    assert len(question.choices) == 0

def test_set_correct_choices_success():
    question = Question(title='q1')
    choice1 = question.add_choice('Opção A')
    choice2 = question.add_choice('Opção B')
    
    question.set_correct_choices([choice2.id])
    
    assert not choice1.is_correct
    assert choice2.is_correct

def test_set_correct_choices_invalid_id():
    question = Question(title='q1')
    question.add_choice('Opção A')
    
    with pytest.raises(Exception, match='Invalid choice id 999'):
        question.set_correct_choices([999])

def test_correct_selected_choices_success():
    question = Question(title='q1', max_selections=2)
    choice1 = question.add_choice('Opção A', is_correct=True)
    choice2 = question.add_choice('Opção B', is_correct=False)
    choice3 = question.add_choice('Opção C', is_correct=True)
    
    correct_selections = question.correct_selected_choices([choice1.id, choice2.id])
    
    assert len(correct_selections) == 1
    assert choice1.id in correct_selections
    assert choice2.id not in correct_selections

def test_correct_selected_choices_exceeds_max_selections():
    question = Question(title='q1', max_selections=1)
    choice1 = question.add_choice('Opção A')
    choice2 = question.add_choice('Opção B')
    
    with pytest.raises(Exception, match='Cannot select more than 1 choices'):
        question.correct_selected_choices([choice1.id, choice2.id])