import streamlit as st
import plotly.graph_objects as go
import api_client as api


def render_health_gauge(score):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score if score is not None else 0,
        number={'suffix': "/100", 'font': {'color': '#DDE7F1', 'size': 30}},
        gauge={
            'axis': {'range': [0, 100], 'tickcolor': '#64748B'},
            'bar': {'color': '#5EA8D9'},
            'bgcolor': 'rgba(0,0,0,0)',
            'borderwidth': 0,
            'steps': [
                {'range': [0, 40], 'color': 'rgba(224, 107, 107, 0.25)'},
                {'range': [40, 70], 'color': 'rgba(245, 158, 11, 0.25)'},
                {'range': [70, 100], 'color': 'rgba(85, 213, 157, 0.25)'},
            ],
        },
    ))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#DDE7F1'), height=220, margin=dict(l=20, r=20, t=10, b=10))
    return fig


def render_health(): 
    statement_id = st.session_state.get("selected_statement_id")
    company_id = st.session_state.get("selected_company_id")

    if not statement_id:
        st.info("Select a statement in the sidebar to load the executive overview.")
        return

    hs = api.get_health_score(statement_id)
    rec = api.get_recommendation(statement_id)
    ratios = api.get_ratios(statement_id)
    wc = api.get_working_capital(statement_id)

    growth, _ = api.get(f"/companies/{company_id}/growth")
    growth = growth or {}

    st.markdown(
        '<div class="auth-card">'
        '<div style="color:#718397; font-size:9px; letter-spacing:1px; text-transform:uppercase;">Financial Intelligence</div>'
        '<div style="color:#DDE7F1; font-size:15px; margin-top:6px;">Executive Overview</div>'
        '</div>',
        unsafe_allow_html=True
    )
    st.write("")

    col_gauge, col_radar, col_action = st.columns([1, 1.4, 1])

    with col_gauge:
        st.markdown("<div style='color:#7F91A5; font-size:9px; text-transform:uppercase; margin-bottom:8px;'>Health Score</div>", unsafe_allow_html=True)
        score = hs.get("financial_health_score")
        st.plotly_chart(render_health_gauge(score), use_container_width=True)

    with col_radar:
        st.markdown("<div style='color:#7F91A5; font-size:9px; text-transform:uppercase; margin-bottom:8px;'>Score Dimensions</div>", unsafe_allow_html=True)
        components = hs.get("component_scores") or {}

        theta = list(components.keys())
        r = list(components.values())

        rev_growth = growth.get("revenue_growth")
        if rev_growth is not None:
            growth_score = max(0, min(100, 50 + rev_growth * 100))
            theta.append("Revenue Growth")
            r.append(growth_score)

        if theta:
            fig = go.Figure()
            fig.add_trace(go.Scatterpolar(
                r=r, theta=theta, fill='toself',
                line_color='#5EA8D9', fillcolor='rgba(94, 168, 217, 0.2)',
            ))
            fig.update_layout(
                polar=dict(
                    bgcolor='rgba(0,0,0,0)',
                    radialaxis=dict(visible=True, range=[0, 100], color='#64748B', gridcolor='rgba(255,255,255,0.08)'),
                    angularaxis=dict(color='#DDE7F1', gridcolor='rgba(255,255,255,0.08)'),
                ),
                paper_bgcolor='rgba(0,0,0,0)', font=dict(color='#DDE7F1', size=10),
                showlegend=False, height=260, margin=dict(l=30, r=30, t=10, b=10),
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No score components available.")

    with col_action:
        st.markdown("<div style='color:#7F91A5; font-size:9px; text-transform:uppercase; margin-bottom:8px;'>Recommendation</div>", unsafe_allow_html=True)
        if rec:
            action = rec.get("recommended_action", "unknown")
            badge_colors = {
                "reinvest": ("#55D59D", "rgba(85, 213, 157, 0.15)"),
                "debt_paydown": ("#E06B6B", "rgba(224, 107, 107, 0.15)"),
                "build_reserves": ("#F59E0B", "rgba(245, 158, 11, 0.15)"),
                "dividend": ("#5EA8D9", "rgba(94, 168, 217, 0.15)"),
            }
            color, bg = badge_colors.get(action, ("#7F91A5", "rgba(127,145,165,0.15)"))
            st.markdown(
                f'<div style="background:{bg}; border:1px solid {color}; color:{color}; '
                f'padding:12px 16px; border-radius:6px; font-weight:700; text-align:center; '
                f'text-transform:uppercase; letter-spacing:0.5px; margin-top:10px;">'
                f'{action.replace("_", " ")}</div>',
                unsafe_allow_html=True
            )
            st.write("")
            if st.button("Ask AI: Why?", use_container_width=True):
                with st.spinner("Generating explanation..."):
                    memo = api.get_recommendation_memo(statement_id)
                if memo:
                    st.session_state["last_memo"] = memo
                else:
                    st.error("Could not generate explanation.")

            if "last_memo" in st.session_state:
                st.markdown(
                    f'<div style="background:rgba(94,168,217,0.08); border:1px solid rgba(94,168,217,0.3); '
                    f'border-radius:6px; padding:14px 16px; margin-top:10px; color:#DDE7F1; font-size:12px; line-height:1.6;">'
                    f'{st.session_state["last_memo"]}</div>',
                    unsafe_allow_html=True
                )
        else:
            st.info("No recommendation yet.")
            if st.button("Generate Recommendation", type="primary", use_container_width=True):
                result, status = api.post(f"/statements/recommendation/{statement_id}/generate", params={"company_id": company_id})
                if status == 200:
                    st.rerun()
                else:
                    st.error("Failed to generate")

    st.write("")
    st.markdown("<div style='color:#7F91A5; font-size:9px; text-transform:uppercase; margin-bottom:8px;'>Core KPIs</div>", unsafe_allow_html=True)

    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.metric("Health Score", f"{hs.get('financial_health_score'):.1f}" if hs.get("financial_health_score") is not None else "—")
    with k2:
        st.metric("Debt/Equity", f"{ratios.get('debt_to_equity'):.2f}" if ratios.get("debt_to_equity") is not None else "—")
    with k3:
        st.metric("Net Margin", f"{ratios.get('net_margin')*100:.1f}%" if ratios.get("net_margin") is not None else "—")
    with k4:
        st.metric("CCC", f"{wc.get('cash_conversion_cycle'):.0f}d" if wc.get("cash_conversion_cycle") is not None else "—")
    with k5:
        rg = growth.get("revenue_growth")
        st.metric("Revenue Growth", f"{rg*100:+.1f}%" if rg is not None else "—")