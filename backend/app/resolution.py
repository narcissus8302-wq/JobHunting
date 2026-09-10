import re
from typing import Optional
from sqlalchemy.orm import Session
from .models import Company, Person

class ResolutionService:
    def __init__(self, db: Session):
        self.db = db

    def normalize_company_name(self, name: str) -> str:
        """
        Normalize company names for deduplication:
        XYZ AI Technologies Pvt. Ltd. -> xyzai
        """
        if not name:
            return ""
        name = name.lower()
        # Remove common corporate suffixes
        name = re.sub(r'\b(inc|llc|ltd|pvt|corp|corporation|technologies|ai|group)\b\.?', '', name)
        # Remove spaces and punctuation
        name = re.sub(r'[^a-z0-9]', '', name)
        return name

    def normalize_person_name(self, name: str) -> str:
        """
        Jane A. Doe | XYZ -> janedoe
        """
        if not name:
            return ""
        # Strip out anything after common separators like '|', '-', ','
        name = re.split(r'[|\-,]', name)[0]
        name = name.lower()
        # Remove middle initials and punctuation
        name = re.sub(r'\b[a-z]\.\s*', '', name)
        name = re.sub(r'[^a-z]', '', name)
        return name

    def resolve_company(self, name: str, website: Optional[str] = None) -> Company:
        """Find an existing company or create a new one."""
        normalized_name = self.normalize_company_name(name)

        company = self.db.query(Company).filter(Company.normalized_name == normalized_name).first()

        if not company and website:
            # Attempt domain matching if exact name fails
            # Basic domain extraction
            domain = re.sub(r'^https?://(www\.)?', '', website.lower()).split('/')[0]
            if domain:
                company = self.db.query(Company).filter(Company.website.ilike(f'%{domain}%')).first()

        if not company:
            company = Company(name=name, normalized_name=normalized_name, website=website)
            self.db.add(company)
            self.db.commit()
            self.db.refresh(company)

        return company

    def resolve_person(self, name: str, company_id: int, email: Optional[str] = None) -> Person:
        """Find an existing person within a company or create a new one."""
        normalized_name = self.normalize_person_name(name)

        # Try to find by normalized name within the same company
        person = self.db.query(Person).filter(
            Person.normalized_name == normalized_name,
            Person.company_id == company_id
        ).first()

        if not person and email:
            person = self.db.query(Person).filter(
                Person.email == email,
                Person.company_id == company_id
            ).first()

        if not person:
            person = Person(name=name, normalized_name=normalized_name, company_id=company_id, email=email)
            self.db.add(person)
            self.db.commit()
            self.db.refresh(person)

        return person
