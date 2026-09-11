import asyncio
from sqlalchemy.orm import Session
from .models import Company, Person, Opportunity
from .resolution import ResolutionService
from .intelligence.company import CompanyIntelligenceService
from .intelligence.hiring import HiringResearchService
from .intelligence.contact import ContactDiscoveryService
from .verification import CompanyVerificationService, PersonVerificationService, OpportunityScoringService
from .personalization.matching import CandidateMatcher
from .personalization.communication import CommunicationGenerator

class Orchestrator:
    def __init__(self, db: Session):
        self.db = db
        self.resolution = ResolutionService(db)
        self.company_intel = CompanyIntelligenceService(db)
        self.hiring_intel = HiringResearchService()
        self.contact_intel = ContactDiscoveryService()

        self.verify_company = CompanyVerificationService(db)
        self.verify_person = PersonVerificationService(db)

        self.matcher = CandidateMatcher()
        self.communication = CommunicationGenerator()

    async def run_pipeline(self, raw_contact: dict, candidate_profile: dict, email_template: str):
        """
        Connects the entire system (Phase 27).
        Input is a parsed 'RawContact' from an ingest adapter.
        """
        # 1. Deduplicate / Resolve (Phase 4)
        company = self.resolution.resolve_company(raw_contact['company'], raw_contact.get('website'))
        person = self.resolution.resolve_person(raw_contact['name'], company.id, raw_contact.get('email'))
        person.title = raw_contact.get('title', person.title)
        person.linkedin_url = raw_contact.get('linkedin', person.linkedin_url)
        self.db.commit()

        # 2. Verify Company & Identity (Phases 7, 9)
        company_score = self.verify_company.verify_company(company)
        identity_confidence = self.verify_person.verify_identity(person)
        recruiting_authority = self.verify_person.analyze_recruiting_authority(person)

        if company_score < 40 or identity_confidence < 0.5:
            company.status = "REJECTED"
            self.db.commit()
            return {"status": "rejected", "reason": "Failed basic verification"}

        # 3. Deep Research (Phases 10, 13)
        company_profile = await self.company_intel.extract_company_profile(company)
        roles = await self.hiring_intel.discover_opportunities(company)

        # Select best role (simplification for MVP)
        target_role = roles[0] if roles else {"title": "Software Engineering Internship", "category": "General"}

        # 4. Match Candidate (Phase 16)
        match_data = self.matcher.match_opportunity(company, target_role, candidate_profile)

        # 5. Score Opportunity (Phase 17)
        # Simplified scoring logic mapping to MVP percentages
        contact_quality = 1.0 if recruiting_authority == "HIGH" else 0.5
        role_relevance = 1.0 if "Backend" in str(target_role) or "AI" in str(target_role) else 0.5
        candidate_fit = match_data.get('fit_score', 50) / 100.0

        overall_score = OpportunityScoringService.calculate_overall_score(
            company_score, contact_quality * 100, role_relevance * 100, candidate_fit * 100
        )

        opportunity = Opportunity(
            company_id=company.id,
            person_id=person.id,
            company_score=company_score,
            contact_score=contact_quality * 100,
            role_score=role_relevance * 100,
            candidate_score=candidate_fit * 100,
            overall_score=overall_score,
            status="QUALIFIED" if overall_score >= 70 else "REVIEW"
        )
        self.db.add(opportunity)
        self.db.commit()

        if overall_score >= 70:
            opportunity.status = "PERSONALIZING"
            self.db.commit()

            # 6. Personalize (Phases 20-21)
            summary = self.communication.generate_short_description(company, person, target_role, match_data)

            email_context = {
                "company_name": company.name,
                "contact_name": person.name.split()[0],
                "company_focus": company_profile.get("product", "technology"),
                "company_recent_activity": "raised funding recently", # Stub
                "matching_skill_1": match_data.get("matching_skills", ["Python"])[0],
                "matching_skill_2": match_data.get("matching_skills", ["Python", "FastAPI"])[-1],
                "project_name": "Lawluminous", # Stub from candidate profile
                "role_name": target_role.get('title'),
                "my_name": "Jane Doe"
            }

            email = self.communication.generate_cold_email(email_template, email_context)

            opportunity.status = "PACKAGE_READY"
            self.db.commit()

            return {
                "status": "package_ready",
                "opportunity_id": opportunity.id,
                "score": overall_score,
                "summary": summary,
                "email_draft": email
            }

        return {"status": "review_required", "opportunity_id": opportunity.id, "score": overall_score}
