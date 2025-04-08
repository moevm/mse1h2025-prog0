class CommentMetric:

    def __init__(self, code: str):
        self.code = code.split('\n')
        self.total_lines = len(self.code)
        self.comment_lines = 0
        self.comment_percentage = self._count_comments()

    def _count_comments(self) -> float:
        in_block_comment = False
        for line in self.code:
            if (not in_block_comment and ('//' in line or '/*' in line)) or in_block_comment:
                self.comment_lines += 1

                i = 0
                while i < len(line) - 1:
                    # ситуации // что угодно дальше, но не /* //
                    if not in_block_comment and line[i:i + 2] == '//':
                        break
                    # ситуации /* не в многострочном комментарии и что угодно дальше
                    elif not in_block_comment and line[i:i + 2] == '/*':
                        i += 1
                        in_block_comment = True
                    # ситуации  */ при нахождении в многострочном комментарии и что угодно дальше
                    elif in_block_comment and line[i:i + 2] == '*/':
                        i += 1
                        in_block_comment = False
                    i += 1

        if self.total_lines > 0:
            return round((self.comment_lines / self.total_lines) * 100)
        else:
            return 0

    def get_comment_percentage(self) -> float:
        return self.comment_percentage
