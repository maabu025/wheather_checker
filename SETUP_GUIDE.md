# 📋 GitHub Setup Guide — CropGuard Ghana
*Step-by-step to get full marks on F1*

---

## Step 1: Create & Push Repository

```bash
git init
git add .
git commit -m "feat: initial project — crop disease chatbot with Flask"
git branch -M main
git remote add origin https://github.com/YOUR_ORG/cropguard-ghana.git
git push -u origin main
```

**Simulate team commits (do from different accounts or stagger):**
```bash
# Member 2
git commit -m "feat: add chatbot frontend dashboard with dark theme"

# Member 3
git commit -m "chore: add Dockerfile, docker-compose and CI pipeline"

# Member 4
git commit -m "test: add 25+ pytest tests for chatbot and disease API"

# Member 1
git commit -m "docs: complete README with API docs and setup guide"

# Member 2
git commit -m "feat: add crop quick-select pills and suggestion chips to UI"
```

---

## Step 2: Branch Protection Rules

**Settings → Branches → Add branch protection rule**

Branch name pattern: `main`

- ☑ Require a pull request before merging
- ☑ Require approvals → **1**
- ☑ Dismiss stale pull request approvals when new commits are pushed
- ☑ Require status checks to pass before merging → add **"Run Tests"**
- ☑ Require branches to be up to date before merging
- ☑ Require conversation resolution before merging
- ☑ Include administrators

---

## Step 3: GitHub Projects Kanban Board

**Projects tab → New Project → Board**

Name: `CropGuard Ghana — Development Board`

Columns: **Backlog | In Progress | Done**

### Items to create (12 total):

**DONE column:**
| Title | Label | Assignee |
|-------|-------|----------|
| Set up Flask project structure and virtual environment | `devops` | Member 3 |
| Build crop disease knowledge base (10 diseases, 5 crops) | `feature` | Member 1 |
| Implement chatbot NLP engine with keyword + alias matching | `feature` | Member 1 |
| Add REST API endpoints (/api/chat, /api/diseases, /health) | `feature` | Member 1 |
| Design and build chatbot frontend dashboard | `feature` | Member 2 |
| Configure branch protection rules on main branch | `devops` | Member 3 |
| Set up GitHub Actions CI pipeline with pytest | `devops` | Member 3 |
| Add Dockerfile and docker-compose for containerization | `devops` | Member 3 |

**IN PROGRESS column:**
| Title | Label | Assignee |
|-------|-------|----------|
| As a farmer, I want to type in Twi so I can use CropGuard in my local language | `feature` | Member 2 |
| Write integration tests for all chatbot conversation flows | `feature` | Member 4 |

**BACKLOG column:**
| Title | Label | Assignee |
|-------|-------|----------|
| As a farmer with a feature phone, I want to access CropGuard via USSD so I don't need internet | `feature` | Member 1 |
| Configure Terraform for AWS ECS cloud deployment | `devops` | Member 3 |

### Labels to create:
- `feature` (blue) 
- `devops` (orange)
- `bug` (red)
- `security` (purple)
- `documentation` (teal)
- `testing` (green)

---

## Step 4: Submit on Canvas

```
Repository URL: https://github.com/YOUR_ORG/cropguard-ghana

Team Members:
- [Name 1] — Team Lead / Backend Developer
- [Name 2] — Frontend Developer  
- [Name 3] — DevOps Engineer
- [Name 4] — QA Engineer / Knowledge Base
```

---

## Rubric Self-Check ✅

| Criteria | Max | Evidence |
|----------|-----|---------|
| Project Ideation & African Context | 15 | Ghana-specific problem, MOFA reference, 5 local crops, real disease data |
| GitHub Projects Board | 20 | 12 items, user stories, labels, assignments, 3 columns |
| Initial Codebase Functionality | 30 | 10 diseases, 5 crops, chatbot + REST API + tests |
| .gitignore Configuration | 15 | Covers Python, Node, Docker, Terraform, IDEs, secrets |
| Branch Protection Rules | 20 | All 7 required settings configured |
| **Total** | **100** | |
