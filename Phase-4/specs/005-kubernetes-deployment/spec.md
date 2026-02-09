# Feature Specification: Phase IV – Kubernetes/Helm Local Deployment

**Feature ID**: `005-kubernetes-deployment`
**Created**: 2026-02-05
**Status**: Implemented
**Phase**: IV - Kubernetes/Helm Deployment

## Overview

This specification documents the Kubernetes deployment architecture for the Todo App using Helm charts. Phase IV extends the full-stack conversational AI application (Phases I-III) with production-ready local Kubernetes deployment on Minikube, enabling declarative infrastructure-as-code, scalability, and operational readiness.

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Reproducible Local Deployment (Priority: P1)

As a developer, I want to deploy the entire Todo App stack to my local Minikube cluster using a single Helm command so that I can test the application in a Kubernetes environment without manual configuration.

**Why this priority**: Helm deployment is the foundation of Phase IV. Without it, the application cannot run on Kubernetes. This is the core value proposition of this phase.

**Independent Test**: Can be fully tested by running `helm install` on a fresh Minikube cluster and verifying all pods start successfully. Delivers the value of one-command deployment.

**Acceptance Scenarios**:

1. **Given** Minikube is running with Ingress enabled, **When** I run `helm install todo-app ./todo-helm`, **Then** all three services (database, backend, frontend) deploy successfully
2. **Given** the Helm chart is installed, **When** I check pod status, **Then** all pods reach Running state within 5 minutes
3. **Given** the deployment is complete, **When** I access `http://todo-app.local`, **Then** the frontend loads and I can sign in
4. **Given** the application is running, **When** I restart a pod, **Then** it recovers automatically and reconnects to other services

---

### User Story 2 - Persistent Data Storage (Priority: P1)

As a developer, I want database data to persist across pod restarts and redeployments so that user data is never lost when containers are recreated.

**Why this priority**: Data persistence is critical for any production-like deployment. Without it, all tasks and user accounts are lost on pod restart, making the deployment unusable.

**Independent Test**: Can be fully tested by creating tasks, deleting the database pod, and verifying data still exists after pod recreation. Delivers the value of data durability.

**Acceptance Scenarios**:

1. **Given** the database pod is running, **When** I create a PersistentVolumeClaim, **Then** a 5Gi volume is provisioned
2. **Given** I have created tasks in the application, **When** the database pod is deleted, **Then** the new pod mounts the same volume and all data is intact
3. **Given** I run `helm upgrade`, **When** pods are recreated, **Then** all user accounts and tasks remain accessible
4. **Given** Minikube is stopped, **When** I restart it and the application, **Then** database data persists from previous session

---

### User Story 3 - Configuration Management (Priority: P1)

As a developer, I want environment variables and secrets managed through Kubernetes ConfigMaps and Secrets so that I can change configuration without rebuilding Docker images.

**Why this priority**: Separating configuration from code is a Kubernetes best practice and essential for managing different environments (dev/prod). Critical for security and maintainability.

**Independent Test**: Can be tested by updating values.yaml, running `helm upgrade`, and verifying services use new configuration. Delivers the value of runtime configuration management.

**Acceptance Scenarios**:

1. **Given** I update `values.yaml` with new environment variables, **When** I run `helm upgrade`, **Then** ConfigMaps are updated and pods use new values after restart
2. **Given** I update JWT_SECRET in values.yaml, **When** I run `helm upgrade`, **Then** the Secret is updated and backend uses the new secret
3. **Given** I set `OPENAI_API_KEY` in values.yaml, **When** the backend starts, **Then** it successfully connects to OpenAI without hardcoded keys
4. **Given** database credentials are in values.yaml, **When** backend starts, **Then** it connects using the templated connection string

---

### User Story 4 - Health Monitoring and Self-Healing (Priority: P2)

As a developer, I want Kubernetes to automatically restart unhealthy pods using liveness and readiness probes so that the application recovers from transient failures without manual intervention.

**Why this priority**: Self-healing is a key Kubernetes feature that makes deployments more reliable. Important for production-readiness but application can function without it in simple scenarios.

**Independent Test**: Can be tested by simulating pod failures and verifying Kubernetes restarts them. Delivers the value of automatic recovery.

