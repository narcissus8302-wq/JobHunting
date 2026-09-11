import json
from sqlalchemy.orm import Session
from .models import Company, Person, Evidence
from .llm import LLMInterface
from .research.fetcher import WebFetcher
from .research.extractor import HTMLExtractor

class VerificationBase:
    def __init__(self, db: Session):
        self.db = db

    def add_evidence(self, entity_type: str, entity_id: int, claim: str, confidence: float, source: str = "internal"):
        evidence = Evidence(
            entity_type=entity_type,
            entity_id=entity_id,
            claim=claim,
            confidence=confidence,
            source_type=source
        )
        self.db.add(evidence)
        self.db.commit()


class PersonVerificationService(VerificationBase):
    def __init__(self, db: Session, llm: LLMInterface = None):
        super().__init__(db)
        self.llm = llm or LLMInterface()

    def verify_identity(self, person: Person) -> float:
        """
        Determines identity confidence (Phase 7) via LLM analysis of available data.
        Returns a confidence score 0.0 - 1.0.
        """
        prompt = f"""
        Analyze the identity of this person: {person.name}.
        Title: {person.title}
        Email: {person.email}
        LinkedIn: {person.linkedin_url}
        Company ID: {person.company_id}

        Determine if this is a real, verifiable identity. Return a JSON with:
        - confidence: a float from 0.0 to 1.0.
        - reasoning: string explanation.
        """

        try:
            result = self.llm.generate_json(prompt)
            confidence = float(result.get("confidence", 0.5))
            self.add_evidence("Person", person.id, result.get("reasoning", "LLM determined confidence"), confidence, source="LLM")
        except Exception:
            # Fallback logic
            confidence = 0.5
            if person.linkedin_url and person.email:
                confidence = 0.9
            elif person.linkedin_url:
                confidence = 0.8

        person.identity_confidence = confidence
        self.db.commit()
        return confidence

    def analyze_recruiting_authority(self, person: Person) -> str:
        """
        Determines influence on hiring (Phase 8).
        """
        title = (person.title or "").lower()

        high_authority = ['founder', 'ceo', 'cto', 'recruiter', 'talent', 'hiring manager', 'head of engineering']
        low_authority = ['software engineer', 'intern', 'analyst', 'associate']

        authority = "UNCERTAIN"
        for role in high_authority:
            if role in title:
                authority = "HIGH"
                break

        for role in low_authority:
            if role in title:
                authority = "LOW"
                break

        person.recruiting_authority = authority
        self.db.commit()
        return authority


class CompanyVerificationService(VerificationBase):
    def __init__(self, db: Session, llm: LLMInterface = None):
        super().__init__(db)
        self.llm = llm or LLMInterface()

    def verify_company(self, company: Company, website_text: str = None) -> float:
        """
        Verify legitimacy (Phase 9). Uses explicitly extracted website text.
        """
        score = 0.0

        if company.website:
            score += 0.2
            self.add_evidence("Company", company.id, "Website exists", 0.9)

        if website_text:
            prompt = f"""
            Analyze this raw website text for a company named '{company.name}'.
            Does this appear to be a legitimate, active company with identifiable team members and current activity?
            Return a JSON with:
            - is_legitimate: boolean
            - team_exists: boolean
            - current_hiring: boolean
            - reasoning: brief string

            Text: {website_text[:3000]}
            """
            try:
                result = self.llm.generate_json(prompt)
                if result.get('is_legitimate'):
                    score += 0.4
                    self.add_evidence("Company", company.id, result.get("reasoning", "Website content appears legitimate"), 0.8, "LLM")
                if result.get('team_exists'):
                    score += 0.2
                    self.add_evidence("Company", company.id, "Identifiable team exists", 0.8, "LLM")
                if result.get('current_hiring'):
                    score += 0.2
                    self.add_evidence("Company", company.id, "Current hiring activity found", 0.8, "LLM")
            except Exception:
                pass

        elif company.linkedin_url:
            score += 0.3

        if company.funding_total:
            score += 0.2
            self.add_evidence("Company", company.id, "Funding confirmed", 0.95)

        # Cap score at 1.0 (or 100 on standard scale)
        final_score = min(score, 1.0) * 100
        company.reliability_score = final_score
        self.db.commit()
        return final_score


class OpportunityScoringService:
    @staticmethod
    def calculate_overall_score(company_score: float, contact_score: float, role_score: float, candidate_score: float) -> float:
        """
        Deterministic ranking function (Phase 17).
        Company quality       20%
        Contact quality       20%
        Role relevance        25%
        Candidate fit         25%
        Hiring signal         10% (mocked in role_score for now)
        """
        score = (
            (company_score * 0.20) +
            (contact_score * 0.20) +
            (role_score * 0.35) +
            (candidate_score * 0.25)
        )
        return score * 100 # Returns 0-100 scale
