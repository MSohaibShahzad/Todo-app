# Todo App - Quick Start Guide

## 📚 Deployment Guide Navigation

**Choose your deployment method:**

### 1️⃣ **Docker Compose** (Development & Testing)
📖 **Guide**: [DOCKER_DEPLOYMENT.md](./DOCKER_DEPLOYMENT.md)

**Best for:**
- ✅ Local development
- ✅ Quick testing
- ✅ Simple setup (just Docker required)
- ✅ Small-scale production

**Quick Start:**
```bash
docker-compose up -d --build
# Access: http://localhost:3000
```

---

### 2️⃣ **Kubernetes with Helm** (Production - Full Setup)
📖 **Guide**: [HELM_DEPLOYMENT_GUIDE.md](./HELM_DEPLOYMENT_GUIDE.md)

**Best for:**
- ✅ Production deployments
- ✅ Auto-scaling & high availability
- ✅ Learning Kubernetes in-depth
- ✅ Complete control over configuration

**What's included:**
- Complete Helm chart configuration
- Step-by-step deployment instructions
- Troubleshooting guide
- ConfigMaps, Secrets, PersistentVolumes
- Health probes, Ingress routing
- Horizontal Pod Autoscaling

---

### 3️⃣ **Kubernetes Quick Start** (This Guide - Fastest)
📖 **Guide**: You're here! **QUICKSTART.md**

**Best for:**
- ✅ Daily use after initial deployment
- ✅ Quick start/stop commands
- ✅ Minimal complexity
- ✅ Education & demos

**What you need:**
- Minikube running
- App already deployed (via Helm)

> **⚠️ Note**: This guide assumes you've already deployed the app using [HELM_DEPLOYMENT_GUIDE.md](./HELM_DEPLOYMENT_GUIDE.md). If this is your first time, start there!

---

## 🚀 Starting the Application

> **Prerequisites**: App must be deployed first using the [HELM_DEPLOYMENT_GUIDE.md](./HELM_DEPLOYMENT_GUIDE.md)

### Step 1: Start Minikube
```bash
cd /home/sohaib/hackathon2/Todo-app/Phase-4
minikube start
```

### Step 2: Wait for Pods (30-60 seconds)
```bash
kubectl get pods -n todo-app
```
Wait until all 3 pods show **"Running"** status.

### Step 3: Access Your App

#### **Option A: Frontend Only (Recommended)**
```bash
minikube service todo-app-frontend -n todo-app
```
- Opens browser automatically
- URL like: `http://127.0.0.1:38565`
- Keep terminal open while using the app

#### **Option B: Get All Service URLs**
```bash
# Frontend
minikube service todo-app-frontend -n todo-app --url

# Backend (API)
minikube service todo-app-backend -n todo-app --url

# Database (PostgreSQL)
minikube service todo-app-database -n todo-app --url
```

---

## 🛑 Stopping the Application

### Quick Stop
```bash
# Press Ctrl+C in the terminal (if service is running)
# Then stop Minikube:
minikube stop
```

### Complete Shutdown
```bash
# Kill all port forwards
pkill -f "minikube service"

# Stop Minikube
minikube stop
```

---

## 📋 Daily Workflow

### **Morning (Start Work)**
```bash
cd /home/sohaib/hackathon2/Todo-app/Phase-4
minikube start
minikube service todo-app-frontend -n todo-app
```
✅ Browser opens automatically!

### **Evening (End Work)**
```bash
# Press Ctrl+C
minikube stop
```

---

## 🔍 Useful Commands

### Check Everything is Running
```bash
# Check Minikube
minikube status

# Check all pods
kubectl get pods -n todo-app

# Check all services
kubectl get svc -n todo-app
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

### Restart a Pod
```bash
# Delete pod (it will automatically recreate)
kubectl delete pod -n todo-app <pod-name>
```

---

## 🆘 Troubleshooting

### Pods Won't Start
```bash
# Describe pod to see error
kubectl describe pod -n todo-app <pod-name>

# Check events
kubectl get events -n todo-app --sort-by='.lastTimestamp'
```

### Fresh Restart
```bash
minikube stop
minikube start
# Wait 1-2 minutes for pods to start
kubectl get pods -n todo-app -w
```

### Complete Reset (⚠️ Deletes All Data)
```bash
helm uninstall todo-app -n todo-app
kubectl delete namespace todo-app
# Then redeploy using HELM_DEPLOYMENT_GUIDE.md
```

---

## 🎯 Quick Access URLs

After running `minikube service todo-app-frontend -n todo-app`, you'll get:

- **Frontend**: `http://127.0.0.1:XXXXX` (random port)
- **Backend API**: `http://127.0.0.1:YYYYY/api/v1/health`
- **API Docs**: `http://127.0.0.1:YYYYY/api/docs`

---

## 💾 Data Persistence

✅ **Your data is safe!**
- Database data persists across:
  - Pod restarts
  - Minikube stop/start
  - Laptop restarts

❌ **Data is lost only if you:**
- Run `minikube delete`
- Delete the namespace: `kubectl delete namespace todo-app`
- Uninstall Helm: `helm uninstall todo-app -n todo-app`

---

## ⚡ One-Line Startup (Copy & Paste)

```bash
minikube start && sleep 30 && minikube service todo-app-frontend -n todo-app
```

---

## 📚 Additional Resources

### Deployment Guides

| Guide | When to Use |
|-------|-------------|
| **[DOCKER_DEPLOYMENT.md](./DOCKER_DEPLOYMENT.md)** | Development, testing, or simple Docker Compose setup |
| **[HELM_DEPLOYMENT_GUIDE.md](./HELM_DEPLOYMENT_GUIDE.md)** | Initial Kubernetes setup, production deployment, troubleshooting |
| **[QUICKSTART.md](./QUICKSTART.md)** | Daily start/stop (you're here!) |

### Component Documentation

- **Backend API**: `backend/CLAUDE.md` - FastAPI, OpenAI integration, MCP tools
- **Frontend UI**: `frontend/CLAUDE.md` - Next.js, ChatKit, Better Auth
- **Specifications**: `specs/` - Feature specs and architecture docs

### Common Tasks

| Task | Guide to Use |
|------|--------------|
| First-time deployment | [HELM_DEPLOYMENT_GUIDE.md](./HELM_DEPLOYMENT_GUIDE.md) |
| Daily development | [QUICKSTART.md](./QUICKSTART.md) (this file) |
| Docker Compose setup | [DOCKER_DEPLOYMENT.md](./DOCKER_DEPLOYMENT.md) |
| Troubleshooting pods | [HELM_DEPLOYMENT_GUIDE.md](./HELM_DEPLOYMENT_GUIDE.md) → Troubleshooting section |
| Understanding architecture | [HELM_DEPLOYMENT_GUIDE.md](./HELM_DEPLOYMENT_GUIDE.md) → Architecture section |
| Changing configuration | [HELM_DEPLOYMENT_GUIDE.md](./HELM_DEPLOYMENT_GUIDE.md) → Helm Chart Configuration |

---

**Happy Coding! 🚀**
