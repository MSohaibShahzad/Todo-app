# Quick Start Guide - Todo App on Minikube

## 🚀 Start the Application

### Step 1: Start Minikube (if not running)
```bash
minikube start
```

### Step 2: Check if pods are running
```bash
kubectl get pods -n todo-app
```

**Expected output**: All 3 pods should show `Running`:
- `todo-app-frontend-*`
- `todo-app-backend-*`
- `todo-app-database-*`

### Step 3: Start Port Forwarding
```bash
cd /home/sohaib/hackathon2/Todo-app/Phase-4
./start-port-forward.sh
```

**Keep this terminal window open!** Port forwarding only works while the script is running.

You should see:
```
✅ SUCCESS! Port forwarding is active

Access your Todo App from Windows browser:

  Frontend:  http://172.19.169.234:4000
  Backend:   http://172.19.169.234:9000/api/v1/health
```

### Step 4: Access from Windows Browser

Open any browser in Windows and go to:
```
http://172.19.169.234:4000
```

---

## 🛑 Stop the Application

### To stop port-forwarding:
Press `Ctrl+C` in the terminal running the port-forward script

OR run:
```bash
pkill -f "kubectl port-forward"
```

### To stop Minikube (optional - stops everything):
```bash
minikube stop
```

---

## 🔧 Troubleshooting

### If pods are not running:
```bash
# Check pod status
kubectl get pods -n todo-app

# View logs if any pod is failing
kubectl logs -n todo-app deployment/todo-app-frontend
kubectl logs -n todo-app deployment/todo-app-backend
kubectl logs -n todo-app deployment/todo-app-database
```

### If port-forward fails (ports in use):
```bash
# Check what's using the ports
ss -tlnp | grep -E ':(4000|9000)'

# Kill existing port-forwards
pkill -f "kubectl port-forward"

# Try starting again
./start-port-forward.sh
```

### If WSL IP changes:
```bash
# Get current WSL IP
ip addr show eth0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}'

# Update values.yaml with new IP (sections: NEXT_PUBLIC_API_URL, NEXT_PUBLIC_APP_URL)
# Then upgrade Helm:
helm upgrade todo-app ./todo-helm --namespace todo-app

# Restart port-forward script
```

### If you need to rebuild images:
```bash
# Point Docker to Minikube
eval $(minikube docker-env)

# Rebuild backend
cd backend
docker build -t todo-backend:latest .

# Rebuild frontend
cd ../frontend
docker build -t todo-frontend:latest .

# Restart deployments
kubectl rollout restart deployment/todo-app-backend -n todo-app
kubectl rollout restart deployment/todo-app-frontend -n todo-app
```

---

## 📝 URLs Reference

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://172.19.169.234:4000 | Main application UI |
| **Backend API** | http://172.19.169.234:9000 | REST API endpoints |
| **Backend Health** | http://172.19.169.234:9000/api/v1/health | Health check |
| **API Docs** | http://172.19.169.234:9000/docs | Swagger UI |

---

## ⚙️ Configuration Details

- **Port Mapping**:
  - Frontend: 4000 (WSL) → 3000 (Pod)
  - Backend: 9000 (WSL) → 8000 (Pod)
- **WSL IP**: 172.19.169.234 (may change after WSL restart)
- **Kubernetes Namespace**: todo-app
- **Docker Desktop Ports**: 3000, 8000 (avoided by using 4000, 9000)

---

## 💡 Quick Commands

```bash
# Check everything is running
kubectl get all -n todo-app

# View all environment variables in frontend
kubectl exec -n todo-app deployment/todo-app-frontend -- env | grep NEXT_PUBLIC

# Restart a specific service
kubectl rollout restart deployment/todo-app-frontend -n todo-app

# Delete and redeploy everything
helm uninstall todo-app -n todo-app
helm install todo-app ./todo-helm --namespace todo-app --create-namespace
```

---

**Created**: 2026-02-07
**Phase**: 4 - Kubernetes/Helm Deployment with WSL2 Port Forwarding
