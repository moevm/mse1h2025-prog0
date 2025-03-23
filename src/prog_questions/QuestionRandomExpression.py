import subprocess
import os
import tempfile
from cProfile import runctx

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
        self.space_amount = 1

    @property
    def questionName(self) -> str:
        return f"Сложение чисел"

    @property
    def questionText(self) -> str:
        return f'''Напишите функцию, которая вычисляет значение следующего выражения.
        {self.questionExpression}
        Значения переменных подаются на вход через stdin, через пробел. Результат надо вернуть в stdout.
        Перменные расположены в алфавитном порядке(a b c и тд.)

        Количество переменных: {len(self.vars)}

        Пример задачи: {self.questionExpression}
        Пример входных данных: "{' '.join(str(value) for value in self.testing_values)}"
        Вывод: "{self.testing_result}"

        Список всех операций: "+,-,*,&,|"
        '''

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
            min_tests = 20
            max_tests = 50
            tests_count = min_tests + self.strictness * (max_tests - min_tests)
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

