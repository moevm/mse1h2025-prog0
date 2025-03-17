from .string_operations import generate_operations, generate_input_string, apply_operations, generate_text
from .QuestionBase import QuestionBase

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
    def __init__(self, *, seed: int, num_operations: int):
        super().__init__(seed=seed, num_operations=num_operations)
        self.operations = generate_operations(seed, num_operations)
        self.input_string = generate_input_string(self.operations, min_length=10, max_length=50)
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
        pass
