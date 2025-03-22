import subprocess
import os
import tempfile


class CompilationError(Exception):
    """Ошибка компиляции C-кода"""
    pass


class ExecutionError(Exception):
    """Ошибка выполнения скомпилированной программы"""

    def __init__(self, message: str, exit_code: int):
        super().__init__(message)
        self.exit_code = exit_code


class ExitCodeHandler:
    """Обработчик кодов завершения и сигналов"""

    def __init__(self):
        self.signal_names = {
            2: "SIGINT (Interrupt)",
            3: "SIGQUIT (Quit)",
            4: "SIGILL (Illegal Instruction)",
            5: "SIGTRAP (Trap)",
            6: "SIGABRT (Abort)",
            7: "SIGBUS (Bus Error)",
            8: "SIGFPE (Floating Point Exception)",
            9: "SIGKILL (Kill)",
            10: "SIGUSR1 (User Signal 1)",
            11: "SIGSEGV (Segmentation Violation)",
            12: "SIGUSR2 (User Signal 2)",
            13: "SIGPIPE (Broken Pipe)",
            14: "SIGALRM (Alarm)",
            15: "SIGTERM (Termination)",
            24: "SIGXCPU (CPU Time Limit Exceeded)",
            25: "SIGXFSZ (File Size Limit Exceeded)"
        }

        self.exit_codes = {
            0: "Успешное завершение",
            1: "Общая ошибка",
            126: "Команда не может быть выполнена",
            127: "Команда не найдена",
            255: "Код завершения вне допустимого диапазона"
        }

    def get_exit_message(self, exit_code):
        """Преобразование кода завершения в текстовое сообщение"""
        if exit_code < 0 or 128 <= exit_code < 160:
            signal_number = exit_code if exit_code > 0 else -exit_code
            signal_name = self.signal_names.get(signal_number, f"[{signal_number}]")
            return f"Программа завершена сигналом {signal_name}"
        else:
            return self.exit_codes.get(exit_code, f"Неизвестный код завершения {exit_code}")


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
        self.exit_code_handler = ExitCodeHandler()

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

    def run(self, input_data: str = "", timeout: int = 60) -> str:
        """
        Запуск скомпилированной программы
        :param input_data: Входные данные для программы
        :param timeout: Максимальное время выполнения программы
        :return: Вывод программы
        """
        try:
            run_result = subprocess.run(
                [self.executable_path],
                input=input_data.encode(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                timeout=timeout
            )
        except subprocess.TimeoutExpired:
            raise ExecutionError("Программа зациклилась или не завершилась в течение {} секунд".format(timeout), -1)

        exit_message = self.exit_code_handler.get_exit_message(run_result.returncode)
        if run_result.returncode != 0:
            raise ExecutionError(
                message=exit_message,
                exit_code=run_result.returncode
            )

        return run_result.stdout.decode().strip()

    def __del__(self):
        """Очистка временных файлов при удалении объекта"""
        self.tmp_dir.cleanup()
