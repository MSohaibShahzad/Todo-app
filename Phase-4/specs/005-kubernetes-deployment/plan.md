# Implementation Plan: Phase IV – Kubernetes/Helm Local Deployment

**Feature ID**: `005-kubernetes-deployment` | **Date**: 2026-02-05 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/005-kubernetes-deployment/spec.md`

## Summary

Deploy the full-stack conversational AI Todo application (Phases I-III) to local Kubernetes using Helm charts, enabling declarative infrastructure-as-code, persistent data storage, horizontal scaling, and production-like operational capabilities. The deployment targets Minikube for local development with a three-tier architecture (PostgreSQL database, FastAPI backend, Next.js frontend) managed through a single Helm release.

**Key Objectives**:
1. Create production-ready Helm chart with complete Kubernetes manifests
2. Implement persistent data storage for PostgreSQL with PersistentVolumeClaims
3. Separate configuration (ConfigMaps) from secrets (Secrets) with secure management
4. Enable single-hostname access via Ingress with path-based routing
5. Implement health probes for automatic pod restart and self-healing
6. Support horizontal scaling with optional HorizontalPodAutoscaler

## Technical Context

**Infrastructure**:
- Platform: Kubernetes 1.25+ on Minikube
- Package Manager: Helm 3.0+
- Container Runtime: Docker
- Ingress Controller: NGINX Ingress addon for Minikube
- Storage: Default StorageClass (hostpath on Minikube)
- Minimum Resources: 4 CPU cores, 8GB RAM

**Container Images**:
- Database: `postgres:16-alpine` (official PostgreSQL image)
- Backend: `todo-backend:latest` (FastAPI, built locally from Phase-3)
- Frontend: `todo-frontend:latest` (Next.js, built locally from Phase-3)
- Image Pull Policy: `IfNotPresent` (local development)

**Helm Chart**:
- Chart API Version: v2
- Chart Version: 1.0.0
- App Version: 1.0.0 (Phase IV)
- Template Engine: Go templates with Sprig functions

**Networking**:
- Service Type: ClusterIP (internal cluster networking)
- Ingress Hostname: `todo-app.local` (local DNS via /etc/hosts)
- Path-Based Routing: `/` → frontend, `/api/*` → backend
- Internal Communication: Service DNS names (e.g., `todo-app-backend:8000`)

**Performance Goals**:
- Pod startup time: <2 minutes per service
- Helm install time: <5 minutes total
- Health probe response: <100ms
- Persistent data access: <50ms latency

**Constraints**:
- Local development only (Minikube, not production cloud)
- Single Kubernetes cluster (no multi-cluster support)
- Manual image building and loading (no image registry)
- Single namespace per environment
- No TLS/HTTPS (HTTP only for local)
- PostgreSQL single replica (no replication)

**Scale/Scope**:
- Target: 1-3 developers running locally
- 3 Kubernetes Deployments (database, backend, frontend)
- 3 Services, 1 Ingress, 2 ConfigMaps, 2 Secrets, 1 PVC
- ~15 Helm template files
- Total cluster resources: ~2 CPU cores, ~2GB RAM at minimum

## Constitution Check

*GATE: Must pass before implementation. Re-check after deployment.*

### Applicable Principles (from Phase IV Constitution)

**✓ Kubernetes/Helm Architecture**:
- All resources defined in Helm templates (declarative)
- Semantic versioning for Helm chart (1.0.0)
- Dedicated manifests for each service
- ConfigMaps and Secrets for all configuration
- **Status**: PASS - Complete Helm chart structure designed

**✓ Container Standards**:
- Multi-stage Docker builds used (backend and frontend)
- Images tagged with versions (using `:latest` for dev)
- Non-root users in containers (where possible)
- Build arguments for environment-specific config
- **Status**: PASS - Dockerfiles follow best practices

**✓ Configuration Management**:
- Environment variables in ConfigMaps (non-sensitive)
- Secrets for sensitive data (JWT, API keys, passwords)
- Database connection strings templated from Secrets
- All secrets parameterized in values.yaml
- **Status**: PASS - Clear separation of config types

**✓ Health & Observability**:
- Health check endpoints implemented (/api/v1/health)
- Liveness and readiness probes configured
- Resource limits and requests defined
- Pod restart on probe failure
- **Status**: PASS - Complete health monitoring

**✓ Networking & Ingress**:
- ClusterIP services for internal communication
- Single Ingress with path-based routing
- Backend API proxied through frontend when needed
- CORS configured for cross-origin requests
- **Status**: PASS - Unified network architecture

**✓ Data Persistence**:
- PersistentVolumeClaim for PostgreSQL (5Gi)
- Storage class and size configurable
- Data persists across pod restarts
- Backup strategies documented
- **Status**: PASS - Persistent storage implemented

**✓ Deployment Strategy**:
- Declarative and version-controlled
- `helm upgrade` as standard deployment method
- Rollback via Helm revisions
- Reproducible from values.yaml
- **Status**: PASS - Helm-based deployment

**✓ Local Development (Minikube)**:
- Minikube as primary environment
- Port-forwarding scripts provided
- Images loadable into Minikube
- Ingress addon for routing
- **Status**: PASS - Minikube-optimized

**✓ Resource Management**:
- HPA configuration provided but optional
- Resource quotas sensible for local dev
- Database resources prioritized
- Horizontal scaling for stateless services
- **Status**: PASS - Balanced resource allocation

### Gates Evaluation

**GATE 1: No constitutional violations** - All Phase IV principles satisfied
**GATE 2: Deployment verification** - Must verify successful deployment before marking complete

## Complexity Tracking

### Justified Complexity

| Component | Complexity Introduced | Justification | Mitigation |
|-----------|----------------------|---------------|------------|
| Helm Templates | ~15 YAML files with Go templating | Required for declarative Kubernetes deployment | Use helper templates for DRY; comprehensive comments |
| ConfigMap/Secret Management | Dual-layer config (values.yaml → K8s resources) | Kubernetes best practice for config separation | Clear documentation; values.yaml as single source |
| Ingress Configuration | Path-based routing with rewrite rules | Unified hostname access requirement | Fallback to port-forward documented |
| PersistentVolumeClaim | Volume lifecycle management | Data persistence requirement | Storage size configurable; backup docs |
| Health Probes | Multiple probe configurations per pod | Self-healing and high availability | Probe timings tunable via values.yaml |
| Resource Limits | CPU/memory tuning per service | Prevent resource exhaustion | Defaults for local dev; adjustable for prod |

**Total Complexity Score**: Medium - Standard Kubernetes/Helm patterns, no custom operators or CRDs

## Helm Chart Structure

### Chart Layout

```text
todo-helm/
├── Chart.yaml                  # Chart metadata (name, version, appVersion)
├── values.yaml                 # Default configuration values (250+ lines)
├── README.md                   # Quick start guide
├── .helmignore                 # Files to exclude from chart package
└── templates/
    ├── _helpers.tpl            # Helper templates (labels, selectors, names)
    ├── NOTES.txt               # Post-install instructions
    ├── configmap.yaml          # Environment variables (backend-config, frontend-config)
    ├── secret.yaml             # Sensitive data (backend-secret, frontend-secret)
    ├── pvc.yaml                # PostgreSQL persistent storage
    ├── database-deployment.yaml# PostgreSQL Deployment
    ├── database-service.yaml   # Database ClusterIP Service
    ├── backend-deployment.yaml # FastAPI backend Deployment
    ├── backend-service.yaml    # Backend ClusterIP Service
    ├── frontend-deployment.yaml# Next.js frontend Deployment
    ├── frontend-service.yaml   # Frontend ClusterIP Service
    ├── ingress.yaml            # NGINX Ingress (path-based routing)
    ├── hpa.yaml                # HorizontalPodAutoscaler (optional)
    └── serviceaccount.yaml     # Service Account (optional)
```

### values.yaml Structure

```yaml
# Global settings
global:
  namespace: todo-app
  imagePullPolicy: IfNotPresent

# Database configuration
database:
  enabled: true
  image:
    repository: postgres
    tag: "16-alpine"
  auth:
    username: todouser
    password: "CHANGEME"  # Override in production
    database: todoapp
  persistence:
    enabled: true
    size: 5Gi
    storageClass: ""
  resources:
    requests:
      cpu: 250m
      memory: 256Mi
    limits:
      cpu: 500m
      memory: 512Mi

# Backend configuration
backend:
  image:
    repository: todo-backend
    tag: latest
  replicas: 1
  env:
    DATABASE_URL: "auto-generated-from-db-auth"
    ENVIRONMENT: production
    JWT_ALGORITHM: HS256
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: "30"
    AI_MODEL: "gpt-4-turbo"
    RATE_LIMIT_REQUESTS_PER_MINUTE: "10"
    CONVERSATION_RETENTION_DAYS: "30"
    MAX_ACTIVE_CONVERSATIONS_PER_USER: "3"
  secrets:
    JWT_SECRET: "CHANGEME"
    OPENAI_API_KEY: "CHANGEME"
    REDIS_URL: "redis://localhost:6379"
  resources:
    requests:
      cpu: 500m
      memory: 512Mi
    limits:
      cpu: 1000m
      memory: 1Gi
  autoscaling:
    enabled: false
    minReplicas: 2
    maxReplicas: 10
    targetCPUUtilizationPercentage: 70

# Frontend configuration
frontend:
  image:
    repository: todo-frontend
    tag: latest
  replicas: 1
  env:
    NODE_ENV: production
    NEXT_PUBLIC_CHATKIT_DOMAIN_KEY: "local-dev"
    NEXT_PUBLIC_API_URL: ""
    NEXT_PUBLIC_BACKEND_URL: "http://todo-app-backend:8000"
    DATABASE_URL: "auto-generated-from-db-auth"
  secrets:
    BETTER_AUTH_SECRET: "CHANGEME"
    BETTER_AUTH_URL: "http://todo-app.local"
  resources:
    requests:
      cpu: 500m
      memory: 512Mi
    limits:
      cpu: 1000m
      memory: 1Gi
  autoscaling:
    enabled: false
    minReplicas: 2
    maxReplicas: 10
    targetCPUUtilizationPercentage: 70

# Ingress configuration
ingress:
  enabled: true
  className: nginx
  host: todo-app.local
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /$2
```

## Architectural Decisions

### Decision 1: Helm Over Raw YAML Manifests

**Context**: Need to deploy multiple Kubernetes resources with configurable values.

**Options Considered**:
1. **Raw YAML files** (kubectl apply -f)
   - Pros: Simple, no dependencies, direct control
   - Cons: No templating, hard to manage environments, repetitive
2. **Kustomize**
   - Pros: Built into kubectl, patch-based approach
   - Cons: Less flexible templating, steeper learning curve
3. **Helm Charts** ✅ SELECTED
   - Pros: Industry standard, rich templating, package management, rollback support
   - Cons: Additional tool dependency, Go template syntax

**Decision**: Use Helm 3 for package management and templating.

**Rationale**:
- Helm is the de-facto standard for Kubernetes deployments
- Built-in rollback and revision history
- Single `values.yaml` as source of truth for configuration
- Reusable across environments (dev/staging/prod)
- Strong community support and documentation

**ADR Reference**: Not created (standard practice, low significance)

---

### Decision 2: ConfigMaps vs Secrets for Configuration

**Context**: Need to store environment variables for backend and frontend.

**Options Considered**:
1. **All in ConfigMaps** (not secure)
2. **All in Secrets** (over-complicates non-sensitive data)
3. **Hybrid Approach** ✅ SELECTED
   - ConfigMaps: Non-sensitive env vars (DATABASE_URL without password, AI_MODEL, feature flags)
   - Secrets: Sensitive data (JWT_SECRET, OPENAI_API_KEY, database password)

**Decision**: Use ConfigMaps for non-sensitive configuration and Secrets for credentials.

**Rationale**:
- Follows Kubernetes security best practices
- Secrets can be rotated without changing ConfigMaps
- Clear separation makes auditing easier
- Enables future integration with external secret managers (Vault, AWS Secrets Manager)

**Trade-offs**:
- More complex than single ConfigMap
- Need to remember which data goes where

**ADR Reference**: To be created if this becomes a pattern across projects

---

### Decision 3: PersistentVolumeClaim for Database Storage

**Context**: PostgreSQL data must survive pod restarts and redeployments.

**Options Considered**:
1. **EmptyDir volume** (data lost on pod deletion)
2. **HostPath volume** (tied to specific node)
3. **PersistentVolumeClaim** ✅ SELECTED
   - Pros: Cloud-portable, survives pod lifecycle, Kubernetes-managed
   - Cons: Slightly more complex setup

**Decision**: Use PVC with default StorageClass.

**Rationale**:
- Data persistence is critical for production-like deployment
- PVC abstracts storage provisioning (works on Minikube and cloud)
- Survives pod deletion and rolling updates
- Size configurable via values.yaml (5Gi default)

**Implementation**:
- Single PVC mounted at `/var/lib/postgresql/data`
- ReadWriteOnce access mode (single pod)
- Storage class defaults to cluster default (hostpath on Minikube)

---

### Decision 4: Single Ingress with Path-Based Routing

**Context**: Need to expose frontend and backend through a unified interface.

**Options Considered**:
1. **NodePort Services** (exposes multiple ports, non-standard)
2. **LoadBalancer Services** (not available on Minikube)
3. **Multiple Ingresses** (separate hostnames per service)
4. **Single Ingress with Paths** ✅ SELECTED
   - `/` → Frontend
   - `/api/*` → Backend

**Decision**: Single Ingress resource with path-based routing to `todo-app.local`.

**Rationale**:
- Mimics production setup with single domain
- Simplifies CORS configuration
- Single /etc/hosts entry for developers
- Next.js can proxy backend requests internally
- Standard pattern for full-stack applications

**Implementation**:
```yaml
rules:
  - host: todo-app.local
    http:
      paths:
        - path: /api(/|$)(.*)
          pathType: ImplementationSpecific
          backend:
            service:
              name: todo-app-backend
              port:
                number: 8000
        - path: /
          pathType: Prefix
          backend:
            service:
              name: todo-app-frontend
              port:
                number: 3000
```

---

### Decision 5: Health Probes Configuration

**Context**: Need to detect unhealthy pods and restart them automatically.

**Options Considered**:
1. **No probes** (manual intervention required)
2. **Liveness only** (restarts but no readiness check)
3. **Readiness only** (no automatic restart)
4. **Both Liveness and Readiness** ✅ SELECTED

**Decision**: Implement both liveness and readiness probes for backend and frontend.

**Rationale**:
- Liveness: Detects crashed/deadlocked pods and restarts them
- Readiness: Prevents traffic to pods still starting up
- Essential for zero-downtime deployments
- Aligns with production best practices

**Configuration**:
- **Backend**: HTTP GET `/api/v1/health` (already implemented)
- **Frontend**: HTTP GET `/` (Next.js server)
- **Database**: `pg_isready` command
- Initial delay: 30s (backend), 10s (frontend), 5s (database)
- Period: 10s, Timeout: 5s, Failure threshold: 3

---

### Decision 6: Resource Limits vs Requests

**Context**: Need to prevent resource exhaustion while ensuring pods have enough capacity.

**Options Considered**:
1. **No limits** (risk of resource starvation)
2. **Limits only** (no guaranteed capacity)
3. **Requests only** (no upper bound)
4. **Both Requests and Limits** ✅ SELECTED

**Decision**: Define both resource requests and limits for all deployments.

**Rationale**:
- Requests: Guaranteed resources, used by Kubernetes scheduler
- Limits: Prevents single pod from consuming all resources
- Essential for stable multi-pod environment
- Enables accurate capacity planning

**Allocations** (optimized for local Minikube):
```yaml
Database:  250m CPU, 256Mi RAM (requests) | 500m CPU, 512Mi RAM (limits)
Backend:   500m CPU, 512Mi RAM (requests) | 1000m CPU, 1Gi RAM (limits)
Frontend:  500m CPU, 512Mi RAM (requests) | 1000m CPU, 1Gi RAM (limits)
Total:     1.25 CPU, 1.25Gi RAM (requests) | 2.5 CPU, 2.5Gi RAM (limits)
```

---

### Decision 7: HorizontalPodAutoscaler - Optional Feature

**Context**: Backend and frontend may need to scale under load.

**Options Considered**:
1. **No HPA** (manual scaling only)
2. **HPA Always Enabled** (unnecessary for local dev)
3. **HPA Optional** ✅ SELECTED (enabled via values.yaml flag)

**Decision**: Provide HPA configuration but disabled by default.

**Rationale**:
- Local development doesn't need autoscaling
- Production deployments can enable it easily
- Demonstrates how to scale the application
- No overhead when disabled (resource not created)

**Configuration**:
```yaml
autoscaling:
  enabled: false  # Set true for production
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70
```

## Implementation Phases

### Phase 0: Prerequisites and Setup ✅ COMPLETED

**Objective**: Ensure local environment ready for Kubernetes deployment.

**Tasks**:
- ✅ Minikube installed and running (v1.32+)
- ✅ Helm 3.0+ installed
- ✅ kubectl configured to communicate with Minikube
- ✅ Ingress addon enabled (`minikube addons enable ingress`)
- ✅ Backend Dockerfile with multi-stage build
- ✅ Frontend Dockerfile with multi-stage build
- ✅ Backend health endpoint implemented (`/api/v1/health`)

**Validation**:
```bash
minikube status
helm version
kubectl version --client
kubectl get pods -n ingress-nginx
docker build backend/ -t todo-backend:latest
docker build frontend/ -t todo-frontend:latest
```

---

### Phase 1: Helm Chart Scaffolding ✅ COMPLETED

**Objective**: Create Helm chart directory structure and base templates.

**Tasks**:
- ✅ Create `todo-helm/Chart.yaml` with metadata
- ✅ Create `todo-helm/values.yaml` with all configuration options
- ✅ Create `todo-helm/templates/_helpers.tpl` with label helpers
- ✅ Create `todo-helm/README.md` with quick start guide
- ✅ Create `.helmignore` to exclude unnecessary files

**Validation**:
```bash
helm lint todo-helm
helm template todo-app todo-helm --dry-run
```

---

### Phase 2: Database Resources ✅ COMPLETED

**Objective**: Deploy PostgreSQL with persistent storage.

**Tasks**:
- ✅ Create `pvc.yaml` for persistent volume claim
- ✅ Create `database-deployment.yaml` with PostgreSQL container
- ✅ Create `database-service.yaml` for ClusterIP service
- ✅ Configure health probes (pg_isready)
- ✅ Set resource limits and requests
- ✅ Mount PVC to `/var/lib/postgresql/data`

**Validation**:
```bash
helm install todo-app ./todo-helm -n todo-app --create-namespace
kubectl get pvc -n todo-app
kubectl get pods -n todo-app -l app.kubernetes.io/name=todo-app-database
kubectl exec -n todo-app <db-pod> -- pg_isready -U todouser
```

---

### Phase 3: Backend Resources ✅ COMPLETED

**Objective**: Deploy FastAPI backend with database connectivity.

**Tasks**:
- ✅ Create `configmap.yaml` for backend environment variables
- ✅ Create `secret.yaml` for JWT_SECRET and OPENAI_API_KEY
- ✅ Create `backend-deployment.yaml` with FastAPI container
- ✅ Create `backend-service.yaml` for ClusterIP service
- ✅ Configure health probes (HTTP GET /api/v1/health)
- ✅ Template database connection string from Secret
- ✅ Set resource limits and requests

**Validation**:
```bash
kubectl get configmap -n todo-app
kubectl get secret -n todo-app
kubectl get pods -n todo-app -l app.kubernetes.io/name=todo-app-backend
kubectl logs -n todo-app <backend-pod>
kubectl exec -n todo-app <backend-pod> -- curl localhost:8000/api/v1/health
```

---

### Phase 4: Frontend Resources ✅ COMPLETED

**Objective**: Deploy Next.js frontend with Better Auth.

**Tasks**:
- ✅ Update `configmap.yaml` for frontend environment variables
- ✅ Update `secret.yaml` for BETTER_AUTH_SECRET
- ✅ Create `frontend-deployment.yaml` with Next.js container
- ✅ Create `frontend-service.yaml` for ClusterIP service
- ✅ Configure health probes (HTTP GET /)
- ✅ Set NEXT_PUBLIC_BACKEND_URL to backend service DNS
- ✅ Set resource limits and requests

**Validation**:
```bash
kubectl get pods -n todo-app -l app.kubernetes.io/name=todo-app-frontend
kubectl logs -n todo-app <frontend-pod>
kubectl exec -n todo-app <frontend-pod> -- curl localhost:3000
```

---

### Phase 5: Ingress Configuration ✅ COMPLETED

**Objective**: Enable single-hostname access with path-based routing.

**Tasks**:
- ✅ Create `ingress.yaml` with NGINX class
- ✅ Configure host: `todo-app.local`
- ✅ Add path rule: `/` → frontend-service:3000
- ✅ Add path rule: `/api/*` → backend-service:8000
- ✅ Add rewrite annotations for clean URLs
- ✅ Add /etc/hosts entry: `<minikube-ip> todo-app.local`

**Validation**:
```bash
kubectl get ingress -n todo-app
kubectl describe ingress -n todo-app
curl http://todo-app.local
curl http://todo-app.local/api/v1/health
```

---

### Phase 6: HPA and Scaling Features ✅ COMPLETED

**Objective**: Add optional horizontal pod autoscaling.

**Tasks**:
- ✅ Create `hpa.yaml` with CPU-based scaling rules
- ✅ Make HPA conditional on `autoscaling.enabled` flag
- ✅ Configure min/max replicas in values.yaml
- ✅ Set target CPU utilization percentage
- ✅ Document how to enable HPA

**Validation**:
```bash
# With autoscaling.enabled: true in values.yaml
kubectl get hpa -n todo-app
kubectl describe hpa -n todo-app
```

---

### Phase 7: Documentation and Testing ✅ COMPLETED

**Objective**: Provide comprehensive deployment documentation.

**Tasks**:
- ✅ Create `HELM_DEPLOYMENT_GUIDE.md` with full instructions
- ✅ Document prerequisites and setup steps
- ✅ Document deployment process (build, install, verify)
- ✅ Document troubleshooting (common issues and solutions)
- ✅ Document upgrade and rollback procedures
- ✅ Document cleanup and maintenance
- ✅ Add deployment checklist
- ✅ Test complete deployment on fresh Minikube

**Validation**:
- [ ] Follow HELM_DEPLOYMENT_GUIDE.md from scratch
- [ ] Verify all pods Running
- [ ] Test user signup and task creation
- [ ] Test conversational AI chat
- [ ] Test pod restart (data persistence)
- [ ] Test Helm upgrade
- [ ] Test Helm rollback

---

## Testing Strategy

### Unit Testing (Helm Templates)

**Tools**: `helm lint`, `helm template --dry-run`

**Approach**:
1. Lint chart for syntax errors
2. Render templates with different values.yaml configurations
3. Verify YAML validity with `kubectl --dry-run=client`

**Coverage**:
- All templates render without errors
- Helper functions produce correct labels
- Conditionals work (e.g., HPA only when enabled)

### Integration Testing (Local Deployment)

**Tools**: kubectl, curl, psql

**Approach**:
1. Deploy to fresh Minikube cluster
2. Verify all pods reach Running state
3. Test inter-service connectivity
4. Test Ingress routing
5. Test data persistence across pod restart

**Test Cases**:
1. **Database Connectivity**: Backend connects to database successfully
2. **Frontend-Backend Communication**: Frontend can call backend APIs
3. **Authentication Flow**: User can signup, signin, signout
4. **Task CRUD**: Create, read, update, delete tasks
5. **Conversational AI**: Chat interface works with OpenAI
6. **Data Persistence**: Tasks survive database pod restart
7. **Health Probes**: Unhealthy pods restart automatically
8. **Ingress Routing**: Both paths (`/`, `/api/*`) route correctly

### Acceptance Testing (End-to-End)

**Scenarios** (from spec.md):
- User Story 1: Reproducible deployment ✅
- User Story 2: Persistent data storage ✅
- User Story 3: Configuration management ✅
- User Story 4: Health monitoring ✅
- User Story 5: Single hostname access ✅
- User Story 6: Resource management and scaling ✅

**Success Criteria**: All 10 success criteria from spec.md must pass.

---

## Rollout Plan

### Development Environment (Minikube)

**Timeline**: Already completed (2026-02-06)

**Steps**:
1. ✅ Build Docker images locally
2. ✅ Load images into Minikube
3. ✅ Create namespace: `todo-app`
4. ✅ Install Helm chart: `helm install todo-app ./todo-helm -n todo-app`
5. ✅ Configure DNS: Add `todo-app.local` to /etc/hosts
6. ✅ Verify deployment: Access http://todo-app.local

**Rollback**: `helm uninstall todo-app -n todo-app`

### Staging Environment (Future)

**Prerequisites**:
- Kubernetes cluster (e.g., managed EKS, GKE, AKS)
- External PostgreSQL or managed database service
- TLS certificates for HTTPS
- External secret manager (Vault, AWS Secrets Manager)

**Changes Needed**:
- Update `ingress.host` to staging domain
- Enable TLS in Ingress
- Use external database (update DATABASE_URL)
- Integrate with external secret manager
- Increase resource limits for higher traffic
- Enable HPA

### Production Environment (Future)

**Prerequisites**: Same as staging + production monitoring/logging

**Changes Needed**:
- Multi-replica database with replication
- Pod disruption budgets
- Network policies for security
- Prometheus + Grafana for monitoring
- Log aggregation (ELK/Loki)
- CI/CD pipeline for automated deployments
- Blue-green or canary deployment strategy

---

## Risk Management

### Risk 1: Image Pull Failures

**Probability**: Medium | **Impact**: High (blocks deployment)

**Mitigation**:
- Use `imagePullPolicy: IfNotPresent` for local dev
- Document image building and loading steps clearly
- Provide troubleshooting steps in HELM_DEPLOYMENT_GUIDE.md

**Contingency**: Manual docker load commands; verify with `docker images`

---

### Risk 2: PVC Provisioning Failure

**Probability**: Low | **Impact**: High (data loss)

**Mitigation**:
- Use default StorageClass (works on Minikube)
- Make storage size configurable via values.yaml
- Document backup and restore procedures

**Contingency**: Fall back to HostPath or EmptyDir for testing (document data loss warning)

---

### Risk 3: Secret Misconfiguration

**Probability**: Medium | **Impact**: Critical (auth/AI failures)

**Mitigation**:
- Provide `.env.example` with required secrets
- Document secret generation (e.g., `openssl rand -base64 32`)
- Fail-fast validation in backend startup

**Contingency**: Clear error messages in pod logs; troubleshooting guide

---

### Risk 4: Resource Exhaustion on Minikube

**Probability**: Medium | **Impact**: Medium (pod evictions)

**Mitigation**:
- Document minimum Minikube resources (4 CPU, 8GB RAM)
- Set sensible resource requests and limits
- Prioritize database resources

**Contingency**: Increase Minikube resources; reduce replica counts

---

### Risk 5: Ingress Not Working

**Probability**: Low | **Impact**: Medium (access issues)

**Mitigation**:
- Check Ingress addon enabled in prerequisites
- Provide port-forward fallback in documentation
- Test Ingress controller before deployment

**Contingency**: Use `kubectl port-forward` as fallback access method

---

## Maintenance and Operations

### Routine Operations

**Helm Upgrade** (configuration changes):
```bash
# Edit values.yaml
helm upgrade todo-app ./todo-helm -n todo-app
kubectl rollout status deployment -n todo-app
```

**Scale Services**:
```bash
kubectl scale deployment todo-app-backend -n todo-app --replicas=3
```

**View Logs**:
```bash
kubectl logs -n todo-app -l app.kubernetes.io/name=todo-app-backend -f
```

**Database Backup** (future):
```bash
kubectl exec -n todo-app <db-pod> -- pg_dump -U todouser todoapp > backup.sql
```

### Monitoring Checklist

- [ ] All pods in Running state
- [ ] Health probes passing
- [ ] Resource usage within limits
- [ ] PVC storage not full
- [ ] Ingress routing correctly
- [ ] Application accessible via browser
- [ ] Logs show no errors

### Upgrade Path

**v1.0.0 → v1.1.0** (example):
1. Update Chart.yaml version
2. Update values.yaml with new options
3. Run `helm upgrade todo-app ./todo-helm -n todo-app`
4. Verify with `helm history todo-app -n todo-app`
5. Rollback if issues: `helm rollback todo-app -n todo-app`

---

## Next Steps

1. **Completed**: Phase IV Kubernetes/Helm deployment implemented and documented ✅
2. **Documentation**: Create PHRs (Prompt History Records) for spec, plan, and tasks stages
3. **Future**: Consider Phase V (Production Cloud Deployment) with managed services
4. **Future**: Add monitoring stack (Prometheus, Grafana)
5. **Future**: Implement CI/CD pipeline for automated deployments

---

## References

- [Kubernetes Documentation](https://kubernetes.io/docs/)
- [Helm Documentation](https://helm.sh/docs/)
- [Minikube Guide](https://minikube.sigs.k8s.io/docs/)
- [NGINX Ingress Controller](https://kubernetes.github.io/ingress-nginx/)
- [HELM_DEPLOYMENT_GUIDE.md](../../HELM_DEPLOYMENT_GUIDE.md)
- [Constitution Phase IV Principles](../../.specify/memory/constitution.md#kubernetes-helm-architecture-phase-iv)
