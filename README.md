# Клонирование

Ввиду некоторых проблем с символьными ссылками на **ОС Windows**, для успешного клонирования необходимо, чтобы при установке git была установлена опция `Разрешить символьные ссылки`, а также клонировать репозиторий из консоли с правами администратора следующим образом:

```sh
git clone --recursive -c core.symlinks=true https://github.com/moevm/mse1h2025-prog0.git
```

На **Linux** и **MacOS** для клонирования достаточно следующего:

```sh
git clone --recursive https://github.com/moevm/mse1h2025-prog0.git
```

Если репозиторий уже склонирован, обновление `git submodule` происходит следующим образом:

```sh
git submodule update
```

# Сборка

Для сборки необходимы зависимости, указанные в `requirements.txt`. Результат сборки помещается в `dist`. Запуск сборки:

```sh
python build/build.py
```

# GitHub Actions

В проекте настроен workflow `.github/workflows/run-tests.yml`, запускающий тесты с отчётом о покрытии и сборку проекта. Workflow запускается при открытии пул реквеста или изменении ветки, связанной с ним, или при взаимодействии с веткой `main`.

# Документация

## Интеграция модуля генерации задач в CodeRunner

Для интеграции модуля генерации задач в CodeRunner необходимо в настройках вопроса:

1. В разделе **Support Files (Поддерживаемые файлы)** прикрепляем архив, содержащий модуль генерации задач.

2. В разделе **Coderunner Question Type>Customise (Тип Вопроса CodeRunner>Настройка)** нажать галочку возле поля *Настроить*.

3. В разделе **Coderunner Question Type>Template Params (Тип Вопроса CodeRunner>Параметры шаблона)** необходимо инициализировать вопрос с параметрами шаблонизатора Twig. На примере задачи суммы чисел:

```python
import sys
sys.path.insert(0, 'prog_questions.zip')
from prog_questions import QuestionSum

question = QuestionSum.initTemplate()
print(question.getTemplateParameters())
```

В первых трёх строках происходит импорт класса, далее происходит инициализация вопроса с параметрами шаблонизатора Twig.

4. В разделе **Coderunner Question Type>Template Param Controls (Тип Вопроса CodeRunner>Элементы управления параметрами шаблона)** нажать галочки возле полей: *Hoist template parameters, Twig all, Evaluate per student*. В качестве препроцессора выбрать *Python3*. В случае использования локального Moodle дополнительно выбрать язык *C* в разделе **Advanced Customization > Languages > Ace language**.

5. В разделе **Customisation>Template (Настройка>Шаблон)** необходимо инициализировать вопрос, используя параметр Twig PARAMETERS и осуществить проверку решения. На примере задачи суммы чисел:

```python
import sys
sys.path.insert(0, 'prog_questions.zip')
from prog_questions import QuestionSum

question = QuestionSum.initWithParameters("""{{ PARAMETERS | e('py') }}""")
print(question.test("""{{ STUDENT_ANSWER | e('py') }}"""))
```

В первых трёх строках происходит импорт класса, далее происходит инициализация вопроса с параметром PARAMETERS и вывод результатов проверки кода.

6. В разделе **General>Question Name (Общее>Название вопроса)** указываем `{{ QUESTION_NAME }}`, чтобы иметь возможность менять название вопроса внутри кода.

7. В разделе **General>Question Text (Общее>Текст вопроса)** указываем `{{ QUESTION_TEXT }}`, чтобы иметь возможность менять текст вопроса внутри кода.

8. В разделе **Answer Box Reload (Предварительная загрузка поля ответа)** указываем `{{ PRELOADED_CODE }}`, чтобы иметь возможность менять предзагруженный код.

## Класс `QuestionBase` *(Абстрактный)*
Абстрактный класс обёртки для задания coderunner.

### Методы класса:

`initTemplate(cls, **parameters)` - инициализация в параметрах шаблона Twig

* `parameters` - любые параметры, необходимые для настройки (сложность, въедливость и т.п.). Ввиду особенностей coderunner и простоты реализации, параметры могут быть типами, поддерживающимися JSON (`int`, `float`, `str`, `bool`, `None`, `array`, `dict`)

