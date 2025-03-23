from utility.CProgramRunner import CProgramRunner, CompilationError, ExecutionError
from generators.string_operations import generate_operations, generate_input_string, apply_operations, generate_text
from QuestionBase import QuestionBase

QUESTION_TEXT = """
TODO
"""

PRELOADED_CODE = """
#include <stdio.h>

int main() {

   return 0;
}
"""


class QuestionStringOperations(QuestionBase):
    def __init__(self, *, seed: int, num_operations: int, min_length: int, max_length: int):
        super().__init__(seed=seed, num_operations=num_operations)
        self.operations = generate_operations(seed, num_operations)
        self.input_string = generate_input_string(self.operations, min_length=min_length, max_length=max_length)
        self.expected_output = apply_operations(self.input_string, self.operations)
        self.task_description = generate_text(self.operations)

    @property
    def questionName(self) -> str:
        return "Операции над строками"

    @property
    def questionText(self) -> str:
        return QUESTION_TEXT + '\n' + self.task_description

    @property
    def preloadedCode(self) -> str:
        return PRELOADED_CODE

    def test(self, code: str) -> str:
        try:
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
    test = QuestionStringOperations(seed=20, num_operations=3, min_length=50, max_length=60)
    print(test.questionText)
    print(test.input_string)

