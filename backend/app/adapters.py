from typing import List
from pydantic import BaseModel
import pandas as pd

class RawContact(BaseModel):
    name: str
    company: str
    title: str | None = None
    linkedin: str | None = None
    email: str | None = None
    phone: str | None = None
    source: str

class SourceAdapter:
    def extract(self, source_path: str) -> List[RawContact]:
        raise NotImplementedError("Subclasses must implement extract()")

class ExcelAdapter(SourceAdapter):
    def extract(self, source_path: str) -> List[RawContact]:
        df = pd.read_excel(source_path)
        contacts = []
        for _, row in df.iterrows():
            contacts.append(RawContact(
                name=row.get('Name', ''),
                company=row.get('Company', ''),
                title=row.get('Title'),
                linkedin=row.get('LinkedIn'),
                email=row.get('Email'),
                phone=row.get('Phone'),
                source=f"excel:{source_path}"
            ))
        return contacts
