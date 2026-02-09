# Implementation Tasks: Phase IV – Kubernetes/Helm Local Deployment

**Feature**: 005-kubernetes-deployment
**Branch**: `main` (Phase-4 directory)
**Date**: 2026-02-05
**Total Tasks**: 68
**Estimated Effort**: 2-3 days
**Status**: ✅ COMPLETED (2026-02-06)

## Overview

This document breaks down the implementation of Phase IV Kubernetes/Helm Local Deployment into testable, executable tasks organized by implementation phase. The deployment was completed on 2026-02-06 and is documented in `HELM_DEPLOYMENT_GUIDE.md`.

**Implementation Phases**:
- **Phase 0**: Prerequisites and Setup ✅
- **Phase 1**: Helm Chart Scaffolding ✅
- **Phase 2**: Database Resources ✅
- **Phase 3**: Backend Resources ✅
- **Phase 4**: Frontend Resources ✅
- **Phase 5**: Ingress Configuration ✅
- **Phase 6**: HPA and Scaling Features ✅
- **Phase 7**: Documentation and Testing ✅

**Success Criteria**:
- ✅ Three-tier application deployed to Minikube
- ✅ Persistent data storage working (database survives pod restart)
- ✅ Single hostname access via Ingress (`todo-app.local`)
- ✅ Health probes configured and working
- ✅ Configuration separated (ConfigMaps and Secrets)
- ✅ Complete deployment documentation

## Task Legend

- `[x]` - Completed task
- `[P]` - Parallel execution possible (can run concurrently with other [P] tasks)
- `T###` - Task ID for reference

---

## Phase 0: Prerequisites and Setup

**Goal**: Ensure local environment ready for Kubernetes deployment.

**Duration**: 30 minutes

**Tasks**:

- [x] T001 Verify Minikube installed (`minikube version`)
- [x] T002 Verify Helm 3.0+ installed (`helm version`)
- [x] T003 Verify kubectl installed (`kubectl version --client`)
- [x] T004 Start Minikube with sufficient resources (`minikube start --cpus=4 --memory=8192 --driver=docker`)
- [x] T005 Verify Minikube is running (`minikube status`)
- [x] T006 Enable Ingress addon (`minikube addons enable ingress`)
- [x] T007 Verify Ingress controller pods running (`kubectl get pods -n ingress-nginx`)
- [x] T008 [P] Review backend Dockerfile for Kubernetes compatibility
- [x] T009 [P] Review frontend Dockerfile for Kubernetes compatibility
- [x] T010 [P] Verify backend health endpoint exists (`/api/v1/health`)
- [x] T011 Build backend Docker image (`docker build backend/ -t todo-backend:latest`)
- [x] T012 Build frontend Docker image (`docker build frontend/ -t todo-frontend:latest`)
- [x] T013 Configure Docker to use Minikube's daemon (`eval $(minikube docker-env)`)
- [x] T014 Load backend image into Minikube (`minikube image load todo-backend:latest`)
- [x] T015 Load frontend image into Minikube (`minikube image load todo-frontend:latest`)
- [x] T016 Verify images available in Minikube (`minikube image ls | grep todo`)

**Validation**:
```bash
minikube status
helm version
kubectl get pods -n ingress-nginx
docker images | grep todo
```

---

## Phase 1: Helm Chart Scaffolding

**Goal**: Create Helm chart directory structure and base configuration.

**Prerequisites**: Phase 0 complete

**Duration**: 1 hour

**Tasks**:

- [x] T017 Create `todo-helm/` directory in Phase-4 root
- [x] T018 Create `Chart.yaml` with name, version 1.0.0, appVersion 1.0.0, apiVersion v2
- [x] T019 Create `values.yaml` with global settings structure
- [x] T020 Add database configuration block to `values.yaml` (image, auth, persistence, resources)
- [x] T021 Add backend configuration block to `values.yaml` (image, replicas, env, secrets, resources, autoscaling)
- [x] T022 Add frontend configuration block to `values.yaml` (image, replicas, env, secrets, resources, autoscaling)
- [x] T023 Add ingress configuration block to `values.yaml` (enabled, className, host, annotations)
- [x] T024 Create `templates/` directory
- [x] T025 Create `templates/_helpers.tpl` with label helper templates
- [x] T026 Add `todo-app.name` helper (chart name)
- [x] T027 Add `todo-app.fullname` helper (release name + chart name)
- [x] T028 Add `todo-app.chart` helper (chart name + version)
- [x] T029 Add `todo-app.labels` helper (standard Kubernetes labels)
- [x] T030 Add `todo-app.selectorLabels` helper (app and instance labels)
- [x] T031 Create `templates/NOTES.txt` with post-install instructions
- [x] T032 Create `.helmignore` to exclude unnecessary files from chart package
- [x] T033 Create `README.md` in todo-helm/ with quick start guide

