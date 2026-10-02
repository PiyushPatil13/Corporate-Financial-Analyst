import streamlit as st
import plotly.graph_objects as go
import api_client as api


def render():
    statement_id = st.session_state.get("selected_statement_id")

    if not statement_id:
        st.info("Enter a Statement ID in the sidebar to load ratio analytics.")
        return

    ratios = api.get_ratios(statement_id)
    wc = api.get_working_capital(statement_id)
    line_items_raw = api.get_line_items(statement_id)
    line_items = {i["label"]: i["value"] for i in line_items_raw}

    st.markdown(
        '<div class="auth-card">'
        '<div style="color:#718397; font-size:9px; letter-spacing:1px; text-transform:uppercase;">Fundamental Analysis</div>'
        '<div style="color:#DDE7F1; font-size:15px; margin-top:6px;">Ratio Analytics</div>'
        '</div>',
        unsafe_allow_html=True
    )

    st.write("")

    st.subheader("DuPont ROE Decomposition")

    revenue = line_items.get("revenue")
    net_income = line_items.get("net_income")
    total_assets = line_items.get("total_assets")
    total_equity = line_items.get("total_equity")

    if all(
        v is not None and v != 0
        for v in [revenue, net_income, total_assets, total_equity]
    ):
        net_margin = net_income / revenue
        asset_turnover = revenue / total_assets
        equity_multiplier = total_assets / total_equity
        roe = net_margin * asset_turnover * equity_multiplier

        fig = go.Figure(
            go.Waterfall(
                orientation="v",
                measure=[
                    "relative",
                    "relative",
                    "relative",
                    "total"
                ],
                x=[
                    "Net Margin",
                    "Asset Turnover",
                    "Equity Multiplier",
                    "ROE"
                ],
                y=[
                    net_margin,
                    asset_turnover,
                    equity_multiplier,
                    roe
                ],
                connector={
                    "line": {
                        "color": "rgba(255,255,255,0.2)"
                    }
                },
                increasing={
                    "marker": {
                        "color": "#55D59D"
                    }
                },
                decreasing={
                    "marker": {
                        "color": "#E06B6B"
                    }
                },
                totals={
                    "marker": {
                        "color": "#5EA8D9"
                    }
                }
            )
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="#DDE7F1",
                size=11
            ),
            yaxis=dict(
                gridcolor="rgba(255,255,255,0.08)",
                tickformat=".2f"
            ),
            height=320,
            margin=dict(
                l=10,
                r=10,
                t=20,
                b=10
            )
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.caption(
            f"ROE = {net_margin:.1%} × "
            f"{asset_turnover:.2f} × "
            f"{equity_multiplier:.2f} = "
            f"{roe:.1%}"
        )

    else:
        st.info(
            "Missing revenue, net income, total assets, or total equity — "
            "cannot compute DuPont breakdown."
        )

    st.write("")

    st.subheader("Cash Conversion Cycle")

    dso = wc.get("dso")
    dio = wc.get("dio")
    dpo = wc.get("dpo")

    if dso is not None and dio is not None and dpo is not None:
        fig2 = go.Figure()

        fig2.add_trace(
            go.Bar(
                y=["CCC"],
                x=[dio],
                name="DIO",
                orientation="h",
                marker_color="#5EA8D9"
            )
        )

        fig2.add_trace(
            go.Bar(
                y=["CCC"],
                x=[dso],
                name="DSO",
                orientation="h",
                marker_color="#55D59D"
            )
        )

        fig2.add_trace(
            go.Bar(
                y=["CCC"],
                x=[-dpo],
                name="DPO (offset)",
                orientation="h",
                marker_color="#E06B6B"
            )
        )

        fig2.update_layout(
            barmode="relative",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="#DDE7F1",
                size=11
            ),
            xaxis=dict(
                gridcolor="rgba(255,255,255,0.08)",
                title="Days"
            ),
            height=200,
            margin=dict(
                l=10,
                r=10,
                t=10,
                b=10
            ),
            legend=dict(
                orientation="h",
                y=-0.3
            )
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        st.caption(
            f"CCC = {dio:.0f} (DIO) + "
            f"{dso:.0f} (DSO) − "
            f"{dpo:.0f} (DPO) = "
            f"{wc.get('cash_conversion_cycle'):.1f} days"
        )

    else:
        st.info("Cash conversion cycle data unavailable.")

    st.write("")

    st.subheader("Liquidity & Solvency")

    current_ratio = ratios.get("current_ratio")
    quick_ratio = ratios.get("quick_ratio")
    interest_coverage = ratios.get("interest_coverage")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.metric(
            "Current Ratio",
            f"{current_ratio:.2f}"
            if current_ratio is not None
            else "—"
        )

    with c2:
        st.metric(
            "Quick Ratio",
            f"{quick_ratio:.2f}"
            if quick_ratio is not None
            else "—"
        )

    with c3:
        st.metric(
            "Interest Coverage",
            f"{interest_coverage:.2f}x"
            if interest_coverage is not None
            else "—"
        )

    if current_ratio is not None and quick_ratio is not None:
        fig3 = go.Figure(
            go.Bar(
                x=[
                    "Current Ratio",
                    "Quick Ratio"
                ],
                y=[
                    current_ratio,
                    quick_ratio
                ],
                marker_color=[
                    "#5EA8D9",
                    "#55D59D"
                ]
            )
        )

        fig3.add_hline(
            y=1.0,
            line_dash="dash",
            line_color="#E06B6B",
            annotation_text="Safety threshold (1.0x)"
        )

        fig3.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(
                color="#DDE7F1",
                size=11
            ),
            yaxis=dict(
                gridcolor="rgba(255,255,255,0.08)"
            ),
            height=280,
            margin=dict(
                l=10,
                r=10,
                t=20,
                b=10
            )
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )