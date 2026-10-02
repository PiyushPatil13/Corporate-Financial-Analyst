from fastapi import APIRouter
from app.engine.stress_testing import StressTestingModule
from pydantic import BaseModel
from app.schemas.scenario_schema import StressTestRequest

router = APIRouter()

@router.post("/scenarios/stress-test")
def run_stress_test(request: StressTestRequest):
    module = StressTestingModule()
    data = {
        "base_cash_flows" : request.base_cash_flows,
        "discount_rate" : request.discount_rate,
        "scenarios" : [
            {"label" : s.label, "revenue_shock_pct" : s.revenue_shock_pct}
            for s in request.scenarios
        ],
    }
    result = module.run(data)
    return {
        "scenario_results" : result.values.get("scenario_results"),
        "warnings" : result.warnings,
    }

from pydantic import BaseModel
from app.engine.monte_carlo import MonteCarloModule

class MonteCarloRequest(BaseModel):
    base_cash_flows: list[float]
    discount_rate: float
    num_simulations: int = 5000
    volatility: float = 0.15

@router.post("/scenarios/monte-carlo")
def run_monte_carlo(request: MonteCarloRequest):
    module = MonteCarloModule()
    data = {
        "base_cash_flows": request.base_cash_flows,
        "discount_rate": request.discount_rate,
        "num_simulations": request.num_simulations,
        "volatility": request.volatility,
    }
    result = module.run(data)
    return result.values
