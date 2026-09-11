# SUNIKFLOW Deployment Guide

## Local Development

### Prerequisites
- Python 3.9+
- uv package manager
- PostgreSQL (optional, SQLite works for development)

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/darcko2/Sunikapp.git
   cd Sunikapp
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   ```

4. **Initialize database**
   ```bash
   python -m backend.database
   ```

5. **Run the application**
   ```bash
   python -m uvicorn backend.main:app --reload
   ```

The application will be available at `http://localhost:8000`

## Docker Deployment

### Development with Docker Compose

```bash
docker-compose -f docker-compose.yml up
```

This starts:
- API server on port 8000
- Frontend on port 3000 (Nginx)

### Production with Docker Compose

1. **Set up environment**
   ```bash
   cp .env.example .env.production
   # Edit .env.production with production values
   ```

2. **Start services**
   ```bash
   docker-compose -f docker/compose.prod.yml up -d
   ```

This starts:
- API server (internal port 8000)
- PostgreSQL database
- Nginx reverse proxy (ports 80, 443)

## Cloud Deployment

### Heroku

1. **Install Heroku CLI**
   ```bash
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login and create app**
   ```bash
   heroku login
   heroku create sunikflow-app
   ```

3. **Add PostgreSQL**
   ```bash
   heroku addons:create heroku-postgresql:hobby-dev
   ```

4. **Deploy**
   ```bash
   git push heroku main
   ```

### AWS with Docker

1. **Push to ECR**
   ```bash
   aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com
   docker build -t sunikflow .
   docker tag sunikflow:latest YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/sunikflow:latest
   docker push YOUR_ACCOUNT.dkr.ecr.us-east-1.amazonaws.com/sunikflow:latest
   ```

2. **Deploy with ECS**
   - Create ECS cluster
   - Create task definition with ECR image
   - Create service with load balancer

### Google Cloud Run

1. **Build and push**
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT/sunikflow
   ```

2. **Deploy**
   ```bash
   gcloud run deploy sunikflow --image gcr.io/YOUR_PROJECT/sunikflow --platform managed --region us-central1
   ```

## SSL/TLS Configuration

### With Let's Encrypt

1. **Install Certbot**
   ```bash
   sudo apt-get install certbot python3-certbot-nginx
   ```

2. **Obtain certificate**
   ```bash
   sudo certbot certonly --standalone -d yourdomain.com
   ```

3. **Update Nginx configuration**
   - Point to certificate and key paths
   - Enable HTTPS redirect

## Database Backups

### PostgreSQL Backup

```bash
# Full backup
pg_dump -U sunikapp -h localhost sunikapp > backup.sql

# Restore
psql -U sunikapp -h localhost sunikapp < backup.sql
```

### Automated Backups

```bash
# Create backup script
#!/bin/bash
BACKUP_DIR="/backups"
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump -U sunikapp -h localhost sunikapp > $BACKUP_DIR/backup_$DATE.sql

# Add to crontab
0 2 * * * /path/to/backup_script.sh  # Daily at 2 AM
```

## Monitoring

### Application Health

```bash
curl http://localhost:8000/health
```

### Logging

```bash
# View logs
docker-compose logs -f api

# Or with journalctl (systemd)
journalctl -u sunikflow -f
```

### Performance Monitoring

- Use Prometheus for metrics
- Set up Grafana dashboards
- Monitor CPU, memory, disk usage
- Track API response times

## Security Checklist

- [ ] Change default database credentials
- [ ] Set strong API secrets
- [ ] Enable HTTPS/TLS
- [ ] Configure CORS properly
- [ ] Set up rate limiting
- [ ] Enable authentication/authorization
- [ ] Regular security updates
- [ ] Database encryption at rest
- [ ] Secure API keys management
- [ ] Regular backups with verification

## Troubleshooting

### Database connection issues
```bash
# Test connection
psql -U sunikapp -h localhost -d sunikapp -c "SELECT 1"
```

### Port already in use
```bash
# Find and kill process
lsof -i :8000
kill -9 <PID>
```

### Memory issues
```bash
# Check usage
free -h
docker stats
```

## Performance Optimization

1. **Database optimization**
   - Add indexes to frequently queried columns
   - Regular VACUUM and ANALYZE

2. **Caching**
   - Implement Redis for session caching
   - Cache frequently accessed data

3. **CDN**
   - Use CloudFlare or Akamai for static files
   - Distribute content globally

4. **Load balancing**
   - Run multiple API instances
   - Use Nginx/HAProxy for load balancing

## Updates and Maintenance

```bash
# Pull latest code
git pull origin main

# Update dependencies
uv sync

# Restart services
docker-compose restart
```

## Support

For deployment issues, please open an issue on GitHub or contact the development team.
