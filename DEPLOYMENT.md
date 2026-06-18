# Deployment Guide

## Local Development

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)

### Setup

```bash
# 1. Navigate to project
cd QuizApp

# 2. Create and activate virtual environment
python -m venv .venv
# Windows (PowerShell):
.venv\Scripts\Activate.ps1
# Windows (cmd):
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run
python app.py

# 5. Open http://localhost:5000
```

### Configuration

In `app.py`:
- `debug=True` — auto-reload on changes
- `app.secret_key` — change to secure random string in production

### Troubleshooting

| Issue | Solution |
|-------|----------|
| ModuleNotFoundError: Flask | `pip install -r requirements.txt` with venv active |
| Port 5000 in use | Change port: `app.run(debug=True, port=5001)` |
| Images not loading | Check paths in quiz JSON match files in `img/` |

## Docker

### Build and Run

```bash
docker build -t quiz-app:latest .
docker run -p 5000:5000 quiz-app:latest
```

### With Persistent Data (Recommended)

```bash
docker run -d \
  -p 5000:5000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/img:/app/img \
  --name quiz-app \
  quiz-app:latest
```

**Windows PowerShell:**
```powershell
docker run -d `
  -p 5000:5000 `
  -v $pwd/data:/app/data `
  -v $pwd/img:/app/img `
  --name quiz-app `
  quiz-app:latest
```

### Docker Compose

```yaml
version: '3.8'
services:
  quiz-app:
    build: .
    ports:
      - "5000:5000"
    volumes:
      - ./data:/app/data
      - ./img:/app/img
```

```bash
docker-compose up -d
```

## Production Considerations

### Security

```python
import secrets, os
app.secret_key = os.getenv('SECRET_KEY', secrets.token_hex(32))
app.config['SESSION_COOKIE_SECURE'] = True      # HTTPS only
app.config['SESSION_COOKIE_HTTPONLY'] = True     # No JS access
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
```

### Performance

- Switch SQLite to PostgreSQL for multi-instance scaling
- Serve static files via nginx or CDN
- Use multiple app instances behind a load balancer

### Data Persistence

- `data/scores.db` — SQLite database (persisted on disk)
- `data/quizzes/` — Quiz JSON files
- `img/` — Question images
- Use volume mounts in Docker to persist across container restarts
