# Todo App Helm Chart

A comprehensive Helm chart for deploying the Todo App with Conversational AI on Kubernetes.

## Overview

This Helm chart deploys a full-stack todo application with three main components:

- **PostgreSQL Database**: Persistent data storage with automatic backups
- **FastAPI Backend**: REST API with OpenAI-powered conversational AI capabilities
- **Next.js Frontend**: Modern React-based UI with ChatKit integration

## Prerequisites

- Kubernetes 1.19+
- Helm 3.0+
- Minikube (for local development)
- NGINX Ingress Controller (for ingress support)
- Docker images built and available:
  - `todo-backend:latest`
  - `todo-frontend:latest`

## Quick Start

### 1. Build Docker Images

First, ensure your Docker images are built and available to your Kubernetes cluster:

```bash
# For Minikube, use the Minikube Docker daemon
eval $(minikube docker-env)

# Build backend image
cd backend
docker build -t todo-backend:latest .

# Build frontend image
cd ../frontend
docker build -t todo-frontend:latest .
```

### 2. Enable Ingress on Minikube

```bash
minikube addons enable ingress
```

### 3. Install the Chart

```bash
# Create namespace
kubectl create namespace todo-app

# Install the chart
helm install todo-app ./todo-helm --namespace todo-app
```

### 4. Configure /etc/hosts

Add the following entry to your `/etc/hosts` file:

```bash
echo "$(minikube ip) todo-app.local" | sudo tee -a /etc/hosts
```

### 5. Access the Application

Open your browser and navigate to:
- Frontend: http://todo-app.local
- Backend API: http://todo-app.local/api

## Configuration

### Required Configuration

Before deploying, update the following values in `values.yaml`:

#### Backend Secrets

```yaml
backend:
  secrets:
    JWT_SECRET: "your-super-secret-jwt-key-minimum-32-characters"
    OPENAI_API_KEY: "sk-your-openai-api-key-here"
    REDIS_URL: "redis://your-redis-host:6379"
```

#### Frontend Secrets

```yaml
frontend:
  secrets:
    BETTER_AUTH_SECRET: "your-super-secret-better-auth-key-minimum-32-characters"
```

#### Database Credentials

```yaml
database:
  auth:
    username: todouser
    password: change-this-strong-password
    database: todoapp
```

### Optional Configuration

#### Resource Limits

Adjust resource limits based on your cluster capacity:

```yaml
backend:
  resources:
    limits:
      cpu: 1000m
      memory: 1Gi
    requests:
      cpu: 500m
      memory: 512Mi
```

#### Autoscaling

Enable horizontal pod autoscaling:

```yaml
backend:
  autoscaling:
    enabled: true
    minReplicas: 2
    maxReplicas: 10
    targetCPUUtilizationPercentage: 70
```

#### Persistent Storage

Configure database storage:

```yaml
database:
  persistence:
    enabled: true
    storageClass: "standard"  # Use your storage class
    size: 10Gi
```

## Deployment Examples

### Development Deployment

```bash
helm install todo-app ./todo-helm \
  --namespace todo-app \
  --create-namespace \
  --set backend.image.tag=dev \
  --set frontend.image.tag=dev \
  --set database.persistence.size=5Gi
```

### Production Deployment

```bash
helm install todo-app ./todo-helm \
  --namespace todo-app-prod \
  --create-namespace \
  --values values-production.yaml
```

### Upgrade Deployment

```bash
helm upgrade todo-app ./todo-helm \
  --namespace todo-app \
  --reuse-values \
  --set backend.image.tag=v1.1.0
```

## Values Reference

### Global Settings

| Parameter | Description | Default |
|-----------|-------------|---------|
| `global.imagePullPolicy` | Default image pull policy | `IfNotPresent` |

### Database Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `database.enabled` | Enable PostgreSQL deployment | `true` |
| `database.image.repository` | PostgreSQL image | `postgres` |
| `database.image.tag` | PostgreSQL version | `16-alpine` |
| `database.service.port` | Database service port | `5432` |
| `database.auth.username` | Database username | `todouser` |
| `database.auth.password` | Database password | `todopass` |
| `database.auth.database` | Database name | `todoapp` |
| `database.persistence.enabled` | Enable persistent storage | `true` |
| `database.persistence.size` | Storage size | `5Gi` |

### Backend Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `backend.enabled` | Enable backend deployment | `true` |
| `backend.image.repository` | Backend image | `todo-backend` |
| `backend.image.tag` | Backend version | `latest` |
| `backend.service.port` | Backend service port | `8000` |
| `backend.replicaCount` | Number of replicas | `1` |
| `backend.env.AI_MODEL` | OpenAI model | `gpt-4-turbo` |
| `backend.env.RATE_LIMIT_REQUESTS_PER_MINUTE` | API rate limit | `10` |

### Frontend Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `frontend.enabled` | Enable frontend deployment | `true` |
| `frontend.image.repository` | Frontend image | `todo-frontend` |
| `frontend.image.tag` | Frontend version | `latest` |
| `frontend.service.port` | Frontend service port | `3000` |
| `frontend.replicaCount` | Number of replicas | `1` |

### Ingress Configuration

| Parameter | Description | Default |
|-----------|-------------|---------|
| `ingress.enabled` | Enable ingress | `true` |
| `ingress.className` | Ingress class | `nginx` |
| `ingress.frontend.host` | Frontend hostname | `todo-app.local` |
| `ingress.backend.path` | Backend API path | `/api` |

## Monitoring and Troubleshooting

### Check Pod Status

```bash
kubectl get pods -n todo-app
```

### View Logs

```bash
# Backend logs
kubectl logs -n todo-app -l app.kubernetes.io/name=todo-app-backend -f

# Frontend logs
kubectl logs -n todo-app -l app.kubernetes.io/name=todo-app-frontend -f

# Database logs
kubectl logs -n todo-app -l app.kubernetes.io/name=todo-app-database -f
```

### Access Services Locally (without Ingress)

```bash
# Frontend
kubectl port-forward -n todo-app svc/todo-app-frontend 3000:3000

# Backend
kubectl port-forward -n todo-app svc/todo-app-backend 8000:8000

# Database
kubectl port-forward -n todo-app svc/todo-app-database 5432:5432
```

### Check Ingress

```bash
kubectl get ingress -n todo-app
kubectl describe ingress -n todo-app
```

### Verify ConfigMaps and Secrets

```bash
kubectl get configmap -n todo-app
kubectl get secret -n todo-app
```

## Uninstalling

```bash
helm uninstall todo-app --namespace todo-app
```

To delete the namespace and all resources:

```bash
kubectl delete namespace todo-app
```

## Security Considerations

1. **Never commit sensitive values**: Use external secret management (e.g., Sealed Secrets, External Secrets Operator)
2. **Update default passwords**: Change all default passwords before production deployment
3. **Enable TLS**: Configure TLS certificates for production ingress
4. **Network Policies**: Implement network policies to restrict pod communication
5. **RBAC**: Configure appropriate RBAC rules for service accounts

## Production Checklist

- [ ] Update all secrets and passwords
- [ ] Configure TLS certificates
- [ ] Set appropriate resource limits and requests
- [ ] Enable autoscaling based on load testing
- [ ] Configure monitoring and alerting
- [ ] Set up backup strategy for database
- [ ] Enable network policies
- [ ] Review and harden security settings
- [ ] Test disaster recovery procedures
- [ ] Document runbooks for common operations

## Support

For issues and questions:
- GitHub Issues: https://github.com/yourusername/todo-app/issues
- Documentation: https://github.com/yourusername/todo-app/docs

## License

[Your License Here]
