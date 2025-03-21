class PackageGatewayError(Exception):
    def __init__(self, should_try_again: bool, *args: object) -> None:
        self._should_try_again = should_try_again
        super().__init__(*args)

    @property
    def should_try_again(self) -> bool:
        return self._should_try_again


class PackageSendFailed(PackageGatewayError):
    def __init__(self, should_try_again: bool, *args: object) -> None:
        super().__init__(should_try_again, *args)


class PackageDownloadFailed(PackageGatewayError):
    def __init__(self, should_try_again: bool, *args: object) -> None:
        super().__init__(should_try_again, *args)
