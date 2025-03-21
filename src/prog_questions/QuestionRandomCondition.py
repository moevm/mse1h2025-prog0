from abc import abstractmethod
from utility.CProgramRunner import CProgramRunner, CompilationError, ExecutionError
import sys
import json
import random
from textwrap import dedent
from temp import Task
from QuestionBase import QuestionBase

PRELOADED_CODE = """
#include <stdio.h>

int main() {

   return 0;
}
"""

class QuestionRandomCondition(QuestionBase):

    def __init__(self, *, seed: int, condition_length: int, array_length: int):
        super().__init__(seed=seed, condition_length=condition_length, array_length=array_length)
        self.task = Task(array_length, condition_length, seed)
        self.sample_code = self.task.code
        self.parse(self.task.text)
        random.seed(seed)

    @property
    def questionName(self) -> str:
        return "Случайное условие"

    @property
    def questionText(self) -> str:
        # TODO: add examples of program work

        base_text = """\
            Напишите программу, которая обрабатывает подаваемый на вход массив согласно условию. Условие необходимо пересчитывать после каждого изменения массива.

            Ваше условие:
            {condition}

            Для нулевого элемента массива принять arr[i - 1] = 0

            На вход программе в stdin подаётся массив чисел длины {array_length}. Числа разделены пробелом. Изменённый массив необходимо вернуть в stdout, элементы разделить пробелами.

            Пример входных данных:
            {example_input}
            Пример выходных данных:
            {example_output}
        """

        # clean all tabs and insert f-values
        cleaned_text = dedent(base_text)
        result = cleaned_text.format(
            condition = self.task.text,
            array_length = self.task.array_length,
            example_input = [random.randint(1, 100) for _ in range(self.parameters['array_length'])],
            example_output = self.run_sample_code([random.randint(1, 100) for _ in range(self.parameters['array_length'])])
        )

        return result

    @property
    def preloadedCode(self) -> str:
        return PRELOADED_CODE

    # get arguments from task
    def parse(self, task_text: str):
        task_strings = task_text.split("\n")
        first_string = task_strings[0][5:]
        self.condtition_string = first_string.split(")")[0][2:]
        self.condition_operator = first_string.split(")")[1][1:3]

    def run_sample_code(self, arr: list) -> list:
        condition_string = self.condtition_string
        condition_operator = self.condition_operator
        threshold = self.task.threshold
        then_number = self.task.then_number
        else_number = self.task.else_number

        exec(self.sample_code)
        #print(arr)
        return arr

    # test INT edge case
    def test_int_edge_case(self):
        self.run_sample_code([10 ** 10] * self.parameters['array_length'])
        self.run_sample_code([-10 ** 10] * self.parameters['array_length'])

    # test


    def test(self, code: str) -> str:
        try:
            runner = CProgramRunner(code)
            output = runner.run(self.input_array)
            if output == self.expected_output:
                return "OK"
            else:
                return f"Ошибка: ожидалось '{self.expected_output}', получено '{output}'"
        except CompilationError as e:
            return f"Ошибка компиляции: {e}"
        except ExecutionError as e:
            return f"Ошибка выполнения (код {e.exit_code}): {e}"

if __name__ == "__main__":
    test = QuestionRandomCondition(seed=52, condition_length=10, array_length=10)
    print(test.questionText)
    test.test_int_edge_case()
