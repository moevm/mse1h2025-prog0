from prog_questions import QuestionRandomExpression, utility
from prog_questions.utility import CompilationError, ExecutionError
from utility import moodleInit


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
                if (scanf("%d %d %d %d", &a, &b, &c, &d) != 4) return 0;

                // w=a, x=b, y=c, z=d (алфавитный порядок)
                int w = a, y = c, z = d, x = b;
                int result = w * y & w + x - y * w;

                printf("%d\n", result);
                return 0;
            }
            '''
        )
        assert result == 'OK', f"Ожидалось OK, получено: {result}"

    def test_compilation_errors(self):
        # Тест 1: Неправильный синтаксис
        code1 = r'''
        #include <stdio.h>

        int main() {
            int a, b, c, d
            // Пропущена точка с запятой
            if (scanf("%d %d %d %d", &a, &b, &c, &d) != 4) return 0;

            int result = w * y & w + x - y * w;
            printf("%d\n", result);
        }
        '''
        assert "Ошибка компиляции" in self.question.test(code1)


    def test_incorrect_results(self):
        # Тест 1: Неправильный порядок операций
        code1 = r'''
        #include <stdio.h>

        int main() {
            int a, b, c, d;
            if (scanf("%d %d %d %d", &a, &b, &c, &d) != 4) return 0;
            int w = a, y = c, z = d, x = b;
            int result = w * (y & w) + x - y * w;

            printf("%d\n", result);
            return 0;
        }
        '''
        res1 = self.question.test(code1)
        assert res1 != 'OK', "Ожидалась ошибка выполнения, но тест пройден"


class TestQuestionRandomExpressionSimpleMode:
    question = moodleInit(QuestionRandomExpression, seed=52, is_simple_task=True)

    def test_task_text(self):
        assert "w * y & w + x - y * w" in self.question.questionText

    def test_correct_solution(self):
        try:
            result = self.question.test(
                r'''int random_expression(int w, int x, int y, int z) {
    int result = w * y & w + x - y * w;
    return result;
}
                '''
            )

            assert result == 'OK', f"""Ожидалось OK, получено: {result}"""
        except CompilationError as e:
            print("Ошибка компиляции:")
            print(str(e))
            raise Exception(str(e))

        except ExecutionError as e:
            print(f"Ошибка выполнения [{e.exit_code}]: {str(e)}")



    def test_compilation_errors(self):
        # Тест 1: Неправильный синтаксис
        code1 = r'''
int random_expression(int w int x, int y, int z) {
    int result = w * y & w + x - y * w;
    return result;
}
        '''
        assert "Ошибка компиляции" in self.question.test(code1)

#
    def test_incorrect_results(self):
        # Тест 1: Неправильный порядок операций
        code1 = r'''
int random_expression(int w, int x, int y, int z) {
    int result = w * (y & w) + x - y * w;
    return result;
}
        '''
        res1 = self.question.test(code1)
        assert res1 != 'OK', "Ожидалась ошибка выполнения, но тест пройден"

