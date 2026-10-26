from functools import reduce
from collections import namedtuple

Plant = namedtuple("Plant", ["ptype", "name", "value"])

ALLOWED_MONTHS = [
    "январь", "февраль", "март", "апрель", "май", "июнь",
    "июль", "август", "сентябрь", "октябрь", "ноябрь", "декабрь"
]

def get_type_name(plant):
    names = {"tree": "Дерево", "shrub": "Кустарник", "cactus": "Кактус"}
    return names.get(plant.ptype, "Неизвестно")

def get_unique_value(plant):
    if plant.ptype == "tree":
        return f"Возраст = {plant.value} лет"
    elif plant.ptype == "shrub":
        return f"Месяц цветения = {plant.value.capitalize()}"
    elif plant.ptype == "cactus":
        return f"Длина колючек = {plant.value} см"
    return ""

def plant_to_string(plant):
    return f"{get_type_name(plant)} | Название: {plant.name} | Уник. параметр: {get_unique_value(plant)}"

def make_tree(name, value):
    try:
        age = int(value)
        return Plant("tree", name, age)
    except ValueError:
        raise ValueError(f"Некорректный возраст: {value}")

def make_shrub(name, value):
    month = value.lower()
    if month not in ALLOWED_MONTHS:
        raise ValueError(f"Неизвестный месяц: {value}")
    return Plant("shrub", name, month)

def make_cactus(name, value):
    try:
        length = float(value)
        return Plant("cactus", name, length)
    except ValueError:
        raise ValueError(f"Некорректная длина колючек: {value}")

def make_plant(ptype, name, value):
    makers = {
        "tree": make_tree,
        "shrub": make_shrub,
        "cactus": make_cactus
    }
    maker = makers.get(ptype.lower())
    if maker is None:
        raise ValueError(f"Неизвестный тип растения: {ptype}")
    return maker(name, value)

def add_plant(plants, plant):
    return plants + [plant]

def print_all(plants):
    if not plants:
        print("Контейнер пуст.")
        return plants
    for i, plant in enumerate(plants, start=1):
        print(f"{i}. {plant_to_string(plant)}")
    return plants

def check_condition(val1, op, val2):
    ops = {
        ">": lambda a, b: a > b,
        "<": lambda a, b: a < b,
        "==": lambda a, b: a == b,
        ">=": lambda a, b: a >= b,
        "<=": lambda a, b: a <= b
    }
    func = ops.get(op)
    if func is None:
        return False
    return func(val1, val2)

def plant_matches_condition(plant, param_name, operator, value_to_compare):
    if param_name == "age" and plant.ptype == "tree":
        return check_condition(plant.value, operator, int(value_to_compare))
    elif param_name == "spine_length" and plant.ptype == "cactus":
        return check_condition(plant.value, operator, float(value_to_compare))
    elif param_name == "month" and plant.ptype == "shrub":
        current_val = ALLOWED_MONTHS.index(plant.value) + 1
        val_to_comp = ALLOWED_MONTHS.index(value_to_compare) + 1
        return check_condition(current_val, operator, val_to_comp)
    return False

def remove_by_condition(plants, condition_str):
    parts = condition_str.split()
    if len(parts) != 3:
        print("Ошибка: неверный формат условия. Пример: age > 10")
        return plants

    param_name, operator, value_to_compare = parts[0], parts[1], parts[2]

    if param_name == "month":
        value_to_compare = value_to_compare.lower()
        if value_to_compare not in ALLOWED_MONTHS:
            print(f"Ошибка: неизвестный месяц '{value_to_compare}'")
            return plants

    new_plants = list(filter(
        lambda p: not plant_matches_condition(p, param_name, operator, value_to_compare),
        plants
    ))
    removed_count = len(plants) - len(new_plants)
    print(f"Удалено объектов по условию '{condition_str}': {removed_count}")
    return new_plants

def parse_add_command(data_part):
    parts = data_part.split(";")
    if len(parts) != 3:
        raise ValueError("Ошибка формата ADD. Нужно: ADD Тип;Название;Значение")
    ptype, name, value = parts[0].lower(), parts[1], parts[2]
    return make_plant(ptype, name, value)

def process_line(plants, line):
    line = line.strip()
    if not line:
        return plants

    print(f"\nВыполняется команда: {line}")

    if line.startswith("ADD "):
        try:
            plant = parse_add_command(line[4:].strip())
            return add_plant(plants, plant)
        except ValueError as e:
            print(f"Ошибка при добавлении: {e}")
            return plants

    elif line.startswith("REM "):
        condition = line[4:].strip()
        return remove_by_condition(plants, condition)

    elif line == "PRINT":
        return print_all(plants)

    else:
        print("Неизвестная команда")
        return plants

def process_file(filename, initial_plants):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print(f"Файл {filename} не найден")
        return initial_plants

    return reduce(process_line, lines, initial_plants)

if __name__ == "__main__":
    initial_garden = []
    input_file = "plants.txt"

    print("Программа обработки артефактов (Растения, ФП)")
    final_garden = process_file(input_file, initial_garden)