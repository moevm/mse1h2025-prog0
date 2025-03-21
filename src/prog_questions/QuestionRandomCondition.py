from utility.CProgramRunner import CProgramRunner, CompilationError, ExecutionError
import random
from textwrap import dedent
from temp import Task
from QuestionBase import QuestionBase

PRELOADED_CODE = """\
#include <stdio.h>

int main() {

   return 0;
}
"""

BASE_TEXT = """\
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

EXAMPLE_CODE = """\
#include <stdio.h>

int main() {{
    long long arr[{array_length}];
    int i;

    for (int i = 0; i < {array_length}; i++) {{
        scanf("%lld", &arr[i]);
    }}

    for (int i = 0; i < {array_length}; i++) {{
        long long prev = (i - 1 >= 0) ? arr[i - 1] : 0;
        long long condition = {condition_string};
        if (condition {condition_operator} {threshold}) {{
            arr[i] = prev {then_operator} {then_number};
        }} else {{
            arr[i] = arr[i] {else_operator} {else_number};
        }}
    }}

    for (i = 0; i < {array_length}; i++) {{
        printf("%lld ", arr[i]);
    }}

    return 0;
}}
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
        cleaned_text = dedent(BASE_TEXT)
        example_arr = [random.randint(1, 100) for _ in range(self.parameters['array_length'])]
        result = cleaned_text.format(
            condition = self.task.text,
            array_length = self.task.array_length,
            example_input = example_arr,
            example_output = self.run_sample_code(example_arr.copy())
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
        self.then_operator = task_strings[1].split()[-2]
        self.else_operator = task_strings[2].split()[-2]

    def run_sample_code(self, arr: list) -> list:
        condition_string = self.condtition_string
        condition_operator = self.condition_operator
        threshold = self.task.threshold
        then_number = self.task.then_number
        else_number = self.task.else_number

        exec(self.sample_code)

        return arr

    # form test: INT edge case
    def test_int_edge_case(self, code: str) -> str:
        upper_edge = self.test_case([10 ** 6] * self.parameters['array_length'], code)
        if upper_edge != "OK":
            return upper_edge
        lower_edge = self.test_case([-10 ** 10] * self.parameters['array_length'], code)
        return lower_edge

    # test specific case
    def test_case(self, arr: list, code: str) -> str:
        input = " ".join(map(str, arr))

        example_solution = EXAMPLE_CODE.format(
            array_length = self.task.array_length,
            condition_string = self.condtition_string,
            condition_operator = self.condition_operator,
            threshold = self.task.threshold,
            then_number = self.task.then_number,
            else_number = self.task.else_number,
            then_operator = self.then_operator,
            else_operator = self.else_operator
        )

        expected_output_runner = CProgramRunner(example_solution)
        expected_output = expected_output_runner.run(input)

        try:
            runner = CProgramRunner(code)
            output = runner.run(input)
            if output == expected_output:
                return "OK"
            else:
                return f"Ошибка: ожидалось '{expected_output}', получено '{output}'"
        except CompilationError as e:
            return f"Ошибка компиляции: {e}"
        except ExecutionError as e:
            return f"Ошибка выполнения (код {e.exit_code}): {e}"

    # test
    def test(self, code: str) -> str:
        out2 = self.test_int_edge_case(code)
        return out2

if __name__ == "__main__":
    test = QuestionRandomCondition(seed=52, condition_length=10, array_length=10)
    print(test.questionText)

    with open("test.c", "r", encoding="utf-8") as file:
        c_code = file.read()

    print(test.test_int_edge_case(c_code))