`initWithParameters(cls, parameters: str)` - инициализация в основном шаблоне, после инициализации параметров шаблона Twig. **Подразумевается использование только в связке с Twig параметром `PARAMETERS`**.
* `parameters` - любые параметры в виде строки JSON, передаваемые в конструктор

### Методы экземпляра класса:

`getTemplateParameters(self) -> str` - возвращает параметры в формате JSON для шаблонизатора Twig

`test(self, code: str) -> str` *(Абстрактный)* - логика проверки кода.

* `code` - код, отправленный студентом на проверку
* *Возвращаемое значение* - строка-результат проверки, которую увидит студент. Если проверка пройдёна - вернуть `OK`

### Свойства экземпляра класса:

`questionName: str` *(Абстрактный)* - название вопроса

`questionText: str` *(Абстрактный)* - задание/текст вопроса

`preloadedCode: str` *(Абстрактный)* - код, который подгружается в поле редактирования кода

### Пример реализации:
```python
from .QuestionBase import QuestionBase
from io import StringIO
from contextlib import redirect_stdout

class PrintSeedQuestion(QuestionBase):
    @property
    def questionName(self) -> str:
        return 'Печать случайного seed'

    @property
    def questionText(self) -> str:
        return f'Напечатайте в консоль случайный сид: {self.seed}'

    @property
    def preloadedCode(self) -> str:
        return f'# TODO: напечатать {self.seed}'

    def test(self, code: str) -> str:
        with StringIO() as f, redirect_stdout(f):
            try:
                eval(code)
            except Exception as e:
                return str(e)

            result = f.getvalue()

        if result.strip() != f'{self.seed}':
            return 'Wrong answer'

        return 'OK'

```

## Класс `QuestionRandomCondition`
Класс обёртки для задания изменения массива по случайному условию.

### Методы экземпляра класса:

`__init__(self, *, seed: int, condition_length: int, array_length: int, strictness: float)` - метод инициализации экземпляра.

* `seed` - случайное зерно, используемое для воспроизводимости результатов псевдослучайной генерации случайных значений;
* `condition_length` - целое число, указывающее длину условия (количество операндов в генерируемом условии);
* `array_length` - целое число, указывающее длину массива, элементы которого нужно изменить;
* `strictness` - число с плавающей точкой, в диапазоне `[0; 1]`, регулирующее въедливость проверки.

`parse(self, task_text: str)` - метод, позволяющий получить характеристики сгенерированного условия, которые не хранятся в исходном классе как отдельные атрибуты.

* `task_text` - текст условия сгенерированного задания.

`test_case(self, arr: list, code: str, space_amount: int) -> str` - метод, позволяющий запустить переданный код на конкретных входных данных.

* `arr` - список чисел, подающийся на вход программе;
* `code` - код, тестирование которого необходимо произвести;
* `space_amount` - количество пробелов, зависящее от въедливости проверки.

В зависимости от результата работы программы возвращается одна из строк:

* `OK` - если результат совпал с ожидаемым результатом;
* `Ошибка: ожидалось '{expected_output}', получено '{output}'` - если результат работы программы не совпадает с ожидаемым результатом;
* `Ошибка компиляции: {e}` - если произошла ошибка компиляции;
* `Ошибка выполнения (код {e.exit_code}): {e}` - если произошла ошибка выполнения.

# HERE

`test_same_numbers_case(self, code: str, amount: int, exponentiation: int) -> str` - метод, организующий тестирование на входных данных, состоящих из повтора одного числа.

* `code` - код, тестирование которого необходимо произвести;
* `amount` - целое число, количество вариантов входных данных (отличаются количеством пробелов);
* `exponentiation` - целое число, показатель степени элементов массива входных данных. При значении `>9` осуществляет проверку выхода за границу `INT`.

В случае возникновения ошибки выполнение остальных тестов заканчивается и возвращается соответствующая полученной ошибке строка. Если все тесты выполнены корректно - метод возвращает строку `OK`.

`test_alternate_numbers_case(self, code: str, amount: int, exponentiation: int) -> str` - метод, организующий тестирование на входных данных, состоящих из чередования близких к нулю и удалённых от нуля значений.

