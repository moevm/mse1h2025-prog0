from prog_questions import QuestionStringOperations, utility
from utility import moodleInit


class TestQuestionRandomCondition:
    question = moodleInit(QuestionStringOperations, seed=52)

    def test_code_preload(self):
        utility.CProgramRunner.CProgramRunner(self.question.preloadedCode)

    def test_task_text(self):
        assert "Перевести все гласные ['A', 'E', 'I', 'O', 'U', 'Y'] в верхний регистр" in self.question.questionText
        assert "Замените каждый пробел на число символов “_” в исходной строке. Если число больше 7, то укажите его остаток от деления на 13" in self.question.questionText
        assert "Замените все цифры в строке остатками их деления на 2" in self.question.questionText

    def test_code_success_run(self):
        assert self.question.test(
            r'''
#include <stdio.h>
#include <string.h>
#include <ctype.h>
#include <stdlib.h>

int is_vowel(char c) {
    c = toupper(c);
    return (c == 'A' || c == 'E' || c == 'I' || c == 'O' || c == 'U' || c == 'Y');
}

void replace_spaces_with_count(char *str) {
    int underscore_count = 0;
    for (int i = 0; str[i] != '\0'; i++) {
        if (str[i] == '_') underscore_count++;
    }

    int replace_value = underscore_count;
    if (underscore_count > 7) replace_value = underscore_count % 13;

    char *new_str = (char *)malloc(1000 * sizeof(char));
    int new_index = 0;

    for (int i = 0; str[i] != '\0'; i++) {
        if (str[i] == ' ') {
            char num_str[10];
            sprintf(num_str, "%d", replace_value);
            strcpy(&new_str[new_index], num_str);
            new_index += strlen(num_str);
        } else {
            new_str[new_index++] = str[i];
        }
    }
    new_str[new_index] = '\0';

    strcpy(str, new_str);
    free(new_str);
}

void replace_digits(char *str) {
    for (int i = 0; str[i] != '\0'; i++) {
        if (isdigit(str[i])) {
            int digit = str[i] - '0';
            str[i] = (digit % 2) + '0';
        }
    }
}

int main() {
    char str[101];
    fgets(str, sizeof(str), stdin);
    str[strcspn(str, "\n")] = '\0';

    for (int i = 0; str[i] != '\0'; i++) {
        if (is_vowel(str[i])) {
            str[i] = toupper(str[i]);
        }
    }

    replace_spaces_with_count(str);

    replace_digits(str);
    printf("%s\n", str);

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

