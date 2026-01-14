# Claude Code Custom Agents & Skills

This directory contains custom agent configurations and skills for specialized authentication tasks.

## What are Custom Agents?

Custom agents are specialized sub-agents that Claude can spawn for specific tasks. They are defined in YAML files that specify:
- **Model**: Which Claude model to use (opus, sonnet, haiku)
- **Tools**: Which tools the agent can access (bash, read, write, etc.)
- **Skills**: Which skills the agent should use
- **Description**: When to use this agent

## Available Agents

### 1. better-auth Agent

**File**: `better-auth.md`

Specialized agent for implementing Better-Auth authentication services.

**When to use:**
```
You: "Setup Better-Auth for my project"
You: "Add custom user fields to auth service"
You: "Generate auth service with JWT support"
```

**What it does:**
- Uses **Opus model** for complex auth service setup
- Has access to the **better-auth skill** (scripts and comprehensive docs)
- Can autonomously implement complete Node.js/TypeScript auth systems
- Handles database configuration, custom fields, and security settings
- Uses **Context7 MCP** to fetch latest Better-Auth documentation

### 2. frontend-auth-integration Agent

**File**: `frontend-auth-integration.md`

Specialized agent for integrating Better-Auth into React and Vue frontends.

**When to use:**
```
You: "Add login page to React app"
You: "Integrate Better-Auth with Vue frontend"
You: "Protect frontend routes with authentication"
You: "Setup auth client and session management"
```

**What it does:**
- Uses **Opus model** for complex frontend integration
- Has access to the **frontend-auth-integration skill**
- Implements login/signup UI components
- Sets up session management with useSession hooks
- Configures route protection and auth state
- Uses **Context7 MCP** to fetch latest docs for @better-auth/react, @better-auth/vue, React Router, and Vue Router

### 3. backend-auth-integration Agent

**File**: `backend-auth-integration.md`

Specialized agent for integrating Better-Auth into Python FastAPI backends.

**When to use:**
```
You: "Protect FastAPI endpoints with authentication"
You: "Validate Better-Auth sessions in Python"
You: "Verify JWT tokens in FastAPI"
You: "Add auth middleware to Python backend"
```

**What it does:**
- Uses **Opus model** for complex backend integration
- Has access to the **backend-auth-integration skill**
- Implements session validation middleware
- Sets up JWT token verification
- Creates FastAPI dependencies for auth
- Handles CORS configuration for auth requests
- Uses **Context7 MCP** to fetch latest docs for FastAPI, httpx, and PyJWT

### 4. jwt-access-token Agent

**File**: `jwt-access-token.md`

Specialized agent for solving the "user logged in but backend doesn't know" problem.

**When to use:**
```
You: "User logged in but backend returns 401 Unauthorized"
You: "How do I send JWT tokens to backend?"
You: "Backend not getting JWT tokens"
You: "Frontend and backend on different ports, auth not working"
```

**What it does:**
- Uses **Opus model** for debugging auth flows
- Has access to the **jwt-access-token skill**
- Implements `getJWTToken()` pattern for frontend
- Fixes Authorization header issues
- Diagnoses JWT token flow problems
- Solves the specific problem: session cookies don't work with backend API

### 5. auth-troubleshooting Agent

**File**: `auth-troubleshooting.md`

Specialized agent for diagnosing and fixing all authentication problems.

**When to use:**
```
You: "Auth not working"
You: "Getting CORS errors"
You: "Session not persisting after refresh"
You: "JWT verification failed"
You: "Rate limiting blocking users"
You: "Custom fields not saving"
```

**What it does:**
- Uses **Opus model** for comprehensive debugging
- Has access to the **auth-troubleshooting skill**
- Diagnoses 8 common authentication problems
- Fixes CORS configuration issues
- Resolves session persistence problems
- Debugs JWT verification failures
- Adjusts rate limiting
- Fixes custom field configuration

## Context7 MCP Integration

All authentication agents now use the **Context7 MCP** (Model Context Protocol) to fetch the latest documentation from official sources. This ensures agents always have up-to-date information about:

- **Better-Auth**: Latest API changes, new features, and best practices
- **@better-auth/react**: React hooks and components
- **@better-auth/vue**: Vue composables and patterns
- **FastAPI**: Python web framework updates
- **React Router / Vue Router**: Routing and navigation
- **httpx / PyJWT**: HTTP clients and JWT libraries

### How Context7 Works

When an agent needs documentation:
1. Calls `mcp__context7__resolve-library-id` to find the right library
2. Calls `mcp__context7__query-docs` to fetch relevant documentation
3. Uses the latest docs to generate accurate, up-to-date code

This means the agents automatically adapt to library updates without manual skill updates!

