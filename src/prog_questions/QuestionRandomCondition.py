from abc import abstractmethod
from utility.CProgramRunner import CProgramRunner, CompilationError, ExecutionError
import sys
import json
from temp import Task
from QuestionBase import QuestionBase


QUESTION_TEXT = """
Напишите программу, которая обрабатывает подаваемый на вход массив согласно следующему условию:

TODO: add condition from params
TODO: change N on params value
TODO: add examples of program work

На вход программе в stdin подаётся массив чисел длины N. Числа разделены пробелом. Изменённый массив необходимо вернуть в stdout, элементы разделить пробелами.

Пример входных данных:
Пример выходных данных:
"""

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

    @property
    def questionName(self) -> str:
        return "Случайное условие"

    @property
    def questionText(self) -> str:
        return QUESTION_TEXT

    @property
    def preloadedCode(self) -> str:
        return PRELOADED_CODE

    def test(self, code: str) -> str:
        pass

if __name__ == "__main__":
    test = QuestionRandomCondition(seed=52, condition_length=3, array_length=10)
    print(test.task.text)
