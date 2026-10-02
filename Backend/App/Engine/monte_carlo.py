import numpy as np
import numpy_financial as npf
from typing import Any
from app.engine.base_module import FinanceModule, ModuleResult

class MonteCarloModule(FinanceModule):
    module_name = "monte_carlo"

    def compute(self, data : dict[str, Any]) -> dict[str, Any]:
        base_cash_flows = data.get("base_cash_flows")
        discount_rate = data.get("discount_rate")
        num_simulations =  data.get("num_simulations",10000)
        volatility = data.get("volatility",0.15)

        npv_results = []

        if base_cash_flows is None or discount_rate is None:
            return {"mean_npv": None, "median_npv": None, "p5_npv": None, "p95_npv": None, "probability_positive_npv": None}

        for _ in range(num_simulations):
            randomized_flows = [base_cash_flows[0]] # initial outlay stays fixed, no uncertainty
            for flow in base_cash_flows[1:]:
                random_factor = np.random.normal(1.0, volatility)
                randomized_flows.append(flow*random_factor)

            npv = npf.npv(discount_rate, randomized_flows)
            npv_results.append(npv)

            npv_results = []
        all_paths = []  # NEW — one path (list of cumulative values) per simulation

        for _ in range(num_simulations):
            randomized_flows = [base_cash_flows[0]]
            for flow in base_cash_flows[1:]:
                random_factor = np.random.normal(1.0, volatility)
                randomized_flows.append(flow * random_factor)

            npv = npf.npv(discount_rate, randomized_flows)
            npv_results.append(npv)

            # NEW — build the cumulative path for this simulation
            cumulative = 0
            path = []
            for flow in randomized_flows:
                cumulative += flow
                path.append(round(cumulative, 2))
            all_paths.append(path)

        return {
            "mean_npv": round(float(np.mean(npv_results)), 2),
            "median_npv": round(float(np.median(npv_results)), 2),
            "p5_npv": round(float(np.percentile(npv_results, 5)), 2),
            "p95_npv": round(float(np.percentile(npv_results, 95)), 2),
            "probability_positive_npv": round(
                sum(1 for x in npv_results if x > 0) / len(npv_results), 4
            ),
            "sample_paths": all_paths[:200],  # cap at 200 lines so the chart stays readable and the payload stays light
        }

