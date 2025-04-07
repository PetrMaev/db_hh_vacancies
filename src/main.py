from src.api_vacancies import HeadHunterAPI
from src.db_creater import DBCreater
from src.user_interactive import (get_all_vacancies, get_avg_salary, get_companies_and_vacancies_count,
                                  get_vacancies_with_higher_salary, get_vacancies_with_keyword)


def main():
    hh_id_companies = ["68587", "4216955", "78638", "3529", "4181", "654435", "1305791", "39305", "80", "5591530"]
    HeadHunterAPI().get_vacancies(hh_id_companies)

    DBCreater().db_create()

    print("Привет! Добро пожаловать в программу работы с базами данных вакансий.\n")
    get_companies_and_vacancies_count()
    get_all_vacancies()
    get_avg_salary()
    get_vacancies_with_higher_salary()
    get_vacancies_with_keyword()


main()