## Available Skills

### 1. better-auth Skill

**Location**: `.claude/skills/better-auth/`
**Package**: `better-auth.skill`

Comprehensive toolkit for implementing Better-Auth authentication services.

**Includes:**
- ✅ `SKILL.md` - Complete instructions and workflows
- ✅ `scripts/setup_auth.py` - Generates complete auth service with custom fields
- ✅ `scripts/test_auth.py` - Tests all authentication endpoints
- ✅ `references/workflows.md` - Detailed workflow guides
- ✅ `references/configuration.md` - Configuration reference

### 2. frontend-auth-integration Skill

**Location**: `.claude/skills/frontend-auth-integration/`
**Package**: `frontend-auth-integration.skill`

Complete toolkit for integrating Better-Auth into React and Vue frontends.

**Includes:**
- ✅ `SKILL.md` - React and Vue integration patterns
- ✅ Component examples for login, signup, profile pages
- ✅ Session management with useSession hooks
- ✅ Route protection strategies
- ✅ Error handling and loading states
- ✅ JWT token management for API calls

### 3. backend-auth-integration Skill

**Location**: `.claude/skills/backend-auth-integration/`
**Package**: `backend-auth-integration.skill`

Complete toolkit for integrating Better-Auth into Python FastAPI backends.

**Includes:**
- ✅ `SKILL.md` - FastAPI integration patterns
- ✅ Session validation via HTTP calls
- ✅ JWT token verification
- ✅ FastAPI middleware and dependencies
- ✅ CORS configuration for auth
- ✅ Role-based access control patterns
- ✅ Testing utilities

### 4. jwt-access-token Skill

**Location**: `.claude/skills/jwt-access-token/`
**Package**: `jwt-access-token.skill`

Solve the "user logged in but backend doesn't know" problem.

**Includes:**
- ✅ `SKILL.md` - Complete JWT flow guide
- ✅ getJWTToken() implementation pattern
- ✅ Frontend API call patterns with JWT
- ✅ Backend JWT verification
- ✅ Common mistakes and fixes
- ✅ Complete flow diagram
- ✅ Testing scripts
- ✅ Real-world examples from this project

### 5. auth-troubleshooting Skill

**Location**: `.claude/skills/auth-troubleshooting/`
**Package**: `auth-troubleshooting.skill`

Comprehensive authentication debugging and problem-solving guide.

**Includes:**
- ✅ `SKILL.md` - Troubleshooting workflows for 8 common problems
- ✅ CORS error diagnosis and fixes
- ✅ Session persistence debugging
- ✅ JWT verification failure solutions
- ✅ Rate limiting adjustments
- ✅ Custom fields configuration
- ✅ Environment variable checklist
- ✅ Testing commands and debugging tools

## How Skills Work with Agents

The authentication skills provide:
1. **Knowledge**: SKILL.md contains instructions Claude reads when triggered
2. **Tools**: Scripts and code patterns Claude can use
3. **References**: Documentation Claude loads when needed
4. **Live Docs**: Context7 MCP fetches latest library documentation

When you ask Claude to work with authentication:
1. The appropriate skill automatically triggers (based on description match)
2. Claude reads SKILL.md for instructions
3. Claude uses Context7 to get latest documentation
4. Claude executes scripts and generates code
5. Claude uses built-in agents (Explore, Plan) as needed for complex steps

## Complete Authentication Workflow

For a full-stack application with authentication:

**1. Setup Backend Auth Service:**
```
You: "Setup Better-Auth with custom user fields for my e-learning platform"

→ better-auth agent triggers
→ Uses better-auth skill
→ Generates complete Node.js auth service
→ Configures custom fields (softwareBackground, hardwareBackground, interestArea)
```

**2. Integrate Frontend:**
```
You: "Add login and signup pages to my React app"

→ frontend-auth-integration agent triggers
→ Uses frontend-auth-integration skill
→ Creates login/signup components
→ Sets up session management
→ Configures protected routes
```

**3. Protect Backend API:**
```
You: "Protect my FastAPI endpoints with Better-Auth sessions"

→ backend-auth-integration agent triggers
→ Uses backend-auth-integration skill
→ Implements session validation
→ Creates auth middleware
→ Sets up CORS for auth
```

## Example Usage

### Basic Auth Service Setup

```
You: "Create auth service with email/password and custom fields for role and tier"

Claude: *Triggers better-auth skill*
        *Uses Context7 to get latest Better-Auth docs*
        *Runs setup_auth.py with custom fields*
        *Creates complete TypeScript auth service*
        *Provides setup instructions*
```

### React Frontend Integration

