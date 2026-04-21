from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import json
import os
import random
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'quiz_app_secret_key'  # Change in production

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
QUIZ_FILE = os.path.join(DATA_DIR, 'quizzes.json')
DB_FILE = os.path.join(DATA_DIR, 'scores.db')

def load_quiz_data():
    with open(QUIZ_FILE, 'r') as f:
        return json.load(f)

def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS scores
                 (id INTEGER PRIMARY KEY, date TEXT, score INTEGER, total INTEGER, percentage REAL, categories TEXT, question_counts TEXT, timer_used INTEGER)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/img/<path:filename>')
def serve_img(filename):
    return send_from_directory('img', filename)

@app.route('/')
def home():
    data = load_quiz_data()
    categories = [cat['name'] for cat in data['categories']]
    return render_template('index.html', categories=categories)

@app.route('/start_quiz', methods=['POST'])
def start_quiz():
    data = load_quiz_data()
    selected_questions = []
    categories_selected = []
    question_counts = {}
    
    for cat in data['categories']:
        count_key = f'count_{cat["name"]}'
        count = request.form.get(count_key, '0')
        if count.isdigit() and int(count) > 0:
            num = int(count)
            available = len(cat['questions'])
            num = min(num, available)
            selected = random.sample(cat['questions'], num)
            selected_questions.extend(selected)
            categories_selected.append(cat['name'])
            question_counts[cat['name']] = num
    
    if not selected_questions:
        return redirect(url_for('home'))  # No questions selected
    
    random.shuffle(selected_questions)
    session['questions'] = selected_questions
    session['current'] = 0
    session['answers'] = {}
    session['categories'] = categories_selected
    session['question_counts'] = question_counts
    session['timer'] = request.form.get('timer', '')
    session['start_time'] = datetime.now().isoformat()
    
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
    score = 0
    total = len(questions)
    
    for i, q in enumerate(questions):
        key = f'q{i}'
        user_ans = request.form.getlist(key)  # getlist for multi
        user_ans = [int(x) for x in user_ans]
        answers[i] = user_ans
        correct = q['correct']
        if set(user_ans) == set(correct):
            score += 1
    
    percentage = (score / total) * 100 if total > 0 else 0
    
    # Save to db
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('INSERT INTO scores (date, score, total, percentage, categories, question_counts, timer_used) VALUES (?, ?, ?, ?, ?, ?, ?)',
              (datetime.now().isoformat(), score, total, percentage, json.dumps(session.get('categories', [])), json.dumps(session.get('question_counts', {})), int(session.get('timer', 0) or 0)))
    conn.commit()
    conn.close()
    
    session['score'] = score
    session['total'] = total
    session['percentage'] = percentage
    session['answers'] = answers
    
    return redirect(url_for('results'))

@app.route('/results')
def results():
    score = session.get('score', 0)
    total = session.get('total', 0)
    percentage = session.get('percentage', 0)
    return render_template('results.html', score=score, total=total, percentage=percentage)

if __name__ == '__main__':
    app.run(debug=True)