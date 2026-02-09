---
id: 002
title: Design Helm Chart Architecture Plan
stage: plan
date: 2026-02-09
surface: agent
model: claude-sonnet-4-5-20250929
feature: 005-kubernetes-deployment
branch: main
user: sohaib
command: continuation from spec creation
labels: ["kubernetes", "helm", "architecture", "planning", "phase-4"]
links:
  spec: /home/sohaib/hackathon2/Todo-app/Phase-4/specs/005-kubernetes-deployment/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - /home/sohaib/hackathon2/Todo-app/Phase-4/specs/005-kubernetes-deployment/plan.md
tests:
  - Helm chart structure matches plan design
  - All architectural decisions traceable to implementation
  - Constitution principles validated
---

## Prompt

Continuing retrospective documentation for Phase-4 Kubernetes/Helm deployment. After creating spec.md, now need to document the architectural decisions and implementation plan that guided the actual Helm chart development.

User request context:
> "...and after that also create a history/prompts for spec, plan and task and also maintain Phase-4/specs..."

Task: Create plan.md documenting:
- Helm chart architecture and design decisions
- ConfigMap vs Secret separation strategy
- PersistentVolumeClaim approach for database storage
- Ingress path-based routing design
- Health probe configuration
- Resource management strategy
- Implementation phases (0-7)

## Response snapshot

Created `specs/005-kubernetes-deployment/plan.md` documenting the Helm chart architecture with the following structure:

**Summary**:
- Deploy full-stack AI Todo app to local Kubernetes using Helm
- Three-tier architecture: PostgreSQL, FastAPI, Next.js
- Single Helm release managing all resources
- Target: Minikube for local development

**Technical Context**:
- Infrastructure: Kubernetes 1.25+ on Minikube, Helm 3.0+, Docker, NGINX Ingress
- Container Images: postgres:16-alpine, todo-backend:latest, todo-frontend:latest
- Networking: ClusterIP services, Ingress hostname `todo-app.local`
- Performance: <5 min install, <2 min pod startup, <50ms PVC latency
- Constraints: Local dev only, single cluster, manual image building, HTTP only
- Scale: 1-3 developers, 3 deployments, ~15 templates, ~2 CPU/2GB RAM minimum

**Constitution Check** (✅ All principles satisfied):
- Kubernetes/Helm Architecture: Declarative templates, semantic versioning, dedicated manifests
- Container Standards: Multi-stage builds, semantic tags, non-root users
- Configuration Management: ConfigMaps vs Secrets separation, templated connection strings
- Health & Observability: Health endpoints, liveness/readiness probes, resource limits
- Networking & Ingress: ClusterIP internal, single Ingress, path-based routing
- Data Persistence: PVC for PostgreSQL, configurable storage, backup docs
- Deployment Strategy: Helm-based, rollback support, reproducible
- Local Development: Minikube-optimized, port-forward fallback, Ingress addon
- Resource Management: Optional HPA, sensible quotas, horizontal scaling for stateless

**Complexity Tracking** (Medium complexity):
- Helm Templates: ~15 YAML files - justified for declarative deployment
- ConfigMap/Secret Management: Dual-layer config - Kubernetes best practice
- Ingress Configuration: Path-based routing - unified hostname requirement
- PersistentVolumeClaim: Volume lifecycle - data persistence requirement
- Health Probes: Multiple probes per pod - self-healing requirement
- Resource Limits: CPU/memory tuning - prevent resource exhaustion

**Helm Chart Structure**:
- Chart.yaml, values.yaml (250+ lines), README.md, .helmignore
- templates/: _helpers.tpl, NOTES.txt, 12 resource manifests
- ConfigMaps (backend/frontend env vars), Secrets (JWT, API keys, DB password)
- PVC (5Gi PostgreSQL), 3 Deployments, 3 Services, 1 Ingress, optional HPA

**Architectural Decisions** (7 major decisions documented):

