from app.config import get_settings
from langchain_google_genai import ChatGoogleGenerativeAI

class MemoGenerator:
    def __init__(self):
        settings = get_settings()
        self.llm = ChatGoogleGenerativeAI(
            model = "gemini-2.5-flash",
            google_api_key = settings.GOOGLE_API_KEY,
        )

    def _build_prompt(self, recommendation) -> str:
        action = recommendation.recommended_action
        metrics = recommendation.supporting_metrics

        npv = metrics.get("npv")
        wacc = metrics.get("wacc")
        health_score = metrics.get("health_score")
        interest_coverage = metrics.get("interest_coverage")
        cash_conversion_cycle = metrics.get("cash_conversion_cycle")

        return f"""You are writing a brief executive memo for a CFO, summarizing a capital allocation recommendation.

            Recommendation: {action}

            Supporting data:
            - NPV: {npv}
            - WACC: {wacc}
            - Financial Health Score: {health_score}
            - Interest Coverage: {interest_coverage}
            - Cash Conversion Cycle: {cash_conversion_cycle} days

            Instructions:
            - Write 2-3 sentences explaining WHY this recommendation makes sense, citing the specific numbers above.
            - Use a professional, concise tone appropriate for a CFO audience.
            - Do not invent numbers not provided above.

            Memo:"""

    def generate_memo(self, recommendation) -> str:
        PROMPT = self._build_prompt(recommendation)
        response = self.llm.invoke(PROMPT)
        return response.content 