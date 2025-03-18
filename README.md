# Клонирование

В репозитории используется `git submodule`, поэтому клонирование происходит следющим образом:

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

## Класс `CProgramRunner`
Класс для компиляции и выполнения программ на языке C.

### Методы класса:
`__init__(self, c_code: str)` - инициализирует объект класса с компиляцией переданного C-кода

* `c_code` - исходный код на C в виде строки
* Компилирует код в исполняемый файл и сохраняет путь к нему

`_compile(self) -> str` - компилирует код в исполняемый файл
* *Возвращаемое значение* - путь к скомпилированному исполняемому файлу
* *Исключение* - `CompilationError` если компиляция не удалась

`run(self, input_data: str = "") -> str` - запускает скомпилированную программу с передачей входных данных
* `input_data` - входные данные для программы (по умолчанию пустая строка)
* *Возвращаемое значение* - вывод программы
* *Исключение* - `ExecutionError` если выполнение программы завершилось с ошибкой

`__del__(self)` - очищает временные файлы при удалении объекта

### Исключения класса:
`CompilationError` - исключение, вызываемое при ошибке компиляции C-кода

`ExecutionError` - исключение, вызываемое при ошибке выполнения скомпилированной программы
* `message` - сообщение об ошибке
* `exit_code` - код завершения программы

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
