from pydantic import BaseModel

class CopilotQuestion(BaseModel):
    question: str
    statement_id: str | None = None