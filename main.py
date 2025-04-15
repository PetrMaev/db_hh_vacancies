from src.api_vacancies import HeadHunterAPI
from src.user_interactive import get_data_for_create_db


def main():
    hh_id_companies = ["68587", "4216955", "78638", "3529", "4181", "654435", "1305791", "39305", "80", "5591530"]
    HeadHunterAPI().get_vacancies(hh_id_companies)

    print("Привет! Добро пожаловать в программу работы с базами данных вакансий.\n")
    get_data_for_create_db()


main()
