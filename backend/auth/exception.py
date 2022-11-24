class IncorrectEmailOrPasswordError(RuntimeError):
    pass


class EmailAlreadyRegisteredError(RuntimeError):
    pass


class UserNotFoundError(RuntimeError):
    pass
