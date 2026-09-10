from sqlalchemy.orm import Session
from .models import Company, Person, Evidence

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
    def verify_identity(self, person: Person) -> float:
        """
        Determines identity confidence (Phase 7).
        In a full implementation, this queries LinkedIn or web data.
        Returns a confidence score 0.0 - 1.0.
        """
        confidence = 0.5 # default unknown
        if person.linkedin_url and person.email:
            confidence = 0.9
            self.add_evidence("Person", person.id, "LinkedIn and Email provided", 0.9)
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
    def verify_company(self, company: Company) -> float:
        """
        Verify legitimacy (Phase 9).
        """
        score = 0.0

        if company.website:
            score += 0.4
            self.add_evidence("Company", company.id, "Website exists", 0.9)

        if company.linkedin_url:
            score += 0.3

        if company.funding_total:
            score += 0.3
            self.add_evidence("Company", company.id, "Funding confirmed", 0.95)

        company.reliability_score = score
        self.db.commit()
        return score


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
