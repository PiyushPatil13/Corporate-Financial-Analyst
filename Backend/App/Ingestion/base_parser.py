from abc import ABC, abstractmethod
from dataclasses import dataclass, field

@dataclass
class RawLineItem:
    raw_label : str
    value : float

@dataclass # will generate the __init__ now we don't have to 
class RawStatement:
    statement_type : str
    period_label : str
    line_items : list[RawLineItem] = field(default_factory=list)
    source_filename : str = ""

class BaseParser(ABC):
    @abstractmethod
    def parse(self, file_path: str) -> RawStatement:
        raise NotImplementedError
    def supports(self, file_path: str) -> bool:
        return False

class BaseParser(ABC):
    @abstractmethod
    def parse(self, file_path: str) -> RawStatement:
        raise NotImplementedError

    def parse_multi(self, file_path: str) -> list[RawStatement]:
        """Default: treat as single-period, wrap parse() in a list.
        Override in parsers that can detect multiple period columns."""
        return [self.parse(file_path)]

    def supports(self, file_path: str) -> bool:
        return False
    