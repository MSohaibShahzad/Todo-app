#!/bin/bash
# Port Forward Script for WSL2 + Minikube
# This makes your Todo App accessible from Windows browser

echo "========================================="
echo "Starting Port Forwarding for Todo App"
echo "========================================="
echo ""

# Get WSL IP
WSL_IP=$(ip addr show eth0 | grep -oP '(?<=inet\s)\d+(\.\d+){3}' | head -1)
echo "WSL IP Address: $WSL_IP"
echo ""

# Kill any existing port forwards on these ports
echo "Cleaning up existing port forwards..."
pkill -f "kubectl port-forward.*todo-app-frontend" 2>/dev/null || true
pkill -f "kubectl port-forward.*todo-app-backend" 2>/dev/null || true
sleep 2

# Start port forwarding in background (using alternate ports to avoid Docker Desktop conflicts)
echo "Starting Frontend port-forward (4000:3000)..."
kubectl port-forward -n todo-app svc/todo-app-frontend 4000:3000 --address=0.0.0.0 > /tmp/frontend-pf.log 2>&1 &
FRONTEND_PID=$!

echo "Starting Backend port-forward (9000:8000)..."
kubectl port-forward -n todo-app svc/todo-app-backend 9000:8000 --address=0.0.0.0 > /tmp/backend-pf.log 2>&1 &
BACKEND_PID=$!

# Wait a moment for port forwards to start
sleep 3

# Check if they're running
if ps -p $FRONTEND_PID > /dev/null && ps -p $BACKEND_PID > /dev/null; then
    echo ""
    echo "========================================="
    echo "✅ SUCCESS! Port forwarding is active"
    echo "========================================="
    echo ""
    echo "Access your Todo App from Windows browser:"
    echo ""
    echo "  Frontend:  http://$WSL_IP:4000"
    echo "  Backend:   http://$WSL_IP:9000/api/v1/health"
    echo ""
    echo "NOTE: Using ports 4000/9000 to avoid conflict with Docker Desktop"
    echo ""
    echo "========================================="
    echo ""
    echo "⚠️  IMPORTANT: Keep this terminal window open!"
    echo "    Closing it will stop port forwarding."
    echo ""
    echo "To stop port forwarding, press Ctrl+C"
    echo ""
    echo "Process IDs:"
    echo "  Frontend: $FRONTEND_PID"
    echo "  Backend:  $BACKEND_PID"
    echo ""
    
    # Save PIDs for later cleanup
    echo $FRONTEND_PID > /tmp/frontend-pf.pid
    echo $BACKEND_PID > /tmp/backend-pf.pid
    
    # Wait for user interrupt
    trap "echo ''; echo 'Stopping port forwards...'; kill $FRONTEND_PID $BACKEND_PID 2>/dev/null; exit 0" INT TERM
    
    # Keep script running
    wait
else
    echo "❌ ERROR: Port forwarding failed to start"
    echo "Check logs:"
    echo "  Frontend: /tmp/frontend-pf.log"
    echo "  Backend: /tmp/backend-pf.log"
    exit 1
fi