```
You: "Add authentication to my React app with login and protected routes"

Claude: *Triggers frontend-auth-integration skill*
        *Uses Context7 to get latest @better-auth/react docs*
        *Creates Login.tsx and Signup.tsx components*
        *Sets up useSession hook*
        *Implements ProtectedRoute component*
```

### Python Backend Protection

```
You: "Protect my FastAPI routes with Better-Auth session validation"

Claude: *Triggers backend-auth-integration skill*
        *Uses Context7 to get latest FastAPI docs*
        *Creates auth.py utilities*
        *Implements session validation*
        *Shows usage with Depends()*
```

### Testing

```
You: "Test the authentication system end-to-end"

Claude: *Uses all three skills*
        *Tests auth service endpoints*
        *Tests frontend auth flows*
        *Tests backend route protection*
        *Reports results*
```

## Directory Structure

```
.claude/
├── agents/                              # Custom agent configurations
│   ├── README.md                        # This file
│   ├── better-auth.md                   # Auth service setup agent
│   ├── frontend-auth-integration.md     # Frontend integration agent
│   ├── backend-auth-integration.md      # Backend integration agent
│   ├── jwt-access-token.md              # JWT token flow agent
│   └── auth-troubleshooting.md          # Auth debugging agent
├── skills/                              # Skills directory
│   ├── better-auth/                     # Auth service skill
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   │   ├── setup_auth.py
│   │   │   └── test_auth.py
│   │   └── references/
│   │       ├── workflows.md
│   │       └── configuration.md
│   ├── frontend-auth-integration/       # Frontend integration skill
│   │   └── SKILL.md
│   ├── backend-auth-integration/        # Backend integration skill
│   │   └── SKILL.md
│   ├── jwt-access-token/                # JWT token flow skill
│   │   └── SKILL.md
│   └── auth-troubleshooting/            # Auth debugging skill
│       └── SKILL.md
├── packaged-skills/                     # Packaged .skill files
│   ├── better-auth.skill
│   ├── frontend-auth-integration.skill
│   ├── backend-auth-integration.skill
│   ├── jwt-access-token.skill
│   └── auth-troubleshooting.skill
└── skill-creator/                       # Skill creation utilities
```

## Installing Skills

To use these skills in another project:

```bash
# Copy the .skill files to the new project
cp .claude/packaged-skills/better-auth.skill /path/to/new/project/.claude/
cp .claude/packaged-skills/frontend-auth-integration.skill /path/to/new/project/.claude/
cp .claude/packaged-skills/backend-auth-integration.skill /path/to/new/project/.claude/

# Claude will automatically detect and use them
```

Or install directly in Claude Code:
```
You: "Install the .claude/packaged-skills/better-auth.skill file"

Claude will extract and set up the skill automatically.
```

## Learn More

- **Skills Documentation**: See `.claude/skill-creator/SKILL.md` for skill creation guide
- **Better-Auth Skill**: See `.claude/skills/better-auth/SKILL.md` for usage
- **Frontend Integration**: See `.claude/skills/frontend-auth-integration/SKILL.md`
- **Backend Integration**: See `.claude/skills/backend-auth-integration/SKILL.md`
- **Claude Code Agents**: Ask Claude "How do I use the Task tool with agents?"
- **Context7 MCP**: Ask Claude "How does Context7 MCP work?"

## Creating New Agents

To create a new custom agent:

1. Create a Markdown file in `.claude/agents/` with YAML frontmatter:
```markdown
---
name: my-agent
description: Use this agent when [conditions]. Examples:

<example>
Context: [Scenario description]
user: "[User request]"
assistant: "[How to respond]"
<commentary>
[Why this agent triggers]
</commentary>
</example>

model: opus  # or sonnet/haiku/inherit
color: blue  # or green/purple/red/yellow
tools: ["Read", "Write", "Edit", "Bash", "Grep", "Glob"]
---

You are [agent role and expertise]...

**Your Core Responsibilities:**
1. [Responsibility 1]
2. [Responsibility 2]

**Workflow:**
[Step-by-step process]

**Output Guidelines:**
[What to return]
```

2. Create the corresponding skill in `.claude/skills/my-skill/SKILL.md`

3. Package the skill:
```bash
cd .claude/skill-creator
python3 scripts/package_skill.py ../skills/my-skill ../packaged-skills/
```

## Next Steps

Ready to use authentication in your project:

1. **Setup Auth Service**: "Claude, setup Better-Auth with custom fields"
2. **Add Frontend**: "Claude, integrate auth into my React app"
3. **Protect Backend**: "Claude, protect my FastAPI routes with auth"
4. **Test Everything**: "Claude, test the authentication system"

All agents will automatically use Context7 to fetch the latest documentation and generate up-to-date code!
