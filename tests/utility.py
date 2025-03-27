from prog_questions import QuestionBase
import sys
import json


def moodleInit(questionClass: type[QuestionBase], *, seed: int, **parameters) -> QuestionBase:
    '''
    Создаёт экземпляр класса questionClass с эмуляцией пробрасывания параметров,
    как если бы это было заинтегрировано в moodle
    questionClass - тип класса вопроса, экземпляр которого будет создваться
    seed - сид, с которым будет создаваться вопрос
    parameters - параметры, с которыми будет создаваться вопрос
    Возвращаемое значение - созданный экземпляр класса
    '''
    old_argv = sys.argv
    sys.argv = ['', f'seed={seed}']

    question = questionClass.initTemplate(**parameters)
    question = question.initWithParameters(json.loads(question.getTemplateParameters())['PARAMETERS'])

    sys.argv = old_argv
    return question
