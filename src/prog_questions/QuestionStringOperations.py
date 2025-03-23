from utility.CProgramRunner import CProgramRunner, CompilationError, ExecutionError
from generators.string_operations import generate_operations, generate_input_string, apply_operations, generate_text
from QuestionBase import QuestionBase
from textwrap import dedent
import random

QUESTION_TEXT = """
<h1>Условие задачи</h1>
<p>Дана строка, содержащая латинские буквы (в верхнем и нижнем регистрах), цифры, пробелы и знаки подчеркивания. Необходимо выполнить над этой строкой одну или несколько операций.</p>

<h2>Формат ввода</h2>
<p>На вход подается строка длиной от <code>{min_length}</code> до <code>{max_length}</code>, содержащая латинские буквы (верхний и нижний регистр), цифры, пробелы и знаки подчеркивания. Также задается набор операций, которые необходимо применить к строке.</p>

<h2>Операции вашего варианта</h2>
<ul>
    {operations}
</ul>

<h2>Формат вывода</h2>
<p>Вывести преобразованную строку после применения всех заданных операций.</p>

<h2>Пример</h2>
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
        <td><code>hEllO_102 WOrld_021</code></td>
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
    def __init__(self, *, seed: int, num_operations: int, min_length: int, max_length: int, strictness: float):
        super().__init__(seed=seed, num_operations=num_operations)
        self.operations = generate_operations(seed, num_operations)
        self.min_length = min_length
        self.max_length = max_length
        self.input_string = generate_input_string(self.operations, min_length=min_length, max_length=max_length)
        self.expected_output = apply_operations(self.input_string, self.operations)

    @property
    def questionName(self) -> str:
        return "Операции над строками"

    @property
    def questionText(self) -> str:
        dedent_question_text = dedent(QUESTION_TEXT)
        return dedent_question_text.format(
            min_length=self.min_length,
            max_length=self.max_length,
            operations="\n".join(f"<li>{op.get_text()}</li>" for op in self.operations)
        )

    @property
    def preloadedCode(self) -> str:
        return PRELOADED_CODE

    def noise_input_string(self, input_string: str):
        if self.strictness == 0.0 or len(input_string) >= max_length:
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

            if random.random() < strictness:
                noise = ''.join(random.choices(noise_chars, k=min(noise_level, extra_space)))
                new_words.append(noise + word)
                extra_space -= len(noise)
            else:
                new_words.append(word)

        return " ".join(new_words)

    def test_case(self, runner: CProgramRunner, input_string: str):
        pass

    def boundary_test_case(self):
        pass

    def test(self, code: str) -> str:
        try:
            random.seed(self.seed)
            runner = CProgramRunner(code)
            output = runner.run(self.input_string)
            if output == self.expected_output:
                return "OK"
            else:
                return f"Ошибка: ожидалось '{self.expected_output}', получено '{output}'"
        except CompilationError as e:
            return f"Ошибка компиляции: {e}"
        except ExecutionError as e:
            return f"Ошибка выполнения (код {e.exit_code}): {e}"


if __name__ == "__main__":
    test = QuestionStringOperations(seed=10, num_operations=3, min_length=50, max_length=60, strictness=0.0)
    print(test.questionText)
    print(test.input_string)
    print(apply_operations(test.input_string.replace(" ", "  "), test.operations))

