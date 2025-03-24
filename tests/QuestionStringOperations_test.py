from prog_questions import QuestionRandomCondition, utility
from utility import moodleInit


class TestQuestionRandomCondition:
    question = moodleInit(QuestionRandomCondition, seed=52)

    def test_code_preload(self):
        assert 'main' in self.question.preloadedCode

    def test_task_text(self):
        assert "Перевести все гласные ['A', 'E', 'I', 'O', 'U', 'Y'] в верхний регистр" in self.question.questionText
        assert "Замените каждый пробел на число символов “_” в исходной строке. Если число больше 7, то укажите его остаток от деления на 13" in self.question.questionText
        assert "Замените все цифры в строке остатками их деления на 2" in self.question.questionText

   
