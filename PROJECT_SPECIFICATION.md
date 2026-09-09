# Internship Intelligence Agent: Project Specification

## Overview
The Internship Intelligence Agent is a **local-first, zero-cost research and outreach system**.

The core principle is:
> **Discover → Verify → Research → Rank → Personalize → Prepare → Notify → Human approval**

It is designed to handle both **provided contact lists** and **autonomous startup discovery**.

## Hard Rules
1. Never invent information.
2. Never represent inferred contact information as verified.
3. Never fabricate resume experience.
4. Every important factual claim gets evidence.
5. User approves outreach.
6. Store everything so the same person/company isn't repeatedly researched.

## Inputs
The system eventually accepts:
* Excel files
* CSV files
* Google Sheets links
* Google Docs links
* Lists of companies
* VC names
* Natural-language research requests
* Funding/startup research requests

Examples:
* "Process this Google Sheet and find the best recruiters."
* "Find recently funded AI startups in India."
* "Find VC-backed startups hiring backend interns."
* "Find companies backed by Accel that could be relevant to me."

## Outputs
For each qualified opportunity, the system produces:
* Person
* Company
* Role
* Contact information
* Company research
* Recruiting authority
* Company reliability
* Opportunity score
* Why this is relevant
* Curated resume
* Short description
* Cold email
* Cover letter, when appropriate
* Evidence/sources

## Data Model (PostgreSQL / SQLAlchemy)

### Company
* `id`
* `name`
* `normalized_name`
* `website`
* `linkedin_url`
* `industry`
* `location`
* `employee_count`
* `stage`
* `description`
* `funding_total`
* `reliability_score`
* `status`
* `created_at`
* `updated_at`

### Person
* `id`
* `name`
* `normalized_name`
* `company_id`
* `title`
* `linkedin_url`
* `email`
* `phone`
* `email_status`
* `identity_confidence`
* `recruiting_authority`
* `contact_score`

### Opportunity
* `id`
* `company_id`
* `person_id`
* `role_id`
* `company_score`
* `contact_score`
* `role_score`
* `candidate_score`
* `overall_score`
* `status`
* `created_at`
* `updated_at`

### Evidence
* `id`
* `entity_type`
* `entity_id`
* `claim`
* `source_url`
* `source_type`
* `retrieved_at`
* `confidence`

*(Other entities include User, Role, Source, ResearchRun, Resume, ResumeVersion, Outreach)*

## System Architecture (Local Infrastructure)
Stack: Python, FastAPI, PostgreSQL, SQLAlchemy, Pydantic, Redis, Docker, React, Vite, Gemini / OpenRouter (free APIs), Playwright, BeautifulSoup, LaTeX.

Services (`docker-compose`):
* backend (FastAPI)
* frontend (React/Vite)
* postgres
* redis

## Phases (32 Total)
### R1 Foundation
* **Phase 0: Define the system**: Specification and data model.
* **Phase 1: Local infrastructure**: docker-compose setup.
* **Phase 2: Database architecture**: Models and migrations.
* **Phase 3: Source ingestion framework**: Adapters for Excel, CSV, Google Sheets, Docs.

### R2 Intelligence Core
* **Phase 4: Entity resolution and deduplication**: Canonicalize people and companies.
* **Phase 5: Web research engine**: Infrastructure for HTTP/browser fetching and scraping.
* **Phase 6: Evidence engine**: Storing claims with confidence and source.
* **Phase 7: Person identity verification**: Does this person exist at this company?
* **Phase 8: Recruiting-authority analysis**: Classify influence on hiring.

### R3 Company Intelligence
* **Phase 9: Company verification**: Legitimacy check.
* **Phase 10: Company intelligence**: Deep profile extraction.
* **Phase 11: Funding discovery**: Tracking recently funded startups.
* **Phase 12: VC portfolio discovery**: Startups backed by specific VCs.

### R4 Opportunity Engine
* **Phase 13: Hiring intelligence**: Current opportunities.
* **Phase 14: Contact discovery**: Reachable contact points.
* **Phase 15: Candidate profile engine**: Candidate's master profile (YAML + LaTeX).
* **Phase 16: Opportunity matching**: Fit score generation via LLM.
* **Phase 17: Opportunity scoring**: Deterministic ranking function.

### R5 Personalization
* **Phase 18: Resume engine**: Evidence-constrained tailored PDF generation.
* **Phase 19: Resume audit**: Strict fact-checking against master profile.
* **Phase 20: Short opportunity description**: Brief summary of fit.
* **Phase 21: Cold-email engine**: Template-driven personalized drafts.
* **Phase 22: Cover-letter engine**: Conditional generation for formal applications.

### R6 Product
* **Phase 23: Application package**: Combined bundle (research, resume, drafts).
* **Phase 24: Dashboard**: React UI to view opportunities.
* **Phase 25: Human review system**: Human-in-the-loop approval workflow.
* **Phase 26: Notification system**: Alerts for high-priority packages.

### R7 Automation
* **Phase 27: Orchestrator**: Connecting the entire pipeline into states.
* **Phase 28: Research request interface**: Natural language parsing for ad-hoc requests.
* **Phase 29: Optimization**: Tuning costs (cheap ops first, expensive ops later).

### R8 Optimization
* **Phase 30: Learning from your decisions**: Feedback loop from human reviews.
* **Phase 31: Scheduling and recurring discovery**: Daily/weekly refresh tasks.
* **Phase 32: Final system**: Complete user-in-the-loop architecture.

## Implementation Strategy
Build iteratively in 8 major releases, starting with manual data import -> intelligence core -> dashboard, before attempting fully autonomous discovery and personalization.
