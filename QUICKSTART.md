# SUNIKFLOW - Quick Start Guide

## 🚀 Get Started in 5 Minutes

### Option 1: Local Development (Easiest)

#### Prerequisites
- Python 3.9 or higher
- Git

#### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/darcko2/Sunikapp.git
   cd Sunikapp
   ```

2. **Install uv package manager**
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

3. **Sync dependencies**
   ```bash
   uv sync
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   ```

5. **Run the application**
   ```bash
   uv run python -m uvicorn backend.main:app --reload
   ```

6. **Open in browser**
   - **Frontend**: http://localhost:8000
   - **API Docs**: http://localhost:8000/docs
   - **Alternative Docs**: http://localhost:8000/redoc

✅ **Done!** You're now running SUNIKFLOW locally.

---

### Option 2: Docker Compose (Recommended for Production)

#### Prerequisites
- Docker
- Docker Compose

#### Development Environment

```bash
# Clone the repository
git clone https://github.com/darcko2/Sunikapp.git
cd Sunikapp

# Start services
docker-compose -f docker-compose.yml up
```

Access at: http://localhost:8000

#### Production Environment

```bash
# Configure production environment
cp .env.example .env.production
# Edit .env.production with your production settings

# Start production services
docker-compose -f docker/compose.prod.yml up -d
```

Access at: http://localhost (or your domain)

---

## 📚 Project Structure

```
Sunikapp/
├── backend/              # Python FastAPI application
│   ├── main.py          # Application entry point
│   ├── config.py        # Configuration
│   ├── models.py        # Database models
│   ├── schemas.py       # Pydantic schemas
│   ├── api/             # API routes
│   ├── services/        # Business logic
│   │   ├── audio_synth.py
│   │   ├── audio_effects.py
│   │   ├── mixer_service.py
│   │   └── export_service.py
│   └── database.py      # Database setup
├── frontend/            # Web interface
│   ├── index.html       # Home page
│   ├── studio.html      # Audio studio
│   ├── library.html     # Track library
│   ├── projects.html    # Project management
│   ├── settings.html    # User settings
│   ├── css/             # Stylesheets
│   └── js/              # JavaScript
├── docker/              # Docker configuration
│   ├── Dockerfile.dev
│   ├── Dockerfile.prod
│   ├── nginx.conf
│   └── compose.prod.yml
├── requirements.txt     # Python dependencies
├── pyproject.toml       # Project metadata
├── README.md            # Main documentation
├── ARCHITECTURE.md      # Architecture details
├── API.md               # API documentation
├── DEPLOYMENT.md        # Deployment guide
└── CONTRIBUTING.md      # Contribution guidelines
```

---

## 🎯 What You Can Do

### In the Studio
- 🎚️ **Generate audio** with adjustable frequency and duration
- 🎛️ **Apply effects** like reverb and delay
- 📊 **View waveforms** and spectrum analysis
- 🎵 **Mix multiple tracks** together
- 💾 **Export as** WAV, MP3, or FLAC

### In the Library
- 📂 **Browse all tracks** you've created
- 🔍 **Search and filter** by name or project
- 📥 **Download** your audio files
- 🎧 **Preview** tracks before download

### Project Management
- 📋 **Create projects** to organize your work
- 🏷️ **Tag and categorize** tracks
- 📝 **Add descriptions** for reference
- 🗑️ **Delete** old projects

---

## 🛠️ Common Tasks

### Generate a Simple Audio Tone

1. Go to http://localhost:8000/studio.html
2. Set frequency to 440 Hz (A note)
3. Set duration to 5 seconds
4. Click "Generate"
5. Click "Export WAV" to download

### Add Effects to Audio

1. Generate audio (steps above)
2. Adjust the "Reverb" slider (0-100)
3. Adjust the "Delay" slider (0-100)
4. Export the result

### Create a New Project

1. Go to http://localhost:8000/projects.html
2. Click "+New Project"
3. Enter project name
4. Create tracks within the project

---

## 🔧 Configuration

### Environment Variables (.env)

```env
# Database
DATABASE_URL=sqlite:///./sunikapp.db

# API
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true

# Audio
SAMPLE_RATE=44100
BIT_DEPTH=16

# Environment
ENVIRONMENT=development
DEBUG=true
```

### Change Database

For **PostgreSQL**:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/sunikapp
```

For **SQLite** (default):
```env
DATABASE_URL=sqlite:///./sunikapp.db
```

---

## 📖 API Examples

### Health Check
```bash
curl http://localhost:8000/api/v1/health
```

### Generate Audio (WebSocket)
```javascript
const ws = new WebSocket('ws://localhost:8000/ws/generate');

ws.onopen = () => {
  ws.send(JSON.stringify({
    frequency: 440,
    duration: 5,
    type: 'sine'
  }));
};

ws.onmessage = (event) => {
  console.log('Server:', event.data);
};
```

---

## 🐛 Troubleshooting

### Port 8000 Already in Use
```bash
# Kill the process using port 8000
lsof -i :8000
kill -9 <PID>

# Or use a different port
uv run python -m uvicorn backend.main:app --port 8001 --reload
```

### Database Connection Error
```bash
# Make sure .env is configured correctly
cat .env

# Reset database (SQLite)
rm sunikapp.db
```

### Module Not Found
```bash
# Resync dependencies
uv sync
```

### WebSocket Connection Refused
- Make sure the API server is running
- Check firewall settings
- Verify the correct URL

---

## 📚 Next Steps

1. **Read the Documentation**
   - [Architecture Guide](ARCHITECTURE.md)
   - [API Documentation](API.md)
   - [Deployment Guide](DEPLOYMENT.md)

2. **Explore the Code**
   - Check out `backend/services/` for audio processing
   - Look at `frontend/js/` for frontend logic
   - Review `backend/main.py` for API structure

3. **Try Advanced Features**
   - Create multiple tracks
   - Mix them together
   - Apply different effects
   - Export in different formats

4. **Contribute**
   - Check [Contributing Guide](CONTRIBUTING.md)
   - Review [TODO List](TODO.md) for tasks
   - Open issues for bugs or features

---

## 🆘 Getting Help

- 📖 Check the [Documentation](README.md)
- 🐛 Open an [Issue on GitHub](https://github.com/darcko2/Sunikapp/issues)
- 💬 Start a [Discussion](https://github.com/darcko2/Sunikapp/discussions)
- 📧 Contact the development team

---

## 🎉 You're Ready!

You now have SUNIKFLOW running on your machine. Start creating amazing audio! 🎵

**Happy Creating!** 🚀
