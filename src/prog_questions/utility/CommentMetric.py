import re


class CommentMetric:
    """
    Класс для анализа комментариев в коде на языке C.
    Attributes:
        code (list): Список строк кода.
        total_lines (int): Общее количество строк кода.
        comment_lines (int): Количество строк с комментариями.
        comment_percentage (float): Процент строк с комментариями.
    """

    def __init__(self, code: str):
        """
        Инициализирует объект класса CommentMetric.
        :param code: Исходный код на языке C в виде строки.
        """
        self.code = self._split_code(code)
        self.total_lines = len(self.code)
        self.comment_lines = 0
        self.comment_percentage = self._count_comments()

    def _split_code(self, code: str) -> list:
        """
        Разбивает код на строки, учитывая переносы строк внутри функций.
        :param code: Исходный код на языке C.
        :return: Список строк кода.
        """
        lines = []
        current_line = ''
        i = 0
        while i < len(code):
            if code[i] == '\n':
                # Проверка на функции
                if self._is_in_function(code, i):
                    current_line += '\n'
                else:
                    lines.append(current_line)
                    current_line = ''
            else:
                current_line += code[i]
            i += 1
        lines.append(current_line)
        return lines

    def _is_in_function(self, code: str, pos: int) -> bool:
        """
        Проверяет, находится ли позиция внутри вызова функции.
        :param code: Исходный код на языке C.
        :param pos: Позиция в коде.
        :return: True, если позиция внутри вызова функции, False иначе.
        """
        # Ищем вызовы функций
        functions = ['printf', 'puts', 'fwrite', 'write']
        for func in functions:
            # Проверка на вызов функции перед позицией
            matches = [m for m in re.finditer(r'\b' + func + r'\s*\(', code[:pos])]
            for match in reversed(matches):
                # Проверка на то, что вызов функции заканчивается перед позицией
                end_pos = code.find(');', match.end())
                if end_pos != -1 and end_pos <= pos:
                    continue
                # Проверка на то, что \n находится внутри строки функции
                open_quote = code.rfind('"', match.end(), pos)
                close_quote = code.find('"', match.end())
                if open_quote != -1 and close_quote != -1:
                    return True
        return False

    def _count_comments(self) -> float:
        """
        Подсчитывает количество строк с комментариями и вычисляет процент комментариев.
        :return: Процент строк с комментариями.
        """
        in_block_comment = False
        for line in self.code:
            is_comment_line = False
            is_in_quote = False
            if in_block_comment:
                is_comment_line = True
            i = 0
            while i < len(line) - 1:
                # если комментарий внутри строки, он не будет считаться
                if line[i] == '"' and not in_block_comment:
                    is_in_quote = not is_in_quote
                if is_in_quote:
                    i += 1
                    continue

                # ситуации // что угодно дальше, но не /* //
                if not in_block_comment and line[i:i + 2] == '//':
                    if not is_in_quote:
                        is_comment_line = True
                        break
                # ситуации /* не в многострочном комментарии и что угодно дальше
                elif not in_block_comment and line[i:i + 2] == '/*':
                    if not is_in_quote:
                        is_comment_line = True
                        in_block_comment = True
                # ситуации  */ при нахождении в многострочном комментарии и что угодно дальше
                elif in_block_comment and line[i:i + 2] == '*/':
                    in_block_comment = False
                i += 1
            if is_comment_line:
                self.comment_lines += 1

        if self.total_lines > 0:
            return round((self.comment_lines / self.total_lines) * 100)
        else:
            return 0

    def get_comment_percentage(self) -> float:
        """
        Возвращает процент строк с комментариями.
        :return: Процент строк с комментариями.
        """
        return self.comment_percentage