**Validation**:
```bash
helm lint todo-helm
helm template todo-app todo-helm --dry-run
```

---

## Phase 2: Database Resources

**Goal**: Deploy PostgreSQL with persistent storage.

**Prerequisites**: Phase 1 complete

**Duration**: 45 minutes

**Tasks**:

- [x] T034 Create `templates/pvc.yaml` for PostgreSQL persistent storage
- [x] T035 Configure PVC with 5Gi storage request, ReadWriteOnce access mode
- [x] T036 Make storage class configurable via `database.persistence.storageClass` in values.yaml
- [x] T037 Make storage size configurable via `database.persistence.size` in values.yaml
- [x] T038 Create `templates/database-deployment.yaml` with PostgreSQL container
- [x] T039 Use `postgres:16-alpine` image from values.yaml `database.image`
- [x] T040 Configure database authentication via environment variables (POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB)
- [x] T041 Mount PVC to `/var/lib/postgresql/data` in database container
- [x] T042 Add liveness probe using `pg_isready -U todouser` command
- [x] T043 Add readiness probe using `pg_isready -U todouser` command
- [x] T044 Configure probe timings (initialDelaySeconds: 5, periodSeconds: 10, timeoutSeconds: 5, failureThreshold: 3)
- [x] T045 Set resource requests (cpu: 250m, memory: 256Mi)
- [x] T046 Set resource limits (cpu: 500m, memory: 512Mi)
- [x] T047 Create `templates/database-service.yaml` with ClusterIP type
- [x] T048 Expose port 5432 in database service
- [x] T049 Use helper templates for labels and selectors in database resources

**Validation**:
```bash
helm install todo-app ./todo-helm -n todo-app --create-namespace --set database.enabled=true
kubectl get pvc -n todo-app
kubectl get pods -n todo-app -l app.kubernetes.io/name=todo-app-database
kubectl exec -n todo-app <db-pod> -- pg_isready -U todouser
```

---

## Phase 3: Backend Resources

**Goal**: Deploy FastAPI backend with database connectivity and secrets management.

**Prerequisites**: Phase 2 complete

**Duration**: 1 hour

**Tasks**:

- [x] T050 Create `templates/configmap.yaml` for backend environment variables
- [x] T051 Add backend ConfigMap section with non-sensitive env vars (DATABASE_URL, ENVIRONMENT, JWT_ALGORITHM, AI_MODEL, etc.)
- [x] T052 Template database URL using database service DNS name (`postgresql://{{ .Values.database.auth.username }}:***@todo-app-database:5432/{{ .Values.database.auth.database }}`)
- [x] T053 Create `templates/secret.yaml` for backend sensitive data
- [x] T054 Add backend Secret section with base64-encoded values (JWT_SECRET, OPENAI_API_KEY, REDIS_URL, database password)
- [x] T055 Create `templates/backend-deployment.yaml` with FastAPI container
- [x] T056 Use `todo-backend:latest` image from values.yaml `backend.image`
- [x] T057 Set image pull policy to IfNotPresent for local development
- [x] T058 Configure replicas from values.yaml `backend.replicas` (default 1)
- [x] T059 Inject environment variables from backend-config ConfigMap
- [x] T060 Inject secrets from backend-secret Secret
- [x] T061 Override DATABASE_URL to include password from Secret
- [x] T062 Add liveness probe using HTTP GET `/api/v1/health` on port 8000
- [x] T063 Add readiness probe using HTTP GET `/api/v1/health` on port 8000
- [x] T064 Configure probe timings (initialDelaySeconds: 30, periodSeconds: 10, timeoutSeconds: 5, failureThreshold: 3)
- [x] T065 Set resource requests (cpu: 500m, memory: 512Mi)
- [x] T066 Set resource limits (cpu: 1000m, memory: 1Gi)
- [x] T067 Create `templates/backend-service.yaml` with ClusterIP type
- [x] T068 Expose port 8000 in backend service

**Validation**:
```bash
kubectl get configmap -n todo-app backend-config
kubectl get secret -n todo-app backend-secret
kubectl get pods -n todo-app -l app.kubernetes.io/name=todo-app-backend
kubectl logs -n todo-app <backend-pod> --tail=50
curl -k http://$(kubectl get svc -n todo-app todo-app-backend -o jsonpath='{.spec.clusterIP}'):8000/api/v1/health
```

