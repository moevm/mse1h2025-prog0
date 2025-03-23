from .utility.CProgramRunner import CProgramRunner, CompilationError, ExecutionError
import random
from textwrap import dedent
from .generators.random_condition_loop import Task
from .QuestionBase import QuestionBase

PRELOADED_CODE = """\
#include <stdio.h>

int main() {

   return 0;
}
"""

BASE_TEXT = """\
    Напишите программу, которая обрабатывает подаваемый на вход массив согласно условию. Условие необходимо пересчитывать после каждого изменения массива.
    <br><br>
    <b>Ваше условие:</b>
    <br>
    {condition}
    <br><br>
    Для нулевого элемента массива принять <b>arr[i - 1] = 0</b>
    <br><br>
    На вход программе в stdin подаётся массив чисел длины {array_length}. Числа разделены пробелами (не обязательно одним). Изменённый массив необходимо вернуть в stdout, элементы разделить пробелами.
    <br><br>
    Пример работы программы:
    <br>
    <table border="1">
        <thead>
            <tr>
                <th>Входные данные</th>
                <th>Выходные данные</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>{input}</td>
                <td>{output}</td>
            </tr>
        </tbody>
    </table>

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

    """
    :param seed: Seed для воспроизводимости тестов.
    :param condition_length: Длина условия задачи.
    :param array_length: Длина массива данных.
    :param strictness: Параметр для регулирования количества случайных тестов (0.0 - минимум, 1.0 - максимум).
    """
    def __init__(self, *, seed: int, condition_length: int=4, array_length: int=10, strictness: float=1):
        super().__init__(seed=seed, condition_length=condition_length, array_length=array_length, strictness=strictness)
        self.task = Task(array_length, condition_length, seed)
        self.parse(self.task.text)
        self.seed = seed
        self.example_solution = EXAMPLE_CODE.format(
            array_length=self.task.array_length,
            condition_string=self.condtition_string,
            condition_operator=self.condition_operator,
            threshold=self.task.threshold,
            then_number=self.task.then_number,
            else_number=self.task.else_number,
            then_operator=self.then_operator,
            else_operator=self.else_operator
        )
        self.expected_output_runner = CProgramRunner(self.example_solution)

    @property
    def questionName(self) -> str:
        return "Случайное условие"

    @property
    def questionText(self) -> str:
        cleaned_text = dedent(BASE_TEXT)

        input_arr = [random.randint(1, 500) for _ in range(self.parameters['array_length'])]
        input = " ".join(map(str, input_arr))

        output = self.expected_output_runner.run(input)

        result = cleaned_text.format(
            condition = ("<br>\n".join(self.task.text.split("\n"))),
            array_length = self.task.array_length,
            input = input,
            output = output
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

    # test specific case
    def test_case(self, arr: list, code: str, space_amount: int) -> str:
        separator = " " * space_amount
        input = separator.join(map(str, arr))

        expected_output = self.expected_output_runner.run(input)

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

    # form test: same numbers
    def test_same_numbers_case(self, code: str, amount: int, exponentiation: int) -> str:
        for serial_number in range(amount):
            upper_edge = self.test_case([10 ** exponentiation] * self.parameters['array_length'], code, serial_number + 1)
            if upper_edge != "OK":
                return upper_edge
            lower_edge = self.test_case([-10 ** exponentiation] * self.parameters['array_length'], code, serial_number + 1)
            return lower_edge

    # form test: alternate number
    def test_alternate_numbers_case(self, code: str, amount: int, exponentiation: int) -> str:
        for serial_number in range(amount):
            small_number = random.randint(-10, 10)
            big_number = random.randint((10**(exponentiation-1)), 10**exponentiation)
            alternating_list = []
            for i in range(self.parameters['array_length']):
                if i % 2 == 0:
                    alternating_list.append(big_number)
                else:
                    alternating_list.append(small_number)

            positive_case = self.test_case(alternating_list, code, serial_number + 1)
            if positive_case != "OK":
                return positive_case
            negative_case = self.test_case([-x for x in alternating_list], code, serial_number + 1)
            return negative_case

    # form test: random numbers
    def test_random(self, code: str, amount: int, upper_border: int) -> str:
        for serial_number in range(amount):
            test_arr = []
            for _ in range(self.parameters['array_length']):
                test_arr.append(random.randint(-(10**upper_border), 10**upper_border))

            test_result = self.test_case(test_arr, code, serial_number + 1)
            if test_result != "OK":
                return test_result
        return "OK"

    def distribute_random_tests(self, total_amount: int, exponentiation_amount: int) -> list:
        random_test_amount = [total_amount // exponentiation_amount] * exponentiation_amount
        for ind in range(total_amount % exponentiation_amount):
            random_test_amount[ind] += 1
        return random_test_amount

    # test
    def test(self, code: str) -> str:
        random.seed(self.seed)

        edge_case_exponentiation = [2, 4, 7, 12]

        # same numbers testing
        for exponentiation in edge_case_exponentiation:
            test_result_same_numbers = self.test_same_numbers_case(code, 1, exponentiation)
            if test_result_same_numbers != "OK":
                return test_result_same_numbers

        # alternate numbers testing
        for exponentiation in edge_case_exponentiation:
            test_result_alternate_numbers = self.test_alternate_numbers_case(code, 1, exponentiation)
            if test_result_alternate_numbers != "OK":
                return test_result_alternate_numbers

        # random numbers testing
        random_test_borders = [2, 3, 4, 5, 7, 9, 12]
        min_tests_number = 20 - 4 * len(edge_case_exponentiation)
        max_tests_number = 50 - 4 * len(edge_case_exponentiation)
        random_test_number = round(min_tests_number + self.parameters['strictness'] * (max_tests_number - min_tests_number))
        random_test_amount = self.distribute_random_tests(random_test_number, len(random_test_borders))

        for ind in range(len(random_test_borders)):
            test_result_random_border = self.test_random(code, random_test_amount[ind], random_test_borders[ind])
            if test_result_random_border != "OK":
                return test_result_random_border

        return "OK"

if __name__ == "__main__":
    test = QuestionRandomCondition(seed=52, condition_length=10, array_length=10, strictness=0.7)
    print(test.questionText)

    with open("test.c", "r", encoding="utf-8") as file:
        c_code = file.read()

    print(test.test(c_code))
