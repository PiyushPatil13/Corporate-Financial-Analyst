from typing import Any

from app.engine.base_module import FinanceModule, ModuleResult


class GrowthModule(FinanceModule):
    module_name = "growth"

    def safe_divide(self, numerator, denominator):
        if numerator is None or denominator is None or denominator == 0:
            return None
        return numerator / denominator

    def compute(self, data: dict[str, Any]) -> dict[str, Any]:
        current_revenue = data.get("current_revenue")
        previous_revenue = data.get("previous_revenue")
        current_net_income = data.get("current_net_income")
        previous_net_income = data.get("previous_net_income")

        if current_revenue is None or previous_revenue is None:
            revenue_growth = None
        else:
            revenue_growth = self.safe_divide(current_revenue - previous_revenue, previous_revenue)

        if current_net_income is None or previous_net_income is None:
            net_income_growth = None
        else:
            net_income_growth = self.safe_divide(current_net_income - previous_net_income, previous_net_income)

        return {
            "revenue_growth": round(revenue_growth, 4) if revenue_growth is not None else None,
            "net_income_growth": round(net_income_growth, 4) if net_income_growth is not None else None,
        }   