"""
Тесты для базового класса отчета
"""

from reports.base_report import Report


def test_report_child_registration():
    """
    Проверка регистрации дочерних отчетов
    """

    class RandomReport(Report):
        """Тестовый класс"""
        name = "random"
        headers = ["h"]

        def calculate(self, _):
            """Тестовая функция"""
            return []

    assert "random" in Report.registry
    assert Report.registry["random"] is RandomReport


def test_duplicate_name_override():
    """
    Проверка перезаписи дочернего отчета
    """

    class R1(Report):
        """Тестовый класс"""
        name = "rep"
        headers = ["h"]

        def calculate(self, _):
            """Тестовая функция"""
            return []

    assert "rep" in Report.registry
    assert Report.registry["rep"] is R1

    class R2(Report):
        """Тестовый класс"""
        name = "rep"
        headers = ["h"]

        def calculate(self, _):
            """Тестовая функция"""
            return []

    assert Report.registry["rep"] is R2
