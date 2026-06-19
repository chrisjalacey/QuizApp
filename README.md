# Quiz App

A web-based quiz application similar to VCE exam simulators.

## Features

- JSON-based quiz data with auto-discovery from `data/quizzes/` folder
- Section-based filtering (select specific topics)
- Single-choice and multi-choice questions
- Explanations shown in review
- Optional timer
- Image support for questions
- Historical score tracking with detailed review
- Mobile-friendly responsive design

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run locally: `python app.py`
3. Open http://localhost:5000

## Docker

Build: `docker build -t quiz-app .`
Run: `docker run -p 5000:5000 -v $(pwd)/data/quizzes:/app/data/quizzes quiz-app`

Mount the `data/quizzes/` folder as a volume so you can add or update quizzes without rebuilding the image.

### Docker Compose

```yaml
version: '3.8'
services:
  quiz-app:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./data/quizzes:/app/data/quizzes
```

```bash
docker-compose up -d
```

## Quiz Data

Add `.json` files to `data/quizzes/` — they are auto-discovered on startup.

Format:
```json
{
  "name": "Quiz Display Name",
  "sections": [
    {"id": "section1", "name": "Section Name", "description": "Brief description"}
  ],
  "questions": [
    {
      "text": "Question?",
      "options": ["A", "B", "C"],
      "correct": [0],
      "type": "single",
      "image": "img/image.png",
      "explanation": "Why this answer is correct",
      "section": "section1"
    }
  ]
}
```

## Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) — System design and components
- [API_ROUTES.md](API_ROUTES.md) — Route documentation
- [JSON_SCHEMA.md](JSON_SCHEMA.md) — Quiz data format reference
- [DEPLOYMENT.md](DEPLOYMENT.md) — Setup and deployment guide
- [DEVELOPMENT.md](DEVELOPMENT.md) — Development guide
- [QUICKREF.md](QUICKREF.md) — Quick reference card
