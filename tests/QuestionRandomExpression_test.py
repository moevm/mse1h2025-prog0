from prog_questions import QuestionRandomExpression, utility
from utility import moodleInit


class TestQuestionRandomExpression:
    question = moodleInit(QuestionRandomExpression, seed=52)

    def test_code_preload(self):
        utility.CProgramRunner.CProgramRunner(self.question.preloadedCode)

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
        assert self.question.test(code1) == "Ошибка компиляции"


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

