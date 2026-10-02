from rapidfuzz import process

STANDARD_LABELS = {
    "accounts_receivable" : ["accounts receivable","trave receivables","sundry debtors","debtors"],
    "accounts_payable" : ["accounts payable","trade payables","sundry creditors","creditors"],
    "cash_and_equivalents" : ["cash and cash equivalents","cash","cash in hand"],
    "assets" : ["total_assets","current_assets","non_current_assets","cash","accounts receivables","prepaid_expenses","goodwill"],
    "inventory" : ["inventory","beginning_inventory","ending_inventory","average_inventory","inventory_turnover","inventory_growth","inventory_write_down","days_inventory_outstanding"],
    "total_assets": ["total assets", "total_assets"],
    "total_liabilities": ["total liabilities", "total_liabilities"],
    "total_equity": ["total equity", "shareholders equity", "share capital and reserves", "net worth"],
    "current_assets": ["current assets", "total current assets"],
    "current_liabilities": ["current liabilities", "total current liabilities"],
    "short_term_debt": ["short term borrowings", "short-term debt", "current borrowings"],
    "long_term_debt": ["long term debt", "long-term borrowings", "non-current borrowings"],
    "total_equity": ["total equity", "shareholders equity", "share capital and reserves"],
    "market_cap": ["market capitalization", "market cap"],
    "revenue": ["total revenue", "net sales", "revenue from operations", "sales"],
    "cogs": ["cost of goods sold", "cost of sales", "cost of revenue"],
    "ebit": ["ebit", "operating profit", "profit before interest and tax"],
    "interest_expense": ["interest expense", "finance costs", "interest paid"],
    "gross_profit": ["gross profit"],
    "operating_income": ["operating income", "operating profit"],
    "net_income": ["net income", "net profit", "profit after tax", "pat"],
    }

all_variants = [variant for variants in STANDARD_LABELS.values() for variant in variants]
variant_to_standard = {
    variant: standardized_label
    for standardized_label, variants in STANDARD_LABELS.items()
    for variant in variants
}

class ColumnMapper:
    def __init__(self):
        self.standard_labels = STANDARD_LABELS
        self.all_variants = all_variants
        self.variant_to_standard = variant_to_standard


    def map_label(self,raw_Label : str) -> tuple[str,float]:
        result = process.extractOne(raw_Label,self.all_variants)
        matched_variant, score, index = result
        standardized_label = self.variant_to_standard[matched_variant]
        return standardized_label,score/100
