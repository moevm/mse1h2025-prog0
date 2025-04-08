class CommentMetric:

    def __init__(self, code: str):
        self.code = code.split('\n')
        self.total_lines = len(self.code)
        self.comment_lines = 0
        self.comment_percentage = self._count_comments()

    def _count_comments(self) -> float:
        pass

    def get_comment_percentage(self) -> float:
        return self.comment_percentage
