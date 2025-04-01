from typing import Any


class ValidationResult:
    def __init__(self, valid: bool, value: Any = None, error_msg: str = None):
        self.valid = valid
        self.value = value
        self.error_msg = error_msg
