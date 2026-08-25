# Carwager - Docker Setup Guide

## Prerequisites
- Docker (20.10+)
- Docker Compose (2.0+)

## Quick Start

### 1. Clone and Setup
```bash
cd carwager
cp .env.example .env
```

### 2. Build and Run
```bash
docker-compose up -d
```

This will:
- Start PostgreSQL (port 5432, internal only)
- Start Redis (port 6379, internal only)  
- Run Django/Daphne (port 8000, internal only)
- Start Nginx reverse proxy (port 80)
- Start RQ Worker
- Start RQ Scheduler

### 3. Create Database and Superuser
```bash
docker-compose exec django python manage.py createsuperuser
```

### 4. Access the Application
- **Main app**: http://localhost
- **Admin**: http://localhost/admin

**Note:** Application is now served through Nginx reverse proxy on port 80 (HTTP only).

## Useful Commands

### View logs
```bash
docker-compose logs -f django
docker-compose logs -f nginx
docker-compose logs -f worker
```

### Run management commands
```bash
docker-compose exec django python manage.py migrate
docker-compose exec django python manage.py createsuperuser
docker-compose exec django python manage.py shell
```

### Stop everything
```bash
docker-compose down
```

### Remove volumes (WARNING: deletes data)
```bash
docker-compose down -v
```

## Service Architecture

```
┌─────────────────┐
│  NGINX (80)     │  ← Public entry point
├─────────────────┤
│  Django (8000)  │  ← Daphne ASGI server
│  - WebSockets   │  ← Real-time chat via Channels
│  - REST API     │
├─────────────────┤
│  PostgreSQL     │  ← Database
│  Redis          │  ← Cache & Job Queue
├─────────────────┤
│  RQ Worker      │  ← Background jobs
│  RQ Scheduler   │  ← Scheduled tasks
└─────────────────┘
```

### Service Details

- **nginx** (nginx:alpine)
  - Reverse proxy for Django
  - Serves static files directly
  - Serves media files directly
  - Supports WebSocket upgrades
  - Port: 80 (public)

- **postgres** (postgres:15-alpine)
  - Main application database
  - Port: 5432 (internal only)
  - Data persists in `postgres_data` volume

- **redis** (redis:7-alpine)
  - Cache layer
  - Job queue backend (django-rq)
  - WebSocket channel layer (Channels)
  - Port: 6379 (internal only)

- **django** (built from Dockerfile)
  - Main Django application
  - Runs on Daphne (ASGI server)
  - Port: 8000 (internal only, accessed through Nginx)
  - Volumes:
    - `./carwager/:/app/` - Source code
    - `static_volume:/app/staticfiles` - Collected static files
    - `media_volume:/app/media` - User uploads

- **worker** (built from Dockerfile)
  - RQ worker for background jobs
  - Processes job queue from Redis

- **scheduler** (built from Dockerfile)
  - RQ scheduler for scheduled/recurring tasks
  - Manages job scheduling

## Environment Variables

All can be set in `.env` file:
- `DEBUG` - Enable debug mode (True/False) - Set to False in production
- `POSTGRES_NAME` - Database name (default: carwager)
- `POSTGRES_USER` - Database user (default: carwager)
- `POSTGRES_PASS` - Database password (default: carwager)
- `POSTGRES_HOST` - Database host (in Docker: "postgres")
- `REDIS_HOST` - Redis host (in Docker: "redis")

## Static Files and Media

### Static Files
- Location: `/app/staticfiles/`
- Collected by: `python manage.py collectstatic`
- Served by: Nginx (cached, 30 days)
- Django setting: `STATIC_ROOT = BASE_DIR / "staticfiles"`

### Media Files (Uploads)
- Location: `/app/media/`
- Served by: Nginx (cached, 7 days)
- Django setting: `MEDIA_ROOT = BASE_DIR / "media"`

Both are persisted in Docker volumes and shared between Django and Nginx containers.

## Nginx Configuration

The Nginx server:
1. **Listens on port 80** - HTTP only (no HTTPS in this setup)
2. **Routes /static/** - Directly serves static files (no Django involved)
3. **Routes /media/** - Directly serves media uploads
4. **Routes /* (everything else)** - Proxies to Django:8000
5. **Supports WebSockets** - Via Upgrade header forwarding

Configuration file: `./nginx.conf`

### Key Headers
```
X-Forwarded-For: Client IP (for security logs)
X-Forwarded-Proto: http (for Django to know it's proxied)
X-Real-IP: Original client IP
```

## Troubleshooting

### Port 80 already in use
Change the port mapping in docker-compose.yml:
```yaml
nginx:
  ports:
    - "8080:80"  # Access on http://localhost:8080
```

### Static files not showing
1. Ensure volume is properly mounted: `docker-compose logs nginx`
2. Run collectstatic: `docker-compose exec django python manage.py collectstatic`
3. Check Nginx logs: `docker-compose logs nginx`

### Django can't access static files
This is normal! Django doesn't serve static files in this setup - Nginx does.

### Database connection error
```bash
docker-compose logs django
# Check if postgres is healthy:
docker-compose ps
```

### Clear Docker resources
```bash
docker-compose down -v      # Remove volumes
docker system prune -a      # Remove unused images
docker volume prune         # Remove orphan volumes
```

### WebSocket connection failing
1. Check Redis is running: `docker-compose logs redis`
2. Check Nginx headers: `docker-compose logs nginx`
3. Check browser console for WebSocket errors
4. Verify `proxy_upgrade` headers in nginx.conf

## Production Checklist

For production deployment:
- [ ] Set `DEBUG=False` in `.env`
- [ ] Generate proper `SECRET_KEY` (use Django's get_random_secret_key())
- [ ] Set secure `ALLOWED_HOSTS` in settings.py
- [ ] Configure HTTPS/SSL on reverse proxy (external)
- [ ] Set environment-specific `CSRF_TRUSTED_ORIGINS`
- [ ] Use proper email backend for notifications
- [ ] Enable proper logging and monitoring
- [ ] Configure database backups
- [ ] Use health checks in production orchestration
- [ ] Implement rate limiting in Nginx
- [ ] Add gzip compression to Nginx config

## Development vs Production

### Development (current setup)
- `DEBUG=True` - Full error messages
- No HTTPS - HTTP only
- SQLite possible (but using PostgreSQL)
- Direct Django access (via Nginx proxy)

### Production (recommended changes)
- `DEBUG=False` - Error emails to admins
- HTTPS via reverse proxy (nginx on production server)
- PostgreSQL mandatory
- Redis for sessions/cache
- Gunicorn/Daphne via systemd or orchestration (K8s)
- Separate Nginx reverse proxy
- Monitoring & logging aggregation
- CDN for static files (optional)
