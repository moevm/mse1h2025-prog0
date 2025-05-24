from prog_questions import QuestionN5, Result, utility
from utility import moodleInit
import pytest

class TestQuestionN5:
    question = moodleInit(QuestionN5, seed=123, maxSentenceSize=100)

    def test_code_preload(self):
        utility.CProgramRunner(self.question.preloadedCode)

    def test_question_text(self):
        assert 'Находит строку с наибольшей длиной' in self.question.questionText
        assert '&lt;Число символов&gt;: строка' in self.question.questionText

    def test_code_success_run(self):
        assert self.question.test(r'''
            #include <stdio.h>

            int main() {
                size_t n;
                scanf("%zu\n", &n);

                char sentence[101] = { 0 };
                char bestSentence[101] = { 0 };
                int bestMetric = 0;

                for (size_t i = 0; i < n; i++) {
                    fgets(sentence, sizeof(sentence), stdin);

                    char* ch = sentence;
                    while (*ch) {
                        if (*ch == '\n') {
                            *ch = '\0';
                            break;
                        }
                        ch++;
                    }

                    int metric = 0;
                    ch = sentence;
                    while (*ch) {
                        metric++;
                        ch++;
                    }

                    if (metric <= bestMetric) continue;

                    ch = sentence;
                    char* target = bestSentence;
                    while (*ch) {
                        *target = *ch;
                        ch++;
                        target++;
                    }
                    *target = '\0';
                    bestMetric = metric;
                }

                printf("%d: %s\n", bestMetric, bestSentence);
                return 0;
            }
        ''') == Result.Ok()

    def test_code_compile_error(self):
        with pytest.raises(utility.CompilationError):
            self.question.test(r'''
                #include <stdio.h>

                int main() {
                    size_t n;
                    scanf("%zu\n", &n);

                    char sentence[101] = { 0 };
                    char bestSentence[101] = { 0 };
                    int bestMetric = 0;

                    for (size_t i = 0; i < n; i++) {
                        fgets(sentence, sizeof(sentence), stdin);

                        char* ch = sentence;
                        while (*ch) {
                            if (*ch == '\n') {
                                *ch = '\0';
                                break;
                            }
                            ch++;
                        }

                        int metric = 0;
                        ch = sentence;
                        while (*ch) {
                            metric++;
                            ch++;
                        }

                        if (metric <= bestMetric) continue;

                        ch = sentence;
                        char* target = bestSentence;
                        while (*ch) {
                            *target = *ch
                            ch++;
                            target++;
                        }
                        *target = '\0';
                        bestMetric = metric;
                    }

                    printf("%d: %s\n", bestMetric, bestSentence);
                    return 0;
                }
            ''')

    def test_code_stringh_prohibit(self):
        with pytest.raises(utility.CompilationError):
            self.question.test(r'''
                #include <stdio.h>
                #include <string.h>

                int main() {
                    size_t n;
                    scanf("%zu\n", &n);

                    char sentence[101] = { 0 };
                    char bestSentence[101] = { 0 };
                    int bestMetric = 0;

                    for (size_t i = 0; i < n; i++) {
                        fgets(sentence, sizeof(sentence), stdin);

                        char* ch = sentence;
                        while (*ch) {
                            if (*ch == '\n') {
                                *ch = '\0';
                                break;
                            }
                            ch++;
                        }

                        int metric = 0;
                        ch = sentence;
                        while (*ch) {
                            metric++;
                            ch++;
                        }

                        if (metric <= bestMetric) continue;

                        ch = sentence;
                        char* target = bestSentence;
                        while (*ch) {
                            *target = *ch;
                            ch++;
                            target++;
                        }
                        *target = '\0';
                        bestMetric = metric;
                    }

                    printf("%d: %s\n", bestMetric, bestSentence);
                    return 0;
                }

                #undef _STRING_H
            ''')

    def test_code_runtime_error(self):
        assert self.question.test(r'''
            #include <stdio.h>

            int main() {
                size_t n;
                scanf("%zu\n", &n);

                char sentence[101] = { 0 };
                char bestSentence[101] = { 0 };
                int bestMetric = 0;

                for (size_t i = 0; i < n; i++) {
                    fgets(sentence, sizeof(sentence), stdin);

                    char* ch = sentence;
                    while (*ch) {
                        if (*ch == '\n') {
                            *ch = '\0';
                            break;
                        }
                        ch++;
                    }

                    int metric = 0;
                    while (*ch) {
                        metric++;
                        ch++;
                    }

                    if (metric <= bestMetric) continue;

                    char* target = bestSentence;
                    while (*ch) {
                        *target = *ch;
                        ch++;
                        target++;
                    }
                    *target = '\0';
                    bestMetric = metric;
                }

                printf("%d: %s\n", bestMetric, bestSentence);
                return 0;
            }
        ''') != Result.Ok()

    def test_code_wrong_answer(self):
        assert self.question.test(r'''
            #include <stdio.h>

            int main() {
                size_t n;
                scanf("%zu\n", &n);

                char sentence[2] = { 0 };
                char bestSentence[2] = { 0 };
                int bestMetric = 0;

                for (size_t i = 0; i < n; i++) {
                    fgets(sentence, sizeof(sentence), stdin);

                    char* ch = sentence;
                    while (*ch) {
                        if (*ch == '\n') {
                            *ch = '\0';
                            break;
                        }
                        ch++;
                    }

                    int metric = 0;
                    ch = sentence;
                    while (*ch) {
                        metric++;
                        ch++;
                    }

                    if (metric <= bestMetric) continue;

                    ch = sentence;
                    char* target = bestSentence;
                    while (*ch) {
                        *target = *ch;
                        ch++;
                        target++;
                    }
                    *target = '\0';
                    bestMetric = metric;
                }

                printf("%d: %s\n", bestMetric, bestSentence);
                return 0;
            }
        ''') != Result.Ok()
