"""
Анализ эффективности работы разработчиков
Запуск скрипта
"""

import argparse
from tabulate import tabulate
from file_processing import read_csv
from reports.base_report import Report
# Для регистрации в абстрактном классе
from reports.performance_report import PerformanceReport  # pylint: disable=unused-import


def main():
    """
    Главная функция для запуска скрипта из командной строки
    Парсит аргументы командной строки, считывает CSV-файлы, формирует отчёт и выводит в виде таблицы

    CLI Args:
        --files: Список CSV-файлов для обработки
        --report: Тип отчёта
    """
    parser = argparse.ArgumentParser(
        description="Формирование отчетов о работе разработчиков"
    )
    parser.add_argument(
        "--files",
        nargs="+",
        required=True,
        help="Пути к CSV-файлам с данными (можно несколько)",
    )
    parser.add_argument(
        "--report",
        required=True,
        choices=Report.registry.keys(),
        help=f"Тип отчета ({', '.join(Report.registry.keys())})",
    )
    args = parser.parse_args()

    try:
        data = read_csv(args.files)
        if not data:
            print("Нет данных для составления отчета")
            return
        report_cls = Report.registry[args.report]
        report = report_cls()
        result = report.calculate(data)
        if not result:
            print("Получен пустой отчет")
            return
        print(
            tabulate(
                result,
                report.headers,
                tablefmt="pretty",
                showindex=range(1, len(result) + 1),
            )
        )
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    main()
