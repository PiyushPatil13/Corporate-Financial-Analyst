from app.config import get_settings
from langchain_google_genai import ChatGoogleGenerativeAI

class MappingAssist:
    def __init__(self):
        settings = get_settings()
        self.llm = ChatGoogleGenerativeAI(
            model = "gemini-2.5-flash",
            google_api_key = settings.GOOGLE_API_KEY,
        )

    def _build_prompt(self, raw_label : str, candidate_labels : list[str]) -> str:
        options = "\n".join(f"- {label}" for label in candidate_labels)
        return f"""You are helping standardize financial statement line-item labels.

                Raw label from a company's financial statement: "{raw_label}"

                Valid standardized categories:
                {options}

                Instructions:
                - Choose the SINGLE best-matching category from the list above.
                - Respond with ONLY the exact category name from the list — no explanation, no punctuation, no extra text.

                Category:"""

    def suggest_label(self,raw_label : str, candidate_labels : list[str]) ->str:
        PROMPT = self._build_prompt(raw_label,candidate_labels)
        response = self.llm.invoke(PROMPT)
        return response.content.strip()