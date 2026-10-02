from fastapi import FastAPI
from app.config import get_settings
from app.api import routes_upload
from app.models import company, statement, line_item, ratio_snapshot, scenario, recommendation, user, copilot_session
from app.api import routes_ratios
from app.api import routes_capital_budgeting
from app.api import routes_wacc
from app.api import routes_working_capital
from app.api import routes_scenarios
from app.api import routes_recommendation
from app.api import routes_copilot
from app.api import routes_auth
from app.api import routes_auth
from app.api import routes_companies
from app.api import routes_health_score


settings = get_settings()

app = FastAPI(title=settings.APP_NAME)

app.include_router(routes_upload.router, prefix="/statements", tags=["ingestion"])
app.include_router(routes_ratios.router, prefix="/statements", tags=["analytics"])
app.include_router(routes_capital_budgeting.router, prefix="/statements", tags=["analytics"])
app.include_router(routes_wacc.router, prefix="/statements", tags=["analytics"])
app.include_router(routes_working_capital.router, prefix="/statements", tags=["analytics"])
app.include_router(routes_scenarios.router, prefix="/statements", tags=["analytics"])
app.include_router(routes_recommendation.router, prefix="/statements", tags=["analytics"])
app.include_router(routes_copilot.router, tags=["copilot"])
app.include_router(routes_auth.router, tags=["auth"])
app.include_router(routes_companies.router, tags=["companies"])
app.include_router(routes_health_score.router, prefix="/statements", tags=["analytics"])


@app.get("/health")
def health_check():
    return {
        "status" : "ok",
        "env" : settings.ENV
    }

