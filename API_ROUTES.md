# API Routes and Endpoints

## Overview

Quiz App uses Flask for routing. All routes are server-side rendered (HTML responses). No REST API endpoints currently.

## Routes Reference

### Home Page
**Endpoint**: `GET /`  
**Purpose**: Display home page with quiz selection form  
**Returns**: HTML page (index.html)  

**Process**:
- Load quizzes_registry.json to get list of available quizzes
- Render form with quiz dropdown, question count input, optional timer

**Template Context**:
```python
{
  "quizzes": [
    {"id": "math", "name": "Mathematics", "file": "data/math.json"},
    {"id": "science", "name": "Science", "file": "data/science.json"},
    {"id": "gce", "name": "Google Associate Cloud Engineer", "file": "data/gce.json"}
  ]
}
```

**UI Elements**:
- Quiz selection dropdown
- Question count input (numeric)
- Optional timer duration input (numeric, minutes)
- "Start Quiz" button
- "View Previous Attempts" button (links to `/history`)

---

### Start Quiz
**Endpoint**: `POST /start_quiz`  
**Purpose**: Process quiz selection and prepare session  
**Request Form Data**:
```
quiz_id: <string>     # Quiz ID from registry (e.g., "math")
count: <integer>      # Number of questions to select
timer: <integer or empty>  # Optional timer in minutes
```

**Example Form Data**:
```
quiz_id=gce
count=15
timer=60
```

**Process**:
1. Validate quiz_id against registry
2. Load quiz from corresponding JSON file (e.g., data/gce.json)
3. Randomly sample specified number of questions
4. Shuffle questions
5. Store in Flask session:
   - `questions` - List of question objects
   - `quiz_id` - Selected quiz ID
   - `quiz_name` - Quiz name from registry
   - `timer` - Timer duration
   - `start_time` - ISO timestamp
6. Redirect to `/quiz`

**Returns**: Redirect (302) to `/quiz` on success  
**Errors**: 
- Invalid quiz_id → Redirects to `/`
- Invalid count → Redirects to `/`
- Quiz file not found → Redirects to `/`

---

### Quiz Page
**Endpoint**: `GET /quiz`  
**Purpose**: Display quiz questions and answer form  
**Returns**: HTML page (quiz.html)  
**Requires**: Active session with questions  

**Template Context**:
```python
{
  "questions": [
    {
      "text": "Question text?",
      "options": ["Option A", "Option B", "Option C"],
      "correct": [0, 2],
      "type": "single",
      "image": null
    },
    {
      "text": "Which are correct?",
      "options": ["A", "B", "C", "D"],
      "correct": [0, 1, 3],
      "type": "multi",
      "image": "questions/sample.png"
    }
  ],
  "timer": "60" or ""
}
```

**UI Elements**:
- Question number and text
- **Multi-choice hint**: "(Select X correct answers)" displayed for multi-choice questions
- Image shown if present (via `/img/` route)
- Radio buttons for single-choice (`type: "single"`)
- Checkboxes for multi-choice (`type: "multi"`)
- Optional JavaScript timer countdown (if timer set)
- Auto-submit when timer reaches 0
- Submit button

**Session Check**: If no questions in session, redirects to `/`

---

### Submit Quiz
**Endpoint**: `POST /submit_quiz`  
**Purpose**: Grade quiz, persist answers, save results  
**Request Form Data**:
```
q0: <index>           # Single-choice: one value
q0: <index>           # Multi-choice: can be multiple
q0: <index>
q1: <index>
...
```

**Example**:
```
q0=1          (single-choice answer: index 1)
q1=0          (multi-choice answer: index 0)
q1=2          (multi-choice answer: index 2)
q2=3          (single-choice answer: index 3)
```

**Process**:
1. Retrieve all submitted answers using `request.form.getlist()` for multi-choice support
2. Convert indices to integers
3. For each question:
   - Get user answers
   - Build review data: question text, options, correct answers, user answers, is_correct flag
   - Compare with `correct` array as sets (order-independent)
   - Award 1 point if exact match
4. Calculate score, total, and percentage
5. Convert answers to list format: `{0: [1], 1: [0, 2]}` → `[[1], [0, 2]]`
6. Insert into SQLite database:
   ```sql
   INSERT INTO scores 
   (date, score, total, percentage, categories, question_counts, timer_used, answers)
   VALUES (NOW, score, total, percentage, json_categories, json_counts, timer_mins, json_answers)
   ```
7. Store in session:
   - `score` - Points earned
   - `total` - Total questions
   - `percentage` - Score/total * 100
   - `answers` - User responses dict (for display)
   - `review_data` - Detailed review objects for each question
   - `quiz_name` - Quiz name
8. Redirect to `/results`

**Returns**: Redirect (302) to `/results`

---

### Results Page
**Endpoint**: `GET /results`  
**Purpose**: Display quiz results with detailed answer review  
**Returns**: HTML page (results.html)  

**Template Context**:
```python
{
  "score": 8,
  "total": 10,
  "percentage": 80.0,
  "quiz_name": "Google Associate Cloud Engineer",
  "review_data": [
    {
      "question_index": 0,
      "question_text": "Which service...",
      "question_type": "single",
      "options": ["A", "B", "C", "D"],
      "correct_indices": [1],
      "correct_labels": ["Cloud Run"],
      "correct_count": 1,
      "user_answers": [1],
      "user_labels": ["Cloud Run"],
      "is_correct": True,
      "image": null
    },
    {
      "question_index": 1,
      "question_text": "Which are valid...",
      "question_type": "multi",
      "options": ["Option 1", "Option 2", "Option 3"],
      "correct_indices": [0, 2],
      "correct_labels": ["Option 1", "Option 3"],
      "correct_count": 2,
      "user_answers": [0],
      "user_labels": ["Option 1"],
      "is_correct": False,
      "image": null
    }
  ]
}
```

