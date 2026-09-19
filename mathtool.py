import math
import sys


MAX_COEFFICIENT = 10000


def print_help():
    """Вывод справки."""
    print("Решение алгебраических уравнений")
    print()
    print("Уравнение:")
    print("  A*x^2 + B*x + C = 0")
    print()
    print("Способы запуска:")
    print("  python mathtool.py")
    print("      вывод справки")
    print()
    print("  python mathtool.py --help")
    print("      вывод справки")
    print()
    print("  python mathtool.py solve")
    print("      ввод коэффициентов A, B и C с клавиатуры")
    print()
    print("  python mathtool.py solve -a 1 -b -3 -c 2")
    print("      решение с заданными коэффициентами")
    print()
    print("Допустимые значения коэффициентов:")
    print("  целые числа от -10000 до 10000")


def is_valid_coefficient(value):
    """Проверка допустимого диапазона коэффициента."""
    return -MAX_COEFFICIENT <= value <= MAX_COEFFICIENT


def read_coefficient(name):
    """Ввод коэффициента с клавиатуры."""
    try:
        value = int(input(f"Введите {name}: "))
    except ValueError:
        print(
            f"Ошибка: коэффициент {name} не является целым числом.",
            file=sys.stderr
        )
        # return None
        sys.exit(1)

    if not is_valid_coefficient(value):
        print(
            f"Ошибка: значение вне допустимого диапазона. "
            f"Коэффициент {name} должен находиться в диапазоне [-10000; 10000].",
            file=sys.stderr
        )
        # return None
        sys.exit(1)

    return value


def solve_linear(b, c):
    """Решение линейного уравнения B*x + C = 0."""
    print("Линейное.")

    x = -c / b

    print(f"Корень: x = {x:.3f}")

    return 0


def solve_quadratic(a, b, c):
    """Решение квадратного уравнения A*x^2 + B*x + C = 0."""
    print("Квадратное.")

    discriminant = b * b - 4 * a * c

    print(f"D = {discriminant}")

    if discriminant < 0:
        print("Действительных корней нет.")
        return 0

    if discriminant == 0:
        x = -b / (2 * a)
        print(f"Корень: x = {x:.3f}")
        return 0

    sqrt_discriminant = math.sqrt(discriminant)

    x1 = (-b + sqrt_discriminant) / (2 * a)
    x2 = (-b - sqrt_discriminant) / (2 * a)

    # print("Корни:")
    print(f"x1 = {x1:.3f}")
    print(f"x2 = {x2:.3f}")

    return 0


def solve(a, b, c):
    """Определение вида уравнения и его решение."""

    # A = 0 и B = 0 — это не уравнение
    if a == 0 and b == 0:
        print(
            "Не уравнение: неизвестного нет.",
            file=sys.stderr
        )
        sys.exit(1)

    # A = 0 — линейное уравнение
    if a == 0:
        return solve_linear(b, c)

    # A != 0 — квадратное уравнение
    return solve_quadratic(a, b, c)


def parse_arguments(args):
    """
    Обработка параметров команды solve.

    Возвращает:
        (a, b, c) — если коэффициенты заданы;
        None — если параметры некорректны.
    """

    if len(args) != 6:
        print(
            "Ошибка: неверный набор параметров.",
            file=sys.stderr
        )
        print(
            "Использование: python mathtool.py solve -a A -b B -c C",
            file=sys.stderr
        )
        sys.exit(1)

    values = {}

    i = 0

    while i < len(args):
        parameter = args[i]

        if parameter not in ("-a", "-b", "-c"):
            print(
                f"Ошибка: это не уравнение, неизвестное отсутствует '{parameter}'.",
                file=sys.stderr
            )
            sys.exit(1)

        # После параметра должно быть значение
        if i + 1 >= len(args):
            print(
                f"Ошибка: для параметра {parameter} отсутствует значение.",
                file=sys.stderr
            )
            sys.exit(1)

        value_string = args[i + 1]

        try:
            value = int(value_string)
        except ValueError:
            print(
                f"Ошибка: значение параметра {parameter} "
                f"должно быть целым числом.",
                file=sys.stderr
            )
            sys.exit(1)

        if not is_valid_coefficient(value):
            print(
                f"Ошибка: коэффициент {parameter} должен находиться "
                f"в диапазоне [-10000; 10000].",
                file=sys.stderr
            )
            sys.exit(1)

        if parameter in values:
            print(
                f"Ошибка: параметр {parameter} указан несколько раз.",
                file=sys.stderr
            )
            sys.exit(1)

        values[parameter] = value

        i += 2

    # Проверяем наличие всех коэффициентов
    if "-a" not in values or "-b" not in values or "-c" not in values:
        print(
            "Ошибка: необходимо указать параметры -a, -b и -c.",
            file=sys.stderr
        )
        sys.exit(1)

    return values["-a"], values["-b"], values["-c"]


def main():
    """Главная функция программы."""

    args = sys.argv[1:]

    # Без параметров — справка
    if len(args) == 0:
        print_help()
        return 0

    # --help — справка
    if len(args) == 1 and args[0] == "--help":
        print_help()
        return 0

    # Неизвестная команда
    if args[0] != "solve":
        print(
            f"Ошибка: неизвестная команда '{args[0]}'.",
            file=sys.stderr
        )
        print(
            "Используйте python mathtool.py --help.",
            file=sys.stderr
        )
        return 1

    # python mathtool.py solve
    if len(args) == 1:
        a = read_coefficient("A")
        if a is None:
            return 1

        b = read_coefficient("B")
        if b is None:
            return 1

        c = read_coefficient("C")
        if c is None:
            return 1

        return solve(a, b, c)

    # python mathtool.py solve -a ... -b ... -c ...
    coefficients = parse_arguments(args[1:])

    if coefficients is None:
        return 1

    a, b, c = coefficients

    return solve(a, b, c)


if __name__ == "__main__":
    sys.exit(main())

