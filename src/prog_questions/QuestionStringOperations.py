from .QuestionBase import QuestionBase
from .utility import CProgramRunner, CompilationError, ExecutionError
from riscv_course.random_expressions.string_operations import generate_operations, generate_input_string, apply_operations, generate_text
from textwrap import dedent
import random

QUESTION_TEXT = """
<h1>Условие задачи</h1>
<p>Дана строка, содержащая латинские буквы (в верхнем и нижнем регистрах), цифры, пробелы и знаки подчеркивания. Необходимо выполнить над этой строкой одну или несколько операций.</p>
<h4>Формат ввода</h4>
<p>На вход подается строка по длине не превосходящая <code>{max_length}</code>, содержащая латинские буквы (верхний и нижний регистр), цифры, пробелы, специальные символы (!@#$%^&*()[]{{}}/?|~) и знаки подчеркивания.</p>

<h4>Операции вашего варианта</h4>
<ul>
    {operations}
</ul>
<h4>Формат вывода</h4>
<p>Вывести преобразованную строку после применения всех заданных операций.</p>
<h5>Пример</h5>
<table>
    <tr>
        <th>Входные данные</th>
        <th>Выходные данные</th>
    </tr>
    <tr>
        <td>
            <strong>Строка:</strong> <code>HELLO_123 WORLD_456</code><br>
            <strong>Операции:</strong>
            <ul>
                <li>Заменить все цифры остатками от деления на 3</li>
                <li>Перевести все гласные буквы ['A', 'E', 'I', 'O', 'U', 'Y'] в нижний регистр</li>
            </ul>
        </td>
        <td><code>HeLLo_120 WoRLD_120</code></td>
    </tr>
</table>
"""

PRELOADED_CODE = """
#include <stdio.h>
int main() {
   return 0;
}
"""


class QuestionStringOperations(QuestionBase):
    """
    :param seed: Seed для воспроизводимости тестов.
    :param num_operations: количество операций задачи.
    :param min_length: минимальная длина входных данных.
    :param max_length: максимальная длина входных данных.
    :param strictness: Параметр для регулирования количества случайных тестов (0.0 - минимум, 1.0 - максимум).
    """
    def __init__(self, *, seed: int, num_operations: int=3, min_length: int=30, max_length: int=100, strictness: float=1):
        super().__init__(seed=seed, num_operations=num_operations,
                         min_length=min_length, max_length=max_length, strictness=strictness)
        self.strictness = strictness
        self.operations = generate_operations(seed, num_operations)
        self.min_length = min_length
        self.max_length = max_length

    @property
    def questionName(self) -> str:
        return "Операции над строками"

    @property
    def questionText(self) -> str:
        dedent_question_text = dedent(QUESTION_TEXT)
        return dedent_question_text.format(
            max_length=self.max_length,
            operations="\n".join(f"<li>{op.get_text()}</li>" for op in self.operations)
        )

    @property
    def preloadedCode(self) -> str:
        return PRELOADED_CODE

    def noise_input_string(self, input_string: str):
        if self.strictness == 0.0 or len(input_string) >= self.max_length:
            return input_string

        noise_chars = "!@#$%^&*()[]{}/?|~"
        noise_level = int(self.strictness * 10)

        words = input_string.split(" ")
        extra_space = self.max_length - len(input_string)

        new_words = []
        for word in words:
            if extra_space <= 0:
                new_words.append(word)
                continue

            if random.random() < self.strictness:
                noise = ''.join(random.choices(noise_chars, k=min(noise_level, extra_space)))
                if random.random() < 0.5:
                    new_words.append(noise + word)
                else:
                    new_words.append(word + noise)
                extra_space -= len(noise)
            else:
                new_words.append(word)

        return " ".join(new_words).strip()

    def test_case(self, runner: CProgramRunner, input_string: str, noise: bool = True):
        if noise:
            input_string = self.noise_input_string(input_string)
        output = runner.run(input_string)
        expected_output = apply_operations(input_string, self.operations)
        if output == expected_output:
            return "OK"
        else:
            return f"Ошибка: ожидалось '{expected_output}', получено '{output}'"

    def test(self, code: str) -> str:
        try:
            random.seed(self.seed)
            runner = CProgramRunner(code)

            boundary_inputs = [
                "", "A", "A" * self.max_length,
                "123467890", "___  __   _",
                "BCDFG", "AEIOUY"
            ]

            random_count = 20 + self.strictness * 30
            random_inputs = [
                generate_input_string(self.operations, self.min_length, self.max_length) for _ in range(random_count)
            ]

            for input_string in boundary_inputs:
                result = self.test_case(runner, input_string, False)
                if result != "OK":
                    return result

            for input_string in random_inputs:
                result = self.test_case(runner, input_string)
                if result != "OK":
                    return result

            return "OK"
        except CompilationError as e:
            return f"Ошибка компиляции: {e}"
        except ExecutionError as e:
            return f"Ошибка выполнения (код {e.exit_code}): {e}"

