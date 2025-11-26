"""
Обработка csv-файла
"""
import csv
from typing import TypedDict, List


class Employee(TypedDict):
    """
    Словарь-тип работника

    Args:
        name(str): имя работника
        position(str): должность
        completed_tasks(int): число выполненных задач
        performance(float): эффективность работы
        skills(List[str]): навыки
        team(str): название штата
        experience_years(int): стаж работы
    """

    name: str
    position: str
    completed_tasks: int
    performance: float
    skills: List[str]
    team: str
    experience_years: int


def parse_skills(raw_value: str) -> List[str]:
    """
    Парсинг строки навыков
    """
    if not raw_value:
        return []
    cleaned = raw_value.strip().strip('"').strip("'")
    return [skill.strip() for skill in cleaned.split(",") if skill.strip()]


def read_csv(file_list: List[str]) -> List[Employee]:
    """
    Чтение данных из файлов

    Args:
        file_list (List[str]): Список путей к файлам

    Returns:
        data (List[Employee]): Список работников, где каждый представлен экземпляром класса Employee
    """
    data = []
    for filename in file_list:
        try:
            with open(filename, newline="", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    employee: Employee = {
                        "name": row["name"],
                        "position": row["position"],
                        "completed_tasks": int(row["completed_tasks"]),
                        "performance": float(row["performance"]),
                        "skills": parse_skills(row["skills"]),
                        "team": row["team"],
                        "experience_years": int(row["experience_years"]),
                    }
                    data.append(employee)
        except FileNotFoundError:
            print(f"Ошибка: файл '{filename}' не найден.")
            return []
        except Exception as e:
            print(f"Ошибка при чтении файла '{filename}': {e}")
            return []
    return data
