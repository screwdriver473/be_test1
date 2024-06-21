from dataclasses import field
from enum import Enum
from typing import Optional
from pydantic import field_validator
from sqlmodel import Field, Relationship, SQLModel
from uuid import UUID, uuid4


# Shared properties
# TODO replace email str with EmailStr when sqlmodel supports it
class Gender(str, Enum):
    male = "male"
    female = "female"

class Role(str, Enum):
    unassigned = "unassigned" 
    trail = "trail" #trail login to try out the software, must be expired in configured days
    demo = "demo" #demo login to give demo to customers
    guest = "guest" # temp login to surf or view or feel the application
    patient = "patient"
    lab_technitian = "lab_tech" #lab technitian who can enter values in the given form.
    local_admin = "local_admin" #local admin is mangages bunch of lab technitians.
    branch_admin = "branch_admin" #branch admin can have multiple branches in the same area under him
    group_admin = "group_admin" #group admin manages multiple branch admins
    super_admin = "super_admin" #super admin manages multiple group admins, can see everything they do.
    owner = "owner" #Can see overall branches buisiness and dashboards and finances
    deployer = "deployer" #Deployer can see some logs and do some basic settings
    developer = "developer" #Developer can debug and change advanced settings etc
    root = "root" #Top priority, can do anything

class UserBase(SQLModel):
    first_name: str | None = Field(default=None, min_length=3, max_length=10)
    last_name: str | None = Field(default=None, min_length=3, max_length=10)
    middle_name: Optional[str] = None
    gender: Gender | None = None
    email: str = Field(unique=True, index=True, min_length=4, max_length=20)
    age: int | None = None
    is_superuser: bool = False

    def __post_init__(self) -> None:
        self.full_name = f"{self.first_name} {self.last_name}"

    @field_validator('age')
    def age_validation(cls, value: int) -> int:
        if value is not None and (value <= 0):
            return ValueError('age value must be > 0')
        return value

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=5, max_length=10)
    class Config:
        schema_extra = {
            'examples': [
                {
                    'firstname': 'John',
                    'lastname': 'Doe',
                    'email': 'john.doe@gmail.com',
                    'gender': 'male',
                    'password': 'DoeJohn!',
                    'age': '29',
                    'password': 'john@Doe8877'
                }
            ]
        }


# TODO replace email str with EmailStr when sqlmodel supports it
class UserCreateOpen(SQLModel):
    email: str
    password: str
    full_name: str | None = None


# Properties to receive via API on update, all are optional
# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdate(UserBase):
    first_name: str | None = None
    last_name: str | None = None
    middle_name: Optional[str] = None
    gender: Gender | None = None
    email: str | None = None
    age: int | None = None
    password: str | None = None

    @field_validator('age')
    def age_validation(cls, value: int) -> int:
        if value is not None and (value <= 0 or value > 200):
            return ValueError('age value must be > 0 and <= 200')
        return value

    @field_validator('email')
    def email_validation(cls, em: str) -> str:
        len = em.length()
        if len < 10 or len > 20:
            return ValueError('email length must be >= 10 and <= 20')
        return str

# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdateMe(UserUpdate):
    pass

class UpdatePassword(SQLModel):
    current_password: str
    new_password: str


# Database model, database table inferred from class name
class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
     # using field from dataclasses and init=False enforce the rule not provide id as part of initialization
    uuid: UUID = field(init=False, default_factory=uuid4, repr=False)
    hashed_password: str
    is_active: bool = True
    role: Role = Role.unassigned
    items: list["Item"] = Relationship(back_populates="owner")

# Properties to return via API, id is always required
class UserOut(UserBase):
    id: int
    uuid: UUID
    role: Role
    is_active: bool

class UsersOut(SQLModel):
    data: list[UserOut]
    count: int

class Patient(UserBase, table=True):
    pid: int | None = Field(default=None, primary_key=True)
     # using field from dataclasses and init=False enforce the rule not provide id as part of initialization
    uuid: UUID = field(init=False, default_factory=uuid4, repr=False)
    hashed_password: str
    is_active: bool = True
    role: Role = Role.patient

class PatientOut(Patient):
    pid: int
    uuid: UUID
    role: Role
    is_active: bool

class PatientsOut(SQLModel):
    data: list[PatientOut]
    count: int

class PatientCreate(UserBase):
    password: str = Field(min_length=8, max_length=12)
    class Config:
        schema_extra = {
            'examples': [
                {
                    'firstname': 'John',
                    'lastname': 'Doe',
                    'email': 'john.doe@gmail.com',
                    'gender': 'male',
                    'password': 'DoeJohn!',
                    'age': '29',
                    'password': 'john@Doe8877'
                }
            ]
        }

class LabSupportedTestsBase(SQLModel):
    cbc: bool
    hba1c: bool
    thyroid: bool

class LabSupportedTests(LabSupportedTestsBase, table=True):
    labid: int = Field(default=None, primary_key=True)

class PatientOptedTests(SQLModel, table=True):
    pid: int | None = Field(default=None, primary_key=True)
    uuid: UUID
    #test: LabSupportedTestsBase | None = None

class PatientTestRequestId(SQLModel, table=True):
    reqid: int | None = Field(default=None, primary_key=True)

class CBC(SQLModel, table=True):
    pid: int | None = Field(default=None, primary_key=True)
    hb: str
    hb_untis: str = "mmol/L"

class HBA1C(SQLModel, table=True):
    pid: int | None = Field(default=None, primary_key=True)
    pass

# Shared properties
class ItemBase(SQLModel):
    title: str
    description: str | None = None


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = None  # type: ignore


# Database model, database table inferred from class name
class Item(ItemBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    title: str
    owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemOut(ItemBase):
    id: int
    owner_id: int


class ItemsOut(SQLModel):
    data: list[ItemOut]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: int | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str
