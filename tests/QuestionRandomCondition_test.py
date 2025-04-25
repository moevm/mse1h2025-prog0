from prog_questions import QuestionRandomCondition, utility
from utility import moodleInit


class TestQuestionRandomCondition:
    question = moodleInit(QuestionRandomCondition, seed=52, is_simple_task=False)

    def test_code_preload(self):
        utility.CProgramRunner(self.question.preloadedCode)

    def test_task_text(self):
        assert "(arr[0] & arr[7] ^ arr[4] + arr[9]) > 275" in self.question.questionText
        assert "arr[i] = arr[i - 1] | 24" in self.question.questionText
        assert "arr[i] = arr[i] + 45" in self.question.questionText

    def test_code_success_run(self):
        assert self.question.test(
            r'''
            #include <stdio.h>

            int main() {
                long long arr[10];
                int i;

                for (int i = 0; i < 10; i++) {
                    scanf("%lld", &arr[i]);
                }

                for (int i = 0; i < 10; i++) {
                    long long prev = (i - 1 >= 0) ? arr[i - 1] : 0;
                    long long condition = arr[0] & arr[7] ^ arr[4] + arr[9];
                    //printf("%d %lld %lld\n", i, arr[i], condition);
                    if (condition > 275) {
                        arr[i] = prev | 24;
                    } else {
                        arr[i] = arr[i] + 45;
                    }
                }

                for (i = 0; i < 10; i++) {
                    printf("%lld ", arr[i]);
                }

                return 0;
            }

            '''
        ) == 'OK'

    def test_code_compile_error(self):
        assert 'Ошибка компиляции' in self.question.test(
            r'''
            #include <stdio.h>

            int main() {
                long long arr[10];
                int i;

                for (int i = 0; i < 10; i++) {
                    scanf("%lld", &arr[i]);
                }

                for (int i = 0; i < 10; i++) {
                    long long prev = (i - 1 >= 0) ? arr[i - 1] : 0;
                    long long condition = arr[0] & arr[7] ^ arr[4] + arr[9];
                    //printf("%d %lld %lld\n", i, arr[i], condition);
                    if (condition > 275) {
                        arr[i] = prev | 24
                    } else {
                        arr[i] = arr[i] + 45;
                    }
                }

                for (i = 0; i < 10; i++) {
                    printf("%lld ", arr[i]);
                }

                return 0;
            }

            '''
        )

    def test_code_runtime_error(self):
        assert 'Ошибка выполнения' in self.question.test(
            r'''
            #include <stdio.h>

            int main() {
                long long arr[10];
                int i;

                for (int i = 0; i < 10; i++) {
                    scanf("%lld", &arr[i]);
                }

                for (int i = 0; i < 10; i++) {
                    long long prev = (i - 1 >= 0) ? arr[i - 1] : 0;
                    long long condition = arr[0] & arr[7] ^ arr[4] + arr[9];
                    //printf("%d %lld %lld\n", i, arr[i], condition);
                    if (condition > 275) {
                        arr[i] = prev | 24/0;
                    } else {
                        arr[i] = arr[i] + 45;
                    }
                }

                for (i = 0; i < 10; i++) {
                    printf("%lld ", arr[i]);
                }

                return 0;
            }

            '''
        )

    def test_code_wrong_answer(self):
        assert 'Ошибка: ожидалось' in self.question.test(
            r'''
            #include <stdio.h>

            int main() {
                int arr[10];
                int i;

                for (int i = 0; i < 10; i++) {
                    scanf("%d", &arr[i]);
                }

                for (int i = 0; i < 10; i++) {
                    int prev = (i - 1 >= 0) ? arr[i - 1] : 0;
                    int condition = arr[0] & arr[7] ^ arr[4] + arr[9];
                    //printf("%d %lld %lld\n", i, arr[i], condition);
                    if (condition > 275) {
                        arr[i] = prev | 24;
                    } else {
                        arr[i] = arr[i] + 45;
                    }
                }

                for (i = 0; i < 10; i++) {
                    printf("%d ", arr[i]);
                }

                return 0;
            }

            '''
        )


class TestQuestionRandomConditionSimple(TestQuestionRandomCondition):
    question = moodleInit(QuestionRandomCondition, seed=52, is_simple_task=True)

    def test_code_preload(self):
        assert "random_condition_solver" in self.question.preloadedCode

    def test_code_success_run(self):
        assert self.question.test(
            r'''
            void random_condition_solver(long long *arr, size_t arr_length) {
                for (int i = 0; i < arr_length; i++) {
                    long long prev = (i - 1 >= 0) ? arr[i - 1] : 0;
                    long long condition = arr[0] & arr[7] ^ arr[4] + arr[9];
                    //printf("%d %lld %lld\n", i, arr[i], condition);
                    if (condition > 275) {
                        arr[i] = prev | 24;
                    } else {
                        arr[i] = arr[i] + 45;
                    }
                }
            }
            '''
        ) == 'OK'

    def test_code_compile_error(self):
        assert 'Ошибка компиляции' in self.question.test(
            r'''
            void random_condition_solver(long long *arr, size_t arr_length) {
                for (int i = 0; i < arr_length; i++) {
                    long long prev = (i - 1 >= 0) ? arr[i - 1] : 0;
                    long long condition = arr[0] & arr[7] ^ arr[4] + arr[9];
                    //printf("%d %lld %lld\n", i, arr[i], condition);
                    if (condition > 275) {
                        arr[i] = prev | 24
                    } else {
                        arr[i] = arr[i] + 45;
                    }
                }
            }
            '''
        )

    def test_code_runtime_error(self):
        assert 'Ошибка выполнения' in self.question.test(
            r'''
            void random_condition_solver(long long *arr, size_t arr_length) {
                for (int i = 0; i < arr_length; i++) {
                    long long prev = (i - 1 >= 0) ? arr[i - 1] : 0;
                    long long condition = arr[0] & arr[7] ^ arr[4] + arr[9];
                    //printf("%d %lld %lld\n", i, arr[i], condition);
                    if (condition > 275) {
                        arr[i] = prev | 24/0;
                    } else {
                        arr[i] = arr[i] + 45;
                    }
                }
            }
            '''
        )

    def test_code_wrong_answer(self):
        assert 'Ошибка: ожидалось' in self.question.test(
            r'''
            void random_condition_solver(long long *arr, size_t arr_length) {
                for (int i = 0; i < arr_length; i++) {
                    int prev = (i - 1 >= 0) ? arr[i - 1] : 0;
                    int condition = arr[0] & arr[7] ^ arr[4] + arr[9];
                    //printf("%d %lld %lld\n", i, arr[i], condition);
                    if (condition > 275) {
                        arr[i] = prev | 24;
                    } else {
                        arr[i] = arr[i] + 45;
                    }
                }
            }
            '''
        )