**Acceptance Scenarios**:

1. **Given** health probes are configured, **When** a pod becomes unresponsive, **Then** Kubernetes restarts it automatically
2. **Given** backend has a `/api/v1/health` endpoint, **When** the probe checks health, **Then** unhealthy pods are removed from service rotation
3. **Given** frontend has liveness probes, **When** it crashes, **Then** Kubernetes detects and restarts the pod
4. **Given** database is starting up, **When** readiness probe runs, **Then** it prevents traffic until database is ready

---

### User Story 5 - Single Hostname Access with Ingress (Priority: P2)

As a developer, I want all services accessible through a single hostname (`todo-app.local`) with path-based routing so that I don't need to manage multiple ports or hostnames.

**Why this priority**: Ingress provides a production-like URL structure and simplifies access. Enhances usability significantly but port-forwarding can be used as fallback.

**Independent Test**: Can be tested by accessing frontend and backend through different paths on the same hostname. Delivers the value of unified access point.

**Acceptance Scenarios**:

1. **Given** Ingress is configured, **When** I access `http://todo-app.local/`, **Then** I reach the Next.js frontend
2. **Given** Ingress rules are set, **When** I access `http://todo-app.local/api/v1/health`, **Then** the request routes to the backend
3. **Given** DNS is configured, **When** I open `http://todo-app.local` in a browser, **Then** the application loads without CORS errors
4. **Given** multiple services are running, **When** I use path-based routing, **Then** each service receives only its designated traffic

---

### User Story 6 - Resource Management and Scaling (Priority: P3)

As a developer, I want to configure resource limits and horizontal pod autoscaling so that the application uses resources efficiently and can scale under load.

**Why this priority**: Important for production environments but not critical for local development. Application functions without autoscaling; it just won't scale automatically.

**Independent Test**: Can be tested by configuring HPA and simulating load to trigger scaling. Delivers the value of automatic capacity management.

**Acceptance Scenarios**:

1. **Given** resource limits are defined, **When** pods start, **Then** Kubernetes enforces CPU and memory constraints
2. **Given** HPA is enabled, **When** CPU usage exceeds 70%, **Then** additional backend pods are created
3. **Given** load decreases, **When** CPU drops below threshold, **Then** excess pods are terminated
4. **Given** database has resource requests, **When** scheduling occurs, **Then** Kubernetes ensures sufficient node capacity

---

### Edge Cases

- **Image Pull Failures**: What happens when Docker images are not available in Minikube's daemon?
- **Secret Misconfiguration**: How does the system handle missing or invalid JWT_SECRET or OPENAI_API_KEY?
- **Volume Provisioning Failures**: What happens when PersistentVolumeClaim cannot be satisfied?
- **Ingress Controller Not Ready**: How does the application behave when Ingress addon is disabled?
- **Resource Exhaustion**: What happens when Minikube runs out of CPU or memory?
- **Helm Upgrade Conflicts**: How are conflicting configuration changes handled during upgrades?
- **Database Migration Failures**: What happens if Alembic migrations fail during backend startup?
- **Port Conflicts**: How does the system handle port conflicts on the host machine?
- **Multiple Helm Releases**: What happens if someone tries to install the chart twice in the same namespace?
- **Namespace Deletion**: How is cleanup handled when the namespace is deleted unexpectedly?

## Requirements *(mandatory)*

### Functional Requirements

#### Helm Chart Structure
- **FR-001**: Helm chart MUST be located in `todo-helm/` directory with Chart.yaml version 1.0.0
- **FR-002**: Chart MUST include templates for all Kubernetes resources (Deployments, Services, ConfigMaps, Secrets, Ingress, PVC)
- **FR-003**: Chart MUST use `values.yaml` as single source of configuration
- **FR-004**: Chart MUST include helper templates in `_helpers.tpl` for consistent labeling
- **FR-005**: Chart MUST provide post-installation instructions via `NOTES.txt`

