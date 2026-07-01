# Project Board Seed — Soko Bora

Use this to populate your GitHub Projects (Kanban) board. Create the board
under the repo's **Projects** tab, add these as issues/cards, and sort
into **Backlog / In Progress / Done** columns. Suggested labels and
milestones are included per item.

> Minimum requirement: 8–10 backlog items, mixing feature work and DevOps
> tasks, in user-story format where applicable.

| # | Item | Type | Label(s) | Milestone | Suggested Assignee |
|---|------|------|----------|-----------|---------------------|
| 1 | As a farmer, I want to submit a crop price report so that other users can see current market rates. | Feature | `feature` | F1 | Backend lead |
| 2 | As a buyer, I want to browse all reported prices so that I can find fair deals. | Feature | `feature` | F1 | Backend lead |
| 3 | As a farmer, I want to filter prices by crop and region so that I can compare only what's relevant to me. | Feature | `feature` | F1 | Backend lead |
| 4 | Set up initial Flask project structure with a working health check endpoint. | DevOps | `devops` | F1 | DevOps lead |
| 5 | Write initial pytest test suite covering the core price-reporting feature. | DevOps / QA | `devops`, `testing` | F1 | QA lead |
| 6 | Set up GitHub repository with README, .gitignore, and branch protection rules. | DevOps | `devops` | F1 | DevOps lead |
| 7 | Containerize the application with a secure, non-root Dockerfile. | DevOps | `devops`, `security` | F2 | DevOps lead |
| 8 | Set up docker-compose for local development with a PostgreSQL service. | DevOps | `devops` | F2 | DevOps lead |
| 9 | Build GitHub Actions CI pipeline: lint, test, and Docker build on every push/PR. | DevOps | `devops`, `ci-cd` | F2 | DevOps lead |
| 10 | As a farmer, I want to see price trends over time for a crop so that I can time my sale better. | Feature | `feature`, `future` | F3 | Frontend lead |
| 11 | Add input validation and basic rate-limiting to the price-submission endpoint. | Security | `security`, `devops` | F3 | Backend lead |
| 12 | As an NGO field agent, I want to export price data as CSV so that I can share it with cooperatives. | Feature | `feature` | Summative | Backend lead |

## Board Columns

- **Backlog** — items not yet started (most items above, initially)
- **In Progress** — items 1, 2, 4 typically move here first for F1
- **Done** — move items here as they're completed and merged to `main`

## Labels to Create

`feature`, `devops`, `bug`, `security`, `testing`, `ci-cd`, `documentation`,
`future`

## Milestones to Create

- `F1 - Project Foundation` (due Jun 27)
- `F2 - Containerization & CI` (due Jul 4/5, per your syllabus)
- `F3 - IaC & Monitoring` (later in course)
- `Summative - Production System`

Align each milestone's due date with the actual Canvas deadlines.
