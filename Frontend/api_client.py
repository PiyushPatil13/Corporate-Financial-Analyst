import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"


def _headers():
    return {"Authorization": f"Bearer {st.session_state.get('token', '')}"}


def get(path: str, params: dict = None):
    resp = requests.get(f"{API_URL}{path}", headers=_headers(), params=params)
    return resp.json() if resp.status_code == 200 else None, resp.status_code


def post(path: str, json: dict = None, params: dict = None, files=None):
    resp = requests.post(
        f"{API_URL}{path}",
        headers=_headers(),
        json=json,
        params=params,
        files=files
    )
    return resp.json() if resp.status_code == 200 else None, resp.status_code


def get_companies():
    data, _ = get("/companies")
    return data or []


def get_ratios(statement_id):
    data, _ = get(f"/statements/ratios/{statement_id}")
    return (data or {}).get("ratios", {})


def get_wacc(statement_id):
    data, _ = get(f"/statements/WACC/{statement_id}")
    return (data or {}).get("WACC_VALUES", {})


def get_working_capital(statement_id):
    data, _ = get(f"/statements/Working_Capital/{statement_id}")
    return (data or {}).get("Working_capital_VALUES", {})


def get_health_score(statement_id):
    data, _ = get(f"/statements/health_score/{statement_id}")
    return data or {}


def get_recommendation(statement_id):
    data, _ = get(f"/statements/Recommendation/{statement_id}")
    return data


def get_line_items(statement_id):
    data, _ = get(f"/statements/line_items/{statement_id}")
    return data or []


def get_company_statements(company_id):
    data, _ = get(f"/companies/{company_id}/statements")
    return data or []

def get_recommendation_memo(statement_id):
    data, _ = get(f"/statements/recommendation/{statement_id}/memo")
    return (data or {}).get("memo")

def get_npv_profile(cash_flows, rate_start=0.0, rate_end=0.30, rate_step=0.02):
    result, status = post(
        "/statements/capital_budgeting/npv_profile",
        json={"cash_flows": cash_flows, "rate_start": rate_start, "rate_end": rate_end, "rate_step": rate_step},
    )
    return result if status == 200 else None

def get_monte_carlo(cash_flows, discount_rate, num_simulations=5000, volatility=0.15):
    result, status = post("/statements/scenarios/monte-carlo", json={
        "base_cash_flows": cash_flows, "discount_rate": discount_rate,
        "num_simulations": num_simulations, "volatility": volatility,
    })
    return result if status == 200 else None

def run_stress_test(cash_flows, discount_rate, scenarios):
    result, status = post("/statements/scenarios/stress-test", json={
        "base_cash_flows": cash_flows, "discount_rate": discount_rate, "scenarios": scenarios,
    })
    return (result or {}).get("scenario_results")

def ask_copilot(company_id, statement_id, question):
    result, status = post(f"/companies/{company_id}/copilot", json={"question": question, "statement_id": statement_id})
    return (result or {}).get("answer") if status == 200 else None