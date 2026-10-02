from abc import ABC,abstractmethod
from dataclasses import dataclass, field
from typing import Any

@dataclass
class ModuleResult:
    module_name : str
    values :dict[str,float] = field(default_factory=dict)
    warnings : list[str] = field(default_factory=list)

class FinanceModule(ABC):
    module_name : str = "base"

    def run(self, data:dict[str,Any]) -> ModuleResult:
        prepared = self.prepare(data)
        raw_values = self.compute(prepared)
        return self.validate(raw_values)

    def prepare(self, data: dict[str,Any]) ->dict[str,Any]:
        return data

    @abstractmethod
    def compute(self, data: dict[str,Any]) -> dict[str,float]:
        raise NotImplementedError

    def validate(self,values: dict[str,float]) -> ModuleResult:
        warnings = [k for k, v in values.items() if v is None]
        return ModuleResult(module_name=self.module_name, values = values,warnings = warnings)

    
