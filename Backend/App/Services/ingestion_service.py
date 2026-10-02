from app.ingestion.excel_parser import ExcelParser
from app.ingestion.column_mapper import ColumnMapper
from app.ingestion.validators import StatementValidator
from app.repositories.statement_repository import StatementRepository
from app.repositories.line_item_repository import LineRepository
from app.models.statement import Statement
from app.models.line_item import LineItem
from app.genai.mapping_assist import MappingAssist

class IngestionService: 
    def __init__(self,db):
        self.parser = ExcelParser()
        self.mapper = ColumnMapper()
        self.validator = StatementValidator()
        self.statement_repoy = StatementRepository(db)
        self.line_repo = LineRepository(db)
        self.mapping_assist = MappingAssist()

    def ingest_file(self,file_path:str,company_id,period_end):
        raw_statement = self.parser.parse(file_path)
        statement = self.statement_repoy.create(Statement(
            company_id = company_id,
            statement_type = raw_statement.statement_type,
            period_end = period_end,
            period_label = raw_statement.period_label,
            source_filename = raw_statement.source_filename,
        ))
        saved_items = []
        for raw_item in raw_statement.line_items:
            standardized_label, confidence = self.mapper.map_label(raw_item.raw_label)

            if confidence < 0.6:
                candidate_labels = list(self.mapper.standard_labels.keys())
                standardized_label = self.mapping_assist.suggest_label(raw_item.raw_label, candidate_labels)
                confidence = 1.0

            line_item = self.line_repo.create(LineItem(
                statement_id=statement.id,
                raw_label=raw_item.raw_label,
                standardized_label=standardized_label,
                value=raw_item.value,
                mapping_confidence=confidence,
            ))
            saved_items.append(line_item)

        validation_result = self.validator.validate_balance_sheet(saved_items)
        return statement,validation_result

def ingest_file(self, file_path: str, company_id, period_end):
    raw_statements = self.parser.parse_multi(file_path)
    results = []

    for raw_statement in raw_statements:
        statement = self.statement_repo.create(Statement(
            company_id=company_id,
            statement_type=raw_statement.statement_type,
            period_end=period_end,
            period_label=raw_statement.period_label,
            source_filename=raw_statement.source_filename,
        ))

        saved_items = []
        for raw_item in raw_statement.line_items:
            standardized_label, confidence = self.mapper.map_label(raw_item.raw_label)
            if confidence < 0.6:
                candidate_labels = list(self.mapper.standard_labels.keys())
                standardized_label = self.mapping_assist.suggest_label(raw_item.raw_label, candidate_labels)
                confidence = 1.0

            line_item = self.line_repo.create(LineItem(
                statement_id=statement.id,
                raw_label=raw_item.raw_label,
                standardized_label=standardized_label,
                value=raw_item.value,
                mapping_confidence=confidence,
            ))
            saved_items.append(line_item)

        validation_result = self.validator.validate_balance_sheet(saved_items)
        results.append((statement, validation_result))

    return results