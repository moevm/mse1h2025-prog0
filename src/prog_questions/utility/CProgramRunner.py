import tempfile


class CProgramRunner:
    """Класс для компиляции и выполнения C-кода"""

    def __init__(self, c_code: str):
        """
        Инициализация с компиляцией переданного C-кода
        :param c_code: Исходный код на C в виде строки
        """
        self.c_code = c_code
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.executable_path = self._compile()
        pass

    def _compile(self) -> str:
        """Компиляция кода в исполняемый файл, возвращает путь к исполняемому файлу"""

        pass

    def run(self, input_data: str = "") -> str:
        """
        Запуск скомпилированной программы
        :param input_data: Входные данные для программы
        :return: Вывод программы
        """
        pass
