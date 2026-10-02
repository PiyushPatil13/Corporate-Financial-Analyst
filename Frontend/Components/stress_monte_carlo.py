import streamlit as st
import plotly.graph_objects as go
import numpy as np
import api_client as api


def render_monte_carlo():
    st.markdown(
        '<div class="auth-card">'
        '<div style="color:#718397; font-size:9px; letter-spacing:1px; text-transform:uppercase;">Risk Simulation</div>'
        '<div style="color:#DDE7F1; font-size:15px; margin-top:6px;">Stress & Monte Carlo</div>'
        '</div>',
        unsafe_allow_html=True
    )
    st.write("")

    with st.expander("Project parameters", expanded=True):
        initial_outlay = st.number_input("Initial outlay (negative)", value=-2500000.0, key="mc_outlay")
        year_flows = st.text_input("Future cash flows (comma-separated)", value="600000,750000,850000,900000,950000", key="mc_flows")
        discount_rate = st.number_input("Discount rate", value=0.10, step=0.01, key="mc_rate")
        volatility = st.slider("Volatility (std dev)", 0.05, 0.40, 0.15, step=0.05)
        num_sims = st.select_slider("Simulations", options=[1000, 2500, 5000, 10000], value=5000)

        if st.button("Run Simulation", type="primary"):
            cash_flows = [initial_outlay] + [float(x.strip()) for x in year_flows.split(",")]
            with st.spinner("Running Monte Carlo..."):
                mc = api.get_monte_carlo(cash_flows, discount_rate, num_sims, volatility)
            if mc:
                st.session_state["mc_result"] = mc

            with st.spinner("Running stress scenarios..."):
                scenarios = [
                    {"label": "2008 Financial Crisis", "revenue_shock_pct": -35},
                    {"label": "COVID-style Shock", "revenue_shock_pct": -20},
                    {"label": "Mild Recession", "revenue_shock_pct": -10},
                    {"label": "Supply Chain Squeeze", "revenue_shock_pct": -15},
                    {"label": "Base Case", "revenue_shock_pct": 0},
                ]
                stress = api.run_stress_test(cash_flows, discount_rate, scenarios)
            if stress:
                st.session_state["stress_result"] = stress

    if "mc_result" in st.session_state:
        mc = st.session_state["mc_result"]
        st.subheader("Monte Carlo NPV Distribution")

        c1, c2, c3, c4 = st.columns(4)
        with c1: st.metric("Mean NPV", f"{mc.get('mean_npv'):,.0f}" if mc.get("mean_npv") is not None else "—")
        with c2: st.metric("Median NPV", f"{mc.get('median_npv'):,.0f}" if mc.get("median_npv") is not None else "—")
        with c3: st.metric("VaR (5th pct)", f"{mc.get('p5_npv'):,.0f}" if mc.get("p5_npv") is not None else "—")
        with c4: st.metric("P(NPV > 0)", f"{mc.get('probability_positive_npv')*100:.1f}%" if mc.get("probability_positive_npv") is not None else "—")

        dist = mc.get("npv_distribution")
        if dist:
            fig = go.Figure()
            fig.add_trace(go.Histogram(x=dist, nbinsx=40, marker_color="#5EA8D9", opacity=0.85))
            for label, key, color in [("P5 (VaR)", "p5_npv", "#E06B6B"), ("Median", "median_npv", "#F59E0B"), ("P95", "p95_npv", "#55D59D")]:
                val = mc.get(key)
                if val is not None:
                    fig.add_vline(x=val, line_dash="dash", line_color=color, annotation_text=label, annotation_position="top")
            fig.add_vline(x=0, line_color="#7F91A5")
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#DDE7F1', size=11),
                xaxis=dict(gridcolor='rgba(255,255,255,0.08)', title="NPV"),
                yaxis=dict(gridcolor='rgba(255,255,255,0.08)', title="Frequency"),
                height=380, margin=dict(l=10, r=10, t=20, b=10),
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Run a simulation to see the distribution (older backend response missing npv_distribution).")

    if "stress_result" in st.session_state:
        st.subheader("Scenario Stress Test")
        results = st.session_state["stress_result"]
        labels = list(results.keys())
        npvs = [results[k]["npv"] for k in labels]
        base_npv = results.get("Base Case", {}).get("npv", 0)
        deltas = [v - base_npv for v in npvs]
        colors = ["#55D59D" if d >= 0 else "#E06B6B" for d in deltas]

        fig2 = go.Figure(go.Bar(
            y=labels, x=deltas, orientation="h", marker_color=colors,
        ))
        fig2.add_vline(x=0, line_color="#7F91A5")
        fig2.update_layout(
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#DDE7F1', size=11),
            xaxis=dict(gridcolor='rgba(255,255,255,0.08)', title="NPV Impact vs. Base Case"),
            yaxis=dict(gridcolor='rgba(255,255,255,0.08)', autorange="reversed"),
            height=320, margin=dict(l=10, r=10, t=20, b=10),
        )
        st.plotly_chart(fig2, use_container_width=True)
        paths = mc.get("sample_paths")
        if paths:
            st.subheader("Simulated Cash Flow Paths (Fan Chart)")
            fig3 = go.Figure()

            for path in paths:
                final_value = path[-1]
                if final_value >= 0:
                    color = "rgba(85, 213, 157, 0.18)"   # green — ended profitable
                else:
                    color = "rgba(224, 107, 107, 0.18)"  # red — ended at a loss

                fig3.add_trace(go.Scatter(
                    y=path, mode="lines",
                    line=dict(width=0.7, color=color),
                    showlegend=False, hoverinfo="skip",
                ))

            # Overlay the mean path on top, bold and bright, so it stands out from the fan
            mean_path = [sum(p[i] for p in paths) / len(paths) for i in range(len(paths[0]))]
            fig3.add_trace(go.Scatter(
                y=mean_path, mode="lines",
                line=dict(width=3, color="#5EA8D9"),
                name="Mean Path",
            ))

            fig3.add_hline(y=0, line_color="#F8FAFC", line_dash="dash", line_width=1)
            fig3.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                font=dict(color='#DDE7F1', size=11),
                xaxis=dict(gridcolor='rgba(255,255,255,0.08)', title="Year"),
                yaxis=dict(gridcolor='rgba(255,255,255,0.08)', title="Cumulative Cash Flow"),
                showlegend=True, legend=dict(font=dict(color='#DDE7F1')),
                height=400, margin=dict(l=10, r=10, t=20, b=10),
            )
            st.plotly_chart(fig3, use_container_width=True)