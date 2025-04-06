import os

import psycopg2

from dotenv import load_dotenv

from src.json_reader import JSONFileManager

load_dotenv()


class DBCreater:
    """Класс создания базы данных"""

    def __init__(self):
        self.get_password = os.getenv("PASSWORD")
        self.hh_id_companies = [
            "68587",
            "4216955",
            "78638",
            "3529",
            "4181",
            "654435",
            "1305791",
            "39305",
            "80",
            "5591530",
        ]
        self.vacancies_json = JSONFileManager().get_data_from_file()

    def db_create(self) -> None:
        """Метод создания баз данных и заполнения их данными"""
        connection = psycopg2.connect(
            host="localhost", port="5432", database="vacancies", user="postgres", password=f"{self.get_password}"
        )

        # Открытие курсора
        cur = connection.cursor()

        cur.execute("TRUNCATE TABLE vacancies RESTART IDENTITY")

        cur.execute("DROP TABLE IF EXISTS vacancies")

        cur.execute(
            "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = 'employers' AND pid <> pg_backend_pid()"
        )

        cur.execute("DROP TABLE IF EXISTS employers")

        cur.execute("CREATE TABLE employers (employer_id varchar(25) PRIMARY KEY)")

        cur.execute(
            "CREATE TABLE vacancies (id serial PRIMARY KEY, vacancies_id varchar(25), department_name varchar(225), vacancy_name varchar(225) NOT NULL, salary int NOT NULL, url_vacancy text, employer_id varchar(25) REFERENCES employers(employer_id) NOT NULL)"
        )

        # Фиксируем изменения в базе данных
        connection.commit()

        for id_company in self.hh_id_companies:
            cur.execute("INSERT INTO employers (employer_id) VALUES (%s) returning *", (id_company,))

        connection.commit()
        res_employers = cur.fetchall()
        print(res_employers)

        for vacancies in self.vacancies_json:
            for vacancy in vacancies:
                if vacancy["salary"]["from"] is not None and vacancy["salary"]["to"] is not None:
                    salary = (int(vacancy["salary"]["from"]) + int(vacancy["salary"]["to"])) / 2
                elif vacancy["salary"]["from"] is None:
                    salary = vacancy["salary"]["to"]
                elif vacancy["salary"]["to"] is None:
                    salary = vacancy["salary"]["from"]

                if vacancy["department"] is not None:
                    name_department = vacancy["department"]["name"]
                else:
                    name_department = vacancy["employer"]["name"]

                cur.execute(
                    "INSERT INTO vacancies (vacancies_id, department_name, vacancy_name, salary, url_vacancy, employer_id) VALUES (%s, %s, %s, %s, %s, %s) returning *",
                    (
                        vacancy["id"],
                        name_department,
                        vacancy["name"],
                        salary,
                        vacancy["alternate_url"],
                        vacancy["employer"]["id"],
                    ),
                )

        connection.commit()
        res_vacancies = cur.fetchall()
        print(res_vacancies)

        # Закрытие курсора
        cur.close()

        # Закрытие соединения
        connection.close()


if __name__ == "__main__":
    create_db = DBCreater().db_create()
    print(create_db)
