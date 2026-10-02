import streamlit as st
import plotly.graph_objects as go
import api_client as api


def render_capital_budget():
    st.markdown(
        '<div class="auth-card">'
        '<div style="color:#718397; font-size:9px; letter-spacing:1px; text-transform:uppercase;">Project Evaluation</div>'
        '<div style="color:#DDE7F1; font-size:15px; margin-top:6px;">Capital Budgeting</div>'
        '</div>',
        unsafe_allow_html=True
    )
    st.write("")

    with st.expander("Project cash flows", expanded=True):
        initial_outlay = st.number_input("Initial outlay (negative)", value=-1000000.0)
        year_flows = st.text_input("Future cash flows (comma-separated)", value="300000,400000,400000,350000")

        if st.button("Analyze Project", type="primary"):
            cash_flows = [initial_outlay] + [float(x.strip()) for x in year_flows.split(",")]
            result = api.get_npv_profile(cash_flows)
            if result:
                st.session_state["npv_profile"] = result
                st.session_state["cb_cash_flows"] = cash_flows
            else:
                st.error("Failed to compute NPV profile.")

    if "npv_profile" not in st.session_state:
        st.info("Enter cash flows above and click Analyze Project.")
        return

    profile = st.session_state["npv_profile"]
    rates = profile["rates"]
    npvs = profile["npvs"]
    irr = profile.get("irr")

    st.subheader("NPV Profile")
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[r * 100 for r in rates], y=npvs, mode="lines", name="NPV",
        line=dict(color="#5EA8D9", width=2),
    ))
    fig.add_hline(y=0, line_dash="dash", line_color="#E06B6B")
    if irr is not None:
        fig.add_vline(x=irr * 100, line_dash="dot", line_color="#55D59D",
                       annotation_text=f"IRR = {irr:.1%}", annotation_position="top")
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#DDE7F1', size=11),
        xaxis=dict(gridcolor='rgba(255,255,255,0.08)', title="Discount Rate (%)"),
        yaxis=dict(gridcolor='rgba(255,255,255,0.08)', title="NPV"),
        height=380, margin=dict(l=10, r=10, t=20, b=10),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Cumulative Cash Flow / Payback")
    cash_flows = st.session_state["cb_cash_flows"]
    cumulative = []
    running = 0
    for cf in cash_flows:
        running += cf
        cumulative.append(running)

    colors = ["#E06B6B" if v < 0 else "#55D59D" for v in cumulative]
    fig2 = go.Figure(go.Scatter(
        x=list(range(len(cumulative))), y=cumulative, mode="lines+markers",
        line=dict(color="#5EA8D9"), marker=dict(color=colors, size=9),
        fill="tozeroy", fillcolor="rgba(94,168,217,0.1)",
    ))
    fig2.add_hline(y=0, line_dash="dash", line_color="#7F91A5")
    fig2.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#DDE7F1', size=11),
        xaxis=dict(gridcolor='rgba(255,255,255,0.08)', title="Year"),
        yaxis=dict(gridcolor='rgba(255,255,255,0.08)', title="Cumulative Cash Flow"),
        height=320, margin=dict(l=10, r=10, t=20, b=10),
    )
    st.plotly_chart(fig2, use_container_width=True)