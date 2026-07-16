from dataclasses import dataclass
from typing import Any


@dataclass
class ValidationResult:
    name: str
    passed: bool
    details: Any