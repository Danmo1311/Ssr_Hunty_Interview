from typing import List

from pydantic import BaseModel


class Event(BaseModel):
    pass


class Skills(Event):
    skillName: str
    skillYears: int


class Vacante(Event):
    PositionName: str
    CompanyName: str
    Salary: int
    Currency: str
    VacancyId: str
    VacancyLink: str
    RequiredSkills: List[Skills]


class Usuario(Event):
    UserId: str
    FirstName: str
    LastName: str
    Email: str
    YearsPreviousExperience: int
    Skills: List[Skills]


class Empresa(Event):
    CompanyId: str
    CompanyName: str
