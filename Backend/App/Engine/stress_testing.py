from typing import Any
import numpy_financial as npf
from app.engine.base_module import FinanceModule, ModuleResult

class StressTestingModule(FinanceModule):
    module_name = "stress_testing"

    def compute(self, data: dict[str,Any]) -> dict[str, Any]:
        base_cash_flows = data.get("base_cash_flows")
        discount_rate = data.get("discount_rate")
        scenarios = data.get("scenarios", [])

        results = {}

        for scenario in scenarios:
            label = scenario["label"]
            shock_pct = scenario["revenue_shock_pct"]
            multiplier = 1 + (shock_pct/100)
            shocked_flows = [base_cash_flows[0]]

            for flow in base_cash_flows[1:]:
                shocked_flows.append(flow*multiplier)

            npv = npf.npv(discount_rate, shocked_flows)

            results[label] = {
                "shock_pct" : shock_pct,
                "npv" : round(npv, 2),
                "still_profitable" : bool(npv > 0),
            }

        return {"scenario_results": results}

    




    