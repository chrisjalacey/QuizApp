# Implementation Details

## Setup and Installation

### Local Development Setup

1. **Prerequisites**: Python 3.11+, pip, virtual environment

2. **Create Virtual Environment**:
   ```bash
   python -m venv .venv
   # Windows
   .venv\Scripts\Activate.ps1
   # macOS/Linux
   source .venv/bin/activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Locally**:
   ```bash
   python app.py
   ```
   Access at `http://localhost:5000`

### Project Initialization

- **Directory Creation**: Create `data/`, `img/`, `templates/`, `static/` directories
- **Database Initialization**: SQLite database created automatically on app start via `init_db()` function
- **Quiz Data**: Populate `data/quizzes.json` with quiz questions following JSON_SCHEMA.md format

## Core Logic Implementation

### Quiz Selection Flow (start_quiz route)

1. Load quiz data from JSON
2. Iterate through categories in form submission
3. For each category with selected question count:
   - Use `random.sample()` to select random questions
   - Add to selection pool
4. Shuffle all selected questions globally
5. Store in Flask session with metadata (categories, question_counts, timer)
6. Redirect to quiz page

### Quiz Submission and Grading (submit_quiz route)

1. Retrieve all submitted form data using `request.form.getlist()` for multi-choice
2. For each question:
   - Get user answers (list of option indices)
   - Compare with `correct` list as sets (order-independent)
   - Award 1 point if exact match
3. Calculate percentage: `(score / total) * 100`
4. Save to SQLite database with timestamp and metadata
5. Store results in session and redirect to results page

### Timer Implementation

**JavaScript-based client-side timer:**
- Timer duration passed from Flask to template as variable
- JavaScript countdown loop using `setInterval()` with 1-second tick
- Auto-submit form when `timeLeft <= 0`
- Formatted as MM:SS display

**Note**: Timer is not enforced server-side; JavaScript handles client-side enforcement. For high-security scenarios (exam proctoring), implement server-side timeout validation.

### Image Serving

- Images referenced in JSON as relative paths (e.g., "math_primes.png" becomes "img/math_primes.png")
- Flask route `/img/<path:filename>` serves from `img/` directory
- Template references images as `/img/{{ questions[i].image }}`

### Session Management

**Session Keys Used:**
- `questions` - List of selected question objects
- `current` - Current question index (for future pagination)
- `answers` - User answers as {question_index: [option_indices]}
- `categories` - List of selected category names
- `question_counts` - Dict {category_name: count}
- `timer` - Timer duration in minutes (empty string if no timer)
- `start_time` - ISO timestamp of quiz start
- `score` - Final score (after submission)
- `total` - Total questions
- `percentage` - Final percentage

## Dependencies

- **Flask==3.0.3** - Web framework
- **Python 3.11 standard library**: json, os, random, sqlite3, datetime (no additional packages needed)

## Database Operations

**Initialization (init_db)**:
```python
CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY,
    date TEXT,
    score INTEGER,
    total INTEGER,
    percentage REAL,
    categories TEXT,  # JSON array
    question_counts TEXT,  # JSON object
    timer_used INTEGER
)
```

**Insert Score**:
```python
INSERT INTO scores (date, score, total, percentage, categories, question_counts, timer_used)
VALUES (?, ?, ?, ?, ?, ?, ?)
```

## Frontend Features

### Bootstrap Components Used
- Container grid layout
- Form controls (input, radio, checkbox)
- Alert boxes for timer/results
- Responsive utilities (img-fluid)

### JavaScript Functionality
- Timer countdown with zero-padding
- Form auto-submit on timer completion

### Mobile Responsiveness
- Viewport meta tag for device scaling
- Bootstrap responsive utilities
- Touch-friendly input sizes

## Testing Considerations

1. **Quiz Selection**: Verify correct number of questions per category
2. **Single-choice**: Only one radio button can be selected
3. **Multi-choice**: Multiple checkboxes can be selected
4. **Timer**: Countdown displays correctly and auto-submits
5. **Scoring**: Exact match grading for multi-choice
6. **Database**: Scores persist across sessions
7. **Images**: Images load correctly from img/ folder
8. **Mobile**: Test on various screen sizes

## Common Modifications

- **Change Secret Key**: Update `app.secret_key` in app.py (use environment variable in production)
- **Modify Timer**: Update timer logic in quiz.html JavaScript or app.py
- **Add Question Types**: Extend question rendering logic in quiz.html based on `type` field
- **Styling**: Add custom CSS to static/style.css and link in templates
- **Database Queries**: Use sqlite3 module directly in new routes