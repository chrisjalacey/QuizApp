# Development Guide

## Quick Start

```bash
# 1. Navigate to project
cd c:\Users\601234026\OneDrive - BT Plc\Documents\Git\QuizApp

# 2. Activate venv (if not already active)
.venv\Scripts\Activate.ps1

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run app
python app.py

# 5. Open browser
# http://localhost:5000
```

## Project Organization

### File Purposes

**Application:**
- **app.py** - All Flask routes, session logic, database operations, and initialization

**Quiz Data:**
- **data/quizzes_registry.json** - Central index of all available quizzes (id, name, file path)
- **data/{quiz_id}.json** - Individual quiz files (e.g., math.json, science.json, gce.json)
- **data/scores.db** - SQLite database auto-created on first run; stores quiz scores and individual answers

**Templates:**
- **templates/index.html** - Home page with quiz selection dropdown
- **templates/quiz.html** - Quiz page with dynamic question rendering, multi-choice hints, timer
- **templates/results.html** - Results page with score summary and accordion-style question review
- **templates/history.html** - History page showing last 10 quiz attempts
- **templates/history_detail.html** - Detailed view of a historical quiz attempt

**Assets:**
- **static/** - (Empty) Reserved for CSS/JavaScript assets
- **img/** - Question images referenced in quiz JSON files

**Configuration & Documentation:**
- **requirements.txt** - Python dependencies (Flask only)
- **Dockerfile** - Container configuration for Docker deployment
- **.gitignore** - Version control exclusions
- **README.md** - User-facing project overview
- **ARCHITECTURE.md** - System design and components
- **IMPLEMENTATION.md** - Implementation details and logic
- **JSON_SCHEMA.md** - Quiz data format and registry structure
- **DEPLOYMENT.md** - Setup and deployment instructions
- **API_ROUTES.md** - Route documentation with examples
- **DEVELOPMENT.md** - This file

## Common Development Tasks

### Add a New Quiz Topic

1. **Create Quiz File**: Create `data/{quiz_id}.json`:
   ```json
   {
     "questions": [
       {
         "text": "Question 1?",
         "options": ["A", "B", "C"],
         "correct": [0],
         "type": "single",
         "image": null
       }
     ]
   }
   ```

2. **Register Quiz**: Edit `data/quizzes_registry.json` and add:
   ```json
   {
     "id": "{quiz_id}",
     "name": "Display Name",
     "file": "data/{quiz_id}.json"
   }
   ```

3. **Restart App**: Restart Flask app to load registry changes

4. **Test**: Verify quiz appears in home page dropdown and questions load correctly

5. **Commit**: 
   ```bash
   git add data/{quiz_id}.json data/quizzes_registry.json
   git commit -m "Feature: Add {Display Name} quiz with X questions"
   ```

### Add a New Question to Existing Quiz

1. Edit `data/{quiz_id}.json`
2. Add question object to `questions` array:
   ```json
   {
     "text": "What is...?",
     "options": ["Option A", "Option B", "Option C"],
     "correct": [0],
     "type": "single",
     "image": null
   }
   ```
   
   For multi-choice:
   ```json
   {
     "text": "Which are correct? (Select all that apply)",
     "options": ["Option A", "Option B", "Option C"],
     "correct": [0, 2],
     "type": "multi",
     "image": null
   }
   ```

3. Save file and test by taking the quiz
4. Commit:
   ```bash
   git add data/{quiz_id}.json
   git commit -m "Add question to {quiz_name}: {brief question description}"
   ```

### Add Question Image

1. Place image file in `img/` folder (supports subdirectories)
   ```
   img/physics/forces.png
   img/gcp/architecture.png
   ```

2. Reference in quiz JSON:
   ```json
   "image": "physics/forces.png"
   ```

3. Image displays in quiz and results pages automatically

### Test Multi-Choice Questions

1. Navigate to quiz with multi-choice questions
2. Verify hint displays: "(Select X correct answers)"
3. Test grading by:
   - Selecting all correct answers → Should pass ✓
   - Selecting only some correct answers → Should fail ✗
   - Selecting correct + incorrect answers → Should fail ✗
   - Selecting no answers → Should fail ✗

### Test History Feature

1. Complete a quiz (note the score and date)
2. Complete another quiz with different questions
3. Navigate to "View History" button
4. Verify last 2 attempts appear in table
5. Click "View Details" on one attempt
6. Verify attempt metadata displays (quiz name, score, date)

### Modify Quiz Styling

1. Create/edit `static/style.css`
2. Link in templates:
   ```html
   <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
   ```
3. Add custom classes or override Bootstrap
4. Restart app to load CSS changes

### Add New Route/Page

1. Create HTML template in `templates/new_page.html`
2. Add route to `app.py`:
   ```python
   @app.route('/new_page')
   def new_page():
       return render_template('new_page.html', variable=value)
   ```
3. Link from existing page via href or form action
4. Test by accessing `/new_page`
5. Commit:
   ```bash
   git add app.py templates/new_page.html
   git commit -m "Feature: Add new page with description"
   ```

### Change Timer Logic

**Client-side adjustment** (in quiz.html):
- Modify JavaScript `updateTimer()` function
- Change `setInterval()` timing (currently 1000ms = 1 second)
- Modify MM:SS format display

**Server-side adjustment** (in app.py):
- Add server-side timeout enforcement in `/submit_quiz`
- Validate quiz completion time against timer duration
- Example: Check if `datetime.now() - session['start_time']` exceeds timer

### Debug Quiz Loading Issues

1. **Check Registry**: Verify `data/quizzes_registry.json` is valid JSON
   ```bash
   python -c "import json; json.load(open('data/quizzes_registry.json'))"
   ```

2. **Check Quiz File**: Verify individual quiz file is valid JSON
   ```bash
   python -c "import json; json.load(open('data/gce.json'))"
   ```

3. **Check Flask Logs**: Watch terminal output for errors when quiz loads

4. **Verify File Paths**: Ensure file paths in registry match actual filenames

### Monitor Database Changes

1. View scores table:
   ```bash
   python -c "import sqlite3; c = sqlite3.connect('data/scores.db'); print(list(c.execute('SELECT * FROM scores ORDER BY date DESC LIMIT 3')))"
   ```

2. Check if answers column exists:
   ```bash
   python -c "import sqlite3; c = sqlite3.connect('data/scores.db'); print([col[1] for col in c.execute('PRAGMA table_info(scores)')])"
   ```

## Testing Workflow

1. **Unit Testing**: Test individual components (routes, grading logic)
   - Take quizzes with known answers
   - Verify score calculation
   - Check database persistence

2. **Integration Testing**: Test full workflows
   - Quiz selection → submission → results → history
   - Timer expiration
   - Multi-choice grading

3. **Regression Testing**: After changes, verify
   - Existing quizzes still load
   - Previous scores still display
   - History page still functions

## Code Standards

- **Naming**: Use snake_case for Python functions, camelCase for JavaScript
- **Comments**: Add comments for complex logic (grading, session management)
- **Docstrings**: Add docstrings to routes explaining purpose
- **Error Handling**: Redirect on errors rather than 500 pages
- **Validation**: Validate quiz_id and user inputs before processing

### Query Score Database

```python
import sqlite3

conn = sqlite3.connect('data/scores.db')
c = conn.cursor()

# Get all scores
c.execute('SELECT * FROM scores')
all_scores = c.fetchall()

# Get scores for specific category
c.execute("SELECT * FROM scores WHERE categories LIKE '%Math%'")
math_scores = c.fetchall()

# Average score
c.execute('SELECT AVG(percentage) FROM scores')
avg = c.fetchone()[0]

conn.close()
```

## Debugging Tips

### Enable Verbose Logging

```python
# In app.py
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Session Data

```python
# In any route
print(f"Session: {session}")
print(f"Questions count: {len(session.get('questions', []))}")
```

### Test with Print Statements

```python
# In start_quiz route
print(f"Categories requested: {request.form}")
print(f"Selected questions: {selected_questions}")
```

### Browser Developer Tools

- **Console**: Check for JavaScript errors in timer
- **Network**: Monitor form submissions and redirects
- **Storage**: Inspect session cookies (encrypted but visible size)
- **Elements**: Inspect HTML form structure

### Common Issues

| Issue | Diagnosis | Fix |
|-------|-----------|-----|
| Questions not showing | Check quizzes.json syntax | Use JSON validator |
| Score not saving | Check database permissions | Verify data/ folder writable |
| Timer not counting | Check browser console | Verify JavaScript enabled |
| Images broken | Check img/ folder structure | Verify path in quizzes.json |
| 500 error | Check app.py logs | Enable DEBUG mode |

## Code Standards

### Flask Best Practices
- Use `render_template()` for HTML responses
- Use `redirect()` and `url_for()` for navigation
- Store state in session (not globals)
- Validate form input before processing

### HTML/CSS Standards
- Use Bootstrap classes for consistency
- Semantic HTML5 structure
- Mobile-first responsive design

### Python Standards
- Type hints where helpful (optional)
- Descriptive variable names
- Comments for complex logic
- PEP 8 style guide

## Testing Workflow

1. **Manual Testing**:
   - Select quiz with all question types
   - Verify single-choice (radio buttons)
   - Verify multi-choice (checkboxes, multiple selection)
   - Submit and check score calculation
   - Verify results saved to database

2. **Edge Cases**:
   - Select 0 questions (should redirect to home)
   - Select more questions than available (should cap at available)
   - Submit form without answering (should score 0)
   - Use timer and let it expire (should auto-submit)

3. **Database Verification**:
   ```python
   # Check scores were saved
   SELECT COUNT(*) FROM scores;
   SELECT * FROM scores WHERE date > datetime('now', '-1 hour');
   ```

## Performance Considerations

- **Quiz Loading**: Shuffling is O(n); minimal impact even with 1000 questions
- **Database Writes**: SQLite fine for single-instance app; switch to PostgreSQL for scale
- **Session Storage**: Default Flask sessions use signed cookies (no server storage)
- **Image Delivery**: Flask fine for small images; use CDN for production

## Security Checklist

- [ ] Change `app.secret_key` before production
- [ ] Never commit secrets to version control
- [ ] Validate form input (already done implicitly)
- [ ] Escape user input in templates (Jinja2 does this by default)
- [ ] Use HTTPS in production (add with reverse proxy like nginx)
- [ ] Set secure session cookies for production

## Future Enhancement Ideas

1. **User Accounts**: Track scores per user (add login/register)
2. **Question Review**: Show correct answers after quiz
3. **Performance Analytics**: Dashboard with score trends
4. **Question Difficulty**: Track question performance across users
5. **Timed Per-Question**: Timer per question instead of total
6. **Export Scores**: CSV/PDF report generation
7. **Question Import**: Upload new quizzes from file
8. **Randomized Ordering**: Shuffle options within each question
9. **Hints System**: Optional hints for questions
10. **Mobile App**: Native iOS/Android app using same backend API