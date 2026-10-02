from app.engine.base_module import FinanceModule,ModuleResult
from typing import Any 

class RatiosModule(FinanceModule):
    module_name = "ratios"

    def safe_divide(self,Numerator,Denominator):
        if Numerator is None or Denominator is None or Denominator == 0:
            return None
        return Numerator/Denominator

    def safe_round(self, value, digits=4):
        return round(value, digits) if value is not None else None

    def compute(self,data:dict[str,Any]) -> dict[str,float]:
        # liquidity
        current_assets = data.get("current_assets")
        current_liabilities = data.get("current_liabilities")
        inventory = data.get("inventory")

        # leverage 
        short_term_debt = data.get("short_term_debt") or 0
        long_term_debt = data.get("long_term_debt") or 0   
        total_debt = short_term_debt + long_term_debt if (short_term_debt or long_term_debt) else data.get("total_debt")
        total_equity = data.get("total_equity")
        ebit = data.get("ebit")
        interest_expense = data.get("interest_expense")

        # efficiency
        accounts_receivable = data.get("accounts_receivable")
        revenue = data.get("revenue")
        cogs = data.get("cogs")
        accounts_payable = data.get("accounts_payable")
        days_in_period = data.get("days_in_period",365)

        # profitability
        gross_profit = data.get("gross_profit")
        operating_income = data.get("operating_income")
        net_income = data.get("net_income")

        # liquidity calculations
        current_ratio = self.safe_divide(current_assets,current_liabilities)
        if current_assets is not None and inventory is not None:
            quick_ratio = self.safe_divide(current_assets - inventory, current_liabilities)
        else:
            quick_ratio = None

        # leverage calculations 
        debt_to_equity = self.safe_divide(total_debt,total_equity)
        interest_coverage = self.safe_divide(ebit,interest_expense)

        # efficiency calculations
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

        #profitabilty calculations
        gross_margin = self.safe_divide(gross_profit,revenue)
        operating_margin = self.safe_divide(operating_income,revenue)
        net_margin = self.safe_divide(net_income,revenue)

        

        return {
            "current_ratio" : self.safe_round(current_ratio),
            "quick_ratio" : self.safe_round(quick_ratio),
            "debt_to_equity" : self.safe_round(debt_to_equity),
            "interest_coverage" : self.safe_round(interest_coverage),
            "dso" : self.safe_round(dso),
            "dio" : self.safe_round(dio),
            "dpo" : self.safe_round(dpo),
            "gross_margin" : self.safe_round(gross_margin),
            "operating_margin" : self.safe_round(operating_margin),
            "net_margin" : self.safe_round(net_margin),
        }
    
                



    
