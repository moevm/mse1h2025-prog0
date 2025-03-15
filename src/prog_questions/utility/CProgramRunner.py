import subprocess
import os
import tempfile


class CompilationError(Exception):
    """Ошибка компиляции C-кода"""
    pass


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

    def _compile(self) -> str:
        """Компиляция кода в исполняемый файл, возвращает путь к исполняемому файлу"""
        # Сохраняем код в файл
        src_path = os.path.join(self.tmp_dir.name, 'program.c')
        with open(src_path, 'w') as f:
            f.write(self.c_code)

        # Компилируем программу
        exec_path = os.path.join(self.tmp_dir.name, 'program')
        compile_result = subprocess.run(
            ['gcc', src_path, '-o', exec_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )

        if compile_result.returncode != 0:
            raise CompilationError(compile_result.stderr.decode())

        return exec_path

    def run(self, input_data: str = "") -> str:
        """
        Запуск скомпилированной программы
        :param input_data: Входные данные для программы
        :return: Вывод программы
        """
        pass

    def __del__(self):
        """Очистка временных файлов при удалении объекта"""
        self.tmp_dir.cleanup()
