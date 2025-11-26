"""
Тесты для обработки файлов
"""

import pytest
from file_processing import read_csv, parse_skills


@pytest.fixture
def sample_csv(tmp_path):
    """
    Создание временного CSV
    """
    content = (
        "name,position,completed_tasks,performance,skills,team,experience_years\n"
        'David Chen,Mobile Developer,36,4.6,"Swift, Kotlin, React Native, iOS",Mobile Team,3\n'
        'Elena Popova,Backend Developer,43,4.8,"Java, Spring Boot, MySQL, Redis",API Team,4\n'
    )

    file = tmp_path / "employees.csv"
    file.write_text(content, encoding="utf-8")
    return str(file)


@pytest.mark.parametrize(
    "raw, expected",
    [
        ("Python, Django", ["Python", "Django"]),
        (" Java, Spring ", ["Java", "Spring"]),
        ("", []),
        (None, []),
    ],
)
def test_parse_skills(raw, expected):
    """
    Парсинг строки навыков
    """
    assert parse_skills(raw) == expected


def test_read_csv_success(sample_csv):
    """
    Чтение одного файла
    """
    data = read_csv([sample_csv])

    assert len(data) == 2

    assert data[0]["name"] == "David Chen"
    assert data[0]["completed_tasks"] == 36
    assert data[0]["performance"] == 4.6
    assert data[0]["skills"] == ["Swift", "Kotlin", "React Native", "iOS"]

    assert data[1]["name"] == "Elena Popova"
    assert data[1]["completed_tasks"] == 43
    assert data[1]["performance"] == 4.8
    assert data[1]["skills"] == ["Java", "Spring Boot", "MySQL", "Redis"]


def test_read_csv_file_not_found(capsys):
    """
    Чтение несуществующего файла
    """
    result = read_csv(["filenotfound.csv"])
    out = capsys.readouterr().out.lower()
    assert not result
    assert "файл 'filenotfound.csv' не найден" in out


def test_read_multiple_files(sample_csv, tmp_path):
    """
    Чтение нескольких файлов
    """
    extra_content = (
        "name,position,completed_tasks,performance,skills,team,experience_years\n"
        'Julia Martin,QA Engineer,38,4.5,"Playwright, Jest, API Testing",Testing Team,3\n'
    )
    file2 = tmp_path / "extra.csv"
    file2.write_text(extra_content, encoding="utf-8")

    data = read_csv([sample_csv, str(file2)])

    assert len(data) == 3
    assert data[-1]["name"] == "Julia Martin"
    assert data[-1]["completed_tasks"] == 38
    assert data[-1]["performance"] == 4.5
    assert data[-1]["skills"] == ["Playwright", "Jest", "API Testing"]
