import os
import pandas as pd
from app.ingestion.base_parser import BaseParser, RawStatement, RawLineItem

class ExcelParser(BaseParser):
    def supports(self, file_path: str) -> bool:
        return file_path.lower().endswith((".xlsx",".xls",".csv"))

    def parse(self,file_path : str) -> RawStatement:
        statement_type, period_label = self._infer_metadata(file_path)

        if file_path.lower().endswith(".csv"):
            df = pd.read_csv(file_path,header=None)
        else :
            df = pd.read_excel(file_path,header=None)

        line_items : list[RawLineItem] = []
        for _, row in df.iterrows():
            label = row.iloc[0]
            value = row.iloc[1] if len(row) > 1 else None
            if pd.isna(label) or pd.isna(value):
                continue
            try:
                numeric_value = float(str(value).replace(",","").replace("₹","").strip())
            except (ValueError, TypeError):
                continue
            line_items.append(RawLineItem(raw_label=str(label).strip(), value = numeric_value))

        return RawStatement(
            statement_type=statement_type,
            period_label=period_label,
            line_items=line_items,
            source_filename=os.path.basename(file_path),
        )

    @staticmethod
    def _infer_metadata(file_path : str) -> tuple[str,str] : 
        name = os.path.basename(file_path).lower()
        if "balance" in name :
            stype = "balance_sheet"
        elif "income" in name : 
            stype = "income_statement"
        elif "cash" in name :
            stype = "cash_flow"
        else : 
            stype = "unknown"

        return stype, "unknown_period"

def parse_multi(self, file_path: str) -> list[RawStatement]:
    statement_type, _ = self._infer_metadata(file_path)

    if file_path.lower().endswith(".csv"):
        df = pd.read_csv(file_path, header=None)
    else:
        df = pd.read_excel(file_path, header=None)

    header_row_index, period_labels = self._find_period_header(df)

    if header_row_index is None or len(period_labels) <= 1:
        # not multi-period — fall back to normal single-column parsing
        return [self.parse(file_path)]

    statements = {col: [] for col in period_labels}

    for row_idx in range(header_row_index + 1, len(df)):
        row = df.iloc[row_idx]
        label = row.iloc[0]
        if pd.isna(label):
            continue
        for col_index, period_label in period_labels.items():
            value = row.iloc[col_index]
            if pd.isna(value):
                continue
            try:
                numeric_value = float(str(value).replace(",", "").replace("₹", "").strip())
            except (ValueError, TypeError):
                continue
            statements[col_index].append(RawLineItem(raw_label=str(label).strip(), value=numeric_value))

    return [
        RawStatement(
            statement_type=statement_type,
            period_label=str(period_labels[col_index]).strip(),
            line_items=items,
            source_filename=f"{os.path.basename(file_path)} [{period_labels[col_index]}]",
        )
        for col_index, items in statements.items()
        if items
    ]

@staticmethod
def _find_period_header(df) -> tuple[int | None, dict[int, str]]:
    for row_idx in range(min(10, len(df))):
        row = df.iloc[row_idx]
        period_cols = {}
        for col_idx in range(1, len(row)):
            value = row.iloc[col_idx]
            if pd.isna(value):
                continue
            text = str(value).strip()
            # heuristic: looks like a period label, not a number
            try:
                float(text.replace(",", ""))
                continue  # it's numeric, not a period label
            except ValueError:
                period_cols[col_idx] = text
        if len(period_cols) >= 2:
            return row_idx, period_cols
    return None, {}
                