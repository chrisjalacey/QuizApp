from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import json
import os
import random
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'quiz_app_secret_key'  # Change in production

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
REGISTRY_FILE = os.path.join(DATA_DIR, 'quizzes_registry.json')
DB_FILE = os.path.join(DATA_DIR, 'scores.db')

def load_quizzes_registry():
    """Load the quizzes registry to get list of available quizzes."""
    with open(REGISTRY_FILE, 'r') as f:
        return json.load(f)

def load_quiz(quiz_id):
    """Load a specific quiz by its ID from the registry and file."""
    registry = load_quizzes_registry()
    quiz_info = None
    for q in registry['quizzes']:
        if q['id'] == quiz_id:
            quiz_info = q
            break
    
    if not quiz_info:
        return None
    
    quiz_file = os.path.join(os.path.dirname(__file__), quiz_info['file'])
    with open(quiz_file, 'r') as f:
        data = json.load(f)
        return {'id': quiz_id, 'name': quiz_info['name'], 'data': data, 'sections': data.get('sections', [])}

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scores
                 (id INTEGER PRIMARY KEY, date TEXT, score INTEGER, total INTEGER, percentage REAL, categories TEXT, question_counts TEXT, timer_used INTEGER)''')
    
    # Migration: Add answers column if it doesn't exist
    c.execute("PRAGMA table_info(scores)")
    columns = {column[1] for column in c.fetchall()}
    if 'answers' not in columns:
        c.execute('ALTER TABLE scores ADD COLUMN answers TEXT')
    
    conn.commit()
    conn.close()

init_db()

@app.route('/img/<path:filename>')
def serve_img(filename):
    return send_from_directory('img', filename)

@app.route('/')
def home():
    registry = load_quizzes_registry()
    quizzes = registry['quizzes']
    
    # Load sections for each quiz
    quizzes_with_sections = []
    for q in quizzes:
        quiz_data = load_quiz(q['id'])
        quizzes_with_sections.append({
            'id': q['id'],
            'name': q['name'],
            'sections': quiz_data.get('sections', [])
        })
    
    return render_template('index.html', quizzes=quizzes_with_sections)

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    quiz_id = request.form.get('quiz_id')
    count = request.form.get('count', '0')
    sections = request.form.getlist('sections')  # Get selected sections
    
    if not quiz_id or not count.isdigit() or int(count) == 0:
        return redirect(url_for('home'))
    
    quiz = load_quiz(quiz_id)
    if not quiz:
        return redirect(url_for('home'))
    
    all_questions = quiz['data'].get('questions', [])
    
    # Filter by sections if any are selected
    if sections:
        questions = [q for q in all_questions if q.get('section') in sections]
    else:
        questions = all_questions
    
    num = min(int(count), len(questions))
    if num == 0:
        # Fall back to all questions if not enough in selected sections
        questions = all_questions
        num = min(int(count), len(questions))
    
    selected_questions = random.sample(questions, num)
    random.shuffle(selected_questions)
    
    session['questions'] = selected_questions
    session['current'] = 0
    session['answers'] = {}
    session['quiz_id'] = quiz_id
    session['quiz_name'] = quiz['name']
    session['timer'] = request.form.get('timer', '')
    session['start_time'] = datetime.now().isoformat()
    session['sections'] = sections  # Store selected sections
    
    return redirect(url_for('quiz'))

@app.route('/quiz')
def quiz():
    questions = session.get('questions', [])
    if not questions:
        return redirect(url_for('home'))
    return render_template('quiz.html', questions=questions, timer=session.get('timer', ''))

@app.route('/submit_quiz', methods=['POST'])
def submit_quiz():
    questions = session.get('questions', [])
    answers = {}
    review_data = []
    score = 0
    total = len(questions)
    
    for i, q in enumerate(questions):
        key = f'q{i}'
        user_ans = request.form.getlist(key)  # getlist for multi
        user_ans = [int(x) for x in user_ans]
        answers[i] = user_ans
        correct = q['correct']
        is_correct = set(user_ans) == set(correct)
        
        if is_correct:
            score += 1
        
        # Build review data for this question
        user_labels = [q['options'][idx] for idx in user_ans]
        correct_labels = [q['options'][idx] for idx in correct]
        
        review_item = {
            'question_index': i,
            'question_text': q['text'],
            'question_type': q['type'],
            'options': q['options'],
            'correct_indices': correct,
            'correct_labels': correct_labels,
            'correct_count': len(correct),
            'user_answers': user_ans,
            'user_labels': user_labels,
            'is_correct': is_correct,
            'image': q.get('image'),
            'explanation': q.get('explanation', '')
        }
        review_data.append(review_item)
    
    percentage = (score / total) * 100 if total > 0 else 0
    
    # Convert answers dict to list format: {0: [1], 1: [0, 2]} -> [[1], [0, 2]]
    answers_list = [answers.get(i, []) for i in range(total)]
    
    # Save to db
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('INSERT INTO scores (date, score, total, percentage, categories, question_counts, timer_used, answers) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
              (datetime.now().isoformat(), score, total, percentage, 
               json.dumps([session.get('quiz_name', 'Unknown')]), 
               json.dumps({'questions': total}), 
               int(session.get('timer', 0) or 0),
               json.dumps(answers_list)))
    conn.commit()
    conn.close()
    
    session['score'] = score
    session['total'] = total
    session['percentage'] = percentage
    session['answers'] = answers
    session['review_data'] = review_data
    session['quiz_name'] = session.get('quiz_name', 'Unknown')
    
    return redirect(url_for('results'))

@app.route('/results')
def results():
    score = session.get('score', 0)
    total = session.get('total', 0)
    percentage = session.get('percentage', 0)
    review_data = session.get('review_data', [])
    quiz_name = session.get('quiz_name', 'Unknown')
    return render_template('results.html', score=score, total=total, percentage=percentage, review_data=review_data, quiz_name=quiz_name)

@app.route('/history')
def history():
    """Display last 10 quiz attempts."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT id, date, categories, score, total, percentage FROM scores ORDER BY date DESC LIMIT 10')
    rows = c.fetchall()
    conn.close()
    
    attempts = []
    for row in rows:
        attempt_id, date, categories_json, score, total, percentage = row
        categories = json.loads(categories_json)
        quiz_name = categories[0] if categories else 'Unknown'
        attempts.append({
            'id': attempt_id,
            'date': date,
            'quiz_name': quiz_name,
            'score': score,
            'total': total,
            'percentage': percentage
        })
    
    return render_template('history.html', attempts=attempts)

@app.route('/history/<int:attempt_id>')
def history_detail(attempt_id):
    """Display detailed review of a specific quiz attempt."""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT date, categories, score, total, percentage, answers FROM scores WHERE id = ?', (attempt_id,))
    row = c.fetchone()
    conn.close()
    
    if not row:
        return redirect(url_for('history'))
    
    date, categories_json, score, total, percentage, answers_json = row
    categories = json.loads(categories_json)
    quiz_name = categories[0] if categories else 'Unknown'
    answers_list = json.loads(answers_json) if answers_json else []
    
    # Reconstruct review data from answers
    # Need to load the quiz file to get questions with explanations
    review_data = []
    
    # Try to find the quiz by name from registry
    registry = load_quizzes_registry()
    quiz_id = None
    for q in registry['quizzes']:
        if q['name'] == quiz_name:
            quiz_id = q['id']
            break
    
    if quiz_id:
        quiz = load_quiz(quiz_id)
        if quiz and 'questions' in quiz['data']:
            questions = quiz['data']['questions']
            # Map stored answers to questions
            for i, user_ans in enumerate(answers_list):
                if i < len(questions):
                    q = questions[i]
                    correct = q.get('correct', [])
                    is_correct = set(user_ans) == set(correct)
                    user_labels = [q['options'][idx] for idx in user_ans] if user_ans else []
                    correct_labels = [q['options'][idx] for idx in correct]
                    
                    review_item = {
                        'question_index': i,
                        'question_text': q.get('text', ''),
                        'question_type': q.get('type', 'single'),
                        'options': q.get('options', []),
                        'correct_indices': correct,
                        'correct_labels': correct_labels,
                        'correct_count': len(correct),
                        'user_answers': user_ans,
                        'user_labels': user_labels,
                        'is_correct': is_correct,
                        'image': q.get('image'),
                        'explanation': q.get('explanation', '')
                    }
                    review_data.append(review_item)
    
    return render_template('history_detail.html', 
                         attempt_id=attempt_id,
                         date=date,
                         quiz_name=quiz_name,
                         score=score,
                         total=total,
                         percentage=percentage,
                         review_data=review_data)

if __name__ == '__main__':
    app.run(debug=True)