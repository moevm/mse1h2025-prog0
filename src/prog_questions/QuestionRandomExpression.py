import subprocess
import os
import tempfile
from .QuestionBase import QuestionBase
from generators.random_expressions import get_expression

QUESTION_TEXT = f'''Напишите функцию, которая вычисляет значение следующего выражения.
Значения переменных подаются на вход через stdin, через пробел. Результат надо вернуть.
'''

PRELOADED_CODE = '''#include <stdio.h>

int main() {

   return 0;
}
'''


class QuestionSum(QuestionBase):
    """Демонстрационный класс, реализующий задачу сложения чисел"""

    def __init__(self, *, seed: int, difficulty=1, vars: str, operations: str, length: int, random_seed: int,
                 minuses_threshold=0,
                 brackets_treshold=0, minus_symbol="-", all_variables=False):
        super().__init__(seseed=seed, difficulty=difficulty, vars=vars, operations=operations, length=length,
                         random_seed=random_seed, minuses_threshold=minuses_threshold,
                         brackets_treshold=brackets_treshold, minus_symbol=minus_symbol, all_variables=all_variables)
        self.difficulty = difficulty
        self.vars = vars
        self.operations = operations
        self.length = length
        self.random_seed = random_seed
        self.minuses_threshold = minuses_threshold
        self.brackets_treshold = brackets_treshold
        self.minus_symbol = minus_symbol
        self.all_variables = all_variables

    @property
    def questionName(self) -> str:
        return f"Сложение чисел"

    @property
    def questionText(self) -> str:
        return QUESTION_TEXT

    @property
    def preloadedCode(self) -> str:
        return PRELOADED_CODE

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
