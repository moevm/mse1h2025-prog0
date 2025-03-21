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

    def __init__(self, *, seed: int, difficulty=1, vars=['x','y','z','w'], operations=['+','-','*','&','|'], length=1,
                 minuses_threshold=0,
                 brackets_treshold=0, minus_symbol="-", all_variables=False, strictness=0):
        super().__init__(seed=seed, difficulty=difficulty, vars=vars, operations=operations, length=length,
                         minuses_threshold=minuses_threshold,
                         brackets_treshold=brackets_treshold, minus_symbol=minus_symbol, all_variables=all_variables, strictness=strictness)
        self.difficulty = difficulty
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
        Пример входных данных: "{','.join(str(value) for value in self.testing_values)}"
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

            #крайний случай с пустым вводом
            runner = CProgramRunner(code)
            output = runner.run('')
            if output != '':
                return f"Тест пройден с ошибкой"

            for i in 25:
                random.seed(self.seed)
                testing_values = [random.randint(0, 100000) for _ in self.vars]
                testing_vars = {key: value for key, value in zip(self.vars, testing_values)}
                testing_result = eval(self.questionExpression, testing_vars)
                runner = CProgramRunner(code)
                output = runner.run(input_data=' '.join(str(value) for value in self.testing_values))
                if output != testing_result:
                    return f"Тест {i + 1} из {26} пройден с ошибкой"
            return "OK"

        except CompilationError as e:
            return "Ошибка компиляции"


        except ExecutionError as e:
            return f"Ошибка выполнения [{e.exit_code}]: {str(e)}"

        except Exception as e:
            return f"Неожиданная ошибка:{str(e)}"

