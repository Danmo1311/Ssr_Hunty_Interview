import http

from bson import ObjectId

from fastapi import HTTPException

from conf.db_config import mydb
from domain import events,commands

"""
Handlers es el archivo encargado de toda la logica para no cargar los endpoints con operaciones complejas
y que estos solo se encarguen de devolver la respuesta al request
"""""


def count_skills(skills_req, user_skills):
    numb_skills = 0
    for skill in user_skills:
        for item in skills_req:

            if item["skillName"] == skill["skillName"] and skill["skillYears"] >= item["skillYears"]:
                numb_skills = numb_skills + 1

    return numb_skills


def get_user(user_id: str):
    mycol = mydb["usuarios"]
    user = mycol.find_one({"_id": ObjectId(user_id)})

    return user["Skills"]


def recomendacion_vacantes(user_id: str) -> [events.Vacante]:
    user_skills = get_user(user_id=user_id)
    mycol = mydb["vacantes"]
    refer_vacant = []
    response = []
    vacants_skills = list(mycol.find({}))

    for item in vacants_skills:
        numb_paired_up = 0
        five_porcent = len(item["RequiredSkills"]) / 2
        if five_porcent > 1:
            numb_paired_up = count_skills(skills_req=item["RequiredSkills"], user_skills=user_skills)
        if numb_paired_up > five_porcent:
            refer_vacant.append(item)

    for item in refer_vacant:
        vacantes = events.Vacante(
            PositionName=item["PositionName"],
            CompanyName=item["CompanyName"],
            Salary=item["Salary"],
            Currency=item["Currency"],
            VacancyId=str(item["_id"]),
            VacancyLink=item["VacancyLink"],
            RequiredSkills=item["RequiredSkills"]
        )
        response.append(vacantes)

    return response


def get_usuarios() -> [events.Usuario]:
    mycol = mydb["usuarios"]

    if len(list(mycol.find({}))) >= 1:
        usuarios = mycol.find({})
        response = []

        for item in usuarios:
            vacante = events.Usuario(
                UserId=str(item["_id"]),
                FirstName=item["FirstName"],
                LastName=item["LastName"],
                Email=item["Email"],
                YearsPreviousExperience=item["YearsPreviousExperience"],
                Skills=item["Skills"]
            )
            response.append(vacante)

        return response
    else:
        raise HTTPException(
            status_code=400, detail="No hay usuarios aún, inserte por favor uno"
        )


def get_vacantes() -> [events.Vacante]:
    mycol = mydb["vacantes"]

    if len(list(mycol.find({}))) >= 1:
        vacantes = mycol.find({})
        response = []
        for item in vacantes:
            vacante = events.Vacante(

                PositionName=item["PositionName"],
                CompanyName=item["CompanyName"],
                Salary=item["Salary"],
                Currency=item["Currency"],
                VacancyId=str(item["_id"]),
                VacancyLink=item["VacancyLink"],
                RequiredSkills=item["RequiredSkills"]
            )
            response.append(vacante)

        return response
    else:
        raise HTTPException(

            status_code=400, detail="No hay Vacantes aún, inserte por favor una"

        )


def get_empresas_by_id(empresa_id: str) -> events.Empresa:
    mycol = mydb["empresas"]

    try:
        empresa = mycol.find_one({"_id": ObjectId(empresa_id)})
        response = events.Empresa(
            CompanyId=str(empresa["_id"]),
            CompanyName=empresa["CompanyName"]

        )

        return response
    except:
        raise HTTPException(
            status_code=404, detail=f"La empresa con ID {empresa_id} no se ha encontrado"
        )


def get_empresas() -> [events.Empresa]:
    mycol = mydb["empresas"]

    if len(list(mycol.find({}))) >= 1:
        empresas = mycol.find({})
        response = []
        for item in empresas:
            empresa = events.Empresa(
                CompanyId=str(item["_id"]),
                CompanyName=item["CompanyName"],
            )
            response.append(empresa)

        return response
    else:
        raise HTTPException(
            status_code=400, detail="No hay Empresas aún, inserte por favor una"
        )


