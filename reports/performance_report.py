"""Класс отчета эффективности разработчиков"""

from typing import List, Tuple
from file_processing import Employee
from reports.base_report import Report


class PerformanceReport(Report):
    """
    Класс отчета по средней эффективности разработчиков
    """

    name = "performance"
    headers = ["Position", "Average performance"]

    def calculate(self, employees: List[Employee]) -> List[Tuple[str, float]]:
        """
        Вычисление средней эффективности для каждой позиции

        Args:
            employees (List[Employee]): список информации по работникам

        Returns:
            List[Tuple[str, float]]: отчет (позиция, средняя эффективность)
        """
        performance_data = {}
        for per in employees:
            position = per["position"]
            performance = per["performance"]
            if position not in performance_data:
                performance_data[position] = {"total_performance": 0, "count": 0}
            performance_data[position]["total_performance"] += performance
            performance_data[position]["count"] += 1
        report = [
            (position, round(data["total_performance"] / data["count"], 2))
            for position, data in performance_data.items()
        ]
        return sorted(report, key=lambda x: x[0])
