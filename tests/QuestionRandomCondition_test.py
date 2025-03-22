from prog_questions import QuestionRandomCondition
from utility import moodleInit


class TestQuestionSum:
    question = moodleInit(QuestionRandomCondition, seed=52)

    def test_code_preload(self):
        assert 'main' in self.question.preloadedCode

    def test_code_run(self):
        assert self.question.test(
            r'''
            #include <stdio.h>

            void main() {
                int sum = 0, next = 0;
                while (scanf("%d", &next) == 1) sum += next;

                printf("%d\n", sum);
            }
            '''
        ) == 'OK'
