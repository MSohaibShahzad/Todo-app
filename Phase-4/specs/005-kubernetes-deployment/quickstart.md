# Quickstart: Kubernetes/Helm Deployment

**Feature**: 005-kubernetes-deployment
**Date**: 2026-02-05
**Target Audience**: Developers deploying Todo App to local Kubernetes

## Overview

This quickstart guide walks through deploying the full-stack Todo App (with conversational AI) to a local Minikube cluster using Helm charts. By the end, you'll have a production-like Kubernetes deployment running locally.

**Time Estimate**: 30-45 minutes for first-time deployment

## Prerequisites

✅ **Required Software**:
- Minikube 1.25+ installed
- Helm 3.0+ installed
- kubectl installed and configured
- Docker installed
- 4+ CPU cores and 8+ GB RAM available

✅ **Required Credentials**:
- OpenAI API key (for conversational AI features)
- Generated secrets (JWT_SECRET, BETTER_AUTH_SECRET)

✅ **Application State**:
- Phase III conversational AI implementation complete
- Backend and frontend Dockerfiles working
- Backend health endpoint (`/api/v1/health`) implemented

## Architecture Quick View

```
┌─────────────────────────────────────────────────┐
│             Ingress (todo-app.local)            │
│   / → Frontend (3000)  |  /api/* → Backend (8000)
└────────────────┬────────────────────────────────┘
                 │
        ┌────────┴─────────┐
        ↓                   ↓
┌──────────────┐    ┌──────────────┐
│  Frontend    │    │  Backend     │
│  (Next.js)   │    │  (FastAPI)   │
│  ClusterIP   │    │  ClusterIP   │
└──────┬───────┘    └───────┬──────┘
       │                    │
       └────────┬───────────┘
                ↓
        ┌──────────────┐
        │  Database    │
        │ (PostgreSQL) │
        │  ClusterIP   │
        └──────┬───────┘
               │
        ┌──────┴───────┐
        │     PVC      │
        │   (5Gi)      │
        └──────────────┘
```

## Quick Deploy (5 Steps)

### Step 1: Start Minikube (5 minutes)

```bash
# Start Minikube with sufficient resources
minikube start --cpus=4 --memory=8192 --driver=docker

# Enable Ingress addon (required for single-hostname access)
minikube addons enable ingress

# Verify ingress controller is running
kubectl get pods -n ingress-nginx
```

**✅ Checkpoint**: Ingress controller pods show `Running` status

---

### Step 2: Build and Load Images (10 minutes)

```bash
# Configure Docker to use Minikube's daemon
eval $(minikube docker-env)

# Navigate to Phase-4 directory
cd /home/sohaib/hackathon2/Todo-app/Phase-4

# Build backend image
cd backend
docker build -t todo-backend:latest .
cd ..

# Build frontend image
cd frontend
docker build -t todo-frontend:latest .
cd ..

# Verify images are available in Minikube
docker images | grep todo
```

**✅ Checkpoint**: Both `todo-backend:latest` and `todo-frontend:latest` appear in output

---

### Step 3: Configure Secrets (5 minutes)

**CRITICAL**: Edit `todo-helm/values.yaml` and update the following secrets:

```yaml
# Backend secrets (lines 50-55)
backend:
  secrets:
    JWT_SECRET: "your-32-character-secret-here"  # Generate: openssl rand -base64 32
    OPENAI_API_KEY: "sk-your-openai-api-key"
    REDIS_URL: "redis://localhost:6379"

# Frontend secrets (lines 90-93)
frontend:
  secrets:
    BETTER_AUTH_SECRET: "your-32-character-secret-here"  # Generate: openssl rand -base64 32
    BETTER_AUTH_URL: "http://todo-app.local"

# Database password (line 20)
database:
  auth:
    password: "strong-database-password-here"
```

**💡 Generate secrets**: Run `openssl rand -base64 32` to generate secure secrets

**✅ Checkpoint**: All three secrets (JWT_SECRET, BETTER_AUTH_SECRET, OPENAI_API_KEY) updated

---

### Step 4: Deploy with Helm (3 minutes)

```bash
# Create namespace
kubectl create namespace todo-app

# Install Helm chart
helm install todo-app ./todo-helm --namespace todo-app

# Watch pods starting (wait for all to show Running)
kubectl get pods -n todo-app -w
# Press Ctrl+C when all pods are Running
```

**✅ Checkpoint**: All three pods (database, backend, frontend) show `1/1 Running`

Expected output:
```
NAME                               READY   STATUS    RESTARTS   AGE
todo-app-backend-xxxxx             1/1     Running   0          2m
todo-app-database-xxxxx            1/1     Running   0          2m
todo-app-frontend-xxxxx            1/1     Running   0          2m
```

---

### Step 5: Configure DNS and Access (2 minutes)

```bash
# Get Minikube IP
minikube ip

# Add to /etc/hosts (replace <MINIKUBE_IP> with actual IP)
echo "$(minikube ip) todo-app.local" | sudo tee -a /etc/hosts

# Verify DNS
ping -c 1 todo-app.local

# Open application in browser
xdg-open http://todo-app.local  # Linux
# or open http://todo-app.local  # macOS
```

**✅ Checkpoint**: Browser opens and shows Todo App login page

---

## Verification Checklist

Run these commands to verify deployment:

