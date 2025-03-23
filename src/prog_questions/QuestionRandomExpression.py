import subprocess
import os
import tempfile
from cProfile import runctx
from select import select

from .QuestionBase import QuestionBase
from .generators.random_expressions import get_expression
import random
from .utility.CProgramRunner import CProgramRunner, ExecutionError, CompilationError

PRELOADED_CODE = '''#include <stdio.h>

int main() {

   return 0;
}
'''


class QuestionRandomExpression(QuestionBase):
    """Демонстрационный класс, реализующий задачу сложения чисел"""

    def __init__(self, *, seed: int, vars=['x','y','z','w'], operations=['+','-','*','&','|'], length=5,
                 minuses_threshold=0,
                 brackets_treshold=0, minus_symbol="-", all_variables=False, strictness=0):
        """
                Конструктор класса QuestionRandomExpression.

                :param seed: Сид для генерации случайных данных
                :param vars: Список переменных для генерации выражений (по умолчанию ['x','y','z','w'])
                :param operations: Допустимые операции для выражений (по умолчанию ['+','-','*','&','|'])
                :param length: Длина генерируемого выражения (по умолчанию 5)
                :param minuses_threshold: Порог для использования унарных минусов (0-1, по умолчанию 0)
                :param brackets_treshold: Порог для генерации скобок (0-1, по умолчанию 0)
                :param minus_symbol: Символ для отображения минуса (по умолчанию "-")
                :param all_variables: Флаг обязательного использования всех переменных (по умолчанию False)
                :param strictness: Уровень строгости проверки (0-1, влияет на количество тестов)
                :param space_amount: Количество пробелов между значениями ввода (по умолчанию 1)
        """
        super().__init__(seed=seed, vars=vars, operations=operations, length=length,
                         minuses_threshold=minuses_threshold,
                         brackets_treshold=brackets_treshold, minus_symbol=minus_symbol, all_variables=all_variables, strictness=strictness)
        self.vars = vars
        self.operations = operations
        self.length = length
        self.minuses_threshold = minuses_threshold
        self.brackets_treshold = brackets_treshold
        self.minus_symbol = minus_symbol
        self.all_variables = all_variables
        random.seed(self.seed)
        self.testing_values = [random.randint(0, 100) for _ in self.vars]
        self.testing_vars = {key:value for key, value in zip(self.vars, self.testing_values)}
        self.testing_result = eval(self.questionExpression, self.testing_vars)
        self.strictness = strictness
        self.min_tests = 20
        self.max_tests = 50
        self.space_amount = self.min_tests + self.strictness * (self.max_tests - self.min_tests)

    @property
    def questionName(self) -> str:
        return f"Сложение чисел"

    @property
    def questionText(self) -> str:
        operations_list = ["+", "-", "*", "&", "|"]
        operations_html = "\n".join(
            f"<li><code>{op}</code></li>"
            for op in operations_list
        )

        return f"""
            <h1>Условие задачи</h1>
            <p>Напишите функцию, которая вычисляет значение следующего выражения:</p>
            <pre>{self.questionExpression}</pre>

            <h4>Формат ввода</h4>
            <p>На вход через stdin подаются значения {len(self.vars)} переменных в алфавитном порядке ({' '.join(sorted(self.vars))}) через пробел.</p>

            <h4>Доступные операции</h4>
            <ul>
                {operations_html}
            </ul>

            <h4>Формат вывода</h4>
            <p>Результат вычисления выражения должен быть выведен в stdout.</p>

            <h4>Пример</h4>
            <table>
                <tr>
                    <th>Входные данные</th>
                    <th>Выходные данные</th>
                </tr>
                <tr>
                    <td><code>{' '.join(str(v) for v in self.testing_values)}</code></td>
                    <td><code>{self.testing_result}</code></td>
                </tr>
            </table>
            """

    @property
    def preloadedCode(self) -> str:
        return ""

    @property
    def questionExpression(self) -> str:
        return get_expression(self.vars, self.operations, self.length, self.seed, self.minuses_threshold,
                              self.brackets_treshold, self.minus_symbol, self.all_variables)


    def test(self, code: str) -> str:
        try:
            runner = CProgramRunner(code)

            # Тест с пустым вводом
            output = runner.run('')
            if output != '':
                return "Ошибка: Пустой ввод не обработан корректно"

            # Список краевых случаев
            edge_cases = [
                {
                    'name': 'все нули',
                    'values': [0] * len(self.vars)
                },
                {
                    'name': 'все единицы',
                    'values': [1] * len(self.vars)
                },
                {
                    'name': 'отрицательные значения',
                    'values': [-1 * (i + 1) for i in range(len(self.vars))]
                },
                {
                    'name': 'чередование знаков',
                    'values': [(-1) ** i * i for i in range(len(self.vars))]
                },
                {
                    'name': 'большие числа',
                    'values': [10 ** 9] * len(self.vars)
                },
                {
                    'name': 'разные пробелы',
                    'values': [5, 10, 15, 20][:len(self.vars)],
                    'input_data': '   5  10   15   20   '  # Пример для 4 переменных
                }
            ]

            # Проверка краевых случаев
            for case in edge_cases:
                values = case['values']
                input_data = case.get('input_data', (' ' * self.space_amount).join(map(str, values)))

                try:
                    expected = eval(self.questionExpression, dict(zip(self.vars, values)))
                    output = runner.run(input_data)

                    if output != expected:
                        return (
                            f"Краевой случай '{case['name']}': Ошибка\n"
                            f"Вход: {input_data}\n"
                            f"Ожидалось: {expected}\n"
                            f"Получено: {output}"
                        )
                except ExecutionError as e:
                    return f"Ошибка выполнения в тесте '{case['name']}': {str(e)}"

            # Случайные тесты (существующая логика)

            tests_count = self.min_tests + self.strictness * (self.max_tests - self.min_tests)
            self.space_amount = tests_count
            random.seed(self.seed)
            for i in range(int(tests_count)):
                values = [random.randint(-10 ** 6, 10 ** 6) for _ in self.vars]
                input_data = (' ' * self.space_amount).join(map(str, values))
                expected = eval(self.questionExpression, dict(zip(self.vars, values)))

                try:
                    output = runner.run(input_data)
                    if output != expected:
                        return (
                            f"Случайный тест {i + 1}/{tests_count}: Ошибка\n"
                            f"Вход: {input_data}\n"
                            f"Ожидалось: {expected}\n"
                            f"Получено: {output}"
                        )
                except ExecutionError as e:
                    return f"Ошибка выполнения в случайном тесте {i + 1}: {str(e)}"

            return "OK"

        except CompilationError as e:
            return "Ошибка компиляции"
        except Exception as e:
            return f"Неожиданная ошибка: {str(e)}"

