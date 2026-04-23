# QuizApp - Quick Reference

## Project Structure
```
QuizApp/
├── app.py              # Flask application (8 routes)
├── data/
│   ├── quizzes_registry.json  # Quiz index
│   ├── math.json       # Math quiz (2 questions)
│   ├── science.json    # Science quiz (1 question)
│   ├── gce.json        # GCP quiz (20 questions)
│   └── scores.db       # SQLite database
└── templates/          # 5 HTML templates
```

## Tech Stack
- Flask 3.1.3, Python 3.11, SQLite3, Bootstrap 5.3.0

## Routes
| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Home page (quiz selection) |
| `/start_quiz` | POST | Start quiz with selected questions |
| `/quiz` | GET | Display quiz questions |
| `/submit_quiz` | POST | Grade and save results |
| `/results` | GET | Show score with detailed review |
| `/history` | GET | List last 10 attempts |
| `/history/<id>` | GET | View specific attempt details |
| `/img/<path>` | GET | Serve question images |

## Quiz JSON Format
```json
{
  "questions": [{
    "text": "Question?",
    "options": ["A", "B", "C"],
    "correct": [0],
    "type": "single",
    "explanation": "Why answer is correct"
  }]
}
```

## Database Schema
- Table: `scores` (id, date, score, total, percentage, categories, question_counts, timer_used, answers)

## Running
```bash
python app.py  # Runs on http://127.0.0.1:5000
```

## Docker
```bash
docker build -t quizapp .
docker run -p 5000:5000 quizapp
```