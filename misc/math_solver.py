from sympy import symbols, Eq, solve, simplify

# Определим переменные
x = symbols('x')

# Определим уравнение
equation = Eq(x**2 - 4, 0)

# Печатаем исходное уравнение
print("Исходное уравнение:", equation)

# Шаг 1: Приводим уравнение к стандартному виду
print("Приводим уравнение к стандартному виду:", equation)

# Шаг 2: Решаем уравнение
solutions = solve(equation, x)
print("Решение уравнения:", solutions)

# Шаг 3: Проверяем решения
for sol in solutions:
    check = equation.subs(x, sol)
    print(f"Проверка решения {sol}: {check} -> {simplify(check)}")
