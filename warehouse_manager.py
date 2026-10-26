from dataclasses import dataclass
from typing import List


class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"


@dataclass
class Product:
    name: str
    quantity: int
    price_per_unit: float

    @property
    def total_cost(self) -> float:
        return self.quantity * self.price_per_unit


def read_string(prompt: str, error_msg: str) -> str:
    while True:
        value = input(f"{Color.CYAN}{prompt}{Color.RESET}").strip()
        if value:
            return value
        print(f"{Color.RED} {error_msg}{Color.RESET}")


def read_int(prompt: str, error_msg: str, allow_negative: bool = False) -> int:
    while True:
        try:
            value = int(input(f"{Color.CYAN}{prompt}{Color.RESET}").strip())
            if allow_negative or value >= 0:
                return value
        except ValueError:
            pass
        print(f"{Color.RED} {error_msg}{Color.RESET}")


def read_float(prompt: str, error_msg: str) -> float:
    while True:
        try:
            raw = input(f"{Color.CYAN}{prompt}{Color.RESET}").strip().replace(",", ".")
            value = float(raw)
            if value >= 0:
                return value
        except ValueError:
            pass
        print(f"{Color.RED} {error_msg}{Color.RESET}")



def print_header():
    print(f"{Color.CYAN}{Color.BOLD}")
    print("╔══════════════════════════════════════════════════════╗")
    print("║          СИСТЕМА УПРАВЛЕНИЯ СКЛАДСКИМИ ЗАПАСАМИ      ║")
    print("╚══════════════════════════════════════════════════════╝")
    print(Color.RESET)


def print_menu():
    print(f"\n{Color.YELLOW}{Color.BOLD}МЕНЮ:{Color.RESET}")
    print("1. Добавить один товар")
    print("2. Пакетный ввод нескольких товаров")
    print("3. Показать каталог (склад)")
    print("4. Удалить товар")
    print("5. Рассчитать статистику")
    print("6. Сохранить отчёт в файл")
    print("7. Справка")
    print("0. Выход")


def add_single_product(products: List[Product]):
    print(f"\n{Color.GREEN}--- ДОБАВЛЕНИЕ ОДНОГО ТОВАРА ---{Color.RESET}")
    name = read_string("Наименование товара: ", "Название не может быть пустым")
    quantity = read_int("Количество на складе (шт): ", "Количество должно быть целым неотрицательным числом")
    price = read_float("Цена за единицу (руб): ", "Цена должна быть неотрицательным числом")

    products.append(Product(name=name, quantity=quantity, price_per_unit=price))
    print(f"{Color.GREEN}[OK] Товар \"{name}\" успешно добавлен.{Color.RESET}")


def batch_add_products(products: List[Product]):
    print(f"\n{Color.GREEN}--- ПАКЕТНЫЙ ВВОД ТОВАРОВ ---{Color.RESET}")
    count = read_int("Сколько товаров хотите добавить? ", "Введите положительное число")

    for i in range(1, count + 1):
        print(f"\n{Color.CYAN}>>> Товар №{i} из {count} <<<{Color.RESET}")
        name = read_string("Наименование: ", "Название не может быть пустым")
        quantity = read_int("Количество (шт): ", "Количество должно быть целым неотрицательным числом")
        price = read_float("Цена за ед. (руб): ", "Цена должна быть неотрицательным числом")

        products.append(Product(name=name, quantity=quantity, price_per_unit=price))

    print(f"\n{Color.GREEN}[OK] Успешно добавлено товаров: {count}{Color.RESET}")


def show_catalog(products: List[Product]):
    print(f"\n{Color.CYAN}{Color.BOLD}")
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║                          КАТАЛОГ СКЛАДА                          ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print(Color.RESET)

    if not products:
        print(f"{Color.YELLOW}Склад пуст. Добавьте товары через меню.{Color.RESET}")
        return

    print(f"{Color.BLUE}┌─────┬──────────────────────────────┬──────────┬──────────────┬──────────────┐{Color.RESET}")
    print(
        f"{Color.BLUE}{Color.BOLD}│ №   │ Наименование товара          │ Кол-во   │ Цена за ед.  │ Общая стоим. │{Color.RESET}")
    print(f"{Color.BLUE}├───────────────────────────────────┼──────────┼──────────────┼──────────────┤{Color.RESET}")

    for idx, p in enumerate(products, start=1):
        name = p.name if len(p.name) <= 28 else p.name[:25] + "..."
        print(f"│ {idx:<3} │ {name:<28} │ {p.quantity:<8} │ {p.price_per_unit:>12,.2f} │ {p.total_cost:>12,.2f} │")

    print(f"{Color.BLUE}└─────┴──────────────────────────────┴──────────┴──────────────┴──────────────┘{Color.RESET}")


def delete_product(products: List[Product]):
    if not products:
        print(f"\n{Color.YELLOW}Склад пуст, удалять нечего.{Color.RESET}")
        return

    show_catalog(products)
    print(f"\n{Color.RED}--- УДАЛЕНИЕ ТОВАРА ---{Color.RESET}")
    idx = read_int("Введите номер товара для удаления (0 для отмены): ", "Введите корректный номер",
                   allow_negative=True)

    if idx == 0:
        print(f"{Color.YELLOW}Удаление отменено.{Color.RESET}")
        return

    if 1 <= idx <= len(products):
        removed = products.pop(idx - 1)
        print(f"{Color.GREEN}[OK] Товар \"{removed.name}\" успешно удален со склада.{Color.RESET}")
    else:
        print(f"{Color.RED} Товар с таким номером не найден.{Color.RESET}")


