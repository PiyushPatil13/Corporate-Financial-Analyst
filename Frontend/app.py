import streamlit as st
import requests
import api_client as api
import base64
from pathlib import Path
from components.live_market import render_market
from components.ratio_analytics import render
from components.executive_pulse import render_health
from components.capital_budget import render_capital_budget
from components.wacc_optimizer import render_wacc
from components.stress_monte_carlo import render_monte_carlo
from components.copilot_workspace import render_copilot

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Corp Finance Decision Engine",
    layout="wide",
    page_icon="📈"
)

BACKGROUND_PATH = Path(
    r"C:\Users\Lenovo\Downloads\Gemini_Generated_Image_3a6m7d3a6m7d3a6m.png"
)

def load_background():
    if not BACKGROUND_PATH.exists():
        return ""
    with open(BACKGROUND_PATH, "rb") as f:
        return base64.b64encode(f.read()).decode()

bg_image = load_background()

st.markdown(
    f"""
    <style>
    @import url(
        'https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap'
    );

    html,
    body,
    [class*="css"] {{
        font-family: 'Inter', sans-serif;
    }}

    .stApp {{
        background-color: #030811;
        background-image:
            linear-gradient(
                rgba(3, 9, 17, 0.72),
                rgba(3, 9, 17, 0.91)
            )
            {f', url("data:image/png;base64,{bg_image}")' if bg_image else ''};
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        color: #E6EDF5;
    }}

    header[data-testid="stHeader"] {{
        background: rgba(3, 8, 16, 0.45);
        height: 2.8rem;
    }}

    #MainMenu {{
        visibility: hidden;
    }}

    footer {{
        visibility: hidden;
    }}

    .block-container {{
        padding-top: 1.2rem !important;
        padding-bottom: 2rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
    }}

    .app-title {{
        display: flex;
        align-items: center;
        padding: 13px 18px;
        margin-bottom: 12px;
        background:
            linear-gradient(
                135deg,
                rgba(27, 42, 56, 0.94),
                rgba(7, 14, 23, 0.96)
            );
        border: 1px solid
            rgba(137, 160, 183, 0.28);
        border-radius: 4px;
        box-shadow:
            0 10px 30px rgba(0,0,0,0.35),
            inset 0 1px 0 rgba(255,255,255,0.04);
    }}

    .app-title-main {{
        color: #ECF3FA;
        font-size: 17px;
        font-weight: 600;
        letter-spacing: 0.2px;
    }}

    .app-title-sub {{
        margin-left: 18px;
        color: #708196;
        font-size: 9px;
        letter-spacing: 1px;
        text-transform: uppercase;
    }}

    .live-indicator {{
        margin-left: auto;
        font-size: 9px;
        color: #55D59D;
        letter-spacing: 0.8px;
    }}

    .live-dot {{
        display: inline-block;
        width: 6px;
        height: 6px;
        margin-right: 5px;
        border-radius: 50%;
        background: #55D59D;
        box-shadow:
            0 0 8px rgba(85,213,157,0.65);
    }}

    section[data-testid="stSidebar"] {{
        background:
            linear-gradient(
                180deg,
                rgba(11, 21, 32, 0.97),
                rgba(4, 10, 18, 0.98)
            );
        border-right:
            1px solid
            rgba(130, 153, 177, 0.20);
        box-shadow:
            8px 0 30px rgba(0,0,0,0.25);
    }}

    section[data-testid="stSidebar"] > div {{
        padding-top: 1.2rem;
    }}

    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {{
        color: #DCE6F0;
        font-size: 13px;
        font-weight: 600;
    }}

    section[data-testid="stSidebar"] label {{
        color: #7F91A5 !important;
        font-size: 9px !important;
        text-transform: uppercase;
        letter-spacing: 0.6px;
    }}

    div[data-baseweb="input"] {{
        background:
            rgba(4, 11, 19, 0.82);
        border-radius: 3px;
    }}

    input {{
        color: #DDE7F1 !important;
        font-size: 11px !important;
    }}

    div[data-baseweb="input"] > div {{
        background:
            rgba(4, 11, 19, 0.78) !important;
        border:
            1px solid
            rgba(117, 142, 166, 0.28) !important;
        border-radius: 3px !important;
    }}

    div[data-baseweb="input"] > div:focus-within {{
        border-color:
            rgba(77, 210, 157, 0.65) !important;
        box-shadow:
            0 0 0 1px
            rgba(77, 210, 157, 0.10) !important;
    }}

    div[data-baseweb="select"] > div {{
        background:
            rgba(4, 11, 19, 0.82) !important;
        border:
            1px solid
            rgba(117, 142, 166, 0.28) !important;
        border-radius: 3px !important;
        color: #DDE7F1 !important;
    }}

    .stButton > button {{
        background:
            linear-gradient(
                180deg,
                rgba(42, 63, 79, 0.92),
                rgba(18, 30, 42, 0.95)
            );
        color: #BFCBD8;
        border:
            1px solid
            rgba(123, 149, 174, 0.28);
        border-radius: 3px;
        font-size: 10px;
        font-weight: 500;
        transition: all 0.15s ease;
    }}

    .stButton > button:hover {{
        border-color:
            rgba(84, 213, 157, 0.55);
        color: #E7F5EF;
        background:
            linear-gradient(
                180deg,
                rgba(48, 73, 91, 0.95),
                rgba(22, 39, 53, 0.98)
            );
        box-shadow:
            0 0 14px
            rgba(70, 207, 153, 0.10);
    }}

    button[kind="primary"] {{
        background:
            linear-gradient(
                180deg,
                #327E65,
                #225A48
            ) !important;
        border:
            1px solid
            rgba(88, 215, 162, 0.55) !important;
        color: #F1FAF6 !important;
    }}

    button[kind="primary"]:hover {{
        background:
            linear-gradient(
                180deg,
                #3C9678,
                #286C55
            ) !important;
    }}

    button[data-baseweb="tab"] {{
        background:
            rgba(11, 20, 30, 0.72);
        border:
            1px solid
            rgba(112, 137, 161, 0.18);
        border-bottom: none;
        color: #718397;
        font-size: 10px;
        font-weight: 500;
        padding: 9px 15px;
    }}

    button[data-baseweb="tab"]:hover {{
        color: #C7D4E1;
    }}

    button[data-baseweb="tab"][aria-selected="true"] {{
        color: #55D59D;
        background:
            rgba(28, 45, 58, 0.92);
        border-top:
            1px solid
            rgba(82, 211, 155, 0.60);
        box-shadow:
            inset 0 2px 0
            rgba(82, 211, 155, 0.12);
    }}

    div[data-baseweb="tab-highlight"] {{
        background: #55D59D !important;
        height: 1px !important;
    }}

    div[data-testid="stVerticalBlockBorderWrapper"] {{
        background:
            linear-gradient(
                145deg,
                rgba(24, 38, 51, 0.88),
                rgba(6, 14, 23, 0.91)
            );
        border:
            1px solid
            rgba(122, 148, 173, 0.20);
        border-radius: 4px;
    }}

    div[data-testid="stAlert"] {{
        background:
            linear-gradient(
                145deg,
                rgba(25, 40, 54, 0.92),
                rgba(7, 15, 24, 0.94)
            );
        border:
            1px solid
            rgba(109, 139, 166, 0.22);
        border-radius: 4px;
        color: #9DAFC1;
        font-size: 11px;
    }}

    .auth-card {{
        background:
            linear-gradient(
                145deg,
                rgba(26, 41, 54, 0.92),
                rgba(5, 13, 22, 0.96)
            );
        border:
            1px solid
            rgba(139, 162, 184, 0.28);
        border-radius: 5px;
        padding: 28px;
        box-shadow:
            0 20px 60px
            rgba(0,0,0,0.50),
            inset 0 1px 0
            rgba(255,255,255,0.04);
    }}

    .terminal-strip {{
        display: flex;
        align-items: center;
        gap: 28px;
        padding: 8px 13px;
        margin-bottom: 10px;
        background:
            rgba(5, 13, 21, 0.88);
        border:
            1px solid
            rgba(116, 141, 164, 0.18);
        color: #687B8F;
        font-size: 8px;
        letter-spacing: 0.5px;
    }}

    .terminal-green {{
        color: #55D59D;
    }}

    .terminal-red {{
        color: #E06B6B;
    }}

    div[data-testid="stExpander"] {{
        background:
            rgba(8, 16, 25, 0.65);
        border:
            1px solid
            rgba(115, 140, 164, 0.20);
        border-radius: 4px;
    }}

    ::-webkit-scrollbar {{
        width: 6px;
        height: 6px;
    }}

    ::-webkit-scrollbar-track {{
        background: #050C14;
    }}

    ::-webkit-scrollbar-thumb {{
        background: #273848;
        border-radius: 4px;
    }}

    ::-webkit-scrollbar-thumb:hover {{
        background: #385064;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

if "token" not in st.session_state:
    st.session_state.token = None

if "show_signup" not in st.session_state:
    st.session_state.show_signup = False

if st.session_state.token is None:
    st.markdown(
        """
        <div class="terminal-strip">
            <span>CORP-FINANCE DECISION ENGINE</span>
            <span>SECURE AUTHENTICATION</span>
            <span class="terminal-green">● SYSTEM ONLINE</span>
            <span>
                MARKET DATA
                <span class="terminal-green">LIVE</span>
            </span>
            <span>
                NDE-2
                <span class="terminal-red">▼ -0.15%</span>
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    left, center, right = st.columns([1.25, 1, 1.25])

    with center:
        st.markdown(
        '<div class="auth-card">'
        '<div style="color:#718397; font-size:9px; letter-spacing:1.8px; text-transform:uppercase; margin-bottom:10px;">Corporate Finance Terminal</div>'
        '<div style="color:#EDF4FA; font-size:25px; font-weight:600; line-height:1.2; margin-bottom:8px;">Corp-Finance<br>Decision Engine</div>'
        '<div style="color:#7F91A4; font-size:10px; line-height:1.6; margin-bottom:22px;">Financial analysis, valuation and decision intelligence.</div>'
        '<div style="color:#55D59D; font-size:8px; letter-spacing:.8px;">● SECURE ANALYTICS ENVIRONMENT</div>'
        '</div>',
        unsafe_allow_html=True
    )

        st.write("")

        if st.session_state.show_signup:
            full_name = st.text_input(
                "Full name",
                placeholder="Full name"
            )

            email = st.text_input(
                "Email",
                placeholder="Email address"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Password"
            )

            if st.button(
                "CREATE ACCOUNT",
                type="primary",
                use_container_width=True
            ):
                resp = requests.post(
                    f"{API_URL}/auth/signup",
                    json={
                        "email": email,
                        "password": password,
                        "full_name": full_name
                    }
                )

                if resp.status_code == 200:
                    st.session_state.token = (
                        resp.json()["access_token"]
                    )
                    st.rerun()
                else:
                    st.error(
                        resp.json().get(
                            "detail",
                            "Signup failed"
                        )
                    )

            if st.button(
                "← Have an account? Log in",
                use_container_width=True
            ):
                st.session_state.show_signup = False
                st.rerun()

        else:
            email = st.text_input(
                "Email",
                placeholder="Email address"
            )

            password = st.text_input(
                "Password",
                type="password",
                placeholder="Password"
            )

            if st.button(
                "LOG IN",
                type="primary",
                use_container_width=True
            ):
                resp = requests.post(
                    f"{API_URL}/auth/login",
                    data={
                        "username": email,
                        "password": password
                    }
                )

                if resp.status_code == 200:
                    st.session_state.token = (
                        resp.json()["access_token"]
                    )
                    st.rerun()
                else:
                    st.error(
                        "Invalid email or password"
                    )

            if st.button(
                "Need an account? Sign up →",
                use_container_width=True
            ):
                st.session_state.show_signup = True
                st.rerun()

    st.stop()

st.sidebar.markdown(
    """
    <div style="
        color:#EDF4FA;
        font-size:15px;
        font-weight:600;
        margin-bottom:3px;
    ">
        Decision Engine
    </div>

    <div style="
        color:#687B8E;
        font-size:8px;
        letter-spacing:1px;
        text-transform:uppercase;
        margin-bottom:18px;
    ">
        Terminal Controls
    </div>
    """,
    unsafe_allow_html=True
)


companies = api.get_companies()

if not companies:
    st.sidebar.warning("No companies yet.")

    with st.sidebar.expander("+ Create a company"):
        name = st.text_input("Name")
        sector = st.text_input("Sector")
        ticker = st.text_input("Ticker")

        if st.button("Create"):
            result, status = api.post(
                "/companies",
                json={
                    "name": name,
                    "sector": sector or None,
                    "ticker": ticker or None
                }
            )

            st.write("Status:", status)
            st.write("Result:", result)

            if status == 200:
                st.rerun()

    st.stop()
with st.sidebar.expander("+ Create a company"):
        name = st.text_input("Name")
        sector = st.text_input("Sector")
        ticker = st.text_input("Ticker")

        if st.button("Create"):
            result, status = api.post(
                "/companies",
                json={
                    "name": name,
                    "sector": sector or None,
                    "ticker": ticker or None
                }
            )

            st.write("Status:", status)
            st.write("Result:", result)

            if status == 200:
                st.rerun()

company_options = {
    c["name"]: c
    for c in companies
}

selected_company_name = st.sidebar.selectbox(
    "Company",
    list(company_options.keys())
)

selected_company = company_options[
    selected_company_name
]

st.session_state["selected_company_id"] = (
    selected_company["company_id"]
)

ticker_override = st.sidebar.text_input(
    "Ticker (for market data)",
    value=selected_company.get("ticker") or ""
)

st.session_state["selected_ticker"] = ticker_override

statements = api.get_company_statements(selected_company["company_id"])

with st.sidebar.expander("+ Upload new statement"):
    period_end = st.date_input("Period end date")
    uploaded_file = st.file_uploader("File", type=["xlsx", "xls", "csv", "pdf"])

    if st.button("Upload", type="primary", use_container_width=True):
        if uploaded_file is None:
            st.error("Choose a file first.")
        else:
            files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
            params = {"company_id": selected_company["company_id"], "period_end": str(period_end)}

            result, status = api.post("/statements/upload", params=params, files=files)
            st.write("Status code:", status)
            st.write("Response:", result)
            if status == 200:
                labels = [s["period_label"] for s in result["statements"]]
                st.success(f"Uploaded {len(result['statements'])} statement(s): {', '.join(labels)}")
                st.rerun()
            else:
                st.error("Upload failed.")


if statements:
    statement_options = {
        f"{s['period_label']} ({s['statement_type']})": s["statement_id"]
        for s in statements
    }

    selected_statement_label = st.sidebar.selectbox(
        "Statement",
        list(statement_options.keys())
    )

    statement_id = statement_options[selected_statement_label]

else:
    st.sidebar.info("No statements uploaded for this company yet.")
    statement_id = None



st.session_state["selected_statement_id"] = statement_id

st.session_state["selected_statement_id"] = statement_id

st.sidebar.markdown(
    "<br>",
    unsafe_allow_html=True
)

if st.sidebar.button(
    "LOG OUT",
    use_container_width=True
):
    st.session_state.token = None
    st.rerun()

st.markdown(
    '<div class="app-title">'
    f'<div class="app-title-main">Corp-Finance Decision Engine</div>'
    f'<div class="app-title-sub">{selected_company_name}</div>'
    f'<div class="app-title-sub">{ticker_override or "NO TICKER"}</div>'
    '<div class="live-indicator"><span class="live-dot"></span>LIVE TERMINAL</div>'
    '</div>',
    unsafe_allow_html=True
)

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
    [
        "Live Market",
        "Executive Overview",
        "Ratio Analytics",
        "Capital Budgeting",
        "WACC Optimizer",
        "Stress & Monte Carlo",
        "AI Copilot"
    ]
)

with tab1:
    render_market()

with tab2:
    render_health()

with tab3:
    render()

with tab4:
    render_capital_budget()

with tab5:
    render_wacc()

with tab6:
    render_monte_carlo()

with tab7:
    render_copilot()

