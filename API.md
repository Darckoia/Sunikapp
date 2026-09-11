# SUNIKFLOW API Documentation

## Base URL
```
http://localhost:8000
http://your-domain.com  # Production
```

## Authentication

Currently, the API is open. Authentication will be added in a future release.

## Response Format

All responses are in JSON format:

```json
{
  "status": "success",
  "data": {},
  "error": null
}
```

## Endpoints

### Health Check

#### Check API Status
```
GET /health
GET /api/v1/health
```

**Response:**
```json
{
  "status": "ok",
  "service": "SUNIKFLOW API",
  "version": "1.0.0"
}
```

### Users (Planned)

#### Create User
```
POST /api/v1/users
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "secure_password"
}
```

#### Get User
```
GET /api/v1/users/{user_id}
```

#### Update User
```
PUT /api/v1/users/{user_id}
Content-Type: application/json

{
  "username": "new_username",
  "email": "newemail@example.com"
}
```

#### Delete User
```
DELETE /api/v1/users/{user_id}
```

### Projects (Planned)

#### List Projects
```
GET /api/v1/projects
```

#### Create Project
```
POST /api/v1/projects
Content-Type: application/json

{
  "name": "My Project",
  "description": "Project description"
}
```

#### Get Project
```
GET /api/v1/projects/{project_id}
```

#### Update Project
```
PUT /api/v1/projects/{project_id}
Content-Type: application/json

{
  "name": "Updated Name",
  "description": "Updated description"
}
```

#### Delete Project
```
DELETE /api/v1/projects/{project_id}
```

### Tracks (Planned)

#### List Tracks
```
GET /api/v1/tracks
```

**Query Parameters:**
- `project_id` - Filter by project
- `skip` - Pagination offset
- `limit` - Pagination limit

#### Create Track
```
POST /api/v1/tracks
Content-Type: application/json

{
  "title": "Track Title",
  "project_id": 1,
  "duration": 120
}
```

#### Get Track
```
GET /api/v1/tracks/{track_id}
```

#### Update Track
```
PUT /api/v1/tracks/{track_id}
Content-Type: application/json

{
  "title": "Updated Title"
}
```

#### Delete Track
```
DELETE /api/v1/tracks/{track_id}
```

### Audio Generation (Planned)

#### Generate Audio
```
POST /api/v1/generate
Content-Type: application/json

{
  "track_id": 1,
  "prompt": "Generate a sine wave",
  "frequency": 440,
  "duration": 5
}
```

#### Get Generation Status
```
GET /api/v1/generate/{generation_id}
```

### WebSocket - Real-time Generation

```
WS /ws/generate
```

**Send:**
```json
{
  "track_id": 1,
  "action": "generate",
  "parameters": {
    "frequency": 440,
    "duration": 5
  }
}
```

**Receive:**
```json
{
  "status": "processing",
  "progress": 50,
  "data": {...}
}
```

## Error Responses

### 400 Bad Request
```json
{
  "status": "error",
  "error": "Invalid request parameters",
  "details": {...}
}
```

### 404 Not Found
```json
{
  "status": "error",
  "error": "Resource not found"
}
```

### 500 Internal Server Error
```json
{
  "status": "error",
  "error": "Internal server error",
  "message": "Error details"
}
```

## Rate Limiting

Rate limiting will be implemented in future releases:
- 100 requests per minute per IP
- 1000 requests per hour per user

## Pagination

List endpoints support pagination:

```
GET /api/v1/tracks?skip=0&limit=20
```

**Response:**
```json
{
  "items": [...],
  "total": 100,
  "skip": 0,
  "limit": 20
}
```

## Filtering and Sorting

```
GET /api/v1/tracks?project_id=1&sort=created&order=desc
```

## Interactive Documentation

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## SDK/Libraries

Python client library coming soon!

## Changelog

### v1.0.0
- Initial API release
- Health check endpoints
- Database models defined
- Frontend interface created

### v1.1.0 (Planned)
- User authentication
- Full CRUD operations
- Real-time updates via WebSocket
- Audio generation endpoints

## Support

For API support, please open an issue on GitHub or check the documentation at https://sunikflow.com/docs
