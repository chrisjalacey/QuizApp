# Deployment Guide

## Local Development

### Prerequisites
- Python 3.11 or higher
- pip (Python package manager)
- Virtual environment (venv)

### Step-by-Step Setup

1. **Clone/Access Repository**
   ```bash
   cd c:\Users\601234026\OneDrive - BT Plc\Documents\Git\QuizApp
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv .venv
   ```

3. **Activate Virtual Environment**
   - **Windows (PowerShell)**:
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   - **Windows (Command Prompt)**:
     ```cmd
     .venv\Scripts\activate
     ```
   - **macOS/Linux**:
     ```bash
     source .venv/bin/activate
     ```

4. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run Application**
   ```bash
   python app.py
   ```

6. **Access Application**
   - Open browser to `http://localhost:5000`
   - Flask default port: 5000

### Development Configuration

**In app.py:**
- `debug=True` - Auto-reload on file changes, detailed error pages
- `app.secret_key = 'quiz_app_secret_key'` - Change to secure random string in production

### File Preparation

Before first run:
1. Populate `data/quizzes.json` with quiz questions (reference JSON_SCHEMA.md)
2. Add any question images to `img/` folder
3. Database (`data/scores.db`) created automatically

### Troubleshooting Local Setup

| Issue | Solution |
|-------|----------|
| ModuleNotFoundError: Flask | Run `pip install -r requirements.txt` with venv activated |
| Port 5000 in use | Change port: `app.run(debug=True, port=5001)` |
| Images not loading | Check paths in quizzes.json match files in `img/` folder |
| Session not persisting | Ensure `app.secret_key` set; clear browser cookies |

## Docker Deployment

### Prerequisites
- Docker installed and running

### Build Docker Image

```bash
docker build -t quiz-app:latest .
```

**Dockerfile Reference:**
- Base image: `python:3.11-slim`
- Workdir: `/app`
- Exposes port: 5000
- Entrypoint: `python app.py`

### Run Container

```bash
docker run -p 5000:5000 quiz-app:latest
```

**Options:**
- `-p 5000:5000` - Map host port 5000 to container port 5000
- `-v $(pwd)/data:/app/data` - Mount local data volume (persistent scores)
- `-v $(pwd)/img:/app/img` - Mount local images volume
- `-d` - Run in detached mode (background)

### With Volume Mounts (Recommended)

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

### Docker Compose (Optional for Multi-Service Setup)

Create `docker-compose.yml`:
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
    environment:
      - FLASK_ENV=production
```

Run:
```bash
docker-compose up -d
```

### Container Cleanup

```bash
# Stop container
docker stop quiz-app

# Remove container
docker rm quiz-app

# Remove image
docker rmi quiz-app:latest
```

## Production Considerations

### Security

1. **Secret Key**: Use strong random string (use `secrets.token_hex()`)
   ```python
   import secrets
   app.secret_key = secrets.token_hex(32)
   ```

2. **Environment Variables**: Load from .env file
   ```python
   import os
   app.secret_key = os.getenv('SECRET_KEY', 'default-change-me')
   ```

3. **Session Configuration**:
   ```python
   app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
   app.config['SESSION_COOKIE_HTTPONLY'] = True  # No JavaScript access
   app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'  # CSRF protection
   ```

4. **CORS**: If deploying with separate frontend, add Flask-CORS

### Performance

1. **Database**: Switch to PostgreSQL/MySQL for scalability
2. **Caching**: Add Redis for session/quiz data caching
3. **Static Files**: Serve via CDN or nginx (not Flask)
4. **Load Balancing**: Use multiple app instances behind nginx/HAProxy

### Deployment Platform Options

- **Heroku**: `git push heroku main`
- **AWS EC2**: Deploy container or use Elastic Beanstalk
- **Azure**: App Service or Container Instances
- **DigitalOcean**: App Platform or Droplet
- **Kubernetes**: Use Helm charts for complex deployments

### Monitoring

- **Logs**: Redirect to stdout for container logging
- **Health Check**: Add `/health` route for monitoring
- **Metrics**: Integrate Prometheus for performance tracking

## Data Persistence

### Local Storage
- `data/scores.db` - SQLite database (persisted on disk)
- `data/quizzes.json` - Quiz data (persisted on disk)
- `img/` - Question images (persisted on disk)

### Docker Considerations
- Use volume mounts to persist data across container restarts
- Without volumes, data lost when container removed
- For production, use managed database services

## Scaling Strategy

1. **Single Container**: Development and small deployments
2. **Multi-Container**: Separate app, database, reverse proxy
3. **Kubernetes**: For enterprise-scale requirements
4. **Serverless**: Not recommended (sessions require persistence)