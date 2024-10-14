from database.models import PrescriptionBase
from sqlmodel import Field


class Prescription(PrescriptionBase, table=True):
    id: int = Field(primary_key=True)