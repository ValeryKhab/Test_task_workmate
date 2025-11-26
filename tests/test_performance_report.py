"""
Тесты для класса отчета эффективности
"""

import pytest
from reports.performance_report import PerformanceReport


@pytest.fixture
def employees():
    """
    Создание списка работников
    """
    return [
        {
            "name": "David Chen",
            "position": "Mobile Developer",
            "completed_tasks": 36,
            "performance": 4.6,
            "skills": ["Swift", "Kotlin", "React Native", "iOS"],
            "team": "Mobile Team",
            "experience_years": 3,
        },
        {
            "name": "Elena Popova",
            "position": "Mobile Developer",
            "completed_tasks": 43,
            "performance": 4.8,
            "skills": ["Java", "Spring Boot", "MySQL", "Redis"],
            "team": "API Team",
            "experience_years": 4,
        },
        {
            "name": "Chris Wilson",
            "position": "DevOps Engineer",
            "completed_tasks": 39,
            "performance": 4.7,
            "skills": ["Docker", "Jenkins", "GitLab CI", "AWS"],
            "team": "Infrastructure Team",
            "experience_years": 5,
        },
    ]


def test_calculate_performance(employees):
    """
    Проверка вычисления отчета
    """
    report = PerformanceReport()
    result = report.calculate(employees)
    assert isinstance(result, list)
    assert ("Mobile Developer", 4.7) in result
    assert ("DevOps Engineer", 4.7) in result


def test_sorted_by_position(employees):
    """
    Проверка сортировки
    """
    report = PerformanceReport()
    result = report.calculate(employees)
    positions = [pos for pos, _ in result]
    assert positions == sorted(positions)
