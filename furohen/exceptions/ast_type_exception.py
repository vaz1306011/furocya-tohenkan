class ASTTypeException(Exception):
    pass


class UnsupportedASTTypeException(ASTTypeException):
    def __init__(self, ast_type: type) -> None:
        self.ast_type = ast_type
        super().__init__(f"\n  Unsupported AST type: {ast_type.__name__}")
