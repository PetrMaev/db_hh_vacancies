import os

import psycopg2

from dotenv import load_dotenv

load_dotenv()


class DBManager:
    """Класс для работы с данными базы данных"""

    def __init__(self):
        self.get_password = os.getenv("PASSWORD")

    def get_companies_and_vacancies_count(self):
        """Метод вывода всех компаний и количество вакансий у каждой компании"""

        connection = psycopg2.connect(
            host="localhost", port="5432", database="vacancies", user="postgres", password=f"{self.get_password}"
        )

        # Открытие курсора
        cur = connection.cursor()

        cur.execute(
            "SELECT employer_name, COUNT(*) FROM employers JOIN vacancies USING(employer_id) GROUP BY employer_name"
        )

        connection.commit()
        res_count_vacancies = cur.fetchall()
        print(res_count_vacancies)

        # Закрытие курсора
        cur.close()

        # Закрытие соединения
        connection.close()

    def get_all_vacancies(self):
        """Метод получения списка всех вакансий"""

        connection = psycopg2.connect(
            host="localhost", port="5432", database="vacancies", user="postgres", password=f"{self.get_password}"
        )

        # Открытие курсора
        cur = connection.cursor()

        cur.execute(
            "SELECT employer_name, vacancy_name, salary, url_vacancy FROM vacancies JOIN employers USING(employer_id)"
        )

        connection.commit()
        res_all_vacancies = cur.fetchall()
        print(res_all_vacancies)

        # Закрытие курсора
        cur.close()

        # Закрытие соединения
        connection.close()

    def get_avg_salary(self):
        """Метод получения средней зарплаты"""

        connection = psycopg2.connect(
            host="localhost", port="5432", database="vacancies", user="postgres", password=f"{self.get_password}"
        )

        # Открытие курсора
        cur = connection.cursor()

        cur.execute("SELECT AVG(salary) FROM vacancies")

        connection.commit()
        res_avg_vacancies = cur.fetchall()
        print(res_avg_vacancies)

        # Закрытие курсора
        cur.close()

        # Закрытие соединения
        connection.close()

    def get_vacancies_with_higher_salary(self):
        """Метод получения списка вакансий, в которых зарплата выше средней"""

        connection = psycopg2.connect(
            host="localhost", port="5432", database="vacancies", user="postgres", password=f"{self.get_password}"
        )

        # Открытие курсора
        cur = connection.cursor()

        cur.execute(
            "SELECT employer_name, vacancy_name, url_vacancy FROM vacancies JOIN employers USING(employer_id) WHERE salary > 127179"
        )

        connection.commit()
        res_high_vacancies = cur.fetchall()
        print(res_high_vacancies)

        # Закрытие курсора
        cur.close()

        # Закрытие соединения
        connection.close()

    def get_vacancies_with_keyword(self, search_word: str):
        """Метод получения списка вакансий, в названии которых содержится заданное слово"""

        connection = psycopg2.connect(
            host="localhost", port="5432", database="vacancies", user="postgres", password=f"{self.get_password}"
        )

        # Открытие курсора
        cur = connection.cursor()

        cur.execute(f"SELECT * FROM vacancies WHERE vacancy_name LIKE '%{search_word}%'")

        connection.commit()
        res_vacancies_with_keyword = cur.fetchall()
        print(res_vacancies_with_keyword)

        # Закрытие курсора
        cur.close()

        # Закрытие соединения
        connection.close()


if __name__ == "__main__":
    get_count_db = DBManager().get_companies_and_vacancies_count()
    get_all_vac = DBManager().get_all_vacancies()
    get_avg_salary = DBManager().get_avg_salary()
    get_high_salary = DBManager().get_vacancies_with_higher_salary()
    get_vacancies_with_keyword = DBManager().get_vacancies_with_keyword("Инженер")
