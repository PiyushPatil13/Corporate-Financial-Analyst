from app.engine.base_module import ModuleResult,FinanceModule
from typing import Any

class WACCModule(FinanceModule):
    module_name = "wacc"

    def compute(self,data:dict[str,Any]) -> dict[str,float]:
        short_term_debt = data.get("short_term_debt") or 0
        long_term_debt = data.get("long_term_debt") or 0
        total_debt = short_term_debt + long_term_debt if (short_term_debt or long_term_debt) else data.get("total_debt")
        market_cap = data.get("market_cap")
        interest_expense = data.get("interest_expense")
        tax_rate = data.get("effective_tax_rate",0.25)
        beta = data.get("beta",1.0)
        risk_free_rate = data.get("risk_free_rate",0.071)
        market_return = data.get("market_return",0.12)
        if total_debt is None or market_cap is None or interest_expense is None:
            return {"wacc": None, "cost_of_equity": None, "cost_of_debt_after_tax": None}
        market_risk_premium = market_return-risk_free_rate
        total_value = total_debt + market_cap
        if total_value == 0:
            return {"wacc":None,"cost_of_equity":None,"cost_of_debt_after_tax":None}
        cost_of_equity = risk_free_rate + beta*(market_risk_premium)

        cost_of_debt_pretax = interest_expense / total_debt if total_debt > 0 else 0.0
        cost_of_debt_after_tax = cost_of_debt_pretax*(1-tax_rate)

        weight_equity = market_cap/total_value
        weight_debt = total_debt/total_value

        wacc = weight_equity*cost_of_equity + weight_debt*cost_of_debt_after_tax

        return {
            "wacc" : round(wacc,4),
            "cost_of_equity" : round(cost_of_equity, 4),
            "cost_of_debt_after_tax" : round(cost_of_debt_after_tax,4),
            "weight_equity" : round(weight_debt,4),
        }

    def validate(self, values: dict[str,float]) -> ModuleResult:
        result = super().validate(values)
        wacc = values.get("wacc")
        if wacc is not None and (wacc < 0 or wacc > 0.5):
            result.warnings.append(
                f"WACC of {wacc:.1%} is outside a plausible range — check inputs (beta, debt, interest expense)."
            )
        return result

    

    