---

## Phase 4: Frontend Resources

**Goal**: Deploy Next.js frontend with Better Auth and backend connectivity.

**Prerequisites**: Phase 3 complete

**Duration**: 1 hour

**Tasks**:

- [x] T069 Add frontend ConfigMap section to `configmap.yaml`
- [x] T070 Configure frontend environment variables (NODE_ENV, NEXT_PUBLIC_CHATKIT_DOMAIN_KEY, NEXT_PUBLIC_API_URL, NEXT_PUBLIC_BACKEND_URL)
- [x] T071 Set NEXT_PUBLIC_BACKEND_URL to backend service DNS (`http://todo-app-backend:8000`)
- [x] T072 Template DATABASE_URL for Better Auth from database service
- [x] T073 Add frontend Secret section to `secret.yaml`
- [x] T074 Add BETTER_AUTH_SECRET and BETTER_AUTH_URL to frontend secret
- [x] T075 Create `templates/frontend-deployment.yaml` with Next.js container
- [x] T076 Use `todo-frontend:latest` image from values.yaml `frontend.image`
- [x] T077 Set image pull policy to IfNotPresent
- [x] T078 Configure replicas from values.yaml `frontend.replicas` (default 1)
- [x] T079 Inject environment variables from frontend-config ConfigMap
- [x] T080 Inject secrets from frontend-secret Secret
- [x] T081 Add liveness probe using HTTP GET `/` on port 3000
- [x] T082 Add readiness probe using HTTP GET `/` on port 3000
- [x] T083 Configure probe timings (initialDelaySeconds: 10, periodSeconds: 10, timeoutSeconds: 5, failureThreshold: 3)
- [x] T084 Set resource requests (cpu: 500m, memory: 512Mi)
- [x] T085 Set resource limits (cpu: 1000m, memory: 1Gi)
- [x] T086 Create `templates/frontend-service.yaml` with ClusterIP type
- [x] T087 Expose port 3000 in frontend service
- [x] T088 [P] Create Better Auth database schema manually (not automated in Helm chart)
- [x] T089 [P] Execute SQL to create `user`, `session`, `account`, `verification` tables in PostgreSQL

**Validation**:
```bash
kubectl get configmap -n todo-app frontend-config
kubectl get secret -n todo-app frontend-secret
kubectl get pods -n todo-app -l app.kubernetes.io/name=todo-app-frontend
kubectl logs -n todo-app <frontend-pod> --tail=50
kubectl exec -n todo-app <db-pod> -- psql -U todouser -d todoapp -c '\dt'
```

---

## Phase 5: Ingress Configuration

**Goal**: Enable single-hostname access with path-based routing.

**Prerequisites**: Phase 4 complete

**Duration**: 30 minutes

**Tasks**:

- [x] T090 Create `templates/ingress.yaml` with NGINX ingress class
- [x] T091 Make Ingress conditional based on `ingress.enabled` in values.yaml
- [x] T092 Configure hostname `todo-app.local` from `ingress.host`
- [x] T093 Add annotation `nginx.ingress.kubernetes.io/rewrite-target: /$2` for URL rewriting
- [x] T094 Add path rule for backend: `/api(/|$)(.*)` → `todo-app-backend:8000`
- [x] T095 Add path rule for frontend: `/` → `todo-app-frontend:3000`
- [x] T096 Set path type to `ImplementationSpecific` for regex support
- [x] T097 Use helper templates for labels in Ingress resource
- [x] T098 Add Minikube IP to `/etc/hosts` mapping to `todo-app.local`
- [x] T099 Verify Ingress resource created (`kubectl get ingress -n todo-app`)
- [x] T100 Verify Ingress has correct rules (`kubectl describe ingress -n todo-app`)
- [x] T101 Wait for Ingress address assignment (may take 1-2 minutes)

**Validation**:
```bash
kubectl get ingress -n todo-app
kubectl describe ingress todo-app-ingress -n todo-app
cat /etc/hosts | grep todo-app
curl http://todo-app.local
curl http://todo-app.local/api/v1/health
```

---

## Phase 6: HPA and Scaling Features

**Goal**: Add optional horizontal pod autoscaling configuration.

**Prerequisites**: Phase 5 complete

**Duration**: 30 minutes

**Tasks**:

