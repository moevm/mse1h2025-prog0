from prog_questions import QuestionRandomExpression
from utility import moodleInit


class TestQuestionRandomExpression:
    question = moodleInit(QuestionRandomExpression, seed=12345)

    def test_code_preload(self):
        assert 'main' in self.question.preloadedCode

    def test_correct_solution(self):
        result = self.question.test(
            r'''
            #include <stdio.h>

            int main() {
                int a, b, c, d;
                if (scanf("%d %d %d %d", &a, &b, &c, &d) != 4) return 0;

                // w=a, x=b, y=c, z=d (алфавитный порядок)
                int w = a, y = c, z = d;
                int result = (z * w - z) | (y * w) | y;

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

            int result = (d * a - d) | (c * a) | c;
            printf("%d\n", result);
        }
        '''
        assert self.question.test(code1) == "Ошибка компиляции"

        # Тест 2: Несуществующая функция
        code2 = r'''
        #include <stdio.h>

        int main() {
            int a, b, c, d;
            scan("%d %d %d %d", &a, &b, &c, &d); // Опечатка в scanf

            int result = (d * a - d) | (c * a) | c;
            printf("%d\n", result);
            return 0;
        }
        '''
        assert self.question.test(code2) == "Ошибка компиляции"

    def test_incorrect_results(self):
        # Тест 1: Неправильный порядок операций
        code1 = r'''
        #include <stdio.h>

        int main() {
            int a, b, c, d;
            if (scanf("%d %d %d %d", &a, &b, &c, &d) != 4) return 0;

            // Ошибка: z*w - (z | y) вместо (z*w - z) | y
            int result = (d * a - (d | c)) | (c * a);

            printf("%d\n", result);
            return 0;
        }
        '''
        res1 = self.question.test(code1)
        assert res1 != 'OK', "Ожидалась ошибка выполнения, но тест пройден"

        # Тест 2: Неправильные переменные
        code2 = r'''
        #include <stdio.h>

        int main() {
            int a, b, c, d;
            if (scanf("%d %d %d %d", &a, &b, &c, &d) != 4) return 0;

            // Используем неправильные переменные (z вместо w)
            int result = (d * d - d) | (c * d) | c;

            printf("%d\n", result);
            return 0;
        }
        '''
        res2 = self.question.test(code2)
        assert res2 != 'OK', "Ожидалась ошибка выполнения, но тест пройден"
