from numpy_financial import npv
import numpy_financial
from app.engine.base_module import FinanceModule,ModuleResult
from typing import Any

class CapitalBudgetingModule(FinanceModule):
    module_name = "capital_budgeting"

    def compute(self,data:dict[str,Any]) -> dict[str,Any]:
        cash_flows = data.get("cash_flows")
        discount_rate = data.get("discount_rate")
        if cash_flows is None or discount_rate is None:
            return {"npv": None, "irr": None, "payback_period_years": None}
        npv_value = numpy_financial.npv(discount_rate,cash_flows)

        try:
            irr_value = numpy_financial.irr(cash_flows)
        except Exception:
            irr_value = None

        payback = self._payback_period(cash_flows)

        return {
            "npv" : round(npv_value, 2),
            "irr" : round(irr_value, 4) if irr_value is not None else None,
            "payback_period_years" : payback,
        }

    def _payback_period(self,cash_flows : list[float]) -> float | None:
        cumulative = 0.0
        for year,flow in enumerate(cash_flows):
            cumulative += flow
            if(cumulative>=0):
                previous_cumulative = cumulative - flow
                fraction = -previous_cumulative / flow if flow !=0 else 0
                return round(year - 1 + fraction,2) if year > 0 else 0.0

        return None

        

        