def create_usuarios(usuarios: [commands.Usuario]):
    user_to_insert = []
    vacant_skills = []
    mycol = mydb["usuarios"]
    for item in usuarios:

        for skill in item.Skills:
            skills = {
                "skillName": skill.skillName,
                "skillYears": skill.skillYears
            }
            vacant_skills.append(skills)
        usuario = {
            "FirstName": item.FirstName,
            "LastName": item.LastName,
            "Email": item.Email,
            "YearsPreviousExperience": item.YearsPreviousExperience,
            "Skills": vacant_skills
        }
        vacant_skills = []
        user_to_insert.append(usuario)
    mycol.insert_many(user_to_insert)

    return usuarios


def create_vacantes(company_name: str, vacantes: [commands.Vacante]):
    mycol = mydb["empresas"]
    vacant_to_insert = []
    vacant_skills = []

    try:
        if mycol.find_one({"CompanyName": company_name}):
            mycol = mydb["vacantes"]
            for item in vacantes:
                for skill in item.RequiredSkills:
                    skills = {
                        "skillName": skill.skillName,
                        "skillYears": skill.skillYears
                    }
                    vacant_skills.append(skills)
                Vacante = {
                    "PositionName": item.PositionName,
                    "CompanyName": company_name,
                    "Salary": item.Salary,
                    "Currency": item.Currency,
                    "VacancyLink": item.VacancyLink,
                    "RequiredSkills": vacant_skills
                }
                vacant_skills = []
                vacant_to_insert.append(Vacante)
            mycol.insert_many(vacant_to_insert)

        return vacantes
    except:
        raise HTTPException(
            status_code=404, detail=f"la empresa con nombre {company_name} no se ha encontrado"
        )


def get_vacante_by_id(vacante_id: str) -> events.Vacante:
    mycol = mydb["vacantes"]
    try:
        vacante = mycol.find_one({"_id": ObjectId(vacante_id)})
        response = events.Vacante(
            PositionName=vacante["PositionName"],
            CompanyName=vacante["CompanyName"],
            Salary=vacante["Salary"],
            Currency=vacante["Currency"],
            VacancyId=str(vacante["_id"]),
            VacancyLink=vacante["VacancyLink"],
            RequiredSkills=vacante["RequiredSkills"]

        )

        return response
    except:

        raise HTTPException(
            status_code=404, detail=f"la vacante con ID {vacante_id} no se ha encontrado"
        )


def get_usuario_by_id(user_id: str) -> events.Usuario:
    mycol = mydb["usuarios"]

    try:
        usuario = mycol.find_one({"_id": ObjectId(user_id)})
        response = events.Usuario(
            UserId=str(usuario["_id"]),
            FirstName=usuario["FirstName"],
            LastName=usuario["LastName"],
            Email=usuario["Email"],
            YearsPreviousExperience=usuario["YearsPreviousExperience"],
            Skills=usuario["Skills"]

        )

        return response
    except:

        raise HTTPException(
            status_code=404, detail=f"la vacante con ID {user_id} no se ha encontrado"
        )


def actualizar_vacante(vacante: commands.Vacante, vacante_id: str) -> events.Vacante:
    mycol = mydb["vacantes"]
    vacant_skills = []

    try:
        if mycol.find_one({"_id": ObjectId(vacante_id)}):
            myquery = {"_id": ObjectId(vacante_id)}
            for item in vacante.RequiredSkills:
                skills = {
                    "skillName": item.skillName,
                    "skillYears": item.skillYears
                }
                vacant_skills.append(skills)
            vacante = {
                "$set":
                    {"PositionName": vacante.PositionName,
                     "CompanyName": vacante.CompanyName,
                     "Salary": vacante.Salary,
                     "Currency": vacante.Currency,
                     "VacancyLink": vacante.VacancyLink,
                     "RequiredSkills": vacant_skills
                     }
            }

            mycol.update_one(myquery, vacante)

            response = events.Vacante(
                PositionName=vacante["$set"]["PositionName"],
                CompanyName=vacante["$set"]["CompanyName"],
                Salary=vacante["$set"]["Salary"],
                Currency=vacante["$set"]["Currency"],
                VacancyId=vacante_id,
                VacancyLink=vacante["$set"]["VacancyLink"],
                RequiredSkills=vacante["$set"]["RequiredSkills"]
            )

            return response
    except:
        raise HTTPException(
            status_code=404, detail=f"la vacante con ID {vacante_id} no se ha encontrado"
        )


