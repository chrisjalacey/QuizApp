# QuizApp - Quick Reference

## Project Structure
```
QuizApp/
├── app.py              # Flask application (8 routes)
├── data/
│   ├── quizzes/       # Quiz JSON files (auto-discovered)
│   │   └── gce.json   # GCP quiz (20 questions, 5 sections)
│   └── scores.db      # SQLite database
├── img/               # Question images
├── static/            # CSS/JS assets
└── templates/         # 5 HTML templates
```

## Tech Stack
- Flask 3.0.3, Python 3.11, SQLite3, Bootstrap 5.3.0

## Routes
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Home page (quiz selection + sections) |
| `/start_quiz` | POST | Start quiz with selected questions/sections |
| `/quiz` | GET | Display quiz questions |
| `/submit_quiz` | POST | Grade and save results |
| `/results` | GET | Show score with detailed review |
| `/history` | GET | List last 10 attempts |
| `/history/<id>` | GET | View specific attempt details |
| `/img/<path>` | GET | Serve question images |

## Quiz JSON Format
```json
{
  "name": "Quiz Name",
  "sections": [{"id": "...", "name": "...", "description": "..."}],
  "questions": [{
    "text": "Question?",
    "options": ["A", "B", "C"],
    "correct": [0],
    "type": "single",
    "explanation": "Why answer is correct",
    "section": "section_id"
  }]
}
```

## Adding a Quiz
1. Create `data/quizzes/{id}.json` with format above
2. Restart app — auto-discovered from folder

## Database Schema
- Table: `scores` (id, date, score, total, percentage, categories, question_counts, timer_used, answers)

## Running
```bash
python app.py  # http://127.0.0.1:5000
```

## Docker
```bash
docker build -t quiz-app .
docker run -p 5000:5000 quiz-app
```
