from app.repositories.recommendation_repository import RecommendationRepository
from app.genai.embeddings import EmbeddingService
from app.genai.vector_store import VectorStore
from app.genai.copilot_qa import CopilotQA
from app.repositories.line_item_repository import LineRepository

class CopilotService:
    def __init__(self, db):
        self.recommendation_repo = RecommendationRepository(db)
        self.line_repo = LineRepository(db)
        self.embedder = EmbeddingService()

    def ask(self, company_id: str, statement_id: str, question: str) -> str | None:
        recommendations = self.recommendation_repo.get_recommendation_by_company(company_id)
        if not recommendations:
            return None

        store = VectorStore()

        for rec in recommendations:
            metrics = rec.supporting_metrics or {}
            facts = [
                f"Recommended action: {rec.recommended_action}",
                f"Financial health score: {metrics.get('health_score', 'not available')}",
                f"WACC: {metrics.get('wacc', 'not available')}",
                f"NPV: {metrics.get('npv', 'not available')}",
                f"Cash conversion cycle: {metrics.get('cash_conversion_cycle', 'not available')} days",
            ]
            for fact in facts:
                store.add(fact, self.embedder.embed_text(fact))

        if statement_id:
            print("COPILOT STATEMENT ID:", statement_id)

            items = self.line_repo.get_by_statement(statement_id)

            print("COPILOT ITEMS FOUND:", len(items))

            for item in items:
                fact = f"{item.standardized_label.replace('_', ' ').title()}: {item.value}"
                print("COPILOT ADDING:", fact)

                store.add(
                    fact,
                    self.embedder.embed_text(fact)
                )

        qa = CopilotQA(store)
        return qa.ask(question)