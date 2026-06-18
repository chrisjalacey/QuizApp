# API Routes and Endpoints

## Overview

All routes are server-side rendered (HTML responses). No REST API endpoints currently.

## Routes

### GET /
**Purpose**: Home page with quiz selection form

**Process**:
- Scans `data/quizzes/` folder for `.json` files
- Loads each quiz's name and sections
- Renders form with quiz dropdown, section checkboxes, question count, timer

**Template Context**:
```python
{
  "quizzes": [
    {"id": "gce", "name": "Google Associate Cloud Engineer", "sections": [...]}
  ]
}
```

---

### POST /start_quiz
**Purpose**: Process quiz selection and prepare session

**Form Data**:
```
quiz_id: <string>          # Quiz ID (filename without .json)
count: <integer>           # Number of questions
sections: <list>           # Optional selected section IDs
timer: <integer or empty>  # Optional timer in minutes
```

**Process**:
1. Load quiz file from `data/quizzes/{quiz_id}.json`
2. Filter questions by selected sections (if any)
3. Randomly sample specified number of questions
4. Store in session: questions, quiz_id, quiz_name, timer, start_time, sections
5. Redirect to `/quiz`

**Errors**: Invalid quiz_id or count → Redirects to `/`

---

### GET /quiz
**Purpose**: Display quiz questions

**Template Context**:
```python
{
  "questions": [...],  # List of question objects
  "timer": "60"        # or "" if no timer
}
```

**Session Check**: If no questions in session, redirects to `/`

---

### POST /submit_quiz
**Purpose**: Grade quiz, persist answers, save results

**Form Data**:
```
q0: <index>    # Single or multi values per question
q1: <index>
q1: <index>    # Multiple values for multi-choice
...
```

**Process**:
1. Grade each question (set comparison, order-independent)
2. Build review_data with question text, options, correct/user answers, explanation
3. Save to SQLite: date, score, total, percentage, quiz_name, answers JSON
4. Store results in session
5. Redirect to `/results`

---

### GET /results
**Purpose**: Display quiz results with detailed review

**Template Context**:
```python
{
  "score": 8,
  "total": 10,
  "percentage": 80.0,
  "quiz_name": "Google Associate Cloud Engineer",
  "review_data": [
    {
      "question_text": "...",
      "question_type": "single",
      "options": [...],
      "correct_indices": [1],
      "correct_labels": ["Cloud Run"],
      "user_answers": [1],
      "user_labels": ["Cloud Run"],
      "is_correct": True,
      "image": null,
      "explanation": "Cloud Run is..."
    }
  ]
}
```

---

### GET /history
**Purpose**: Display last 10 quiz attempts

**Query**: `SELECT id, date, categories, score, total, percentage FROM scores ORDER BY date DESC LIMIT 10`

---

### GET /history/<int:attempt_id>
**Purpose**: Detailed review of a specific historical attempt

**Process**:
- Load attempt from DB
- Reconstruct review data by loading the quiz file and matching stored answers to questions
- Displays explanations for each question

---

### GET /img/<path:filename>
**Purpose**: Serve question images from `img/` folder

Supports subdirectories (e.g., `/img/gcp/architecture.png`)

---

## Session Keys

| Key | Type | Purpose |
|-----|------|---------|
| `questions` | List[Dict] | Selected questions for current quiz |
| `quiz_id` | str | ID of selected quiz |
| `quiz_name` | str | Display name of quiz |
| `timer` | str | Timer duration in minutes |
| `start_time` | str (ISO) | Quiz start timestamp |
| `sections` | List[str] | Selected section IDs |
| `score` | int | Points earned |
| `total` | int | Total questions |
| `percentage` | float | Score percentage |
| `answers` | Dict | User responses by question index |
| `review_data` | List[Dict] | Detailed review objects per question |

## Error Handling

| Scenario | Behavior |
|----------|----------|
| Invalid quiz_id or count | Redirect to `/` |
| Session expires during quiz | Redirect to `/` |
| Image not found | 404 from `/img/` |
| No sections match | Falls back to all questions |
