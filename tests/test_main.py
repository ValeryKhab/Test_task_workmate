"""
Тесты для главного файла
"""

import main
from reports.base_report import Report
from reports.performance_report import PerformanceReport


def test_main_success(monkeypatch, capsys):
    """
    Успешный запуск
    """

    def fake_calculate(self, _):  # pylint: disable=unused-argument
        """Тестовая функция"""
        return [("David", 4.5)]

    monkeypatch.setattr(PerformanceReport, "calculate", fake_calculate)
    monkeypatch.setattr(
        main, "read_csv", lambda files: [{"name": "David", "performance": 4.5}]
    )
    monkeypatch.setattr(main, "tabulate", lambda *a, **kw: "TABLE_OUTPUT")
    monkeypatch.setattr(
        "sys.argv", ["prog", "--files", "file.csv", "--report", "performance"]
    )
    main.main()
    out = capsys.readouterr().out
    assert "TABLE_OUTPUT" in out


def test_main_file_not_found(monkeypatch, capsys):
    """
    Запуск с несуществующим файлом (файл не найден)
    """

    monkeypatch.setattr(main, "read_csv", lambda _: None)
    monkeypatch.setattr(
        "sys.argv", ["prog", "--files", "missing.csv", "--report", "performance"]
    )
    main.main()
    out = capsys.readouterr().out.lower()
    assert "нет данных для составления отчета" in out


def test_main_empty_report(monkeypatch, capsys):
    """
    Получение пустого отчета
    """

    monkeypatch.setattr(main, "read_csv", lambda _: [{"name": "David"}])

    class FakeReport(Report):
        """Тестовый класс"""
        name = "performance"

        def calculate(self, _):
            """Тестовая функция"""
            return []

    monkeypatch.setattr(Report, "registry", {"performance": FakeReport})
    monkeypatch.setattr(
        "sys.argv", ["prog", "--files", "file.csv", "--report", "performance"]
    )
    main.main()
    out = capsys.readouterr().out.lower()
    assert "получен пустой отчет" in out


def test_main_report_exception(monkeypatch, capsys):
    """
    Получение ошибки во время составления отчета
    """

    monkeypatch.setattr(main, "read_csv", lambda _: [{"name": "Bob"}])

    class ErrorReport(PerformanceReport):
        """Тестовый класс"""
        name = "performance"

        def calculate(self, _):
            """Тестовая функция"""
            raise RuntimeError("fail")

    Report.registry["performance"] = ErrorReport
    monkeypatch.setattr(
        "sys.argv", ["prog", "--files", "f.csv", "--report", "performance"]
    )
    main.main()
    out = capsys.readouterr().out.lower()
    assert "произошла ошибка" in out
