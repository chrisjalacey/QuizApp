# Architecture

## Overview

Quiz App is a web-based quiz application built with Flask (Python backend) and Bootstrap (responsive frontend). It supports multiple quiz topics with single/multi-choice questions, sections, optional timers, explanations, historical score tracking, and detailed answer review with persistence.

## Tech Stack

- **Backend**: Flask 3.0.3 (Python 3.11)
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
├── API_ROUTES.md               # Route documentation
├── JSON_SCHEMA.md              # Quiz data format reference
├── DEPLOYMENT.md               # Setup and deployment guide
├── DEVELOPMENT.md              # Development guide
├── QUICKREF.md                 # Quick reference card
├── data/
│   ├── quizzes/               # Quiz JSON files (auto-discovered)
│   │   └── gce.json           # Google Cloud Engineer quiz
│   └── scores.db             # SQLite database (auto-created)
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
- `POST /start_quiz` - Process quiz selection, section filtering, random question selection
- `GET /quiz` - Display quiz questions with multi-choice hints
- `POST /submit_quiz` - Grade quiz, persist answers, save to database
- `GET /results` - Display results with detailed question-by-question review
- `GET /history` - Show last 10 quiz attempts
- `GET /history/<int:attempt_id>` - Show detailed review of historical attempt
- `GET /img/<filename>` - Serve images from img/ folder

**Session Management:**
- Stores: questions, quiz_id, quiz_name, answers, review_data, score, total, percentage, timer, sections
- Uses secret_key for session security (change in production)

### 2. Quiz Data (Auto-Discovery)

Quizzes are auto-discovered by scanning `data/quizzes/` for `.json` files. No registry file is needed.

**Quiz File Format** (e.g., `data/quizzes/gce.json`):
- Top-level fields: `name`, `id`, `sections`, `questions`
- Each question has: text, options, correct (indices), type, image (optional), explanation (optional), section (optional)

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

### 4. Frontend Templates

**index.html** - Quiz selection dropdown, section checkboxes (dynamically populated), question count, timer input
**quiz.html** - Questions with radio/checkbox inputs, multi-choice hint, optional timer countdown
**results.html** - Score summary, progress bar, accordion-style question review with explanations
**history.html** - Table of last 10 attempts with "View Details" links
**history_detail.html** - Full review of a historical attempt with explanations

## Key Decisions

1. **Auto-Discovery**: Quiz files scanned from `data/quizzes/` folder — no registry needed
2. **Sections**: Questions can belong to sections; users can filter by section before starting
3. **Explanations**: Each question can have an explanation shown in review
4. **Answer Persistence**: Individual answers stored as JSON for historical review
5. **Session Storage**: Quiz state in Flask session (not persisted between browser sessions)
6. **History Limit**: Last 10 attempts displayed

## Future Extensibility

- User authentication for individual score tracking
- Analytics dashboard for score trends
- Additional question types (free text, matching, ordering)
- Pagination for history
- API endpoints for programmatic access
- WCAG compliance for accessibility
