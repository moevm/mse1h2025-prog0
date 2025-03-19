from abc import ABC, abstractmethod
import sys
import json
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


class QuestionRandomCondition(QuestionBase):
    def __init__(self, *, seed: int, **parameters):
        self.seed = seed
        self.parameters = parameters
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
