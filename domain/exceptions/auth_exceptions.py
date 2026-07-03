# domain/exceptions/auth_exceptions.py
class DomainException(Exception):
    """Exceção base para regras de negócio violadas."""
    pass

class InvalidTokenException(DomainException):
    pass

class UserNotFoundException(DomainException):
    pass

class UserAlreadyVerifiedException(DomainException):
    pass