- [x] T102 Create `templates/hpa.yaml` for HorizontalPodAutoscaler
- [x] T103 Make HPA conditional based on `backend.autoscaling.enabled` flag
- [x] T104 Create backend HPA targeting `todo-app-backend` deployment
- [x] T105 Configure minReplicas from `backend.autoscaling.minReplicas` (default 2)
- [x] T106 Configure maxReplicas from `backend.autoscaling.maxReplicas` (default 10)
- [x] T107 Set targetCPUUtilizationPercentage from values.yaml (default 70)
- [x] T108 Create frontend HPA section (conditional on `frontend.autoscaling.enabled`)
- [x] T109 Configure frontend HPA with same structure as backend
- [x] T110 Document how to enable HPA in values.yaml comments
- [x] T111 [P] Create `templates/serviceaccount.yaml` (optional resource)
- [x] T112 [P] Configure ServiceAccount name from values.yaml

**Validation** (with autoscaling enabled):
```bash
# Set backend.autoscaling.enabled: true in values.yaml
helm upgrade todo-app ./todo-helm -n todo-app
kubectl get hpa -n todo-app
kubectl describe hpa todo-app-backend-hpa -n todo-app
```

---

## Phase 7: Documentation and Testing

**Goal**: Provide comprehensive deployment documentation and verify end-to-end functionality.

**Prerequisites**: Phases 0-6 complete

**Duration**: 2 hours

**Tasks**:

- [x] T113 Create `HELM_DEPLOYMENT_GUIDE.md` in Phase-4 root
- [x] T114 Document overview section (what was done, features implemented)
- [x] T115 Document Step 1: Start Minikube (command + resource requirements)
- [x] T116 Document Step 2: Build and load Docker images
- [x] T117 Document Step 3: Configure secrets (JWT_SECRET, OPENAI_API_KEY, BETTER_AUTH_SECRET, database password)
- [x] T118 Document Step 4: Review and adjust resources (CPU/memory table)
- [x] T119 Document Step 5: Install Helm chart (`helm install` command)
- [x] T120 Document Step 6: Configure local DNS (/etc/hosts entry)
- [x] T121 Document Step 7: Verify deployment (kubectl commands)
- [x] T122 Document Step 8: Access the application (URLs for frontend, backend, API docs)
- [x] T123 Document monitoring and troubleshooting section
- [x] T124 Add troubleshooting guide for ImagePullBackOff errors
- [x] T125 Add troubleshooting guide for Ingress not working
- [x] T126 Add troubleshooting guide for database connection issues
- [x] T127 Add port-forward fallback commands for each service
- [x] T128 Document updates and maintenance section (helm upgrade, rollback, scale)
- [x] T129 Document cleanup procedures (helm uninstall, namespace deletion, /etc/hosts cleanup)
- [x] T130 Document Helm chart configuration reference (key values.yaml options)
- [x] T131 Add deployment checklist with all verification steps
- [x] T132 Update `todo-helm/README.md` with quick start guide
- [x] T133 Update `.specify/memory/constitution.md` with Phase IV principles (see separate docs task)
- [x] T134 [P] Test fresh deployment on clean Minikube cluster
- [x] T135 [P] Verify all pods reach Running state within 5 minutes
- [x] T136 [P] Test user signup flow (create account)
- [x] T137 [P] Test user signin flow (authenticate)
- [x] T138 [P] Test task creation via UI
- [x] T139 [P] Test task viewing and filtering
- [x] T140 [P] Test task update and deletion
- [x] T141 [P] Test conversational AI chat interface
- [x] T142 [P] Test database pod restart (verify data persistence)
- [x] T143 [P] Test backend pod restart (verify health probes)
- [x] T144 [P] Test frontend pod restart (verify readiness)
- [x] T145 [P] Test helm upgrade with configuration change
- [x] T146 [P] Test helm rollback functionality

**Validation** (End-to-End Test):
```bash
# Fresh deployment test
minikube delete
minikube start --cpus=4 --memory=8192
# Follow HELM_DEPLOYMENT_GUIDE.md from Step 1
# Verify all acceptance criteria from spec.md pass
```

---

## Dependencies & Execution Strategy

### Critical Path

The following phases must be executed sequentially (each depends on the previous):
1. Phase 0 (Prerequisites) → Phase 1 (Helm Scaffolding)
2. Phase 1 → Phase 2 (Database)
3. Phase 2 → Phase 3 (Backend) - Backend needs database running
4. Phase 3 → Phase 4 (Frontend) - Frontend needs backend for API calls
5. Phase 4 → Phase 5 (Ingress) - Ingress routes to existing services
6. Phase 5 → Phase 6 (HPA) - HPA targets existing deployments
7. Phase 6 → Phase 7 (Documentation) - Document complete system

