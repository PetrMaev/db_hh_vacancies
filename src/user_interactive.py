from config import config
from src.db_creater import DBCreater
from src.db_manager import DBManager

from config import PATH_TO_HH_DATABASE


def get_data_for_create_db():
    print("Введите данные для подключения к базе данных.\n")
    your_host = input("Введите хост: ")
    your_port = input("Введите номер порта: ")
    database_name = input("Введите имя базы данных: ")
    user_name = input("Введите имя пользователя: ")
    your_password = input("Введите пароль: ")

    new_params = f'[postgresql]\nhost={your_host}\nport={your_port}\nuser={user_name}\npassword={your_password}'

    with open(PATH_TO_HH_DATABASE, 'w', encoding='utf-8') as f:
        f.write(new_params)

    params = config()
    DBCreater().db_create(params, database_name)

    # Вывод информации по количеству вакансий у работодателей
    while True:
        question_1 = input("Вывести информацию по количеству вакансий у работодателей из базы данных: Да\Нет ").lower()

        if question_1 == "да":
            print("Вывожу список работодателей с количеством вакансий:")
            get_count_db = DBManager().get_companies_and_vacancies_count(params, database_name)
            print(get_count_db)
            break
        elif question_1 == "нет":
            break
        else:
            print(f"Ошибка. Повторите попытку.\n")

    # Вывод информации по всем вакансиям базы данных
    while True:
        question_2 = input("Вывести информацию по всем вакансиям базы данных: Да\Нет ").lower()

        if question_2 == "да":
            print("Вывожу список всех вакансий:")
            get_all_vac = DBManager().get_all_vacancies(params, database_name)
            print(get_all_vac)
            break
        elif question_2 == "нет":
            break
        else:
            print(f"Ошибка. Повторите попытку.\n")

    # Вывода средней зарплаты вакансий.
    while True:
        question_3 = input("Вывести среднюю зарплату вакансий базы данных: Да\Нет ").lower()

        if question_3 == "да":
            print("Вывожу среднюю зарплату:")
            get_avg_sal = DBManager().get_avg_salary(params, database_name)
            print(get_avg_sal)
            break
        elif question_3 == "нет":
            break
        else:
            print(f"Ошибка. Повторите попытку.\n")

    # Вывод вакансий с зарплатой выше средней.
    while True:
        question_4 = input("Вывести информацию по вакансиям с зарплатой выше средней: Да\Нет ").lower()

        if question_4 == "да":
            get_high_salary = DBManager().get_vacancies_with_higher_salary(params, database_name)
            print(get_high_salary)
            break
        elif question_4 == "нет":
            break
        else:
            print(f"Ошибка. Повторите попытку.\n")

    # Вывод вакансий по заданному слову.
    search_query = input("Введите ключевое слово для фильтрации вакансий: ")
    get_vacancies_of_keyword = DBManager().get_vacancies_with_keyword(search_query, params, database_name)
    print(get_vacancies_of_keyword)


if __name__ == "__main__":
    get_data_for_create_db()
