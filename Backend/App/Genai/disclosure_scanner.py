from app.config import get_settings
from langchain_google_genai import ChatGoogleGenerativeAI

class DisclosureScanner:
    def __init__(self):
        settings = get_settings()
        self.llm = ChatGoogleGenerativeAI(
            model = "gemini-2.5-flash",
            google_api_key = settings.GOOGLE_API_KEY,
        )

    def _build_prompt(self, narrative_text : str) -> str:
        return f"""
        You are a financial analyst reviewing the notes and management discussion section of a company's annual report for risk disclosures.

            Text to review:
            {narrative_text}

            Look for mentions of the following risk categories:
            - Contingent liabilities
            - Related-party transactions
            - Going-concern language
            - Pending litigation

            Instructions:
            - For EACH disclosure you find, quote the relevant sentence and state which category it belongs to.
            - If you find no disclosures in any category, say "No risk disclosures found."
            - Do not invent or infer risks not explicitly stated in the text.

            Findings:  """

    def scan(self, narrative_text : str) -> str:
        PROMPT = self._build_prompt(narrative_text)
        response = self.llm.invoke(PROMPT)
        return response.content