#### Three-Tier Architecture Deployment
- **FR-006**: Chart MUST deploy PostgreSQL database with persistent storage
- **FR-007**: Chart MUST deploy FastAPI backend with health endpoints
- **FR-008**: Chart MUST deploy Next.js frontend with Better Auth
- **FR-009**: Each service MUST have a dedicated Deployment manifest
- **FR-010**: Each service MUST have a ClusterIP Service for internal communication

#### Configuration Management
- **FR-011**: Environment variables MUST be stored in ConfigMaps (backend-config, frontend-config)
- **FR-012**: Sensitive data (JWT_SECRET, OPENAI_API_KEY, database password) MUST be stored in Secrets
- **FR-013**: Database connection string MUST be auto-generated from templates using Secret values
- **FR-014**: ConfigMaps MUST support both local (Minikube) and production configurations
- **FR-015**: Secrets MUST be base64-encoded in Kubernetes but plain-text in values.yaml for developer convenience

#### Persistent Storage
- **FR-016**: Database MUST use a PersistentVolumeClaim for data storage
- **FR-017**: PVC MUST request 5Gi storage with ReadWriteOnce access mode
- **FR-018**: Database pod MUST mount the PVC at `/var/lib/postgresql/data`
- **FR-019**: Data MUST persist across pod restarts and Helm upgrades
- **FR-020**: Storage class and size MUST be configurable via values.yaml

#### Health Probes
- **FR-021**: Backend MUST have liveness probe checking `/api/v1/health`
- **FR-022**: Backend MUST have readiness probe checking `/api/v1/health`
- **FR-023**: Frontend MUST have liveness probe checking root path `/`
- **FR-024**: Database MUST have liveness probe using `pg_isready` command
- **FR-025**: Probe timings (initial delay, period, timeout) MUST be configurable

#### Networking and Ingress
- **FR-026**: Ingress MUST route `/*` to frontend service
- **FR-027**: Ingress MUST route `/api/*` to backend service
- **FR-028**: Ingress MUST use hostname `todo-app.local` for local development
- **FR-029**: All services MUST use ClusterIP type (not NodePort or LoadBalancer)
- **FR-030**: Backend MUST be accessible from frontend using service DNS name

#### Resource Management
- **FR-031**: All deployments MUST define resource requests (CPU, memory)
- **FR-032**: All deployments MUST define resource limits (CPU, memory)
- **FR-033**: Database MUST have priority in resource allocation (higher requests)
- **FR-034**: HPA configuration MUST be provided but optional (can be disabled)
- **FR-035**: HPA MUST target CPU utilization percentage when enabled

#### Container Standards
- **FR-036**: Docker images MUST use multi-stage builds for optimization
- **FR-037**: Images MUST be tagged with semantic versions (supports `:latest` for dev)
- **FR-038**: Image pull policy MUST be IfNotPresent for local development
- **FR-039**: Backend MUST run Alembic migrations before starting uvicorn server
- **FR-040**: Containers SHOULD run as non-root users where possible

#### Deployment Strategy
- **FR-041**: `helm install` MUST be the primary deployment method
- **FR-042**: `helm upgrade` MUST support rolling updates without downtime
- **FR-043**: `helm rollback` MUST allow reverting to previous releases
- **FR-044**: Helm MUST maintain revision history for at least 10 releases
- **FR-045**: Deployment MUST be reproducible from values.yaml and templates

### Key Entities

- **Helm Release**: Represents a deployed instance of the chart. Contains revision history, values, and status. Managed by Helm in Kubernetes as Secrets.

- **ConfigMap**: Stores non-sensitive environment variables for backend and frontend. Key attributes include database URLs, AI model settings, rate limits, and feature flags.

- **Secret**: Stores sensitive data (JWT secrets, API keys, database passwords). Automatically base64-encoded by Kubernetes. Referenced by pods via environment variables.

- **PersistentVolumeClaim**: Requests storage from the cluster. Database pod mounts this to persist PostgreSQL data across restarts.

- **Ingress**: Defines HTTP routing rules. Routes traffic from `todo-app.local` to appropriate services based on path prefix.

- **Service**: Exposes pods within the cluster. ClusterIP services provide stable DNS names for inter-service communication.

