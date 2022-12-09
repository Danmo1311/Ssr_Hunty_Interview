from typing import List

from pydantic import BaseModel


class Command(BaseModel):
    pass


class Skills(Command):
    skillName: str
    skillYears: int


class Vacante(Command):
    PositionName: str
    Salary: int
    Currency: str
    VacancyLink: str
    CompanyName:str
    RequiredSkills: List[Skills]


class Usuario(Command):
    FirstName: str
    LastName: str
    Email: str
    YearsPreviousExperience: int
    Skills: List[Skills]


class Empresa(Command):
    CompanyName: str
