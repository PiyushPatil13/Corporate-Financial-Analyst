import os
import pdfplumber
import pandas as pd
from app.ingestion.base_parser import BaseParser,RawLineItem,RawStatement

class PdfParser(BaseParser):
    def supports(self,file_path:str) -> bool:
        return file_path.lower().endswith(".pdf")

    def parse(self, file_path : str) -> RawStatement:
        statement_type, period_label = self._infer_metadata(file_path)
        line_items : list[RawLineItem] = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_table()
                if tables is None:
                    continue
                for i in tables:
                    label = i[0]
                    value = i[1] if len(i) > 1 else None
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

    def extract_narrative_text(self, file_path: str) -> str:
        all_text = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    all_text.append(text)
        return "\n\n".join(all_text) 


            
