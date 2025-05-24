import pytest
from prog_questions import QuestionStringOperations, utility, Result
from utility import moodleInit

SEED_OPERATIONS = [
    "Перевести все гласные ['A', 'E', 'I', 'O', 'U', 'Y'] в верхний регистр",
    "Замените каждый пробел на число символов “_” в исходной строке. Если число больше 7, то укажите его остаток от деления на 13",
    "Замените все цифры в строке остатками их деления на 2"
]

SUCCESS_BODY = r'''
    char* symbol = str;
    while (*symbol) {
        if (strchr("aeiouy", *symbol)) *symbol -= 'a' - 'A';
        symbol++;
    }

    size_t underscore_count = 0;
    symbol = str;
    while (*symbol) {
        if (*symbol == '_') underscore_count++;
        symbol++;
    }

    if (underscore_count > 7) underscore_count %= 13;
    char target_number[5] = { 0 };
    snprintf(target_number, sizeof(target_number), "%zu", underscore_count);

    symbol = str;
    while (*symbol) {
        if (*symbol == ' ') {
            memmove(symbol + strlen(target_number), symbol + 1, strlen(symbol + 1) + 1);
            strncpy(symbol, target_number, strlen(target_number));
            symbol += strlen(target_number) - 1;
        }
        symbol++;
    }

    symbol = str;
    while (*symbol) {
        if (strchr("0123456789", *symbol)) *symbol = ((*symbol - '0') % 2) + '0';
        symbol++;
    }
'''

RUNTIME_ERROR_BODY = r'''
    int *ptr = NULL;
    *ptr = 42;
'''

COMPILE_ERROR_BODY = r'''
    innt i_am_error_variable = 0;
'''


def generate_code(is_simple_task, body):
    if is_simple_task:
        return f'''
            void processString(char* str) {{
                {body}
            }}
        '''
    else:
        return f'''
        #include <stdio.h>
        #include <string.h>

        int main() {{
            char input[1024] = {{ 0 }};
            fgets(input, sizeof(input), stdin);
            char* str = input;
            {body}
            puts(str);
            return 0;
        }}
        '''



@pytest.mark.parametrize("is_simple_task,strictness", [
    (True, 0),
    (True, 0.5),
    (True, 1),
    (False, 0),
    (False, 0.5),
    (False, 1),
])
class TestQuestionStringOperationsVariants:
    @pytest.fixture(autouse=True)
    def setup(self, is_simple_task, strictness):
        self.question = moodleInit(QuestionStringOperations, seed=52, is_simple_task=is_simple_task, strictness=strictness)

    def test_code_preload(self, is_simple_task):
        if is_simple_task:
            assert "main" not in self.question.preloadedCode
            assert "processString" in self.question.preloadedCode
        else:
            utility.CProgramRunner(self.question.preloadedCode)

    def test_task_text(self):
        assert all(op in self.question.questionText for op in SEED_OPERATIONS)

    def test_code_success_run(self, is_simple_task):
        code = generate_code(is_simple_task, SUCCESS_BODY)
        assert self.question.test(code) == Result.Ok

    def test_code_compile_error(self, is_simple_task):
        broken_code = generate_code(is_simple_task, COMPILE_ERROR_BODY)
        with pytest.raises(CompilationError):
            self.question.test(broken_code)

    def test_code_runtime_error(self, is_simple_task):
        runtime_error_code = generate_code(is_simple_task, RUNTIME_ERROR_BODY)
        with pytest.raises(CompilationError):
            self.question.test(broken_code)
        assert 'Ошибка выполнения' in self.question.test(runtime_error_code)

    def test_code_wrong_answer(self, is_simple_task):
        wrong_code = (
            self.question.preloadedCode if is_simple_task else
            r'''
            #include <stdio.h>

            int main() {
                printf("i can't solve it");
            }
            '''
        )
        assert 'Ошибка: ожидалось' in self.question.test(wrong_code)
