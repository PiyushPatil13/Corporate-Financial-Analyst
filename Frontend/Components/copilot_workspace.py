import streamlit as st
import api_client as api


def render_copilot():
    company_id = st.session_state.get("selected_company_id")
    statement_id = st.session_state.get("selected_statement_id")

    st.markdown(
        '<div class="auth-card">'
        '<div style="color:#718397; font-size:9px; letter-spacing:1px; text-transform:uppercase;">GenAI Analyst</div>'
        '<div style="color:#DDE7F1; font-size:15px; margin-top:6px;">AI Copilot</div>'
        '</div>',
        unsafe_allow_html=True
    )
    st.write("")

    if not company_id:
        st.info("Select a company in the sidebar first.")
        return

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = {}
    if company_id not in st.session_state.chat_history:
        st.session_state.chat_history[company_id] = []

    for msg in st.session_state.chat_history[company_id]:
        with st.chat_message(msg["role"]):
            st.write(msg["text"])

    question = st.chat_input("Ask about this company's financials...")

    if question:
        st.session_state.chat_history[company_id].append({"role": "user", "text": question})
        with st.chat_message("user"):
            st.write(question)

        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                answer = api.ask_copilot(company_id, statement_id, question)
            if answer:
                st.write(answer)
                st.session_state.chat_history[company_id].append({"role": "assistant", "text": answer})
            else:
                st.error("No recommendation history for this company yet — generate one from the Executive Overview tab first.")