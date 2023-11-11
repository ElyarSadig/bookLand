
class UsernameAlreadyExistsError(Exception):
    pass


class EmailAlreadyExistsError(Exception):
    pass


class PhoneNumberAlreadyExistsError(Exception):
    pass


class PublicationsNameAlreadyExistsError(Exception):
    pass


class InvalidUserCredentialsError(Exception):
    pass


class EmailDoesNotExistError(Exception):
    pass


class ExpiredCodeError(Exception):
    pass


class InvalidCodeError(Exception):
    pass


class InvalidFileFormatError(Exception):
    pass


class FileUploadFailedError(Exception):
    pass