```bash
# 1. Check all pods are running
kubectl get pods -n todo-app
# Expected: All 3 pods with status Running

# 2. Check services
kubectl get svc -n todo-app
# Expected: 3 ClusterIP services (backend, frontend, database)

# 3. Check ingress
kubectl get ingress -n todo-app
# Expected: todo-app-ingress with host todo-app.local

# 4. Check persistent volume
kubectl get pvc -n todo-app
# Expected: todo-app-database-pvc with status Bound

# 5. Test backend health
curl http://todo-app.local/api/v1/health
# Expected: {"status":"healthy","timestamp":"..."}

# 6. Test frontend
curl -I http://todo-app.local
# Expected: HTTP/1.1 200 OK
```

**All checks passed? ✅ Deployment successful!**

---

## Post-Deployment Setup

### Create Better Auth Schema (Required - First Time Only)

The frontend uses Better Auth which requires specific database tables:

```bash
# Get database pod name
DB_POD=$(kubectl get pods -n todo-app -l app.kubernetes.io/name=todo-app-database -o jsonpath='{.items[0].metadata.name}')

# Connect to database
kubectl exec -it -n todo-app $DB_POD -- psql -U todouser -d todoapp

# Paste this SQL (then type \q to exit):
CREATE TABLE IF NOT EXISTS "user" (
    id TEXT PRIMARY KEY,
    email TEXT UNIQUE NOT NULL,
    "emailVerified" BOOLEAN DEFAULT FALSE,
    name TEXT,
    image TEXT,
    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS "session" (
    id TEXT PRIMARY KEY,
    "userId" TEXT NOT NULL,
    "expiresAt" TIMESTAMP NOT NULL,
    token TEXT NOT NULL,
    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ("userId") REFERENCES "user"(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "account" (
    id TEXT PRIMARY KEY,
    "userId" TEXT NOT NULL,
    "accountId" TEXT NOT NULL,
    "providerId" TEXT NOT NULL,
    "accessToken" TEXT,
    "refreshToken" TEXT,
    "expiresAt" TIMESTAMP,
    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    "updatedAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY ("userId") REFERENCES "user"(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS "verification" (
    id TEXT PRIMARY KEY,
    identifier TEXT NOT NULL,
    value TEXT NOT NULL,
    "expiresAt" TIMESTAMP NOT NULL,
    "createdAt" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## First Login and Testing

1. **Open browser**: http://todo-app.local
2. **Sign up**: Create a new account (email + password)
3. **Create task**: Test basic task creation
4. **Test chat**: Navigate to `/chat` and try conversational task management
5. **Test persistence**: Delete a pod and verify data survives:
   ```bash
   kubectl delete pod -n todo-app -l app.kubernetes.io/name=todo-app-database
   # Wait for pod to restart, then verify your tasks still exist
   ```

---

## Troubleshooting

### Pods not starting?

```bash
# Check pod status
kubectl describe pod -n todo-app <pod-name>

# Check logs
kubectl logs -n todo-app <pod-name> --tail=50

# Common fix: Restart all pods
kubectl rollout restart deployment -n todo-app
```

### Can't access todo-app.local?

```bash
# Verify /etc/hosts entry
cat /etc/hosts | grep todo-app

# Verify ingress
kubectl get ingress -n todo-app

# Fallback: Use port-forward
kubectl port-forward -n todo-app svc/todo-app-frontend 3000:3000
# Access: http://localhost:3000
```

### Images not found?

```bash
# Re-configure Docker
eval $(minikube docker-env)

# Rebuild and reload
cd backend && docker build -t todo-backend:latest . && cd ..
cd frontend && docker build -t todo-frontend:latest . && cd ..
minikube image load todo-backend:latest
minikube image load todo-frontend:latest

# Restart deployments
kubectl rollout restart deployment -n todo-app
```

---

## Daily Operations

### Start/Stop Application

```bash
# Stop Minikube (preserves data)
minikube stop

# Start again (data persists)
minikube start
kubectl get pods -n todo-app  # Pods auto-restart
```

### Update Configuration

```bash
# Edit values.yaml, then:
helm upgrade todo-app ./todo-helm -n todo-app

# Verify update
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

### Cleanup (Remove Everything)

```bash
# Uninstall release (keeps data)
helm uninstall todo-app -n todo-app

# Delete namespace (removes data too)
kubectl delete namespace todo-app

# Remove /etc/hosts entry
sudo sed -i '/todo-app.local/d' /etc/hosts
```

---

## Next Steps

- ✅ **Read Full Guide**: [HELM_DEPLOYMENT_GUIDE.md](../../HELM_DEPLOYMENT_GUIDE.md) for detailed documentation
- ✅ **Customize**: Edit `todo-helm/values.yaml` to adjust resources, replicas, autoscaling
- ✅ **Monitor**: Set up monitoring with Prometheus/Grafana (future enhancement)
- ✅ **Production**: Adapt chart for cloud deployment (EKS, GKE, AKS)

---

## Quick Reference

| Resource | Command |
|----------|---------|
| Check status | `kubectl get all -n todo-app` |
| View logs | `kubectl logs -n todo-app <pod-name>` |
| Restart pods | `kubectl rollout restart deployment -n todo-app` |
| Access frontend | http://todo-app.local |
| Access backend | http://todo-app.local/api/v1/health |
| API docs | http://todo-app.local/api/docs |
| Minikube dashboard | `minikube dashboard` |
| Helm status | `helm status todo-app -n todo-app` |
| Port forward | `kubectl port-forward -n todo-app svc/<service> <port>:<port>` |

---

**Support**: For detailed troubleshooting, see [HELM_DEPLOYMENT_GUIDE.md](../../HELM_DEPLOYMENT_GUIDE.md) Section: Monitoring and Troubleshooting
