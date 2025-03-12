# Запуск тестов

В проекте используется пакетный менеджер [uv](https://github.com/astral-sh/uv). Команда для запуска тестов:

```sh
uvx pytest
```

# Создание тестов

Тесты пишутся в соответствии с [документацией pytest](https://docs.pytest.org/en/stable). Файлы с тестами автоматически находятся по префиксу/суффиксу `test` в названии. В этих файлах запускаются функции с префиксом `test`, методы с префиксом/суффиксом `test` у классов с префиксом `Test`. Это стандартное поведение pytest.

Дополнительно в файле `utility.py` содержится функция `moodleInit`, позволяющая эмулировать создание экземпляра класса, как если бы это происходило в moodle (с прокидыванием параметров через Twig)

Пример реализации теста:

```py
from prog_questions import QuestionSum
from utility import moodleInit


class TestQuestionSum:
    question = moodleInit(QuestionSum, seed=12345)

    def test_code_preload(self):
        assert 'main' in self.question.preloadedCode

    def test_code_run(self):
        assert self.question.test(
            r'''
            #include <stdio.h>

            void main() {
                int sum = 0, next = 0;
                while (scanf("%d", &next) == 1) sum += next;

                printf("%d\n", sum);
            }
            '''
        ) == 'OK'

```

# Документация `utility.py`

### Функции:

`moodleInit(questionClass: type[QuestionBase], *, seed: int, **parameters) -> QuestionBase` - создаёт экземпляр класса `questionClass` с эмуляцией пробрасывания параметров, как если бы это было заинтегрировано в moodle

 - `questionClass` - **тип** класса вопроса, экземпляр которого будет создаваться
 - `seed` - сид, с которым будет создаваться вопрос
 - `parameters` - параметры, с которыми будет создаваться вопрос
 - *Возвращаемое значение* - созданный экземпляр класса
