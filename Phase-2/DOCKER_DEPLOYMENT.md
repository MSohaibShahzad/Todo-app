# Docker Deployment Guide

Complete guide to deploy the Todo App using Docker and Docker Compose.

## Prerequisites

- Docker (version 20.10 or later)
- Docker Compose (version 2.0 or later)
- At least 2GB of free disk space

## Quick Start (Development)

### 1. Setup Environment Variables

```bash
cd Phase-2

# Create environment file
cp .env.docker.example .env.docker

# Edit and add your secrets (IMPORTANT!)
nano .env.docker  # or use your preferred editor
```

**Important**: Change the default secrets in `.env.docker`:
- `JWT_SECRET`: Random string (min 32 characters)
- `BETTER_AUTH_SECRET`: Random string (min 32 characters)

### 2. Build and Start All Services

```bash
# Build and start in detached mode
docker-compose up -d --build

# View logs
docker-compose logs -f

# Or view specific service logs
docker-compose logs -f backend
docker-compose logs -f frontend
```

### 3. Access the Application

Once all services are running:

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432

### 4. Create Your Account

1. Open http://localhost:3000
2. Click "Sign Up"
3. Create your account
4. Start managing your tasks!

## Service Architecture

```
┌─────────────────────────────────────────────┐
│  Frontend (Next.js)                         │
│  Port: 3000                                 │
│  Container: todo-frontend                   │
└──────────────┬──────────────────────────────┘
               │ HTTP API Calls
┌──────────────▼──────────────────────────────┐
│  Backend (FastAPI)                          │
│  Port: 8000                                 │
│  Container: todo-backend                    │
└──────────────┬──────────────────────────────┘
               │ Database Queries
┌──────────────▼──────────────────────────────┐
│  Database (PostgreSQL)                      │
│  Port: 5432                                 │
│  Container: todo-db                         │
└─────────────────────────────────────────────┘
```

## Docker Commands

### Start Services
```bash
# Start all services
docker-compose up -d

# Start specific service
docker-compose up -d backend
```

### Stop Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes (deletes data!)
docker-compose down -v
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f db

# Last 100 lines
docker-compose logs --tail=100 backend
```

### Restart Services
```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart backend
```

### Rebuild Services
```bash
# Rebuild and restart (after code changes)
docker-compose up -d --build

# Rebuild specific service
docker-compose up -d --build backend
```

### Execute Commands in Containers
```bash
# Backend shell
docker-compose exec backend sh

# Run migrations manually
docker-compose exec backend uv run alembic upgrade head

# Check database
docker-compose exec db psql -U todouser -d todoapp

# Frontend shell
docker-compose exec frontend sh
```

## Health Checks

The services include health checks:

```bash
# Check service status
docker-compose ps

# Backend health endpoint
curl http://localhost:8000/api/v1/health

# Database health
docker-compose exec db pg_isready -U todouser
```

## Troubleshooting

### Services Won't Start

```bash
# Check logs for errors
docker-compose logs

# Check if ports are already in use
netstat -an | grep 3000
netstat -an | grep 8000
netstat -an | grep 5432

# Stop conflicting services
lsof -ti:3000 | xargs kill -9
```

### Database Connection Issues

```bash
# Check database is running
docker-compose ps db

# Check database logs
docker-compose logs db

# Verify connection
docker-compose exec db psql -U todouser -d todoapp -c '\l'
```

### Backend API Not Responding

```bash
# Check backend logs
docker-compose logs backend

# Verify migrations ran
docker-compose exec backend uv run alembic current

# Run migrations manually
docker-compose exec backend uv run alembic upgrade head
```

### Frontend Build Failures

```bash
# Check frontend logs
docker-compose logs frontend

# Rebuild with no cache
docker-compose build --no-cache frontend
docker-compose up -d frontend
```

### Clear Everything and Start Fresh

```bash
# Stop all services and remove volumes
docker-compose down -v

# Remove images
docker-compose down --rmi all

