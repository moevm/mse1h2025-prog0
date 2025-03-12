from prog_questions import QuestionBase
import sys
import json


def moodleInit(questionClass: type[QuestionBase], *, seed: int, **parameters) -> QuestionBase:
    old_argv = sys.argv[:]
    sys.argv = ['', f'seed={seed}']

    question = questionClass.initTemplate(**parameters)
    question = question.initWithParameters(json.loads(question.getTemplateParameters())['PARAMETERS'])

    sys.argv = old_argv
    return question
