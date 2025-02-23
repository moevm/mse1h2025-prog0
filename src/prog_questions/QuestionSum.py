import subprocess
import os
import tempfile
from .QuestionBase import QuestionBase


QUESTION_TEXT = '''Напишите программу, которая вычисляет сумму чисел.
На вход программе подается строка, в которой числа записаны через пробел. Ввод заканчивается переносом строки.
Программа должна считать числа, вычислить их сумму и вывести результат в консоль.
'''

PRELOADED_CODE = '''#include <stdio.h>

int main() {

   return 0;
}
'''


class QuestionSum(QuestionBase):
    """Демонстрационный класс, реализующий задачу сложения чисел"""

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