def calculate_statistics(products: List[Product]):
    print(f"\n{Color.CYAN}{Color.BOLD}")
    print("╔══════════════════════════════════════════════════════════════════╗")
    print("║                        РЕЗУЛЬТАТЫ РАСЧЁТА                        ║")
    print("╚══════════════════════════════════════════════════════════════════╝")
    print(Color.RESET)

    if not products:
        print(f"{Color.YELLOW}Склад пуст. Статистика недоступна.{Color.RESET}")
        return

    sorted_products = sorted(products, key=lambda x: x.total_cost, reverse=True)

    print(f"{Color.BLUE}┌────────────────────────────────────────┬──────────────────┬──────────────┐{Color.RESET}")
    print(
        f"{Color.BLUE}{Color.BOLD}│ Название                               │ Автор/Поставщик  │ Экз./Стоим.  │{Color.RESET}")
    print(f"{Color.BLUE}├────────────────────────────────────────┼──────────────────┼──────────────┤{Color.RESET}")

    for p in sorted_products:
        name = p.name if len(p.name) <= 38 else p.name[:35] + "..."
        print(f"│ {name:<38} │ {p.quantity:<16} │ {p.total_cost:>12,.2f} │")

    print(f"{Color.BLUE}└────────────────────────────────────────┴──────────────────┴──────────────┘{Color.RESET}")

    total_sum = sum(p.total_cost for p in products)
    total_qty = sum(p.quantity for p in products)
    avg_price = total_sum / total_qty if total_qty > 0 else 0
    most_expensive = max(products, key=lambda x: x.total_cost)

    print(f"\n{Color.YELLOW}[+] Наименований товаров:     {len(products)}{Color.RESET}")
    print(f"{Color.YELLOW}[+] Общее количество единиц:  {total_qty}{Color.RESET}")
    print(f"{Color.YELLOW}[+] Средняя цена ед. товара:  {avg_price:,.2f} руб.{Color.RESET}")
    print(
        f"{Color.GREEN}[*] Самый дорогой товар:      {most_expensive.name} ({most_expensive.total_cost:,.2f} руб.){Color.RESET}")
    print(f"\n{Color.GREEN}{Color.BOLD}ОБЩАЯ СТОИМОСТЬ ВСЕХ ТОВАРОВ НА СКЛАДЕ: {total_sum:,.2f} руб.{Color.RESET}")


def save_report_to_file(products: List[Product]):
    if not products:
        print(f"\n{Color.YELLOW}Склад пуст. Отчет не сохранен.{Color.RESET}")
        return

    filename = "warehouse_report.txt"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write("ОТЧЁТ ПО СКЛАДСКИМ ЗАПАСАМ\n")
            f.write("=" * 40 + "\n\n")

            total_sum = 0.0
            total_qty = 0

            for idx, p in enumerate(products, start=1):
                total_sum += p.total_cost
                total_qty += p.quantity
                f.write(
                    f"{idx}. {p.name} | Кол-во: {p.quantity} шт. | Цена: {p.price_per_unit:.2f} руб. | Сумма: {p.total_cost:.2f} руб.\n")

            f.write("\n" + "-" * 40 + "\n")
            f.write(f"Всего наименований: {len(products)}\n")
            f.write(f"Общее количество единиц: {total_qty}\n")
            f.write(f"Общая стоимость склада: {total_sum:.2f} руб.\n")

        print(f"\n{Color.GREEN}[OK] Отчёт успешно сохранен в файл: {filename}{Color.RESET}")
    except Exception as e:
        print(f"{Color.RED} Ошибка при сохранении файла: {e}{Color.RESET}")


def show_help():
    print(f"\n{Color.CYAN}{Color.BOLD}СПРАВКА ПО ПРОГРАММЕ{Color.RESET}")
    print("-" * 40)
    print("Программа ведет учет товаров на складе.")
    print("Для каждого товара хранятся: название, количество, цена.")
    print("\nФормула расчета общей стоимости:")
    print("    Total = SUM(quantity_i * price_i) для i = 1..N")
    print("\nПример:")
    print("    2 товара по 10 шт. (цена 100) и 5 шт. (цена 200)")
    print("    => всего (10*100) + (5*200) = 2000 руб.")
    print("-" * 40)


def pause():
    input(f"\n{Color.CYAN}Нажмите Enter для продолжения...{Color.RESET}")


def main():
    products: List[Product] = []

    while True:
        print_header()
        print_menu()

        choice = input(f"\n{Color.YELLOW}Выберите пункт меню: {Color.RESET}").strip()

        if choice == "1":
            add_single_product(products)
            pause()
        elif choice == "2":
            batch_add_products(products)
            pause()
        elif choice == "3":
            show_catalog(products)
            pause()
        elif choice == "4":
            delete_product(products)
            pause()
        elif choice == "5":
            calculate_statistics(products)
            pause()
        elif choice == "6":
            save_report_to_file(products)
            pause()
        elif choice == "7":
            show_help()
            pause()
        elif choice == "0":
            print(f"\n{Color.GREEN}Выход из программы. До свидания!{Color.RESET}")
            break
        else:
            print(f"{Color.RED}Неверный пункт меню. Попробуйте снова.{Color.RESET}")
            pause()


if __name__ == "__main__":
    main()