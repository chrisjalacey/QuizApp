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
- **Database Initialization**: SQLite database created automatically on app start via `init_db()` function with automatic schema migration
- **Quiz Data**: Create separate JSON files (e.g., data/math.json, data/science.json) and register in data/quizzes_registry.json

## Core Logic Implementation

### Quiz Selection Flow (start_quiz route)

1. Load quiz registry from `data/quizzes_registry.json`
2. Validate quiz_id matches an entry in registry
3. Load specific quiz file (e.g., data/gce.json) based on file path in registry
4. Use `random.sample()` to select random questions from quiz
5. Shuffle all selected questions
6. Store in Flask session with metadata (quiz_id, quiz_name, timer)
7. Redirect to quiz page

### Quiz Display (quiz route)

- Retrieve questions from session
- Pass to quiz.html template along with timer duration
- For each question:
  - If `type: "multi"`, display hint: "(Select X correct answers)" where X = len(question.correct)
  - If `type: "single"`, render radio buttons
  - If `type: "multi"`, render checkboxes
  - Display image if present via `/img/` route

### Quiz Submission and Grading (submit_quiz route)

1. Retrieve all submitted form data using `request.form.getlist()` for multi-choice support
2. For each question:
   - Get user answers (list of option indices)
   - Build review data object with:
     - Question text, type, options
     - Correct indices and labels
     - User answers and labels
     - is_correct flag (exact set match)
   - Compare with `correct` list as sets (order-independent)
   - Award 1 point if exact match
3. Calculate percentage: `(score / total) * 100`
4. Convert answers dict to list format: `{0: [1], 1: [0, 2]}` → `[[1], [0, 2]]`
5. Persist to SQLite database with timestamp, score, answers JSON
6. Store results + review_data in session
7. Redirect to results page

### Results Display (results route)

- Retrieve score, total, percentage, review_data, quiz_name from session
- Pass to results.html template
- Template renders:
  - Quiz name and score summary with progress bar
  - Accordion-style review with green (✓) for correct, red (✗) for incorrect
  - Each question shows: text, image, your answer(s), correct answer(s), multi-choice hint if applicable
  - Incorrect answers shown expanded by default for review

### History Display (history route)

- Query scores table: `SELECT id, date, categories, score, total, percentage FROM scores ORDER BY date DESC LIMIT 10`
- Pass attempts list to history.html template
- Template renders table with columns: Date, Quiz, Score, Percentage, View Details link

### History Detail (history/<int:attempt_id> route)

- Query scores table by attempt_id
- Retrieve date, categories, score, total, percentage, answers JSON
- Pass to history_detail.html template
- Display attempt metadata and placeholder for question review
- Note: Full question reconstruction requires loading quiz file and matching with stored answers (future enhancement)

### Timer Implementation

**JavaScript-based client-side timer:**
- Timer duration passed from Flask to template as variable
- JavaScript countdown loop using `setInterval()` with 1-second tick
- Auto-submit form when `timeLeft <= 0`
- Formatted as MM:SS display
- If timer set to 0, no timer shown

**Note**: Timer is not enforced server-side; JavaScript handles client-side enforcement. For high-security scenarios (exam proctoring), implement server-side timeout validation.

### Image Serving

- Images referenced in JSON as relative paths (e.g., "math_primes.png" or "gcp/architecture.png")
- Flask route `/img/<path:filename>` serves from `img/` directory
- Template references images as `<img src="/img/{{ question.image }}">`
- Supports nested subdirectories in img/ folder

### Session Management

**Session Keys Used:**
- `questions` - List of selected question objects
- `quiz_id` - ID of selected quiz from registry
- `quiz_name` - Display name of quiz
- `timer` - Timer duration in minutes (or empty string)
- `start_time` - ISO timestamp when quiz started
- `answers` - User answers as {question_index: [option_indices]}
- `review_data` - Detailed review objects for each question
- `score` - Points earned
- `total` - Total questions
- `percentage` - Score percentage
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