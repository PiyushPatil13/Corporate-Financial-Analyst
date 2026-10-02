from typing import Any 
from app.engine.base_module import ModuleResult, FinanceModule
from app.engine.wacc import WACCModule
from app.engine.capital_budgeting import CapitalBudgetingModule
from app.engine.working_capital import WorkingCapitalModule
from app.engine.health_score import HealthScoreModule

class RecommendationModule(FinanceModule):

    module_name = "recommendation"

    def __init__(self):
        self.wacc_module = WACCModule()
        self.capital_budgeting_module = CapitalBudgetingModule()
        self.workng_capital_module = WorkingCapitalModule()
        self.health_score_module = HealthScoreModule()

    def compute(self, data:dict[str, Any]) -> dict[str, Any]:
        wacc_result = self.wacc_module.run(data)
        capital_budgeting_result = self.capital_budgeting_module.run(data)
        working_capital_result = self.workng_capital_module.run(data)
        health_score_result = self.health_score_module.run(data)
        if capital_budgeting_result.values.get("npv") is not None:
            npv = capital_budgeting_result.values.get("npv")
        else :
            npv = None
        health_score = health_score_result.values.get("financial_health_score")
        if data.get("interest_coverage") is not None:
            interest_coverage = data.get("interest_coverage")
        else:
            interest_coverage = None

        action = ""
        if interest_coverage is not None and interest_coverage < 2.0:
            action = "debt_paydown"
        elif npv is not None and health_score is not None and npv > 0 and health_score > 70 : 
            action = "reinvest"

        elif health_score is not None and health_score < 50:
            action = "build_reserves"
        
        else:
            action = "dividend"

        return {
            "recommended_action" : action,
            "npv" : npv,
            "health_score" : health_score,
            "interest_coverage" : interest_coverage,
            "wacc" : wacc_result.values.get("wacc"),
            "cash_conversion_cycle" : working_capital_result.values.get("cash_conversion_cycle"),
        }

    
