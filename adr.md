# Architecture Decision Record (ADR)

## Context
The Internship Intelligence Agent aims to automate the discovery, verification, and outreach process for identifying startup opportunities. The user has specifically requested an adr.md file to log architectural decisions and principles to guide development, even though the core deliverables focus on specifications right now.

## Principles

1. **Local-first**
   - *Why*: Privacy, control over data, and to minimize cloud dependency/costs.
   - *Impact*: We rely on local services via Docker instead of most third-party cloud APIs. Exception: LLM capabilities are handled via free API tiers to reduce local compute requirements.

2. **Zero-cost**
   - *Why*: The system should run continuously for free.
   - *Impact*: Open-source tooling for infrastructure (PostgreSQL, Redis) and free-tier APIs for models (Gemini, OpenRouter free models). Rate limiting and intelligent caching must be implemented aggressively to avoid getting blocked by free tier services or sources, reducing the need for paid proxies where possible.

3. **Explicit Human-in-the-Loop**
   - *Why*: AI should augment the human, not act autonomously to the point of sending emails or submitting applications. This avoids reputational damage.
   - *Impact*: The "Approve" step is a hard gate. The system only prepares packages (resume, email draft, research) for human review. It does not send on the user's behalf.

4. **Evidence-based (No Hallucinations)**
   - *Why*: The system needs to be reliable.
   - *Impact*: Every claim (e.g., a person works at a company, an email address) must have a source and confidence score. We explicitly forbid inventing information, especially on resumes.

## Stack Decisions

1. **Backend**: Python + FastAPI
   - *Why*: Fast to develop, asynchronous (essential for web scraping and LLM calls), and excellent ecosystem for data manipulation (Pandas, BeautifulSoup, SQLAlchemy).

2. **Database**: PostgreSQL
   - *Why*: Robust, relational data is perfect for the highly structured entities (Companies, People, Opportunities).

3. **Frontend**: React + Vite
   - *Why*: Standard, fast, and component-based UI for the human review dashboard.

4. **Background Jobs / Cache**: Redis
   - *Why*: Essential for caching expensive web requests (Phase 5) and managing background tasks/queues.

5. **AI / LLM**: Free APIs (Gemini / OpenRouter)
   - *Why*: Offloading LLM execution to free-tier cloud APIs ensures zero cost while reducing the heavy local compute requirements of running models via Ollama.

6. **Web Research**: Playwright + BeautifulSoup
   - *Why*: Playwright can render JS-heavy pages (crucial for modern startup websites), while BeautifulSoup handles lightweight static parsing.

## Pipeline Optimization Strategy
- *Decision*: Execute cheap operations (parsing, deductive resolution, basic filtering) before expensive operations (deep web scraping, LLM analysis, resume generation).
- *Impact*: Keeps local compute requirements reasonable and processing times down.
