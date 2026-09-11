# SUNIKFLOW Architecture

## Overview

SUNIKFLOW is a modern audio generation and synthesis platform built with:
- **Backend**: FastAPI + SQLAlchemy + PostgreSQL
- **Frontend**: HTML5 + CSS3 + Vanilla JavaScript
- **Audio**: NumPy + SciPy for signal processing

## Project Structure

```
sunikapp/
├── backend/                 # Python FastAPI application
│   ├── main.py             # Application entry point
│   ├── config.py           # Configuration management
│   ├── models.py           # SQLAlchemy ORM models
│   ├── schemas.py          # Pydantic validation schemas
│   ├── api/                # REST API routes
│   │   ├── health.py       # Health check endpoints
│   │   ├── users.py        # User management
│   │   ├── projects.py     # Project management
│   │   ├── tracks.py       # Track management
│   │   └── generate.py     # Audio generation
│   ├── services/           # Business logic
│   │   ├── audio_synth.py  # Audio synthesis
│   │   ├── audio_effects.py# Audio effects
│   │   ├── mixer_service.py# Track mixing
│   │   ├── export_service.py# Export functionality
│   │   └── analysis_service.py# Audio analysis
│   ├── middleware/         # Custom middleware
│   └── utils/              # Utility functions
├── frontend/               # Web interface
│   ├── index.html          # Home page
│   ├── studio.html         # Audio studio
│   ├── library.html        # Track library
│   ├── projects.html       # Projects
│   ├── settings.html       # User settings
│   ├── css/                # Stylesheets
│   ├── js/                 # JavaScript modules
│   └── assets/             # Images/resources
├── docker/                 # Docker configuration
│   ├── Dockerfile.dev      # Development image
│   ├── Dockerfile.prod     # Production image
│   ├── nginx.conf          # Nginx configuration
│   └── compose.*           # Docker Compose files
└── tests/                  # Test suite
```

## Database Schema

### Users Table
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email
- `created_at`, `updated_at`: Timestamps

### Projects Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `name`: Project name
- `description`: Project description
- `created_at`, `updated_at`: Timestamps

### Tracks Table
- `id`: Primary key
- `user_id`: Foreign key to users
- `project_id`: Foreign key to projects (optional)
- `title`: Track title
- `duration`: Track duration in seconds
- `file_path`: Path to audio file
- `created_at`, `updated_at`: Timestamps

### Generations Table
- `id`: Primary key
- `track_id`: Foreign key to tracks
- `prompt`: Generation prompt/parameters
- `status`: pending/processing/completed/failed
- `output_file`: Path to generated audio
- `created_at`, `updated_at`: Timestamps

### Presets Table
- `id`: Primary key
- `name`: Preset name
- `description`: Preset description
- `config`: JSON configuration
- `is_default`: Default preset flag
- `created_at`, `updated_at`: Timestamps

## API Endpoints

### Health
- `GET /health` - Basic health check
- `GET /api/v1/health` - API health status

### Users (Planned)
- `POST /api/v1/users` - Create user
- `GET /api/v1/users/{id}` - Get user
- `PUT /api/v1/users/{id}` - Update user
- `DELETE /api/v1/users/{id}` - Delete user

### Projects (Planned)
- `GET /api/v1/projects` - List projects
- `POST /api/v1/projects` - Create project
- `GET /api/v1/projects/{id}` - Get project
- `PUT /api/v1/projects/{id}` - Update project
- `DELETE /api/v1/projects/{id}` - Delete project

### Tracks (Planned)
- `GET /api/v1/tracks` - List tracks
- `POST /api/v1/tracks` - Create track
- `GET /api/v1/tracks/{id}` - Get track
- `PUT /api/v1/tracks/{id}` - Update track
- `DELETE /api/v1/tracks/{id}` - Delete track

### Audio Generation (Planned)
- `POST /api/v1/generate` - Trigger generation
- `GET /api/v1/generate/{id}` - Get generation status
- `WS /ws/generate` - WebSocket for real-time generation

## Audio Services

### AudioSynthesisService
Core audio generation capabilities:
- Sine wave generation
- Chord generation
- ADSR envelope application
- Frequency-based synthesis

### AudioEffectsService
Audio processing effects:
- Reverb
- Delay
- Parametric EQ
- Dynamic range compression

### MixerService
Track mixing and combining:
- Multi-track mixing
- Volume adjustment
- Pan control
- Level normalization

### ExportService
Audio file export:
- WAV export
- Raw audio export
- Audio metadata extraction
- Format conversion (planned)

## Design System

### Color Palette
- **Primary**: Purple (#7C3AED)
- **Secondary**: Cyan (#06B6D4)
- **Accent**: Magenta (#EC4899)
- **Background**: Dark (#0F172A)
- **Surface**: Dark Gray (#1E293B)

### Typography
- **Headlines**: Inter Bold
- **Body**: Inter Regular
- **Code**: JetBrains Mono

## Development Setup

1. Clone the repository
2. Install Python 3.9+
3. Install uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
4. Sync dependencies: `uv sync`
5. Copy .env.example to .env
6. Run: `uv run python backend/main.py`

## Deployment

### Docker Compose (Development)
```bash
docker-compose -f docker-compose.yml up
```

### Docker Compose (Production)
```bash
docker-compose -f docker/compose.prod.yml up -d
```

## Performance Considerations

- Audio processing uses NumPy for efficient computation
- Database queries are optimized with proper indexing
- WebSocket connections for real-time updates
- Async/await throughout for concurrency
- Static file caching in production

## Security

- CORS configuration in production
- Environment variables for secrets
- SQL injection prevention through ORM
- Input validation with Pydantic
- Rate limiting (planned)
- JWT authentication (planned)

## Future Enhancements

- [ ] Machine learning models for audio generation
- [ ] Real-time collaboration
- [ ] Advanced audio analysis
- [ ] Plugin system for custom effects
- [ ] Cloud storage integration
- [ ] Mobile application
- [ ] Community sharing features
