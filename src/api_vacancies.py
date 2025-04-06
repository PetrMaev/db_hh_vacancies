import json
from abc import ABC, abstractmethod

import requests

from config import PATH_TO_HH_VACANCIES


class HH(ABC):
    """Абстрактный класс для получения вакансий"""

    @abstractmethod
    def get_vacancies(self, companies_id_list: list):
        pass


class HeadHunterAPI(HH):
    """Класс для получения вакансий с помощью API с сайта hh.ru"""

    def __init__(self):
        self.__url = "https://api.hh.ru/vacancies"
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params = {"employer_id": "", "only_with_salary": True}
        self.vacancies = []

    def get_vacancies(self, companies_id_list: list) -> None:
        """Метод получения вакансий с hh.ru по заданным ID компаний"""

        try:
            for company_id in companies_id_list:
                self.__params["employer_id"] = company_id
                response = requests.get(self.__url, headers=self.__headers, params=self.__params)
                if response.status_code == 200:
                    vacancies = response.json()["items"]
                    self.vacancies.append(vacancies)
                else:
                    raise ConnectionError("Connection Error. Please check your network connection.")
            with open(PATH_TO_HH_VACANCIES, "w", encoding="utf-8") as f:
                json.dump(self.vacancies, f, ensure_ascii=False, indent=4)

        except KeyError:
            print("KeyError")

        except FileNotFoundError:
            print("FileNotFound")
        else:
            print("Получение данных с hh.ru выполнено успешно")


if __name__ == "__main__":
    hh_id_companies = ["68587", "4216955", "78638", "3529", "4181", "654435", "1305791", "39305", "80", "5591530"]
    hh_api = HeadHunterAPI()
    hh_vacancies = hh_api.get_vacancies(hh_id_companies)
