from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime, ForeignKey, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    normalized_name = Column(String, index=True, nullable=False)
    website = Column(String)
    linkedin_url = Column(String)
    industry = Column(String)
    location = Column(String)
    employee_count = Column(Integer)
    stage = Column(String)
    description = Column(Text)
    funding_total = Column(String)
    reliability_score = Column(Float)
    status = Column(String, default="DISCOVERED")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    people = relationship("Person", back_populates="company")
    opportunities = relationship("Opportunity", back_populates="company")

class Person(Base):
    __tablename__ = 'people'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    normalized_name = Column(String, index=True, nullable=False)
    company_id = Column(Integer, ForeignKey('companies.id'))
    title = Column(String)
    linkedin_url = Column(String)
    email = Column(String)
    phone = Column(String)
    email_status = Column(String)
    identity_confidence = Column(Float)
    recruiting_authority = Column(String)
    contact_score = Column(Float)

    company = relationship("Company", back_populates="people")
    opportunities = relationship("Opportunity", back_populates="person")

class Opportunity(Base):
    __tablename__ = 'opportunities'

    id = Column(Integer, primary_key=True, index=True)
    company_id = Column(Integer, ForeignKey('companies.id'))
    person_id = Column(Integer, ForeignKey('people.id'))
    role_id = Column(Integer, nullable=True) # Assuming a Role table later

    company_score = Column(Float)
    contact_score = Column(Float)
    role_score = Column(Float)
    candidate_score = Column(Float)
    overall_score = Column(Float)

    status = Column(String, default="IDENTIFIED")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    company = relationship("Company", back_populates="opportunities")
    person = relationship("Person", back_populates="opportunities")

class Evidence(Base):
    __tablename__ = 'evidence'

    id = Column(Integer, primary_key=True, index=True)
    entity_type = Column(String, nullable=False) # 'Company', 'Person', etc.
    entity_id = Column(Integer, nullable=False)
    claim = Column(Text, nullable=False)
    source_url = Column(String)
    source_type = Column(String)
    retrieved_at = Column(DateTime, default=datetime.utcnow)
    confidence = Column(Float)
