# Architecture

## Overview

Quiz App is a web-based quiz application built with Flask (Python backend) and Bootstrap (responsive frontend). It supports category-based quizzes with single/multi-choice questions, optional timers, and historical score tracking.

## Tech Stack

- **Backend**: Flask 3.0.3 (Python 3.11)
- **Frontend**: HTML5, Bootstrap 5.3.0, JavaScript
- **Database**: SQLite3 (scores storage)
- **Containerization**: Docker

## Project Structure

```
QuizApp/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── Dockerfile             # Container configuration
├── README.md              # Project overview
├── ARCHITECTURE.md        # This file
├── IMPLEMENTATION.md      # Implementation details
├── JSON_SCHEMA.md         # Quiz data format reference
├── DEPLOYMENT.md          # Setup and deployment guide
├── data/
│   ├── quizzes.json      # Quiz questions and categories
│   └── scores.db         # SQLite database (auto-created)
├── img/                   # Question images (user-provided)
├── static/                # CSS/JS assets (future expansion)
└── templates/
    ├── index.html         # Home page (category selection)
    ├── quiz.html          # Quiz page
    └── results.html       # Results page
```

## Core Components

### 1. Flask Application (app.py)

**Key Routes:**
- `GET /` - Home page with category selection form
- `POST /start_quiz` - Process quiz settings, select random questions
- `GET /quiz` - Display quiz questions
- `POST /submit_quiz` - Grade quiz and save score
- `GET /results` - Display results
- `GET /img/<filename>` - Serve images from img/ folder

**Session Management:**
- Stores selected questions, current progress, and user answers in Flask session
- Uses secret_key for session security (change in production)

### 2. Quiz Data (data/quizzes.json)

Hierarchical structure:
- Top level: `categories` array
- Each category has `name` and `questions` array
- Each question has `text`, `options`, `correct` (indices), `type` (single/multi), `image` (optional)

### 3. Score Database (data/scores.db)

**Table: scores**
- id (INTEGER PRIMARY KEY)
- date (TEXT, ISO format)
- score (INTEGER, correct answers)
- total (INTEGER, total questions)
- percentage (REAL, score/total * 100)
- categories (TEXT, JSON array of category names)
- question_counts (TEXT, JSON object of category:count)
- timer_used (INTEGER, timer minutes or 0)

### 4. Frontend Templates

**index.html**
- Category selection with number inputs for each category
- Optional timer duration input
- Form submits to `/start_quiz`

**quiz.html**
- Displays questions dynamically from Flask context
- Radio buttons for single-choice, checkboxes for multi-choice
- Optional JavaScript timer countdown
- Form submits to `/submit_quiz`

**results.html**
- Shows score, total, and percentage
- Link to home for another quiz

## Key Decisions

1. **Session Storage**: Use Flask sessions for quiz state instead of database—simplifies development and doesn't require user authentication
2. **Timer Enforcement**: JavaScript countdown on client; auto-submit when time expires
3. **Question Selection**: Random sampling from category; shuffled globally
4. **Multi-choice Grading**: Exact set match—all correct answers must be selected, no more, no less
5. **Image Paths**: Stored as relative paths in JSON (e.g., "img/math_primes.png"), served via Flask route

## Future Extensibility

- User authentication for individual score tracking
- Additional question types (free text, matching, etc.)
- Question banks and import/export
- Analytics dashboard for score trends
- Review mode to show correct answers
- WCAG compliance for accessibility