from .QuestionBase import QuestionBase, Result
from .utility import CProgramRunner, ExecutionError
import random
import re

DIGITS = '0123456789'
SYMBOLS_LOWER = 'abcdefghijklmnopqrstuvwxyz'
SYMBOLS_UPPER = SYMBOLS_LOWER.upper()

class QuestionN2(QuestionBase):
    questionName = 'Модификация строки'

    def __init__(self, *, seed, maxInputSize: int = 100):
        super().__init__(seed=seed, maxInputSize=maxInputSize)
        self.maxInputSize = maxInputSize

        random.seed(self.seed)
        self.targetType = random.choice(['digits', 'upper', 'lower'])

    def generateGoodTest(self) -> tuple[str, str]:
        length = random.randint(1, self.maxInputSize-1)
        programInput = ''.join([random.choice([
            random.choice(DIGITS),
            random.choice(SYMBOLS_LOWER),
            random.choice(SYMBOLS_UPPER)
        ]) for _ in range(length)])

        replaceRegex = {
            'digits': r'\d',
            'upper': r'[A-Z]',
            'lower': r'[a-z]'
        }[self.targetType]

        expectedOutput = re.sub(replaceRegex, '', programInput)

        return programInput, expectedOutput

    def generateBadTest(self) -> tuple[str, str]:
        length = random.randint(1, self.maxInputSize-1)
        groups = {
            'digits': DIGITS,
            'upper': SYMBOLS_UPPER,
            'lower': SYMBOLS_LOWER
        }
        groups.pop(self.targetType)

        programInput = ''.join([random.choice(
            random.choice([symbols for symbols in groups.values()])
        ) for _ in range(length)])

        return programInput, programInput

    @property
    def questionText(self) -> str:
        target = {
            'digits': 'все цифры',
            'upper': 'все символы верхнего регистра',
            'lower': 'все символы нижнего регистра'
        }[self.targetType]

        random.seed(self.seed)
        goodTest = self.generateGoodTest()

        random.seed(self.seed+1)
        badTest = self.generateBadTest()

        exampleTable = f'''
            <table border>
                <tr>
                    <th>Входные данные</th><th>Результат</th>
                </tr>
                <tr>
                    <td>{goodTest[0]}</td><td>{goodTest[1]}</td>
                </tr>
                <tr>
                    <td>{badTest[0]}</td><td>{badTest[1]}</td>
                </tr>
            </table>
            '''

        return f'''
            Напишите программу, которая принимает на вход строку длины <b>не более {self.maxInputSize} символов</b> (последним символом всегда является символ перевода строки '\\n'),
            удаляет <b>{target}</b> и выводит результат.<br><br>
            Пример:
            {exampleTable}
            '''

    @property
    def preloadedCode(self) -> str:
        return '\n'.join([
            '#include <stdio.h>',
            '',
            'int main() {',
            '',
            '    return 0;',
            '}'
        ])

    def test(self, code: str) -> Result.Ok | Result.Fail:
        program = CProgramRunner(code)

        random.seed(self.seed)
        for _ in range(5):
            programInput, expectedOutput = self.generateGoodTest()

            try:
                result = program.run(programInput+'\n')
                if result != expectedOutput:
                    return Result.Fail(programInput, expectedOutput, result)
            except ExecutionError as e:
                return Result.Fail(programInput, expectedOutput, str(e))

        random.seed(self.seed+1)
        for _ in range(5):
            programInput, expectedOutput = self.generateBadTest()

            try:
                result = program.run(programInput+'\n')
                if result != expectedOutput:
                    return Result.Fail(programInput, expectedOutput, result)
            except ExecutionError as e:
                return Result.Fail(programInput, expectedOutput, str(e))

        return Result.Ok()
