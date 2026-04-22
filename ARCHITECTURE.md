# Architecture

## Overview

Quiz App is a web-based quiz application built with Flask (Python backend) and Bootstrap (responsive frontend). It supports multiple quiz topics with single/multi-choice questions, optional timers, historical score tracking, and detailed answer review with persistence.

## Tech Stack

- **Backend**: Flask 3.1.3 (Python 3.11)
- **Frontend**: HTML5, Bootstrap 5.3.0, JavaScript
- **Database**: SQLite3 (scores storage with individual answer persistence)
- **Containerization**: Docker

## Project Structure

```
QuizApp/
├── app.py                      # Main Flask application
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container configuration
├── README.md                   # Project overview
├── ARCHITECTURE.md             # This file
├── IMPLEMENTATION.md           # Implementation details
├── JSON_SCHEMA.md              # Quiz data format reference
├── DEPLOYMENT.md               # Setup and deployment guide
├── API_ROUTES.md               # API documentation
├── DEVELOPMENT.md              # Development guide
├── data/
│   ├── quizzes_registry.json  # Quiz index and metadata
│   ├── math.json              # Math quiz questions
│   ├── science.json           # Science quiz questions
│   ├── gce.json               # Google Cloud Engineer quiz
│   └── scores.db              # SQLite database (auto-created)
├── img/                        # Question images (user-provided)
├── static/                     # CSS/JS assets (future expansion)
└── templates/
    ├── index.html              # Home page (quiz selection)
    ├── quiz.html               # Quiz page with questions
    ├── results.html            # Results page with detailed review
    ├── history.html            # History page (last 10 attempts)
    └── history_detail.html     # Historical attempt detail view
```

## Core Components

### 1. Flask Application (app.py)

**Key Routes:**
- `GET /` - Home page with quiz selection
- `POST /start_quiz` - Process quiz selection, random question selection
- `GET /quiz` - Display quiz questions with multi-choice hints
- `POST /submit_quiz` - Grade quiz, persist answers, save to database
- `GET /results` - Display results with detailed question-by-question review
- `GET /history` - Show last 10 quiz attempts
- `GET /history/<int:attempt_id>` - Show detailed review of historical attempt
- `GET /img/<filename>` - Serve images from img/ folder

**Session Management:**
- Stores: questions, quiz_id, quiz_name, answers, review_data, score, total, percentage, timer
- Uses secret_key for session security (change in production)

### 2. Quiz Data Files

**data/quizzes_registry.json**
- Registry of all available quizzes
- Format: `{quizzes: [{id, name, file}, ...]}`
- Used to populate quiz selection on home page

**Separate Quiz Files** (data/math.json, data/science.json, data/gce.json, etc.)
- Each file contains: `{questions: [...]}`
- Questions have: text, options, correct (indices), type (single/multi), image (optional)
- Enables modular quiz management—add new quiz by creating file + adding to registry

### 3. Score Database (data/scores.db)

**Table: scores** (auto-created with migration)
| Column | Type | Purpose |
|--------|------|---------|
| id | INTEGER PRIMARY KEY | Unique record ID |
| date | TEXT | ISO format timestamp |
| score | INTEGER | Correct answers count |
| total | INTEGER | Total questions |
| percentage | REAL | Score percentage |
| categories | TEXT | JSON array [quiz_name] |
| question_counts | TEXT | JSON {questions: count} |
| timer_used | INTEGER | Timer minutes (0 if none) |
| answers | TEXT | JSON array [[user_indices], ...] |

**Database Migration:**
- Auto-adds 'answers' column if missing (non-destructive ALTER TABLE)
- Backward-compatible with existing scores.db

### 4. Frontend Templates

**index.html**
- Quiz selection dropdown (populated from registry)
- Number of questions input (validated on submission)
- Optional timer duration input
- "View Previous Attempts" button links to /history
- Form submits to `/start_quiz`

**quiz.html**
- Displays questions dynamically from Flask context
- Multi-choice questions show hint: "(Select X correct answers)"
- Radio buttons for single-choice, checkboxes for multi-choice
- Optional JavaScript timer countdown with auto-submit
- Images displayed via /img/ route
- Form submits to `/submit_quiz`

**results.html**
- Score summary with progress bar: "X / Y (Z%)"
- Accordion-style question review (green ✓ for correct, red ✗ for incorrect)
- Each question shows: text, image (if exists), your answer(s), correct answer(s)
- Multi-choice shows: "(Correct: X)" label
- Buttons: "Take Another Quiz" and "View History"

**history.html**
- Table listing last 10 quiz attempts
- Columns: Date, Quiz, Score, Percentage, Action
- "View Details" link for each attempt (links to /history/<id>)
- "Back to Home" button
- Message if no attempts exist

**history_detail.html**
- Displays historical attempt with score and date
- Score summary with progress bar (same as results.html)
- Placeholder for detailed review (requires question reconstruction)
- Buttons: "Back to History" and "Home"

## Key Decisions

1. **Separate Quiz Files**: Each quiz is a separate JSON file for maintainability and modularity
2. **Registry System**: Central registry enables dynamic quiz selection without hardcoding
3. **Answer Persistence**: Individual answers stored in database (JSON array) for historical review
4. **Review Data Construction**: Generated during /submit_quiz for immediate results, stored in session
5. **Multi-choice Hints**: Display count of correct answers both before quiz (on quiz.html) and after (in review)
6. **Session Storage**: Quiz state stored in Flask session (not persisted between browser sessions)
7. **Database Scoring**: Scores table tracks aggregates + persists individual answer indices for future reconstruction
8. **History Limit**: Last 10 attempts displayed (can be paginated if needed)

## Future Extensibility

- User authentication for individual/organization score tracking
- Detailed question reconstruction in history (reconstruct full review from stored questions)
- Question bank management (import/export, versioning)
- Analytics dashboard for score trends and performance by topic
- Pagination for history (if > 10 attempts common)
- Additional question types (free text, matching, ordering)
- Image versioning to handle deleted images in historical review
- WCAG compliance for accessibility
- API endpoint for programmatic quiz access