1. **Helm Over Raw YAML**: Industry standard, templating, package management, rollback
2. **ConfigMaps vs Secrets**: Hybrid approach - non-sensitive in ConfigMaps, credentials in Secrets
3. **PVC for Database**: Data persistence, cloud-portable, survives pod lifecycle
4. **Single Ingress with Paths**: Production-like, single domain, simplified CORS, `/` → frontend, `/api/*` → backend
5. **Health Probes (Both)**: Liveness restarts crashed pods, Readiness prevents traffic to starting pods
6. **Resource Limits + Requests**: Requests guarantee capacity, Limits prevent starvation
7. **HPA Optional**: Not needed for local dev, easily enabled for production

**Implementation Phases** (0-7):
- Phase 0: Prerequisites (Minikube, Helm, kubectl, images) ✅
- Phase 1: Helm scaffolding (Chart.yaml, values.yaml, helpers) ✅
- Phase 2: Database (PVC, deployment, service, probes) ✅
- Phase 3: Backend (ConfigMap, Secret, deployment, service) ✅
- Phase 4: Frontend (ConfigMap, Secret, deployment, service, Better Auth schema) ✅
- Phase 5: Ingress (path-based routing, DNS config) ✅
- Phase 6: HPA (optional autoscaling) ✅
- Phase 7: Documentation (HELM_DEPLOYMENT_GUIDE.md, testing) ✅

**Testing Strategy**:
- Unit: helm lint, helm template --dry-run
- Integration: kubectl commands, curl tests, psql verification
- Acceptance: All 6 user stories from spec.md validated

**Rollout Plan**:
- Development: ✅ Completed 2026-02-06 on Minikube
- Staging: Future (managed K8s, external DB, TLS, external secrets)
- Production: Future (multi-replica DB, pod disruption budgets, network policies, monitoring)

**Risk Management** (5 risks documented with mitigation):
1. Image Pull Failures: Use IfNotPresent, document loading steps
2. PVC Provisioning Failure: Use default StorageClass, document backup
3. Secret Misconfiguration: Provide .env.example, fail-fast validation
4. Resource Exhaustion: Document minimum resources, set sensible limits
5. Ingress Not Working: Check addon enabled, port-forward fallback

**Maintenance Operations**:
- Helm upgrade for config changes
- kubectl scale for manual scaling
- kubectl logs for debugging
- pg_dump for database backup (future)

## Outcome

- ✅ Impact: Documented complete architectural design and implementation plan for Helm chart. All 7 major decisions justified with trade-offs. Provides blueprint for understanding deployment structure and rationale.
- 🧪 Tests: Defined testing strategy across unit (helm lint), integration (kubectl), and acceptance (user stories) levels. All phases include validation commands.
- 📁 Files: Created `specs/005-kubernetes-deployment/plan.md` (630 lines) with comprehensive architecture documentation including constitution check, complexity tracking, architectural decisions, and implementation phases.
- 🔁 Next prompts: Create tasks.md breaking down 7 implementation phases into granular, executable tasks with dependencies and parallel execution opportunities.
- 🧠 Reflection: Plan required extracting design decisions from implemented Helm chart templates and HELM_DEPLOYMENT_GUIDE.md. Architectural decisions documented with options considered, trade-offs, and rationale. Implementation phases reflect actual development path (Phase 0→1→2→3→4→5→6→7).

## Evaluation notes (flywheel)

- Failure modes observed: None. Plan creation benefited from completed implementation - could document what actually worked vs theoretical design.
- Graders run and results (PASS/FAIL): Manual review - PASS. All phases documented with validation commands, architectural decisions justified, constitution principles verified, complexity tracking complete.
- Prompt variant (if applicable): Retrospective planning (documenting after implementation) vs prospective planning (designing before implementation)
- Next experiment (smallest change to try): Consider adding architecture diagrams (three-tier topology, Ingress routing flow) to visualize design decisions
