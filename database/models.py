from sqlmodel import SQLModel, Field, Relationship, JSON, Column
from typing import Optional, List
from pydantic import BaseModel


# Base Models
class SupplierBase(SQLModel):
    name: str


class DrugBase(SQLModel):
    name: str
    expiry: Optional[str] = None
    manufacturer: str
    stock: int
    price: int
    supplier_id: int | None = Field(default=None, foreign_key="supplier.id")


# Database Models
class Supplier(SupplierBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    drugs: List["Drug"] = Relationship(back_populates="supplier")


class Drug(DrugBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    supplier: Supplier | None = Relationship(back_populates="drugs")


# Create Models
class SupplierCreate(SupplierBase):
    pass


class DrugCreate(DrugBase):
    pass


# Update Models
class SupplierUpdate(SQLModel):
    name: Optional[str] = None


class DrugUpdate(SQLModel):
    name: Optional[str] = None
    expiry: Optional[str] = None
    manufacturer: Optional[str] = None
    price: Optional[int] = None
    supplier_id: Optional[int] = None


# Public Models
class SupplierPublic(SupplierBase):
    id: int


class DrugPublic(DrugBase):
    id: int


class SupplierPublicWithDrugs(SupplierPublic):
    drugs: List[DrugPublic] = []


class DrugPublicWithSupplier(DrugPublic):
    supplier: SupplierPublic | None = None


# Paginated Response Models
class PaginatedResponseDrug(BaseModel):
    data: List[DrugPublicWithSupplier]
    total: int
    limit: int
    offset: int



class PrescriptionBase(SQLModel):
    patient_name: str
    doctor_name: str
    prescription_date: str
    drugs: List[dict] = Field(sa_column=Column(JSON))