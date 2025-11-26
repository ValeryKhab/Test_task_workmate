"""
Базовый класс отчета
"""

from abc import ABC, abstractmethod
from typing import List, Tuple
from file_processing import Employee


class Report(ABC):
    """
    Абстрактный базовый класс отчета
    """

    registry = {}

    name: str
    headers: List[str]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if hasattr(cls, "name") and cls.name:
            Report.registry[cls.name] = cls

    @abstractmethod
    def calculate(self, employees: List[Employee]) -> List[Tuple[str, float]]:
        """
        Выполняет рассчеты для отчета
        """
