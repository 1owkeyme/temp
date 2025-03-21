class ServiceError(Exception):
    pass


class PackageNotFound(ServiceError):
    def __init__(self, package_id: str, *args: object) -> None:
        message = f"Package `{package_id}` not found"
        super().__init__(message, *args)


class FileNotFound(ServiceError):
    def __init__(self, file_id: str, *args: object) -> None:
        message = f"File `{file_id}` not found"
        super().__init__(message, *args)


class IncompletePackageSend(ServiceError):
    pass