**UI Elements**:
- Quiz name and score summary: "X / Y (Z%)"
- Progress bar showing percentage
- Accordion-style question review:
  - Green ✓ badge for correct answers (expanded by default)
  - Red ✗ badge for incorrect answers (collapsed by default)
  - Each question shows: text, image (if exists), your answer(s), correct answer(s)
  - Multi-choice shows: "(Correct: X)" label
- Buttons: "Take Another Quiz" and "View History"

**Session Requirement**: Must have completed quiz (score/total/review_data in session)

---

### History Page
**Endpoint**: `GET /history`  
**Purpose**: Display last 10 quiz attempts  
**Returns**: HTML page (history.html)  

**Process**:
- Query scores table: `SELECT id, date, categories, score, total, percentage FROM scores ORDER BY date DESC LIMIT 10`
- Format data for display

**Template Context**:
```python
{
  "attempts": [
    {
      "id": 1,
      "date": "2026-04-22T09:15:30.123456",
      "quiz_name": "Google Associate Cloud Engineer",
      "score": 12,
      "total": 15,
      "percentage": 80.0
    },
    ...
  ]
}
```

**UI Elements**:
- Table with columns: Date, Quiz, Score, Percentage, Action
- "View Details" link for each attempt (links to `/history/<id>`)
- "Back to Home" button
- Message if no attempts exist

---

### History Detail Page
**Endpoint**: `GET /history/<int:attempt_id>`  
**Purpose**: Display detailed review of a specific quiz attempt  
**Returns**: HTML page (history_detail.html)  
**URL Format**: `/history/1`, `/history/5`, etc.

**Process**:
- Query scores table by id: `SELECT date, categories, score, total, percentage, answers FROM scores WHERE id = ?`
- Retrieve date, quiz_name, score, total, percentage, answers JSON
- If no record found, redirect to `/history`

**Template Context**:
```python
{
  "attempt_id": 1,
  "date": "2026-04-22T09:15:30.123456",
  "quiz_name": "Google Associate Cloud Engineer",
  "score": 12,
  "total": 15,
  "percentage": 80.0,
  "review_data": []  # Limited in v1 (stored answers only, not full questions)
}
```

**UI Elements**:
- Attempt metadata: Quiz name, date, score, percentage
- Progress bar showing percentage
- Note: "Detailed question review is not available for this attempt" (requires question reconstruction)
- Buttons: "Back to History" and "Home"

**Future Enhancement**: Reconstruct full question data by loading quiz file and matching with stored answers

---

### Image Serving
**Endpoint**: `GET /img/<path:filename>`  
**Purpose**: Serve question images from `img/` folder  
**URL Format**: 
```
/img/math_primes.png
/img/physics/forces.png
```

**Parameters**:
- `filename` - Relative path within `img/` folder (path:filename allows subdirectories)

**Returns**: Image file with appropriate MIME type  
**Response Codes**:
- 200 - Image found and served
- 404 - Image not found

**Usage in Templates**: In quiz.html and results.html: `<img src="/img/{{ question.image }}">`

---

## Session Management

### Session Keys

| Key | Type | Lifecycle | Purpose |
|-----|------|-----------|---------|
| `questions` | List[Dict] | start_quiz → results | Selected questions for quiz |
| `quiz_id` | str | start_quiz → results | ID of selected quiz |
| `quiz_name` | str | start_quiz → results | Display name of quiz |
| `timer` | str | start_quiz → quiz | Timer duration in minutes |
| `start_time` | str (ISO) | start_quiz → submit_quiz | Quiz start timestamp |
| `score` | int | submit_quiz → results | Points earned |
| `total` | int | submit_quiz → results | Total questions |
| `percentage` | float | submit_quiz → results | Score percentage |
| `answers` | Dict | submit_quiz → results | User responses by question index |
| `review_data` | List[Dict] | submit_quiz → results | Detailed review objects per question |

### Session Lifetime
- Created on form submission to `/start_quiz`
- Persists through quiz and results
- Not explicitly cleared (defaults to browser session)

### Security Notes
- Sessions signed with `app.secret_key`
- Tampered sessions rejected by Flask
- For production: Use secure key and HTTPS

---

## Error Handling

| Scenario | Behavior |
|----------|----------|
| No categories in quizzes.json | Home page displays empty form |
| No questions selected | Redirect to `/` (no quiz started) |
| Session expires during quiz | Redirect to `/` (questions not found) |
| Image not found | Broken image displayed (404 from /img/) |
| Invalid form data | Treated as 0 or ignored |
| Database write fails | Exception raised (app crash) |

---

## Data Flow Diagram

```
GET / 
  ↓
[Show Categories Form]
  ↓ (Fill form, select counts and timer)
POST /start_quiz
  ↓ (Validate and sample questions)
[Store in session, shuffle]
  ↓
GET /quiz
  ↓
[Display questions with timer]
  ↓ (Answer questions)
POST /submit_quiz
  ↓ (Grade, save to DB)
[Calculate results]
  ↓
GET /results
  ↓
[Display score]
  ↓ (Link to home)
GET /
```