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

- **app.py** - All Flask routes, session logic, database operations, and initialization
- **data/quizzes.json** - Quiz questions organized by category (JSON format—see JSON_SCHEMA.md)
- **data/scores.db** - SQLite database automatically created on first run; stores all quiz scores
- **templates/index.html** - Home page with category selection form
- **templates/quiz.html** - Quiz page with dynamic question rendering and timer
- **templates/results.html** - Results page showing score and percentage
- **static/** - (Empty) Reserved for CSS/JavaScript assets
- **img/** - Question images referenced in quizzes.json
- **requirements.txt** - Python dependencies (Flask only)
- **Dockerfile** - Container configuration for Docker deployment
- **README.md** - User-facing project overview
- **ARCHITECTURE.md** - System design and components
- **IMPLEMENTATION.md** - Implementation details and logic
- **JSON_SCHEMA.md** - Quiz data format reference
- **DEPLOYMENT.md** - Setup and deployment instructions
- **API_ROUTES.md** - Route documentation

## Common Development Tasks

### Add a New Question

1. Edit `data/quizzes.json`
2. Locate category or add new category object
3. Add question object to `questions` array:
   ```json
   {
     "text": "What is...?",
     "options": ["A", "B", "C"],
     "correct": [0],
     "type": "single",
     "image": null
   }
   ```
4. Save file
5. Reload browser (no app restart needed if quizzes.json loaded per-request)

### Add Question Image

1. Place image file in `img/` folder (supports subdirectories)
2. Reference in quizzes.json:
   ```json
   "image": "filename.png"  // Root img/ folder
   "image": "subfolder/filename.png"  // Nested
   ```
3. Image will display in quiz if path is correct

### Modify Quiz Styling

1. Create/edit `static/style.css`
2. Link in templates:
   ```html
   <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
   ```
3. Add custom classes or override Bootstrap

### Add New Route/Page

1. Create HTML template in `templates/`
2. Add route to `app.py`:
   ```python
   @app.route('/new_page')
   def new_page():
       return render_template('new_page.html', variable=value)
   ```
3. Link from existing page via href or form action

### Change Timer Logic

**Client-side adjustment** (in quiz.html):
- Modify JavaScript `updateTimer()` function
- Change `setInterval()` timing or format

**Server-side adjustment** (in app.py):
- Validate timer in `/start_quiz` route
- Add server-side timeout enforcement in `/submit_quiz`

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