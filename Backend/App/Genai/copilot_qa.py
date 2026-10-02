from app.genai.embeddings import EmbeddingService
from app.genai.vector_store import VectorStore
from app.config import get_settings
from langchain_google_genai import ChatGoogleGenerativeAI

class CopilotQA:
    def __init__(self, vector_store : VectorStore):
        settings = get_settings()
        self.embedder = EmbeddingService()
        self.vector_store = vector_store
        self.llm = ChatGoogleGenerativeAI(
            model = "gemini-2.5-flash",
            google_api_key = settings.GOOGLE_API_KEY,
        )

    def build_prompt(self, question : str , context_texts : list[str]) -> str:
        context = "\n".join(f"- {text}" for text in context_texts)
        return f"""You are a financial analysis assistant helping interpret a company's financial data.

                Context (retrieved financial facts about this company):
                {context}

                Question: {question}

                Instructions:
                - Answer using ONLY the context provided above.
                - If the context doesn't contain enough information to answer confidently, say so explicitly rather than guessing.
                - Keep the answer concise and grounded in the specific numbers/facts given.

                Answer:"""

    def ask(self, question : str, top_k : int = 10) -> str:
        embedded_question = self.embedder.embed_text(question)
        context = self.vector_store.search(embedded_question,top_k=top_k)
        PROMPT = self.build_prompt(question, context)
        response = self.llm.invoke(PROMPT)
        print("\nQUESTION:", question)
        print("RETRIEVED CONTEXT:")
        for i, item in enumerate(context, 1):
            print(f"{i}. {item}")

        PROMPT = self.build_prompt(question, context)
        response = self.llm.invoke(PROMPT)
        return response.content 
