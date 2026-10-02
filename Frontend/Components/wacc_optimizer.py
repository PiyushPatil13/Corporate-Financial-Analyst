import streamlit as st
import plotly.graph_objects as go
import numpy as np
import api_client as api


def render_wacc():
    statement_id = st.session_state.get("selected_statement_id")
    if not statement_id:
        st.info("Select a statement in the sidebar to load WACC analysis.")
        return

    wacc = api.get_wacc(statement_id)

    st.markdown(
        '<div class="auth-card">'
        '<div style="color:#718397; font-size:9px; letter-spacing:1px; text-transform:uppercase;">Cost of Capital</div>'
        '<div style="color:#DDE7F1; font-size:15px; margin-top:6px;">WACC Optimizer</div>'
        '</div>',
        unsafe_allow_html=True
    )
    st.write("")

    weight_equity = wacc.get("weight_equity")
    weight_debt = wacc.get("weight_debt")

    if weight_equity is None or weight_debt is None:
        st.info("WACC inputs unavailable for this statement (needs total_debt, market_cap, interest_expense).")
        return

    col_donut, col_metrics = st.columns([1, 1.2])

    with col_donut:
        st.subheader("Capital Structure")
        fig_donut = go.Figure(go.Pie(
            labels=["Equity", "Debt"],
            values=[weight_equity, weight_debt],
            hole=0.55,
            marker=dict(colors=["#5EA8D9", "#E06B6B"]),
            textfont=dict(color="#DDE7F1"),
        ))
        fig_donut.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#DDE7F1', size=11),
            showlegend=True, legend=dict(font=dict(color='#DDE7F1')),
            height=320, margin=dict(l=10, r=10, t=10, b=10),
        )
        st.plotly_chart(fig_donut, use_container_width=True)

    with col_metrics:
        st.subheader("Current Cost of Capital")
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("WACC", f"{wacc.get('wacc')*100:.2f}%" if wacc.get("wacc") is not None else "—")
        with c2:
            st.metric("Cost of Equity", f"{wacc.get('cost_of_equity')*100:.2f}%" if wacc.get("cost_of_equity") is not None else "—")
        with c3:
            st.metric("Cost of Debt (after tax)", f"{wacc.get('cost_of_debt_after_tax')*100:.2f}%" if wacc.get("cost_of_debt_after_tax") is not None else "—")

        st.write("")
        st.caption(f"Weight of Equity: {weight_equity:.1%}  |  Weight of Debt: {weight_debt:.1%}")

    st.write("")
    st.subheader("WACC Sensitivity: Cost of Equity vs. Cost of Debt")

    ke_range = np.arange(0.06, 0.22, 0.01)
    kd_range = np.arange(0.02, 0.12, 0.01)

    z = []
    for ke in ke_range:
        row = []
        for kd in kd_range:
            w = (weight_equity * ke) + (weight_debt * kd)
            row.append(w)
        z.append(row)

    fig_heat = go.Figure(go.Heatmap(
        z=z,
        x=[f"{k*100:.0f}%" for k in kd_range],
        y=[f"{k*100:.0f}%" for k in ke_range],
        colorscale=[[0, "#55D59D"], [0.5, "#F59E0B"], [1, "#E06B6B"]],
        colorbar=dict(title="WACC", tickfont=dict(color="#DDE7F1"), title_font=dict(color="#DDE7F1")),
    ))
    fig_heat.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#DDE7F1', size=11),
        xaxis=dict(title="Cost of Debt (Kd)"),
        yaxis=dict(title="Cost of Equity (Ke)"),
        height=400, margin=dict(l=10, r=10, t=10, b=10),
    )
    st.plotly_chart(fig_heat, use_container_width=True)
    st.caption("Heatmap uses the company's ACTUAL capital structure weights (Equity/Debt), sweeping Ke and Kd through the real WACC formula — not new backend data.")