- **Deployment**: Manages pod replicas for each application component. Handles rolling updates, health checks, and pod lifecycle.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Developer can deploy entire stack to fresh Minikube cluster in under 10 minutes using documented steps
- **SC-002**: All three pods (database, backend, frontend) reach Running state within 5 minutes of `helm install`
- **SC-003**: Application is accessible via `http://todo-app.local` with fully functional authentication and task management
- **SC-004**: Database data persists across pod deletions (100% data retention after pod restart)
- **SC-005**: `helm upgrade` successfully updates configuration without manual pod restarts
- **SC-006**: Health probes detect and restart unhealthy pods within 30 seconds of failure
- **SC-007**: Path-based routing works correctly (frontend at `/`, backend at `/api/*`) with zero routing errors
- **SC-008**: Secrets are never exposed in logs or pod descriptions (100% security compliance)
- **SC-009**: Resource limits prevent any single pod from consuming more than allocated CPU/memory
- **SC-010**: Complete deployment process documented in HELM_DEPLOYMENT_GUIDE.md with reproducible steps

## Assumptions *(mandatory)*

1. **Minikube Availability**: Developers have Minikube installed and can allocate 4 CPU cores and 8GB RAM
2. **Helm Installation**: Helm 3.0+ is installed and accessible in PATH
3. **kubectl Configuration**: kubectl is configured to communicate with Minikube cluster
4. **Docker Daemon Access**: Developer can build Docker images locally and load them into Minikube
5. **Network Access**: Local machine can resolve `todo-app.local` via /etc/hosts configuration
6. **OpenAI API Key**: Valid OpenAI API key available for conversational AI features
7. **No External Database**: Local PostgreSQL on Kubernetes is sufficient for development; production may use external database
8. **Single Cluster**: Deployment targets single Minikube cluster; multi-cluster support not required
9. **Namespace Isolation**: Each environment (dev/staging) uses separate Kubernetes namespace
10. **Static Configuration**: Configuration changes require Helm upgrade (no dynamic config reload)

## Scope *(mandatory)*

### In Scope

1. **Helm Chart Components**
   - Chart.yaml with metadata and version
   - values.yaml with all configuration parameters
   - Template files for all Kubernetes resources
   - Helper templates for labels and selectors
   - NOTES.txt for post-installation instructions

2. **Kubernetes Resources**
   - Deployments for database, backend, frontend
   - Services for inter-service communication
   - ConfigMaps for environment variables
   - Secrets for sensitive data
   - PersistentVolumeClaim for database storage
   - Ingress for HTTP routing
   - HorizontalPodAutoscaler (optional)
   - ServiceAccount (optional)

3. **Configuration Management**
   - Database credentials (username, password, database name)
   - JWT secrets for authentication
   - OpenAI API key for conversational AI
   - Redis URL for rate limiting
   - Resource limits and requests
   - Replica counts
   - Autoscaling parameters

4. **Deployment Features**
   - One-command installation via `helm install`
   - Rolling updates via `helm upgrade`
   - Rollback capability via `helm rollback`
   - Declarative infrastructure-as-code
   - Version-controlled Helm chart

5. **Operational Features**
   - Health checks (liveness and readiness probes)
   - Resource management (CPU/memory limits)
   - Persistent data storage
   - Automatic pod restarts on failure
   - Horizontal scaling (optional)

6. **Documentation**
   - Complete HELM_DEPLOYMENT_GUIDE.md
   - values.yaml comments explaining all options
   - README.md in todo-helm/ directory
   - Troubleshooting guide for common issues
   - Constitution.md updated with Kubernetes principles

### Out of Scope

1. **Production Cloud Deployment**
   - AWS EKS, Google GKE, Azure AKS configurations
   - Cloud-specific storage classes
   - Cloud load balancers
   - Managed database services (RDS, Cloud SQL)

2. **Advanced Security**
   - NetworkPolicies for pod-to-pod traffic control
   - PodSecurityPolicies or PodSecurityStandards
   - External secret management (Vault, AWS Secrets Manager)
   - TLS/HTTPS certificates
   - Image vulnerability scanning
   - Runtime security monitoring

3. **Advanced Operational Features**
   - Monitoring stack (Prometheus, Grafana)
   - Log aggregation (ELK, Loki)
   - Distributed tracing
   - Service mesh (Istio, Linkerd)
   - GitOps deployment (ArgoCD, Flux)

