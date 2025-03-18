import subprocess
import os
import tempfile
from .QuestionBase import QuestionBase
from .generators.random_expressions import get_expression
import random

PRELOADED_CODE = '''#include <stdio.h>

int main() {

   return 0;
}
'''


class QuestionRandomExpression(QuestionBase):
    """Демонстрационный класс, реализующий задачу сложения чисел"""

    def __init__(self, *, seed: int, difficulty=1, vars=['x','y','z','w'], operations=['+','-','*','&','|'], length=1,
                 minuses_threshold=0,
                 brackets_treshold=0, minus_symbol="-", all_variables=False):
        super().__init__(seed=seed, difficulty=difficulty, vars=vars, operations=operations, length=length,
                         minuses_threshold=minuses_threshold,
                         brackets_treshold=brackets_treshold, minus_symbol=minus_symbol, all_variables=all_variables)
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
        return PRELOADED_CODE

    @property
    def questionExpression(self) -> str:
        return get_expression(self.vars, self.operations, self.length, self.seed, self.minuses_threshold,
                              self.brackets_treshold, self.minus_symbol, self.all_variables)

    def test(self, code: str) -> str:
        # Создание временной директории для файлов
        with tempfile.TemporaryDirectory() as tmp_dir:
            # Сохранение кода студента во временный файл в tmp_dir
            student_code_path = os.path.join(tmp_dir, 'student_code.c')
            with open(student_code_path, 'w') as f:
                f.write(code)

            # Компиляция кода студента
            compile_process = subprocess.run(
                ['gcc', student_code_path, '-o', os.path.join(tmp_dir, 'student_code')],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=tmp_dir
            )
            # Проверка на ошибки компиляции
            if compile_process.returncode != 0:
                return f"Ошибка компиляции:\n{compile_process.stderr.decode()}"

            # Формирование входных данных для программы студента
            numbers = [1, 2, 3]
            input_data = ' '.join(map(str, numbers)) + '\n'
            executable_path = os.path.join(tmp_dir, 'student_code')

            # Выполнение скомпилированного кода с передачей входных данных
            run_process = subprocess.run(
                [executable_path],
                input=input_data.encode(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=tmp_dir
            )
        # Получение данных после выполнения кода
        output = run_process.stdout.decode().strip()
        error_output = run_process.stderr.decode().strip()

        # Проверка на ошибки выполнения
        if run_process.returncode != 0:
            return f"Ошибка выполнения:\n{error_output}"

        expected_sum = sum(numbers)

        # Проверка на совпадение ответов
        if output == str(expected_sum):
            return "OK"
        else:
            return f"Ошибка: Ожидалось {expected_sum}, получено {output}."
