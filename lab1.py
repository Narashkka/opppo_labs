"""Учёт растений на складе.

Поддерживаемые типы растений:
- Tree (дерево) - уникальный параметр: возраст (целое число лет).
- Shrub (кустарник) - уникальный параметр: месяц цветения.
- Cactus (кактус) - уникальный параметр: длина колючек (дробное число).

Команды обработки файла:
- ADD <тип>;<название>;<значение> - добавить растение.
- REM <условие> — удалить растения по условию (например, age > 100).
- PRINT — вывести содержимое контейнера.
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Type, cast


# Константы типов растений
TYPE_TREE: str = "tree"
TYPE_SHRUB: str = "shrub"
TYPE_CACTUS: str = "cactus"

# Константы параметров для условий удаления
PARAM_AGE: str = "age"
PARAM_SPINE_LENGTH: str = "spine_length"
PARAM_MONTH: str = "month"

# Словарь операторов сравнения
# Используем Any + cast, так как strict Protocol несовместим с int/float
_OPERATORS_RAW: Dict[str, Callable[[Any, Any], bool]] = {
    ">": lambda a, b: a > b,
    "<": lambda a, b: a < b,
    "==": lambda a, b: a == b,
    ">=": lambda a, b: a >= b,
    "<=": lambda a, b: a <= b,
}
OPERATORS: Dict[str, Callable[[object, object], bool]] = cast(
    Dict[str, Callable[[object, object], bool]], _OPERATORS_RAW
)


class Plant(ABC):
    """Абстрактный базовый класс растения."""

    name: str

    def __init__(self, name: str) -> None:
        self.name = name

    @abstractmethod
    def get_unique_value(self) -> str:
        pass

    @abstractmethod
    def get_type_name(self) -> str:
        pass

    def to_string(self) -> str:
        return (
            f"{self.get_type_name()} | Название: {self.name} | "
            f"Уник. параметр: {self.get_unique_value()}"
        )


class Tree(Plant):
    """Дерево с уникальным параметром — возраст (целое число лет)."""

    age: int

    def __init__(self, name: str, age: int) -> None:
        super().__init__(name)
        self.age = age

    def get_unique_value(self) -> str:
        return f"Возраст = {self.age} лет"

    def get_type_name(self) -> str:
        return "Дерево"


ALLOWED_MONTHS: List[str] = [
    "январь", "февраль", "март", "апрель", "май", "июнь",
    "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"
]


class Shrub(Plant):
    """Кустарник с уникальным параметром — месяц цветения."""

    bloom_month: str

    def __init__(self, name: str, month_str: str) -> None:
        super().__init__(name)
        month_lower: str = month_str.lower()
        if month_lower not in ALLOWED_MONTHS:
            raise ValueError(f"Неизвестный месяц: {month_str}")
        self.bloom_month = month_lower

    def get_unique_value(self) -> str:
        return f"Месяц цветения = {self.bloom_month.capitalize()}"

    def get_type_name(self) -> str:
        return "Кустарник"


class Cactus(Plant):
    """Кактус с уникальным параметром — длина колючек (дробное число, см)."""

    spine_length: float

    def __init__(self, name: str, spine_length: float) -> None:
        super().__init__(name)
        self.spine_length = spine_length

    def get_unique_value(self) -> str:
        return f"Длина колючек = {self.spine_length} см"

    def get_type_name(self) -> str:
        return "Кактус"


# Словарь-диспетчер для создания растений
PLANT_FACTORIES: Dict[str, Type[Plant]] = {
    TYPE_TREE: Tree,
    TYPE_SHRUB: Shrub,
    TYPE_CACTUS: Cactus,
}


class GardenContainer:
    """Контейнер для хранения и управления коллекцией растений."""

    plants: List[Plant]

    def __init__(self) -> None:
        self.plants = []

    def add_plant(self, plant: Plant) -> None:
        """Добавляет растение в контейнер."""
        self.plants.append(plant)

    def print_all(self) -> None:
        """Выводит содержимое контейнера на экран."""
        if not self.plants:
            print("Контейнер пуст.")
            return

        for i, plant in enumerate(self.plants, start=1):
            print(f"{i}. {plant.to_string()}")

    def remove_by_condition(self, condition_str: str) -> None:
        """Удаляет растения, соответствующие заданному условию."""
        parts: List[str] = condition_str.split()
        if len(parts) != 3:
            print(
                "Ошибка: неверный формат условия. "
                "Пример: age > 10"
            )
            return

        param_name: str = parts[0]
        operator: str = parts[1]
        value_to_compare: str = parts[2]

        if param_name == PARAM_MONTH:
            value_to_compare = value_to_compare.lower()
            if value_to_compare not in ALLOWED_MONTHS:
                print(f"Ошибка: неизвестный месяц '{value_to_compare}'")
                return

        new_plants_list: List[Plant] = []
        removed_count: int = 0

        for plant in self.plants:
            should_remove: bool = False

            if param_name == PARAM_AGE and isinstance(plant, Tree):
                current_val: int = plant.age
                val_to_comp: int = int(value_to_compare)
                should_remove = self.check_condition(current_val, operator, val_to_comp)

            elif param_name == PARAM_SPINE_LENGTH and isinstance(plant, Cactus):
                current_val_f: float = plant.spine_length
                val_to_comp_f: float = float(value_to_compare)
                should_remove = self.check_condition(current_val_f, operator, val_to_comp_f)

            elif param_name == PARAM_MONTH and isinstance(plant, Shrub):
                current_val_i: int = ALLOWED_MONTHS.index(plant.bloom_month) + 1
                val_to_comp_i: int = ALLOWED_MONTHS.index(value_to_compare) + 1
                should_remove = self.check_condition(current_val_i, operator, val_to_comp_i)

            if should_remove:
                removed_count += 1
            else:
                new_plants_list.append(plant)

        self.plants = new_plants_list
        print(f"Удалено объектов по условию '{condition_str}': {removed_count}")

    def check_condition(self, val1: object, op: str, val2: object) -> bool:
        """Проверяет условие сравнения двух значений."""
        func: Optional[Callable[[object, object], bool]] = OPERATORS.get(op)
        if func is None:
            return False
        return func(val1, val2)


def process_file(filename: str, container: GardenContainer) -> None:
    """Читает файл команд и обрабатывает их."""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines: List[str] = file.readlines()
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
        return

    for line in lines:
        line = line.strip()
        if not line:
            continue

        print(f"\nВыполняется команда: {line}")

        if line.startswith("ADD "):
            data_part: str = line[4:].strip()
            parts: List[str] = data_part.split(";")
            if len(parts) != 3:
                print("Ошибка формата ADD. Нужно: ADD Тип;Название;Значение")
                continue

            obj_type: str = parts[0].lower()
            name: str = parts[1]
            value: str = parts[2]

            factory: Optional[Type[Plant]] = PLANT_FACTORIES.get(obj_type)
            if factory is None:
                print(f"Неизвестный тип растения: {obj_type}")
            else:
                try:
                    # так как преобразование происходит безопасно внутри конструктора
                    container.add_plant(factory(name, value))  # type: ignore[call-arg]
                except ValueError as e:
                    print(f"Ошибка при добавлении: {e}")

        elif line.startswith("REM "):
            condition: str = line[4:].strip()
            container.remove_by_condition(condition)

        elif line == "PRINT":
            container.print_all()

        else:
            print("Неизвестная команда")


if __name__ == "__main__":
    garden: GardenContainer = GardenContainer()
    input_file: str = "plants.txt"

    print("Программа обработки артефактов (Растения)")
    process_file(input_file, garden)