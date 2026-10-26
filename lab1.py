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

class Plant(ABC):
    """Абстрактный базовый класс растения"""
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def get_unique_value(self):
        pass

    @abstractmethod
    def get_type_name(self):
        pass

    def to_string(self):
        return f"{self.get_type_name()} | Название: {self.name} | Уник. параметр: {self.get_unique_value()}"

class Tree(Plant):
    """Дерево с уникальным параметром — возраст (целое число лет)"""
    def __init__(self, name, age):
        super().__init__(name)
        self.age = int(age)

    def get_unique_value(self):
        return f"Возраст = {self.age} лет"

    def get_type_name(self):
        return "Дерево"

ALLOWED_MONTHS = ["январь", "февраль", "март", "апрель", "май", "июнь",
                  "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"]

class Shrub(Plant):
    """Кустарник с уникальным параметром — месяц цветения"""
    def __init__(self, name, month_str):
        super().__init__(name)
        month_lower = month_str.lower()
        if month_lower not in ALLOWED_MONTHS:
            raise ValueError(f"Неизвестный месяц: {month_str}")
        self.bloom_month = month_lower

    def get_unique_value(self):
        return f"Месяц цветения = {self.bloom_month.capitalize()}"

    def get_type_name(self):
        return "Кустарник"

class Cactus(Plant):
    """Кактус с уникальным параметром — длина колючек (дробное число, см)"""
    def __init__(self, name, spine_length):
        super().__init__(name)
        self.spine_length = float(spine_length)

    def get_unique_value(self):
        return f"Длина колючек = {self.spine_length} см"

    def get_type_name(self):
        return "Кактус"

class GardenContainer:
    """Контейнер для хранения и управления коллекцией растений"""
    def __init__(self):
        self.plants = []

    def add_plant(self, plant):
        """Добавляет растение"""
        self.plants.append(plant)

    def print_all(self):
        """Выводит содержимое контейнера"""
        if not self.plants:
            print("Контейнер пуст.")
            return

        for i in range(len(self.plants)):
            print(f"{i + 1}. {self.plants[i].to_string()}")

    def remove_by_condition(self, condition_str):
        """Удаляет растения, соответствующие заданному условию"""
        parts = condition_str.split()
        if len(parts) != 3:
            print("Ошибка: неверный формат условия. Пример: age > 10")
            return

        param_name = parts[0]
        operator = parts[1]
        value_to_compare = parts[2]

        if param_name == "month":
            value_to_compare = value_to_compare.lower()
            if value_to_compare not in ALLOWED_MONTHS:
                print(f"Ошибка: неизвестный месяц '{value_to_compare}'")
                return

        new_plants_list = []
        removed_count = 0

        for plant in self.plants:
            should_remove = False

            if param_name == "age" and isinstance(plant, Tree):
                current_val = plant.age
                val_to_comp = int(value_to_compare)
                should_remove = self.check_condition(current_val, operator, val_to_comp)

            elif param_name == "spine_length" and isinstance(plant, Cactus):
                current_val = plant.spine_length
                val_to_comp = float(value_to_compare)
                should_remove = self.check_condition(current_val, operator, val_to_comp)

            elif param_name == "month" and isinstance(plant, Shrub):
                current_val = ALLOWED_MONTHS.index(plant.bloom_month) + 1
                val_to_comp = ALLOWED_MONTHS.index(value_to_compare) + 1
                should_remove = self.check_condition(current_val, operator, val_to_comp)

            if should_remove:
                removed_count += 1
            else:
                new_plants_list.append(plant)

        self.plants = new_plants_list
        print(f"Удалено объектов по условию '{condition_str}': {removed_count}")

    def check_condition(self, val1, op, val2):
        if op == ">": return val1 > val2
        if op == "<": return val1 < val2
        if op == "==": return val1 == val2
        if op == ">=": return val1 >= val2
        if op == "<=": return val1 <= val2
        return False

def process_file(filename, container):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
        return

    for line in lines:
        line = line.strip()
        if not line:
            continue

        print(f"\nВыполняется команда: {line}")

        if line.startswith("ADD "):
            data_part = line[4:].strip()
            parts = data_part.split(";")
            if len(parts) != 3:
                print("Ошибка формата ADD. Нужно: ADD Тип;Название;Значение")
                continue

            obj_type = parts[0].lower()
            name = parts[1]
            value = parts[2]

            try:
                if obj_type == "tree":
                    container.add_plant(Tree(name, value))
                elif obj_type == "shrub":
                    container.add_plant(Shrub(name, value))
                elif obj_type == "cactus":
                    container.add_plant(Cactus(name, value))
                else:
                    print(f"Неизвестный тип растения: {obj_type}")
            except ValueError as e:
                print(f"Ошибка при добавлении: {e}")

        elif line.startswith("REM "):
            condition = line[4:].strip()
            container.remove_by_condition(condition)

        elif line == "PRINT":
            container.print_all()

        else:
            print("Неизвестная команда")

if __name__ == "__main__":
    garden = GardenContainer()
    input_file = "plants.txt"

    print("Программа обработки артефактов (Растения)")
    process_file(input_file, garden)