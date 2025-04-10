import psycopg2

from config import config
from src.json_reader import JSONFileManager


class DBCreater:
    """Класс создания базы данных"""

    def __init__(self):
        self.vacancies_json = JSONFileManager().get_data_from_file()

    def db_create(self, params: dict, database_name: str = 'vacancies') -> None:
        """Метод создания баз данных и заполнения их данными"""

        connection = psycopg2.connect(database="postgres", **params)
        connection.autocommit = True
        # Открытие курсора
        cur = connection.cursor()

        cur.execute(f"DROP DATABASE IF EXISTS {database_name}")

        cur.execute(f"CREATE DATABASE {database_name}")

        # Закрытие курсора
        cur.close()

        # Закрытие соединения
        connection.close()

        connection = psycopg2.connect(database=database_name, **params)

        cur = connection.cursor()

        cur.execute("CREATE TABLE employers (employer_id varchar(25) PRIMARY KEY, employer_name varchar(225))")

        cur.execute(
            """
            CREATE TABLE vacancies (
            id serial PRIMARY KEY, 
            vacancies_id varchar(25), 
            department_name varchar(225), 
            vacancy_name varchar(225) NOT NULL, 
            salary int NOT NULL, url_vacancy text, 
            employer_id varchar(25) REFERENCES employers(employer_id))
            """
        )

        # Фиксируем изменения в базе данных
        connection.commit()

        list_of_id_emp = []
        list_of_emp_name = []
        for vacancies in self.vacancies_json:
            for vacancy in vacancies:
                if vacancy["employer"]["id"] not in list_of_id_emp:
                    list_of_id_emp.append(vacancy["employer"]["id"])
                if vacancy["employer"]["name"] not in list_of_emp_name:
                    list_of_emp_name.append(vacancy["employer"]["name"])

        employers_dict = dict(zip(list_of_id_emp, list_of_emp_name))

        for k, v in employers_dict.items():
            cur.execute("INSERT INTO employers (employer_id, employer_name) VALUES (%s, %s) returning *", (k, v))

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
                    """
                    INSERT INTO vacancies (
                    vacancies_id, 
                    department_name, 
                    vacancy_name, 
                    salary, url_vacancy, 
                    employer_id
                    ) 
                    VALUES (%s, %s, %s, %s, %s, %s) returning *
                    """,
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

        cur.close()
        connection.close()


if __name__ == "__main__":
    my_params = config()
    create_db = DBCreater().db_create(my_params)
    print(create_db)
