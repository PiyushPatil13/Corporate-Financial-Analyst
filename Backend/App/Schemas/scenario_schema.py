from pydantic import BaseModel


class ScenarioInput(BaseModel):
    label: str
    revenue_shock_pct: float


class StressTestRequest(BaseModel):
    base_cash_flows: list[float]
    discount_rate: float
    scenarios: list[ScenarioInput]