# Rebuild and start
docker-compose up -d --build
```

## Production Deployment

### Security Considerations

1. **Change Default Secrets**
   - Generate strong random secrets for `JWT_SECRET` and `BETTER_AUTH_SECRET`
   - Use at least 32 characters

2. **Database Security**
   - Change default database credentials
   - Don't expose PostgreSQL port (5432) publicly
   - Use Docker secrets or environment variable encryption

3. **HTTPS/TLS**
   - Use a reverse proxy (Nginx, Traefik, Caddy)
   - Configure SSL certificates
   - Redirect HTTP to HTTPS

4. **Environment Variables**
   - Never commit `.env.docker` to version control
   - Use Docker secrets or cloud provider secret management

### Example Production Setup with Nginx

```yaml
# Add to docker-compose.yml
nginx:
  image: nginx:alpine
  ports:
    - "80:80"
    - "443:443"
  volumes:
    - ./nginx.conf:/etc/nginx/nginx.conf:ro
    - ./ssl:/etc/nginx/ssl:ro
  depends_on:
    - frontend
    - backend
  networks:
    - todo-network
```

## Performance Optimization

### Build Optimization
```bash
# Multi-stage builds reduce image size
# Frontend: ~200MB (vs 1GB+ without optimization)
# Backend: ~300MB

# Check image sizes
docker images | grep todo
```

### Resource Limits
```yaml
# Add to docker-compose.yml under each service
deploy:
  resources:
    limits:
      cpus: '0.5'
      memory: 512M
```

## Backup and Restore

### Backup Database
```bash
# Create backup
docker-compose exec db pg_dump -U todouser todoapp > backup.sql

# Or with timestamp
docker-compose exec db pg_dump -U todouser todoapp > backup_$(date +%Y%m%d_%H%M%S).sql
```

### Restore Database
```bash
# Restore from backup
cat backup.sql | docker-compose exec -T db psql -U todouser -d todoapp
```

### Backup Docker Volumes
```bash
# Backup postgres data volume
docker run --rm -v phase-2_postgres_data:/data -v $(pwd):/backup alpine tar czf /backup/postgres_backup.tar.gz -C /data .
```

## Monitoring

### Check Resource Usage
```bash
# Container stats
docker stats

# Specific service
docker stats todo-backend todo-frontend todo-db
```

### Log Management
```bash
# Limit log size in docker-compose.yml
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"
```

## Updating the Application

```bash
# 1. Pull latest code
git pull

# 2. Rebuild containers
docker-compose up -d --build

# 3. Run migrations (if any)
docker-compose exec backend uv run alembic upgrade head

# 4. Verify services
docker-compose ps
```

## Environment Variables Reference

### Backend Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Set in docker-compose |
| `JWT_SECRET` | Secret key for JWT tokens | **REQUIRED** |
| `JWT_ALGORITHM` | JWT algorithm | HS256 |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry | 1440 (24h) |
| `FRONTEND_URL` | Frontend URL for CORS | http://localhost:3000 |
| `ENVIRONMENT` | Environment mode | production |

### Frontend Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Public API URL | http://localhost:8000 |
| `NEXT_PUBLIC_BACKEND_URL` | Internal backend URL | http://backend:8000 |
| `DATABASE_URL` | Database URL for Better Auth | Set in docker-compose |
| `BETTER_AUTH_SECRET` | Better Auth secret key | **REQUIRED** |
| `BETTER_AUTH_URL` | Better Auth URL | http://localhost:3000 |
| `NODE_ENV` | Node environment | production |

## Support

For issues or questions:
1. Check logs: `docker-compose logs -f`
2. Verify health: `docker-compose ps`
3. Review this guide's troubleshooting section
4. Check individual service README files

---

**Note**: This setup is optimized for development and small-scale production. For large-scale production deployments, consider:
- Kubernetes for orchestration
- Managed database services (AWS RDS, Google Cloud SQL, etc.)
- CDN for frontend assets
- Load balancing for multiple backend instances
- Centralized logging (ELK stack, Grafana)
- Monitoring (Prometheus, Datadog)