def actualizar_empresa(empresa: commands.Empresa, empresa_id: str) -> events.Empresa:
    mycol = mydb["empresas"]
    try:
        if mycol.find_one({"_id": ObjectId(empresa_id)}):
            myquery = {"_id": ObjectId(empresa_id)}
            empresa = {
                "$set":
                    {
                        "CompanyName": empresa.CompanyName,
                    }
            }
            mycol.update_one(myquery, empresa)
            response = events.Empresa(
                CompanyName=empresa["$set"]["CompanyName"],
                CompanyId=empresa_id,
            )

            return response

    except:
        raise HTTPException(
            status_code=404, detail=f"la vacante con ID {empresa_id} no se ha encontrado"
        )


def actualizar_usuario(usuario: commands.Usuario, user_id: str) -> events.Usuario:
    mycol = mydb["usuarios"]
    vacant_skills = []
    try:
        if mycol.find_one({"_id": ObjectId(user_id)}):
            myquery = {"_id": ObjectId(user_id)}
            for item in usuario.Skills:
                skills = {
                    "skillName": item.skillName,
                    "skillYears": item.skillYears
                }
                vacant_skills.append(skills)
            usuario = {
                "$set":
                    {
                        "FirstName": usuario.FirstName,
                        "LastName": usuario.LastName,
                        "Email": usuario.Email,
                        "YearsPreviousExperience": usuario.YearsPreviousExperience,
                        "Skills": vacant_skills
                    }
            }
            mycol.update_one(myquery, usuario)
            response = events.Usuario(
                FirstName=usuario["$set"]["FirstName"],
                LastName=usuario["$set"]["LastName"],
                Email=usuario["$set"]["Email"],
                YearsPreviousExperience=usuario["$set"]["YearsPreviousExperience"],
                UserId=user_id,
                Skills=usuario["$set"]["Skills"]
            )

            return response
    except:
        raise HTTPException(
            status_code=404, detail=f"la vacante con ID {user_id} no se ha encontrado"
        )


def eliminar_vacante(vacante_id: str):
    mycol = mydb["vacantes"]

    try:
        mycol.delete_one({"_id": ObjectId(vacante_id)})

        return http.HTTPStatus.OK
    except:
        raise HTTPException(
            status_code=404, detail=f"la vacante con ID {vacante_id} no se ha encontrado"
        )


def eliminar_usuario(user_id: str):
    mycol = mydb["usuarios"]

    try:
        mycol.delete_one({"_id": ObjectId(user_id)})

        return http.HTTPStatus.OK
    except:
        raise HTTPException(
            status_code=404, detail=f"la vacante con ID {user_id} no se ha encontrado"
        )


def create_empresas(empresas: [commands.Empresa]):
    mycol = mydb["empresas"]
    company_to_insert = []

    try:
        for item in empresas:
            Vacante = {
                "CompanyName": item.CompanyName,
            }
            company_to_insert.append(Vacante)
        mycol.insert_many(company_to_insert)

        return empresas
    except:
        raise HTTPException(
            status_code=400, detail="no se pudo hacer el insert"
        )


def eliminar_empresa(empresa_id: str):
    mycol = mydb["empresas"]

    try:
        mycol.delete_one({"_id": ObjectId(empresa_id)})
        return http.HTTPStatus.OK
    except:
        raise HTTPException(
            status_code=404, detail=f"la vacante con ID {empresa_id} no se ha encontrado"
        )