* `code` - код, тестирование которого необходимо произвести;
* `amount` - целое число, количество вариантов входных данных (отличаются количеством пробелов);
* `exponentiation` - целое число, показатель степени элементов массива входных данных. При значении `>9` осуществляет проверку выхода за границу `INT`.

В случае возникновения ошибки выполнение остальных тестов заканчивается и возвращается соответствующая полученной ошибке строка. Если все тесты выполнены корректно - метод возвращает строку `OK`.

`test_random(self, code: str, amount: int, upper_border: int) -> str` - метод, организующий тестирование с рандомизированными входными данными.

* `code` - код, тестирование которого необходимо произвести;
* `amount` - целое число, количество вариантов входных данных;
* `upper_border` - целое число `N`, ограничение на промежуток чисел `[-10^N; 10^N]` для генерации элементов массива;

В случае возникновения ошибки выполнение остальных тестов заканчивается и возвращается соответствующая полученной ошибке строка. Если все тесты выполнены корректно - метод возвращает строку `OK`.

`distribute_random_tests(self, total_amount: int, exponentiation_amount: int) -> list` - метод, распределяющий количество оставшихся тестов среди рандомизированных.

* `total_amount` - целое число, количество рандомизированных тестов;
* `exponentiation_amount` - целое число, количество различных групп тестов (в одну группу объединены тесты с одним значением `upper_border`).

`test(self, code: str) -> str` - метод, организующий тестирование в целом.

* `code` - код, тестирование которого необходимо произвести;

В случае возникновения ошибки выполнение остальных тестов заканчивается и возвращается соответствующая полученной ошибке строка. Если все тесты выполнены корректно - метод возвращает строку `OK`.

### Свойства экземпляра класса:

`questionName: str` - название вопроса.

`questionText: str` - задание/текст вопроса.

`preloadedCode: str` - код, который подгружается в поле редактирования кода.

## Класс `CProgramRunner`
Класс для компиляции и выполнения программ на языке C.

### Методы класса:
`__init__(self, c_code: str)` - инициализирует объект класса с компиляцией переданного C-кода

* `c_code` - исходный код на C в виде строки
* Компилирует код в исполняемый файл и сохраняет путь к нему

`_compile(self) -> str` - компилирует код в исполняемый файл
* *Возвращаемое значение* - путь к скомпилированному исполняемому файлу
* *Исключение* - `CompilationError` если компиляция не удалась

`run(self, input_data: str = "", timeout: int = 60) -> str` - запускает скомпилированную программу с передачей входных данных
* `input_data` - входные данные для программы (по умолчанию пустая строка)
* `timeout` - максимальное время выполнения программы в секундах (по умолчанию 60 секунд)
* *Возвращаемое значение* - вывод программы
* *Исключение* - `ExecutionError` если выполнение программы завершилось с ошибкой

`__del__(self)` - очищает временные файлы при удалении объекта

### Исключения класса:
`CompilationError` - исключение, вызываемое при ошибке компиляции C-кода

`ExecutionError` - исключение, вызываемое при ошибке выполнения скомпилированной программы
* `message` - сообщение об ошибке
* `exit_code` - код завершения программы

### Вспомогательный класс `ExitCodeHandler`:
Класс для обработки кодов завершения и сигналов.

Методы класса:

`get_exit_message(self, exit_code) -> str` - преобразует код завершения в текстовое сообщение
* `exit_code` - код завершения программы
* *Возвращаемое значение* - текстовое описание кода завершения

### Пример использования:
```python
from CProgramRunner import CProgramRunner, CompilationError, ExecutionError

C_CODE = """
#include <stdio.h>

int main() {
    printf("42\\n");
    return 0;
}
"""

try:
    runner = CProgramRunner(C_CODE)
    output = runner.run()

    print("Программа успешно выполнена!")
    print("Вывод программы:", output)

except CompilationError as e:
    print("Ошибка компиляции:")
    print(str(e))

except ExecutionError as e:
    print(f"Ошибка выполнения [{e.exit_code}]: {str(e)}")

except Exception as e:
    print("Неожиданная ошибка:")
    print(str(e))

```
