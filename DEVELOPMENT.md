# Development Guide

## Quick Start

```bash
cd QuizApp
.venv\Scripts\Activate.ps1   # Windows PowerShell
pip install -r requirements.txt
python app.py
# Open http://localhost:5000
```

## Common Tasks

### Add a New Quiz

1. Create `data/quizzes/{quiz_id}.json`:
   ```json
   {
     "name": "Display Name",
     "sections": [
       {"id": "section1", "name": "Section Name", "description": "Brief description"}
     ],
     "questions": [
       {
         "text": "Question?",
         "options": ["A", "B", "C"],
         "correct": [0],
         "type": "single",
         "image": null,
         "explanation": "Why A is correct.",
         "section": "section1"
       }
     ]
   }
   ```
2. Restart the app — quiz appears automatically (auto-discovered from folder)

### Add a Question to an Existing Quiz

Edit the quiz JSON file in `data/quizzes/` and add to the `questions` array. No restart needed if Flask debug mode is active.

### Add a Question Image

1. Place image in `img/` (subdirectories supported): `img/gcp/diagram.png`
2. Reference in quiz JSON: `"image": "gcp/diagram.png"`

### Test Multi-Choice Grading

- Selecting all correct answers → Pass ✓
- Selecting only some correct → Fail ✗
- Selecting correct + incorrect → Fail ✗
- No answer selected → Fail ✗

### Monitor the Database

```bash
python -c "import sqlite3; c=sqlite3.connect('data/scores.db'); print(list(c.execute('SELECT * FROM scores ORDER BY date DESC LIMIT 3')))"
```

Or use the included utility scripts:
```bash
python inspect_db.py
python init_and_inspect_db.py
```

## Code Standards

- Python: snake_case, PEP 8
- JavaScript: camelCase
- Use `redirect()` + `url_for()` for navigation
- Validate form input before processing
- Store state in session (not globals)

## Security Checklist

- [ ] Change `app.secret_key` before production
- [ ] Never commit secrets to version control
- [ ] Use HTTPS in production
- [ ] Set secure session cookies

## Debugging

```python
# Enable verbose logging in app.py
import logging
logging.basicConfig(level=logging.DEBUG)

# Print session data in any route
print(f"Session: {session}")
```

### Common Issues

| Issue | Fix |
|-------|-----|
| Questions not showing | Validate quiz JSON syntax |
| Score not saving | Check `data/` folder is writable |
| Timer not counting | Check browser console for JS errors |
| Images broken | Verify path in quiz JSON matches `img/` structure |
| History detail crashes | Ensure quiz file still exists with matching questions |
