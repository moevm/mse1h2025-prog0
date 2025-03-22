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
                        arr[i] = prev | 24/0;
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

