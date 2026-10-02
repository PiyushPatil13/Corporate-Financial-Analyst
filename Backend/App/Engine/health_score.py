from typing import Any
from app.engine.base_module import ModuleResult, FinanceModule

class HealthScoreModule(FinanceModule):

    module_name = "health_score"
    WEIGHTS = {
        "current_ratio" : 0.15,
        "interest_coverage" : 0.2,
        "debt_to_equity" : 0.20,
        "net_margin" : 0.20,
        "operating_margin" : 0.15,
        "cash_conversion_cycle" : 0.10,

    }

    def safe_divide(self,Numerator,Denominator):
        if Numerator is None or Denominator is None or Denominator == 0:
            return None
        return Numerator/Denominator

    def _score_higher_better(self, value, benchmark):
        if value is None:
            return None
        return min(value / benchmark, 1.0)*100

    def _score_lower_better(self, value, penalty_factor, max_score = 100):
        if value is None:
            return None
        return max(0,max_score - (value * penalty_factor))

    def compute(self, data : dict[str, Any]) -> dict[str,Any]:
        current_assets = data.get("current_assets")
        current_liabilities = data.get("current_liabilities")

        accounts_receivable = data.get("accounts_receivable")
        cogs = data.get("cogs")
        accounts_payable = data.get("accounts_payable")
        days_in_period = data.get("days_in_period",365)
        inventory = data.get("inventory")

        # current ratio
        current_ratio = self.safe_divide(current_assets,current_liabilities)

        ebit = data.get("ebit")
        interest_expense = data.get("interest_expense")

        # interest coverage 
        interest_coverage = self.safe_divide(ebit,interest_expense)

        short_term_debt = data.get("short_term_debt") or 0
        long_term_debt = data.get("long_term_debt") or 0
        total_debt = short_term_debt + long_term_debt if (short_term_debt or long_term_debt) else data.get("total_debt")
        total_equity = data.get("total_equity")

        # debt to equity
        debt_to_equity = self.safe_divide(total_debt,total_equity)

        net_income = data.get("net_income")
        revenue = data.get("revenue")
        net_margin = self.safe_divide(net_income,revenue)

        #operarting margin
        operating_income = data.get("operating_income")
        operating_margin = self.safe_divide(operating_income,revenue)

        # cash conversion cycle
        if self.safe_divide(accounts_receivable,revenue) is not None and days_in_period is not None:
            dso = self.safe_divide(accounts_receivable,revenue)*days_in_period #sales
        else :
            dso = None
        if self.safe_divide(inventory,cogs) is not None and days_in_period is not None:
            dio = self.safe_divide(inventory,cogs)*days_in_period  #inventory
        else :
            dio = None
        if self.safe_divide(accounts_payable,cogs) is not None and days_in_period is not None:
            dpo = self.safe_divide(accounts_payable,cogs)*days_in_period  # payable
        else :
            dpo = None

        if dpo is not None and dio is not None and dso is not None and days_in_period is not None:
            cash_conversion_cycle = dso + dio - dpo
        else:
            cash_conversion_cycle = None

        scores = {
            "current_ratio" : self._score_higher_better(current_ratio, 2.0),
            "interest_coverage" : self._score_higher_better(interest_coverage, 5.0),
            "debt_to_equity" : self._score_lower_better(debt_to_equity, 50),
            "net_margin" : self._score_higher_better(net_margin, 0.15),
            "operating_margin" : self._score_higher_better(operating_margin, 0.20),
            "cash_conversion_cycle" : self._score_lower_better(cash_conversion_cycle, 0.5),
        }

        weighted_sum = 0
        weight_used = 0

        for label, score in scores.items():
            if score is not None:
                weighted_sum += score*self.WEIGHTS[label]
                weight_used += self.WEIGHTS[label]


        final_score = weighted_sum / weight_used if weight_used > 0 else None

        return {
            "financial_health_score" : round(final_score, 2) if final_score is not None else None,
            "component_scores" : {k : round(v , 2)if v is not None else None for k, v in scores.items()}
        }

    

    

        