4. **High Availability**
   - Multi-replica database with replication
   - Pod disruption budgets
   - Pod anti-affinity rules
   - Multi-zone deployments

5. **CI/CD Integration**
   - Automated Helm chart testing
   - Image building pipeline
   - Automated deployment on git push
   - Release automation

6. **Multi-Environment Management**
   - Separate charts for dev/staging/prod
   - Environment-specific value files
   - Helmfile for multi-release management

7. **Advanced Networking**
   - Multiple ingress controllers
   - External DNS integration
   - TCP/UDP ingress
   - WebSocket routing optimization

## Dependencies *(mandatory)*

### Infrastructure Dependencies

1. **Minikube**: Local Kubernetes cluster (version 1.25+)
2. **Helm**: Package manager for Kubernetes (version 3.0+)
3. **kubectl**: Kubernetes command-line tool
4. **Docker**: Container runtime for building images
5. **Ingress Controller**: NGINX Ingress addon for Minikube

### Application Dependencies

1. **PostgreSQL Image**: `postgres:16-alpine` from Docker Hub
2. **Backend Image**: `todo-backend:latest` (built locally)
3. **Frontend Image**: `todo-frontend:latest` (built locally)
4. **OpenAI API**: Valid API key for GPT-4 access

### Configuration Dependencies

1. **values.yaml**: All configuration values must be set before installation
2. **Secrets**: JWT_SECRET, BETTER_AUTH_SECRET, OPENAI_API_KEY must be generated
3. **/etc/hosts**: Must map Minikube IP to `todo-app.local`
4. **Resource Availability**: Minikube must have 4+ CPU cores and 8+ GB RAM

### Development Dependencies

1. **Phase III Completion**: Conversational AI features must be implemented and tested
2. **Docker Images Built**: Backend and frontend Dockerfiles must produce working images
3. **Database Migrations**: Alembic migrations must run successfully
4. **Better Auth Setup**: Frontend authentication must work with database schema

## Non-Functional Requirements *(optional)*

### Performance
- **NFR-001**: Helm install completes in under 5 minutes on standard hardware
- **NFR-002**: Pod startup time under 2 minutes for each service
- **NFR-003**: Health probe overhead under 5% CPU per pod
- **NFR-004**: Ingress routing adds less than 10ms latency

### Reliability
- **NFR-005**: Database data persistence guaranteed at 100% (no data loss on pod restart)
- **NFR-006**: Health probes detect failures within 30 seconds
- **NFR-007**: Automatic pod restart within 1 minute of liveness failure
- **NFR-008**: Helm rollback completes in under 2 minutes

### Security
- **NFR-009**: Secrets stored only in Kubernetes Secret resources (not ConfigMaps or logs)
- **NFR-010**: Secrets base64-encoded in Kubernetes but plain-text in values.yaml (not committed to git)
- **NFR-011**: Database password not exposed in pod environment variable listings
- **NFR-012**: Containers run as non-root users where possible

### Maintainability
- **NFR-013**: Helm chart follows standard directory structure and naming conventions
- **NFR-014**: All configuration centralized in values.yaml (no hardcoded values in templates)
- **NFR-015**: Template files use helper functions for DRY principles
- **NFR-016**: HELM_DEPLOYMENT_GUIDE.md provides complete deployment documentation

### Scalability
- **NFR-017**: Backend and frontend support horizontal scaling (multiple replicas)
- **NFR-018**: Database designed for vertical scaling (resource limit increases)
- **NFR-019**: HPA configuration supports scaling to 10 replicas
- **NFR-020**: Service discovery via DNS scales with replica count

## References

- **HELM_DEPLOYMENT_GUIDE.md**: Complete deployment guide with step-by-step instructions, troubleshooting, and maintenance procedures
- **todo-helm/README.md**: Quick start guide and chart overview
- **todo-helm/values.yaml**: Full configuration reference with inline documentation
- **.specify/memory/constitution.md**: Phase IV principles and architectural constraints
- **Phase III Spec** (004-conversational-ai): Application features deployed by this chart
