from prog_questions import QuestionStringOperations, utility
from utility import moodleInit


class TestSimpleQuestionRandomCondition:
    question = moodleInit(QuestionStringOperations, seed=52, is_simple_task=True)

    def test_code_preload(self):
        assert "main" not in self.question.preloadedCode

    def test_task_text(self):
        assert "Перевести все гласные ['A', 'E', 'I', 'O', 'U', 'Y'] в верхний регистр" in self.question.questionText
        assert "Замените каждый пробел на число символов “_” в исходной строке. Если число больше 7, то укажите его остаток от деления на 13" in self.question.questionText
        assert "Замените все цифры в строке остатками их деления на 2" in self.question.questionText

    def test_code_success_run(self):
        assert self.question.test(
            r'''
            int isVowel(char c) {
                // Проверяем только по заглавным буквам
                c = toupper((unsigned char)c);
                return c == 'A' || c == 'E' || c == 'I' || c == 'O' || c == 'U' || c == 'Y';
            }

            void processString(char *str) {
                int len = strlen(str);

                // Считаем количество '_'
                int underscoreCount = 0;
                for (int i = 0; i < len; i++) {
                    if (str[i] == '_') {
                        underscoreCount++;
                    }
                }

                int underscoreReplacement;
                if (underscoreCount > 7) {
                    underscoreReplacement = underscoreCount % 13;
                } else {
                    underscoreReplacement = underscoreCount;
                }

                // Применяем все операции к строке
                for (int i = 0; i < len; i++) {
                    if (isVowel(str[i])) {
                        str[i] = toupper((unsigned char)str[i]);
                    } else if (str[i] == ' ') {
                        str[i] = '0' + underscoreReplacement;
                    } else if (isdigit((unsigned char)str[i])) {
                        int digit = str[i] - '0';
                        str[i] = (digit % 2) + '0';
                    }
                }
            }
            '''
        ) == 'OK'

    def test_code_compile_error(self):
        assert 'Ошибка компиляции' in self.question.test(
            r'''
            void processString(char *str) {
                innt a = 0;
            }
            '''
        )

    def test_code_runtime_error(self):
        assert 'Ошибка выполнения' in self.question.test(
            r'''
            void processString(char *str) {
                int *ptr = NULL;
                *ptr = 42;
                return 0;
            }
            '''
        )

    def test_code_wrong_answer(self):
        assert 'Ошибка: ожидалось' in self.question.test(
            r'''
            void processString(char *str) {

            }
            '''
        )

class TestQuestionRandomCondition:
    question = moodleInit(QuestionStringOperations, seed=52, is_simple_task=False)

    def test_code_preload(self):
        utility.CProgramRunner(self.question.preloadedCode)

    def test_task_text(self):
        assert "Перевести все гласные ['A', 'E', 'I', 'O', 'U', 'Y'] в верхний регистр" in self.question.questionText
        assert "Замените каждый пробел на число символов “_” в исходной строке. Если число больше 7, то укажите его остаток от деления на 13" in self.question.questionText
        assert "Замените все цифры в строке остатками их деления на 2" in self.question.questionText

    def test_code_success_run(self):
        assert self.question.test(
            r'''
            #include <stdio.h>
            #include <string.h>

            int main() {
                char input[1024] = { 0 };
                fgets(input, sizeof(input), stdin);

                char* symbol = input;
                while (*symbol) {
                    if (strchr("aeiouy", *symbol)) *symbol -= 'a' - 'A';
                    symbol++;
                }

                size_t underscore_count = 0;
                symbol = input;
                while (*symbol) {
                    if (*symbol == '_') underscore_count++;
                    symbol++;
                }

                if (underscore_count > 7) underscore_count %= 13;
                char target_number[5] = { 0 };
                snprintf(target_number, sizeof(target_number), "%zu", underscore_count);

                symbol = input;
                while (*symbol) {
                    if (*symbol == ' ') {
                        memmove(symbol + strlen(target_number), symbol + 1, strlen(symbol + 1));
                        strncpy(symbol, target_number, strlen(target_number));
                        symbol += strlen(target_number) - 1;
                    }
                    symbol++;
                }

                symbol = input;
                while (*symbol) {
                    if (strchr("0123456789", *symbol)) *symbol = ((*symbol - '0') % 2) + '0';
                    symbol++;
                }

                puts(input);

                return 0;
            }
            '''
        ) == 'OK'

    def test_code_compile_error(self):
        assert 'Ошибка компиляции' in self.question.test(
            r'''
            #include <stdio.h>

            int main() {
                retuurn 0;
            }
            '''
        )

    def test_code_runtime_error(self):
        assert 'Ошибка выполнения' in self.question.test(
            r'''
            #include <stdio.h>

            int main() {
                int *ptr = NULL;
                *ptr = 42;
                return 0;
            }
            '''
        )

    def test_code_wrong_answer(self):
        assert 'Ошибка: ожидалось' in self.question.test(
            r'''
            #include <stdio.h>

            int main() {
                printf("i can't solve it");
            }

            '''
        )

