from abc import ABC, abstractmethod
import sys
import json
from .QuestionBase import QuestionBase


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

    @property
    @abstractmethod
    def questionName(self) -> str:
        return "Случайное условие"

    @property
    @abstractmethod
    def questionText(self) -> str:
        return QUESTION_TEXT

    @property
    @abstractmethod
    def preloadedCode(self) -> str:
        return PRELOADED_CODE

    @abstractmethod
    def test(self, code: str) -> str:
        '''
        Логика проверки кода
        code - код, отправленный студентом на проверку
        Возвращаемое значение - строка-результат проверки, которую увидит студент.
        Если всё хорошо - вернуть "OK"
        '''
        ...
