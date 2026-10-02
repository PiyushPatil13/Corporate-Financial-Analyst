from dataclasses import dataclass, field

@dataclass
class ValidationResult : 
    is_valid : bool
    errors : list[str] = field(default_factory=list)
    warnings : list[str] = field(default_factory=list)


class StatementValidator:
    def __init__(self):
        pass

    def _get_value(self,line_items:list,label: str) ->float | None:
        for item in line_items:
            if item.standardized_label == label:
                return item.value

        return None
        
    def validate_balance_sheet(self,line_items:list) -> ValidationResult:
        errors = []
        warnings = []

        total_assets = self._get_value(line_items,"total_assets")
        total_liabilities = self._get_value(line_items,"total_liabilities")
        total_equity = self._get_value(line_items,"total_equity")

        if(total_assets==None):
            errors.append("Can't Validate without this")
        if(total_liabilities==None):
            errors.append("Can't Validate without this")
        if(total_equity==None):
            errors.append("Can't Validate without this")

        if total_assets is not None and total_liabilities is not None and total_equity is not None:
            assets = total_liabilities + total_equity
            if abs(assets - total_assets) / total_assets >= 0.01:
                errors.append(f"Assets ({total_assets}) do not equal Liabilities + Equity ({assets})")

        is_valid = len(errors) == 0
        return ValidationResult(is_valid=is_valid,errors=errors,warnings=warnings)

    
