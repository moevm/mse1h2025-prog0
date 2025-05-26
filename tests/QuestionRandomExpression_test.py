from prog_questions import QuestionRandomExpression, utility, Result
from prog_questions.utility import CompilationError, ExecutionError
from utility import moodleInit
import pytest


class TestQuestionRandomExpression:
    question = moodleInit(QuestionRandomExpression, seed=52, is_simple_task=False)

    def test_code_preload(self):
        utility.CProgramRunner(self.question.preloadedCode)

    def test_task_text(self):
        assert "w * y & w + x - y * w" in self.question.questionText

    def test_correct_solution(self):
        result = self.question.test(
            r'''
            #include <stdio.h>

            int main() {
                int a, b, c, d;
                if (scanf("%d %d %d %d", &a, &b, &c, &d) != 4) return 1;

                // w=a, x=b, y=c, z=d (алфавитный порядок)
                int w = a, y = c, z = d, x = b;
                int result = w * y & w + x - y * w;

                printf("%d\n", result);
                return 0;
            }
            '''
        )
        assert result == Result.Ok()

    def test_compilation_errors(self):
        # Тест 1: Неправильный синтаксис
        code = r'''
        #include <stdio.h>

        int main() {
            int a, b, c, d
            // Пропущена точка с запятой
            if (scanf("%d %d %d %d", &a, &b, &c, &d) != 4) return 1;

            int result = w * y & w + x - y * w;
            printf("%d\n", result);
        }
        '''
        with pytest.raises(CompilationError):
            self.question.test(code)

    def test_incorrect_results(self):
        # Тест 1: Неправильный порядок операций
        code = r'''
        #include <stdio.h>

        int main() {
            int a, b, c, d;
            if (scanf("%d %d %d %d", &a, &b, &c, &d) != 4) return 1;
            int w = a, y = c, z = d, x = b;
            int result = w * (y & w) + x - y * w;

            printf("%d\n", result);
            return 0;
        }
        '''
        assert self.question.test(code) != Result.Ok()


class TestQuestionRandomExpressionSimpleMode:
    question = moodleInit(QuestionRandomExpression, seed=52, is_simple_task=True)

    def test_task_text(self):
        assert "w * y & w + x - y * w" in self.question.questionText

    def test_correct_solution(self):
        result = self.question.test(
            r'''int random_expression(int w, int x, int y, int z) {
int result = w * y & w + x - y * w;
return result;
}
            '''
        )
        assert result == Result.Ok()

    def test_compilation_errors(self):
        # Тест 1: Неправильный синтаксис
        code = r'''
int random_expression(int w int x, int y, int z) {
    int result = w * y & w + x - y * w;
    return result;
}
        '''
        with pytest.raises(CompilationError):
            self.question.test(code)

    #
    def test_incorrect_results(self):
        # Тест 1: Неправильный порядок операций
        code = r'''
int random_expression(int w, int x, int y, int z) {
    int result = w * (y & w) + x - y * w;
    return result;
}
        '''
        assert self.question.test(code) != Result.Ok()
