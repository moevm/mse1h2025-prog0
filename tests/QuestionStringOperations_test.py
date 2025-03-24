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

void process_string(char *str) {
    char vowels[] = "AEIOUYaeiouy";
    for (int i = 0; str[i] != '\0'; i++) {
        if (strchr(vowels, str[i]) != NULL) {
            str[i] = toupper(str[i]);
        }
    }

    int underscore_count = 0;
    for (int i = 0; str[i] != '\0'; i++) {
        if (str[i] == '_') {
            underscore_count++;
        }
    }
    int replace_num = underscore_count;
    if (replace_num > 7) {
        replace_num %= 13;
    }

    for (int i = 0; str[i] != '\0'; i++) {
        if (str[i] == ' ') {
            char temp[210] = {0};
            sprintf(temp, "%d", replace_num);

            int num_len = strlen(temp);
            int str_len = strlen(str);

            memmove(&str[i + num_len], &str[i + 1], str_len - i);
            memcpy(&str[i], temp, num_len);
            i += num_len - 1;
        }
    }
    for (int i = 0; str[i] != '\0'; i++) {
        if (isdigit(str[i])) {
            int digit = str[i] - '0';
            str[i] = (digit % 2) + '0';
        }
    }
}

int main() {
    char str[210];
    fgets(str, sizeof(str), stdin);

    size_t len = strlen(str);
    if (len > 0 && str[len - 1] == '\n') {
        str[len - 1] = '\0';
    }

    process_string(str);
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

