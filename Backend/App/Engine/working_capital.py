from typing import Any
from app.engine.base_module import FinanceModule , ModuleResult 

class WorkingCapitalModule(FinanceModule):

    module_name = "working_capital"

    def safe_divide(self,Numerator,Denominator):
        if Numerator is None or Denominator is None or Denominator == 0:
            return None
        return Numerator/Denominator

    def safe_round(self, value, digits=4):
        return round(value, digits) if value is not None else None

    def compute(self, data : dict[float,Any] ) -> dict[float,Any] | None:
        days_in_period = data.get("days_in_period")
        accounts_receivable = data.get("accounts_receivable")
        revenue = data.get("revenue")
        cogs = data.get("cogs")
        accounts_payable = data.get("accounts_payable")
        days_in_period = data.get("days_in_period", 365)
        inventory = data.get("inventory")
        current_assets = data.get("current_assets")
        current_liabilities = data.get("current_liabilities")

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

        if dpo is not None and dio is not None and dso is not None:
            cash_conversion_cycle = dso + dio - dpo
        else:
            cash_conversion_cycle = None

        if current_liabilities is not None and current_assets is not None:
            net_working_capital = current_assets - current_liabilities
        else:
            net_working_capital = None

        return {
            "dso" : self.safe_round(dso,2),
            "dio" : self.safe_round(dio,2),
            "dpo" : self.safe_round(dpo,2),
            "cash_conversion_cycle" : self.safe_round(cash_conversion_cycle,2),
            "net_working_capital" : self.safe_round(net_working_capital,2),
        }






    
