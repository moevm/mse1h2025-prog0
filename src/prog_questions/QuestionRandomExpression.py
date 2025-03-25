from .QuestionBase import QuestionBase
from .utility import CProgramRunner, ExecutionError, CompilationError
from riscv_course.random_expressions.random_expressions import get_expression
import random

PRELOADED_CODE = '''#include <stdio.h>

int main() {
    return 0;
}'''


class QuestionRandomExpression(QuestionBase):
    questionName = "Сложение чисел"
    '''
    Название вопроса
    '''

    def __init__(self, *, seed: int, vars=['x','y','z','w'], operations=['+','-','*','&','|'], length=5,
                 minuses_threshold=0,
                 brackets_treshold=0, minus_symbol="-", all_variables=False, strictness=0):
        """
                Конструктор класса QuestionRandomExpression.

                :param seed: Сид для генерации случайных данных
                :param vars: Список переменных для генерации выражений (по умолчанию ['x','y','z','w'])
                :param operations: Допустимые операции для выражений (по умолчанию ['+','-','*','&','|'])
                :param length: Длина генерируемого выражения (по умолчанию 5)
                :param minuses_threshold: Порог для использования унарных минусов (0-1, по умолчанию 0)
                :param brackets_treshold: Порог для генерации скобок (0-1, по умолчанию 0)
                :param minus_symbol: Символ для отображения минуса (по умолчанию "-")
                :param all_variables: Флаг обязательного использования всех переменных (по умолчанию False)
                :param strictness: Уровень строгости проверки (0-1, влияет на количество тестов)
                :param space_amount: Количество пробелов между значениями ввода (по умолчанию 1)
        """
        super().__init__(seed=seed, vars=vars, operations=operations, length=length,
                         minuses_threshold=minuses_threshold,
                         brackets_treshold=brackets_treshold, minus_symbol=minus_symbol, all_variables=all_variables, strictness=strictness)
        self.vars = vars
        self.operations = operations
        self.length = length
        self.minuses_threshold = minuses_threshold
        self.brackets_treshold = brackets_treshold
        self.minus_symbol = minus_symbol
        self.all_variables = all_variables
        random.seed(self.seed)
        self.testing_values = [random.randint(0, 100) for _ in self.vars]
        self.testing_vars = {key:value for key, value in zip(self.vars, self.testing_values)}
        self.testing_result = eval(self.questionExpression, self.testing_vars)
        self.strictness = strictness
        self.min_space_number = 1
        self.max_space_number = 15
        self.space_amount = self.min_space_number + self.strictness * (self.max_space_number - self.min_space_number)

    def generate_c_code(self):
        # Сортируем переменные в алфавитном порядке
        sorted_vars = sorted(self.vars)

        # Генерируем строки для кода
        vars_declaration = 'int ' + ", ".join(f"{var}" for var in sorted_vars) + ';'  # Объявление переменных
        scanf_format = " ".join("%d" for _ in sorted_vars)  # Формат для scanf
        scanf_vars = ", ".join(f"&{var}" for var in sorted_vars)  # Указатели для scanf

        # Генерация выражения (пример)
        expression = self.questionExpression

        # Генерируем итоговый код
        c_code = f"""
    #include <stdio.h>

    int main() {{
        {vars_declaration}
        if (scanf("{scanf_format}", {scanf_vars}) != {len(sorted_vars)}) return 0;

        // Вычисление выражения
        int result = {expression};
        printf("%d\\n", result);
        return 0;
    }}
    """
        return c_code

    @property
    def preloadedCode(self) -> str:
        return PRELOADED_CODE

    @property
    def questionText(self) -> str:
        operations_list = ["+", "-", "*", "&", "|"]
        operations_html = "\n".join(
            f"<li><code>{op}</code></li>"
            for op in operations_list
        )

        return f"""
            <h1>Условие задачи</h1>
            <p>Напишите функцию, которая вычисляет значение следующего выражения:</p>
            <pre>{self.questionExpression}</pre>

            <h4>Формат ввода</h4>
            <p>На вход через stdin подаются значения {len(self.vars)} переменных в алфавитном порядке ({' '.join(sorted(self.vars))}) через пробел.</p>

            <h4>Доступные операции</h4>
            <ul>
                {operations_html}
            </ul>

            <h4>Формат вывода</h4>
            <p>Результат вычисления выражения должен быть выведен в stdout.</p>

            <h4>Пример</h4>
            <table>
                <tr>
                    <th>Входные данные</th>
                    <th>Выходные данные</th>
                </tr>
                <tr>
                    <td><code>{' '.join(str(v) for v in self.testing_values)}</code></td>
                    <td><code>{self.testing_result}</code></td>
                </tr>
            </table>
            """


    @property
    def questionExpression(self) -> str:
        return get_expression(self.vars, self.operations, self.length, self.seed, self.minuses_threshold,
                              self.brackets_treshold, self.minus_symbol, self.all_variables)

    def test(self, code: str) -> str:
        try:

            # крайний случай с пустым вводом
            runner = CProgramRunner(code)
            general_runner = CProgramRunner(self.generate_c_code())
            output = runner.run('')
            general_output = general_runner.run('')
            # Список краевых случаев
            edge_cases = [
                {
                    'name': 'все нули',
                    'values': [0] * len(self.vars)
                },
                {
                    'name': 'все единицы',
                    'values': [1] * len(self.vars)
                },
                {
                    'name': 'отрицательные значения',
                    'values': [-1 * (i + 1) for i in range(len(self.vars))]
                },
                {
                    'name': 'чередование знаков',
                    'values': [(-1) ** i * i for i in range(len(self.vars))]
                },
                {
                    'name': 'большие числа',
                    'values': [10 ** 9] * len(self.vars)
                }
            ]

            # Проверка краевых случаев
            for case in edge_cases:
                values = case['values']
                input_data = case.get('input_data', (' ' * self.space_amount).join(map(str, values)))

                try:
                    general_output = general_runner.run(input_data)
                    output = runner.run(input_data)

                    if output != general_output:
                        return (
                            f"Краевой случай '{case['name']}': Ошибка\n"
                            f"Вход: {input_data}\n"
                            f"Ожидалось: {general_output}\n"
                            f"Получено: {output}"
                        )
                except ExecutionError as e:
                    return f"Ошибка выполнения в тесте '{case['name']}': {str(e)}"

            if output != general_output:
                return f"Тест пройден с ошибкой"

            min_tests_number = 20
            max_tests_number = 50
            tests_number = min_tests_number + self.strictness * (max_tests_number - min_tests_number)
            random.seed(self.seed)
            for i in range(tests_number):
                general_output = general_runner.run(input_data=(' '*self.space_amount).join(str(value) for value in self.testing_values))
                output = runner.run(input_data=(' '*self.space_amount).join(str(value) for value in self.testing_values))
                if output != general_output:
                    return f"Тест {i + 1} из {tests_number} пройден с ошибкой. Ожидалось: {general_output}, Ваш ответ: {output}"
            return "OK"

        except CompilationError as e:
            return "Ошибка компиляции"


        except ExecutionError as e:
            return f"Ошибка выполнения [{e.exit_code}]: {str(e)}"

        except Exception as e:
            return f"Неожиданная ошибка:{str(e)}"

