# API Routes and Endpoints

## Overview

Quiz App uses Flask for routing. All routes are server-side rendered (HTML responses). No REST API endpoints currently.

## Routes Reference

### Home Page
**Endpoint**: `GET /`  
**Purpose**: Display home page with category selection form  
**Returns**: HTML page (index.html)  
**Response**: 
- Loads quiz categories from `data/quizzes.json`
- Renders form with input fields for each category
- User selects question counts and optional timer

**Template Context**:
```python
{
  "categories": ["Math", "Science", ...]  # List of category names
}
```

---

### Start Quiz
**Endpoint**: `POST /start_quiz`  
**Purpose**: Process quiz selections and prepare session  
**Request Form Data**:
```
count_<category_name>: <integer>  # Repeat for each category
timer: <integer or empty>          # Optional timer in minutes
```

**Example Form Data**:
```
count_Math=5
count_Science=3
timer=30
```

**Process**:
1. Parse form input for each category
2. Randomly sample specified number of questions from each category
3. Shuffle all selected questions
4. Store in Flask session:
   - `questions` - List of question objects
   - `categories` - Selected category names
   - `question_counts` - Dict of category:count
   - `timer` - Timer duration
   - `start_time` - ISO timestamp
5. Redirect to `/quiz`

**Returns**: Redirect (302) to `/quiz`  
**Errors**: 
- No questions selected → Redirects to `/`
- Invalid form data → Treated as 0

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
      "options": ["A", "B", "C"],
      "correct": [0, 1],
      "type": "single" or "multi",
      "image": null or "path/to/image.png"
    },
    ...
  ],
  "timer": "30" or ""  # Timer in minutes
}
```

**UI Elements**:
- Question text displayed
- Image shown if present (via `/img/` route)
- Radio buttons for single-choice questions
- Checkboxes for multi-choice questions
- JavaScript timer countdown (if timer set)
- Submit button

**Session Check**: If no questions in session, redirects to `/`

---

### Submit Quiz
**Endpoint**: `POST /submit_quiz`  
**Purpose**: Grade quiz and save results  
**Request Form Data**:
```
q0: <index>           # Single-choice: one value
q0: <index>           # Multi-choice: multiple values
q0: <index>
q1: <index>
...
```

**Example Form Data** (multi-choice with q0 having indices 0 and 2):
```
q0=0
q0=2
q1=1
q2=0
```

**Process**:
1. Retrieve all submitted answers using `request.form.getlist()`
2. Convert indices to integers
3. For each question:
   - Get user answers
   - Compare with `correct` array as sets
   - Award 1 point if exact match
4. Calculate score, total, and percentage
5. Insert into SQLite database:
   ```sql
   INSERT INTO scores 
   (date, score, total, percentage, categories, question_counts, timer_used)
   VALUES (NOW, score, total, percentage, json_categories, json_counts, timer_mins)
   ```
6. Store in session:
   - `score` - Points earned
   - `total` - Total questions
   - `percentage` - Score/total * 100
   - `answers` - User responses (for review)
7. Redirect to `/results`

**Returns**: Redirect (302) to `/results`

---

### Results Page
**Endpoint**: `GET /results`  
**Purpose**: Display quiz results  
**Returns**: HTML page (results.html)  

**Template Context**:
```python
{
  "score": 8,
  "total": 10,
  "percentage": 80.0
}
```

**UI Elements**:
- Score display (e.g., "8 / 10 (80.00%)")
- Link to home page to take another quiz

**Session Requirement**: Must have completed quiz (score/total in session)

---

### Image Serving
**Endpoint**: `GET /img/<path:filename>`  
**Purpose**: Serve question images from `img/` folder  
**URL Format**: 
```
/img/math_primes.png
/img/physics/forces.png
/img/science/elements.png
```

**Parameters**:
- `filename` - Relative path within `img/` folder

**Returns**: Image file with appropriate MIME type  
**Response Codes**:
- 200 - Image found and served
- 404 - Image not found

**Mounted By**: In quiz.html template: `<img src="/img/{{ questions[i].image }}">`

---

## Session Management

### Session Keys

| Key | Type | Lifecycle | Purpose |
|-----|------|-----------|---------|
| `questions` | List[Dict] | start_quiz → results | Selected questions for quiz |
| `categories` | List[str] | start_quiz → results | Selected category names |
| `question_counts` | Dict | start_quiz → submit_quiz | Category:count mapping |
| `timer` | str | start_quiz → quiz | Timer duration in minutes |
| `start_time` | str (ISO) | start_quiz → submit_quiz | Quiz start timestamp |
| `score` | int | submit_quiz → results | Points earned |
| `total` | int | submit_quiz → results | Total questions |
| `percentage` | float | submit_quiz → results | Score percentage |
| `answers` | Dict | submit_quiz → results | User responses by question index |

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