import json
import os
from abc import ABC, abstractmethod
from json import JSONDecodeError

from config import PATH_TO_HH_VACANCIES


class FileManager(ABC):
    """Абстрактный класс для работы с вакансиями"""

    @abstractmethod
    def get_data_from_file(self, path_to_file):
        pass


class JSONFileManager(FileManager):
    """Класс для работы с вакансиями из csv-файла"""

    def get_data_from_file(self, path_to_file=PATH_TO_HH_VACANCIES):
        """Метод получения данных из csv-файла"""
        try:
            if os.path.isfile(path_to_file) and os.stat(path_to_file).st_size != 0:
                with open(path_to_file, "r", encoding="utf-8") as file:
                    list_of_vacancies = json.load(file)
                return list_of_vacancies
            else:
                raise FileNotFoundError("Файл не найден")
        except JSONDecodeError:
            return "Ошибка декодирования файла"

        except FileNotFoundError:
            return "Файл не найден"


if __name__ == "__main__":
    json_read = JSONFileManager()
    vacancies_json = json_read.get_data_from_file()
    print(vacancies_json)
    print(len(vacancies_json))
