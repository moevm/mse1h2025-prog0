from abc import ABC, abstractmethod
import sys
import json


class QuestionBase(ABC):
    questionName: str = ''
    '''
    Название вопроса
    '''

    def __init__(self, *, seed: int, **parameters):
        self.seed = seed
        self.parameters = parameters

    @classmethod
    def initTemplate(cls, **parameters):
        '''
        Инициализация в параметрах шаблона Twig
        parameters - любые параметры, необходимые для настройки (сложность, въедливость и т.п.).
        Ввиду особенностей coderunner и простоты реализации, параметры могут быть типами,
        поддерживающимися JSON (int, float, str, bool, None, array, dict)
        '''
        stdinData = { parameter.split('=')[0]: parameter.split('=')[1] for parameter in sys.argv[1:] }
        seed = int(stdinData['seed'])

        return cls(seed=seed, **parameters)

    @classmethod
    def initWithParameters(cls, parameters: str):
        '''
        Инициализация в основном шаблоне, после инициализации параметров шаблона Twig.
        Подразумевается использование только в связке с Twig параметром PARAMETERS.
        '''
        return cls(**json.loads(parameters))

    def getTemplateParameters(self) -> str:
        '''
        Возвращает параметры в формате JSON для шаблонизатора Twig
        '''
        return json.dumps({
            'QUESTION_TEXT': self.questionText,
            'PRELOADED_CODE': self.preloadedCode,
            'SEED': self.seed,
            'PARAMETERS': json.dumps(self.parameters | { 'seed': self.seed }),
        })

    @property
    @abstractmethod
    def questionText(self) -> str:
        '''
        Задание/текст вопроса
        '''
        ...

    @property
    @abstractmethod
    def preloadedCode(self) -> str:
        '''
        Код, который подгружается в поле редактирования кода
        '''
        ...

    @abstractmethod
    def test(self, code: str) -> str:
        '''
        Логика проверки кода
        code - код, отправленный студентом на проверку
        Возвращаемое значение - строка-результат проверки, которую увидит студент.
        Если всё хорошо - вернуть "OK"
        '''
        ...