### Parallel Opportunities

Within each phase, tasks marked with `[P]` can run in parallel:

**Phase 0**:
- T008, T009, T010 (Dockerfile reviews) - independent of each other

**Phase 4**:
- T088, T089 (Better Auth schema creation) - can happen while frontend pod starts

**Phase 7**:
- T134-T146 (Testing tasks) - multiple tests can run concurrently if multiple developers

### Resource Dependencies

**Database** (must exist before):
- Backend deployment (needs DATABASE_URL)
- Frontend deployment (needs DATABASE_URL for Better Auth)

**Backend** (must exist before):
- Frontend deployment (needs NEXT_PUBLIC_BACKEND_URL)
- Ingress configuration (backend path routing)

**Frontend** (must exist before):
- Ingress configuration (frontend path routing)

**Ingress Controller** (must exist before):
- Ingress resource creation

---

## Rollback Plan

If deployment fails at any phase:

**Phase 0-1**: Safe to restart, no Kubernetes resources created yet

**Phase 2-6**: Rollback with Helm:
```bash
helm rollback todo-app -n todo-app
# Or complete uninstall
helm uninstall todo-app -n todo-app
kubectl delete namespace todo-app
```

**Phase 7**: If documentation errors found, update files without affecting deployment

**Data Loss Protection**:
- PVC persists even after `helm uninstall` unless explicitly deleted
- To preserve data: Do NOT run `kubectl delete pvc -n todo-app`
- To completely clean: `kubectl delete namespace todo-app` (removes PVC)

---

## Post-Implementation Checklist

Use this checklist to verify Phase IV completion:

- [x] All 7 phases completed
- [x] Helm chart passes `helm lint todo-helm`
- [x] All pods in Running state (`kubectl get pods -n todo-app`)
- [x] Database data persists across pod restart
- [x] Frontend accessible at http://todo-app.local
- [x] Backend health check returns 200 at http://todo-app.local/api/v1/health
- [x] User can signup and signin successfully
- [x] Task CRUD operations work through UI
- [x] Conversational AI chat interface functional
- [x] HELM_DEPLOYMENT_GUIDE.md complete with troubleshooting
- [x] Constitution updated with Phase IV principles
- [x] Spec, plan, and tasks documentation created

---

## Lessons Learned

### What Went Well
- Helm chart structure with helper templates reduced repetition
- Separating ConfigMaps and Secrets improved security clarity
- PersistentVolumeClaim ensured data persistence worked reliably
- Health probes caught unhealthy pods and restarted automatically
- Path-based Ingress routing provided unified access point
- Comprehensive documentation enabled reproducible deployment

### Challenges Encountered
1. **Image Pull Failures**: Initially forgot to load images into Minikube's Docker daemon
   - **Solution**: Documented `minikube image load` step clearly

2. **Better Auth Schema Missing**: Backend created `users` table but Better Auth needed `user` (singular)
   - **Solution**: Manually created Better Auth tables; documented in guide

3. **Double API Routes**: `/api/api/v1/tasks` due to misconfigured `NEXT_PUBLIC_API_URL`
   - **Solution**: Set `NEXT_PUBLIC_API_URL=""` (empty string); rebuilt frontend image

4. **Database Connection String**: Template complexity for injecting password from Secret
   - **Solution**: Used Helm template functions to construct full URL with credentials

5. **Text Visibility Issues**: White text on white background in signin/signup forms
   - **Solution**: Updated Input.tsx styling; applied to Phase-3 as well

### Future Improvements
- Automate Better Auth schema creation in database init script
- Add database backup job (CronJob) for scheduled backups
- Implement monitoring stack (Prometheus, Grafana)
- Add NetworkPolicies for pod-to-pod security
- Create production-ready chart variant for cloud deployment

---

## Related Documentation

- **Spec**: [spec.md](./spec.md) - Feature requirements and success criteria
- **Plan**: [plan.md](./plan.md) - Architectural decisions and design
- **Deployment Guide**: [HELM_DEPLOYMENT_GUIDE.md](../../HELM_DEPLOYMENT_GUIDE.md) - Complete deployment instructions
- **Constitution**: [constitution.md](../../.specify/memory/constitution.md) - Phase IV principles
- **Helm Chart**: [todo-helm/](../../todo-helm/) - Complete Helm chart with templates and values
