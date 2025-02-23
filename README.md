# Документация

## Интеграция модуля генерации задач в CodeRunner
Для интеграции модуля генерации задач в CodeRunner необходимо в настройках вопроса:
1. В разделе Support Files прикрепляем архив, содержащий модуль генерации задач.
2. В разделе Coderunner Question Type>Template Params необходимо инициализировать вопрос с параметрами шаблонизатора Twig. На примере задачи суммы чисел:
```python
import sys
sys.path.insert(0, 'prog_questions.zip')
from prog_questions import QuestionSum

question = QuestionSum.initTemplate()
print(question.getTemplateParameters())
```
В первых трёх строках происходит импорт класса, далее происходит инициализация вопроса с параметрами шаблонизатора Twig.
Также необходимо в разделе Coderunner Question Type>Template Param Controls нажать галочки возле: Hoist template parameters, Twig all, Evaluate per student. В качестве препроцессора выбрать Python3.
3. В разделе Customisation>Template необходимо инициализировать вопрос, используя параметр Twig PARAMETERS и осуществить проверку решения. На примере задачи суммы чисел:
```python
import sys
sys.path.insert(0, 'prog_questions.zip')
from prog_questions import QuestionSum

question = QuestionSum.initWithParameters("""{{ PARAMETERS | e('py') }}""")
print(question.test("""{{ STUDENT_ANSWER | e('py') }}"""))
```
В первых трёх строках происходит импорт класса, далее происходит инициализация вопроса с параметром PARAMETERS и вывод результатов проверки кода.
4. В разделе General>Question Name указываем {{ QUESTION_NAME }}, чтобы иметь возможность менять название вопроса внутри кода.
5. В разделе General>Question Text указываем {{ QUESTION_TEXT }}, чтобы иметь возможность менять текст вопроса внутри кода.
6. В разделе Answer Box Reload указываем {{ PRELOADED_CODE }}, чтобы иметь возможность менять предзагруженный код.

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
