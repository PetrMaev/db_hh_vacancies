from src.db_manager import DBManager


def get_companies_and_vacancies_count() -> str:
    """Функция вывода количества вакансий у каждого работодателя из базы данных."""

    while True:
        question_1 = input("Вывести информацию по количеству вакансий у работодателей из базы данных: Да\Нет ").lower()

        if question_1 == "да":
            print("Вывожу список работодателей с количеством вакансий:")
            get_count_db = DBManager().get_companies_and_vacancies_count()
            return get_count_db
        elif question_1 == "нет":
            break
        else:
            print(f"Ошибка. Повторите попытку.\n")


def get_all_vacancies() -> str:
    """Функция вывода всех вакансий базы данных."""

    while True:
        question_2 = input("Вывести информацию по всем вакансиям базы данных: Да\Нет ").lower()

        if question_2 == "да":
            print("Вывожу список всех вакансий:")
            get_all_vac = DBManager().get_all_vacancies()
            return get_all_vac
        elif question_2 == "нет":
            break
        else:
            print(f"Ошибка. Повторите попытку.\n")


def get_avg_salary() -> str:
    """Функция вывода средней зарплаты вакансий."""

    while True:
        question_3 = input("Вывести среднюю зарплату вакансий базы данных: Да\Нет ").lower()

        if question_3 == "да":
            print("Вывожу среднюю зарплату:")
            get_avg_sal = DBManager().get_avg_salary()
            return get_avg_sal
        elif question_3 == "нет":
            break
        else:
            print(f"Ошибка. Повторите попытку.\n")


def get_vacancies_with_higher_salary() -> str:
    """Функция вывода вакансий с зарплатой выше средней."""

    while True:
        question_4 = input("Вывести информацию по вакансиям с зарплатой выше средней: Да\Нет ").lower()

        if question_4 == "да":
            get_high_salary = DBManager().get_vacancies_with_higher_salary()
            return get_high_salary
        elif question_4 == "нет":
            break
        else:
            print(f"Ошибка. Повторите попытку.\n")


def get_vacancies_with_keyword() -> str:
    """Функция вывода вакансий по заданному слову."""
    search_query = input("Введите ключевое слово для фильтрации вакансий: ")
    get_vacancies_of_keyword = DBManager().get_vacancies_with_keyword(search_query)
    return get_vacancies_of_keyword


if __name__ == "__main__":
    # get_companies_and_vacancies_count()
    # get_all_vacancies()
    # get_avg_salary()
    # get_vacancies_with_higher_salary()
    get_vacancies_with_keyword()
