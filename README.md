# Quiz App

A web-based quiz application similar to VCE exam simulators.

## Features

- JSON-based quiz data with categories
- Select categories and number of questions
- Single-choice and multi-choice questions
- Optional timer
- Image support for questions
- Historical score tracking
- Mobile-friendly responsive design

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run locally: `python app.py`
3. Open http://localhost:5000

## Docker

Build: `docker build -t quiz-app .`
Run: `docker run -p 5000:5000 quiz-app`

## Quiz Data

Edit `data/quizzes.json` to add questions.

Format:
```json
{
  "categories": [
    {
      "name": "Category",
      "questions": [
        {
          "text": "Question?",
          "options": ["A", "B", "C"],
          "correct": [0],  // array for multi-choice
          "type": "single",  // or "multi"
          "image": "img/image.png"  // optional
        }
      ]
    }
  ]
}
```