# 🎵 SUNIKFLOW - Audio Generation & Synthesis Platform

A production-ready audio generation and synthesis platform with a modern FastAPI backend and interactive web interface.

## 🚀 Features

- **FastAPI Backend** - High-performance REST + WebSocket API
- **Audio Synthesis** - Real-time audio generation and processing
- **Project Management** - Organize and manage audio projects
- **Library System** - Browse and manage generated tracks
- **Modern UI** - Interactive web interface with SUNIKFLOW design system
- **Docker Ready** - Production-ready containerization

## 📋 Prerequisites

- Python 3.9+
- `uv` package manager
- PostgreSQL (for production)

### Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## 🔧 Quick Start

### 1. Install Dependencies

```bash
uv sync
```

### 2. Set up Environment Variables

```bash
cp .env.example .env
```

### 3. Run the Backend

```bash
uv run python backend/main.py
```

The API will be available at `http://localhost:8000`
- API Docs: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 📁 Project Structure

```
sunikapp/
├── backend/
│   ├── main.py                 # FastAPI application entry point
│   ├── api/                    # API routes
│   ├── models/                 # SQLAlchemy models
│   ├── schemas/                # Pydantic schemas
│   ├── services/               # Business logic
│   │   ├── audio_synth.py     # Audio synthesis
│   │   ├── audio_effects.py   # Audio effects
│   │   ├── remix_service.py   # Remix functionality
│   │   └── export_service.py  # Export capabilities
│   ├── middleware/             # Custom middleware
│   ├── utils/                  # Utility functions
│   └── config.py              # Configuration
├── frontend/                   # Static web interface
│   ├── index.html             # Home page
│   ├── studio.html            # Audio studio
│   ├── library.html           # Track library
│   ├── projects.html          # Projects management
│   ├── settings.html          # User settings
│   ├── css/                   # Stylesheets
│   ├── js/                    # JavaScript modules
│   └── assets/                # Images and resources
├── docker/                     # Docker configuration
├── requirements.txt            # Python dependencies
├── pyproject.toml             # Project metadata
└── README.md                  # This file
```

## 🐳 Docker Deployment

### Development

```bash
docker-compose -f docker/compose.dev.yml up
```

### Production

```bash
docker-compose -f docker/compose.prod.yml up
```

## 📚 API Documentation

### Key Endpoints

- `GET /api/v1/health` - Health check
- `GET /api/v1/tracks` - List tracks
- `POST /api/v1/generate` - Generate audio
- `WS /ws/generate` - WebSocket for real-time generation

## 🎨 Design System

SUNIKFLOW uses a distinctive visual identity:
- **Primary Colors**: Purple (#7C3AED), Cyan (#06B6D4), Magenta (#EC4899)
- **Base**: Dark theme with light accents
- **Typography**: Modern, clean, and accessible

## 🛠️ Development

### Adding New Services

Create a new service in `backend/services/`:

```python
# backend/services/my_service.py
class MyService:
    def process(self, data):
        # Implementation
        pass
```

### Adding New API Routes

Create a router in `backend/api/`:

```python
# backend/api/my_routes.py
from fastapi import APIRouter

router = APIRouter(prefix="/my-endpoint", tags=["my-endpoint"])

@router.get("/")
async def get_data():
    return {"message": "Hello SUNIKFLOW"}
```

## 📝 Environment Variables

See `.env.example` for all available options:

```env
DATABASE_URL=postgresql://user:password@localhost/sunikapp
API_HOST=0.0.0.0
API_PORT=8000
ENVIRONMENT=development
```

## 🤝 Contributing

Contributions are welcome! Please follow the existing code structure and add tests for new features.

## 📄 License

Apache License 2.0 - See LICENSE file for details

## 🎯 Roadmap

- [ ] Complete backend API implementation
- [ ] Frontend UI refinement
- [ ] Audio effects library expansion
- [ ] User authentication system
- [ ] Advanced project sharing
- [ ] Real-time collaboration features

---

Made with ❤️ for audio creators
