import html
import streamlit as st

from ai_engine import analyze_complaint
from database import initialize_database, save_complaint, get_complaint_history

st.set_page_config(
    page_title="AI Customer Complaint Resolver",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Premium blue / white UI ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
      --navy: #092b68;
      --blue: #1769f5;
      --blue2: #2396ff;
      --ink: #132951;
      --muted: #687b9e;
      --line: #e0eaff;
    }

    html, body, [class*="css"] {
      font-family: 'Inter', sans-serif;
    }

    .stApp {
      background:
        radial-gradient(ellipse at 83% 0%, rgba(71,145,255,.17), transparent 31%),
        linear-gradient(135deg, #f4f8ff 0%, #edf4ff 52%, #f9fbff 100%);
      color: var(--ink);
    }

    /* Streamlit toolbar: remove the white strip and blend it into the page */
    [data-testid="stHeader"],
    [data-testid="stToolbar"],
    [data-testid="stDecoration"] {
      background: transparent !important;
      background-color: transparent !important;
      border: 0 !important;
      box-shadow: none !important;
    }
    [data-testid="stHeader"] {
      backdrop-filter: none !important;
      -webkit-backdrop-filter: none !important;
    }
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
      background: transparent !important;
    }
    [data-testid="stHeader"] button,
    [data-testid="stHeader"] svg {
      color: #17396f !important;
      fill: currentColor;
    }

    .block-container {
      max-width: 1600px;
      padding-top: 1rem !important;
      padding-bottom: 3rem;
    }

    [data-testid="stSidebar"] {
      background: linear-gradient(180deg, #09265c 0%, #104b9e 58%, #1676ee 100%);
      border-right: 1px solid rgba(255,255,255,.2);
    }
    [data-testid="stSidebar"] * {
      color: #f7faff !important;
    }
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
      color: #c5d8ff !important;
    }

    .side-brand {
      display:flex; align-items:center; gap:12px;
      font-size:1.04rem; font-weight:800; line-height:1.25;
      padding:.3rem 0 1.2rem;
    }
    .side-logo {
      width:48px; height:48px; display:grid; place-items:center;
      border-radius:16px; background:rgba(255,255,255,.17);
      font-size:1.7rem;
      box-shadow:inset 0 1px 0 rgba(255,255,255,.35);
    }
    .side-robot {
      font-size:4.4rem; text-align:center; margin:.5rem 0 -.1rem;
      filter:drop-shadow(0 10px 12px rgba(0,0,0,.18));
    }
    .side-note {
      background:rgba(4,32,88,.43); border:1px solid rgba(255,255,255,.17);
      padding:1rem; border-radius:18px; line-height:1.55;
    }

    .hero {
      display:flex; align-items:center; gap:14px; margin-bottom:.2rem;
    }
    .hero-avatar {
      width:56px; height:56px; flex:0 0 56px;
      display:grid; place-items:center; border-radius:18px;
      background:linear-gradient(145deg,#fff,#dbeaff);
      border:1px solid #fff;
      box-shadow:0 8px 24px rgba(30,100,220,.14);
      font-size:1.9rem;
    }
    .hero-title {
      font-size:clamp(1.55rem,2.5vw,2.25rem);
      font-weight:800; letter-spacing:-.055em; color:#102653;
      line-height:1.18; text-shadow:none;
    }
    .hero-title span { color:#1769f5; }
    .hero-sub {
      color:#6c7e9f; font-size:.91rem; margin-top:.5rem; line-height:1.5;
    }
    .top-pill {
      display:inline-block; background:rgba(255,255,255,.92);
      border:1px solid #dce7ff; color:#2c4b7d;
      border-radius:999px; padding:.65rem .9rem;
      font-size:.78rem; font-weight:700; white-space:nowrap;
      box-shadow:0 6px 20px rgba(35,80,150,.06);
    }

    .panel-heading {
      display:flex; align-items:center; gap:11px; margin-bottom:.2rem;
    }
    .panel-icon {
      width:42px; height:42px; display:grid; place-items:center;
      border-radius:14px; background:linear-gradient(145deg,#fff,#e1edff);
      color:#1769f5; font-size:1.25rem;
      box-shadow:0 5px 15px rgba(34,104,230,.12);
    }
    .panel-title {
      font-size:1.12rem; font-weight:800; color:#142b56;
      letter-spacing:-.03em;
    }
    .panel-subtitle {
      font-size:.82rem; color:#7384a4; margin:.25rem 0 1rem;
    }

    .stTextArea textarea {
      background:#f7faff !important; color:#19345f !important;
      border:1px solid #d9e5ff !important; border-radius:16px !important;
      padding:1rem !important; font-size:.93rem !important;
      line-height:1.6 !important;
    }
    .stTextArea textarea::placeholder {
      color:#8b9bbb !important; opacity:1;
    }
    .stTextInput input {
      background:#fff !important; border:1px solid #dce6fa !important;
      border-radius:13px !important; color:#19345f !important;
    }
    .stSelectbox [data-baseweb="select"] > div {
      border-radius:13px; border-color:#dce6fa;
    }

    .stButton > button, .stFormSubmitButton > button, .stDownloadButton > button {
      border:0 !important; border-radius:13px !important;
      background:linear-gradient(100deg,#145bf2,#1698ff) !important;
      color:#fff !important; font-weight:800 !important;
      padding:.72rem 1rem !important;
      box-shadow:0 9px 22px rgba(22,105,245,.22);
      transition:transform .18s ease, box-shadow .18s ease;
    }
    .stButton > button:hover, .stFormSubmitButton > button:hover,
    .stDownloadButton > button:hover {
      transform:translateY(-2px);
      box-shadow:0 13px 27px rgba(22,105,245,.3);
    }

    div[data-testid="stTabs"] button {
      font-weight:700; border-radius:10px 10px 0 0;
    }
    div[data-testid="stTabs"] button[aria-selected="true"] {
      color:#1769f5 !important;
    }

    .metric-card {
      height:100%; min-height:102px; border-radius:17px; padding:1rem;
      border:1px solid #e2ebff;
      background:linear-gradient(145deg,#fff,#edf4ff);
    }
    .metric-card.red {
      background:linear-gradient(145deg,#fff,#fff0f1); border-color:#ffe0e2;
    }
    .metric-card.amber {
      background:linear-gradient(145deg,#fffdf8,#fff4dc); border-color:#ffebc2;
    }
    .metric-label { font-size:.76rem; color:#7182a1; font-weight:600; }
    .metric-value {
      font-size:1rem; color:#1762df; font-weight:800;
      margin-top:.35rem; overflow-wrap:anywhere;
    }
    .metric-card.red .metric-value { color:#d93645; }
    .metric-card.amber .metric-value { color:#b86a00; }

    .result-card {
      background:linear-gradient(110deg,rgba(255,255,255,.97),rgba(242,247,255,.97));
      border:1px solid #e7eefb; border-radius:16px;
      padding:1rem 1.1rem; margin-top:.75rem;
    }
    .result-title {
      font-size:.92rem; font-weight:800; color:#162c56; margin-bottom:.35rem;
    }
    .result-body {
      font-size:.87rem; line-height:1.65; color:#5c6f92; overflow-wrap:anywhere;
    }
    .status-ok {
      display:inline-block; background:#e3faf1; color:#07875e;
      border:1px solid #c5f1e3; border-radius:999px;
      padding:.42rem .7rem; font-size:.76rem; font-weight:700;
    }
    .empty-state {
      text-align:center; padding:2.3rem 1.2rem;
      border:1px dashed #cbdcff; border-radius:18px;
      background:linear-gradient(140deg,#fbfdff,#eef5ff);
    }
    .empty-emoji { font-size:2.5rem; margin-bottom:.5rem; }
    .empty-title { font-weight:800; color:#1b356b; font-size:1.03rem; margin-bottom:.45rem; }
    .empty-copy { color:#7585a5; font-size:.85rem; line-height:1.55; }
    [data-testid="stExpander"] {
      background:rgba(255,255,255,.78); border:1px solid #e1eaff;
      border-radius:14px; overflow:hidden;
    }
    .stAlert { border-radius:13px; }
    hr { border-color:#e2eaff; }

    @media(max-width:900px) {
      .block-container { padding-left:1rem; padding-right:1rem; }
      .hero-avatar { width:45px; height:45px; flex-basis:45px; }
      .top-pill { display:none; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

initialize_database()

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown(
        '<div class="side-brand"><div class="side-logo">💬</div>'
        '<div>AI Customer<br>Complaint Resolver</div></div>',
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown("### ✨ AI support workspace")
    st.caption(
        "Understand issues, recommend solutions, and prepare thoughtful customer responses."
    )
    st.markdown('<div class="side-robot">🤖</div>', unsafe_allow_html=True)
    st.markdown(
        """
        <div class="side-note">
          <b>AI-powered support</b><br>
          <span style="color:#c8dcff;font-size:.88rem;">
          A clearer path from customer frustration to a helpful next step.
          </span>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("")
    st.markdown("**HOW IT WORKS**")
    st.markdown("1. Enter a complaint")
    st.markdown("2. Analyze with AI")
    st.markdown("3. Review the recommendation")
    st.markdown("4. Download the result")
    st.markdown("---")
    st.info("Always review AI recommendations before sending them to customers.")
    st.caption("Generative AI · Streamlit · SQLite")

# ---------- Header ----------
header_left, header_right = st.columns([5, 1.3], vertical_alignment="center")
with header_left:
    st.markdown(
        """
        <div class="hero">
          <div class="hero-avatar">🤖</div>
          <div>
            <div class="hero-title">AI <span>Customer Complaint Resolver</span></div>
            <div class="hero-sub">
              Analyze customer complaints, get intelligent recommendations,
              and draft empathetic replies.
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
with header_right:
    st.markdown(
        '<div class="top-pill">✦ SMART SUPPORT DESK</div>',
        unsafe_allow_html=True,
    )

st.markdown("")
tab_analyze, tab_history = st.tabs(
    ["✦  Analyze Complaint", "◷  Complaints History"]
)

EXAMPLES = {
    "Order Delay": (
        "My order has not arrived for the past two days, and I have been "
        "messaging the support team without receiving a response."
    ),
    "Refund Issue": (
        "I returned my product a week ago, but my refund has not reached "
        "my bank account."
    ),
    "Damaged Product": (
        "My product arrived damaged and it does not work. I need help "
        "resolving this issue."
    ),
    "Payment Failure": (
        "Money was deducted from my account, but the payment failed and "
        "my order was not confirmed."
    ),
}

with tab_analyze:
    left, right = st.columns([0.95, 1.2], gap="large")

    with left:
        st.markdown(
            '<div class="panel-heading">'
            '<div class="panel-icon">✎</div><div>'
            '<div class="panel-title">Submit a Complaint</div>'
            '<div class="panel-subtitle">Describe the issue and let AI analyze it.</div>'
            '</div></div>',
            unsafe_allow_html=True,
        )

        selected_example = st.selectbox(
            "Quick-fill an example",
            ["Choose an example..."] + list(EXAMPLES.keys()),
            key="selected_example",
        )

        # Selecting an example automatically fills the text area on rerun.
        if selected_example in EXAMPLES:
            st.session_state["complaint_draft"] = EXAMPLES[selected_example]

        with st.form("complaint_form"):
            complaint = st.text_area(
                "Customer complaint",
                value=st.session_state.get("complaint_draft", ""),
                placeholder=(
                    "Example: My order has not arrived for two days, "
                    "and support has not replied..."
                ),
                height=210,
                max_chars=5000,
            )
            st.caption(
                "For privacy, do not enter passwords, PINs, OTPs, or unnecessary sensitive details."
            )
            submitted = st.form_submit_button(
                "✦  Analyze Complaint   →",
                type="primary",
                use_container_width=True,
            )

        if submitted:
            st.session_state["complaint_draft"] = complaint
            if not complaint.strip():
                st.warning("Please enter a complaint first.")
            else:
                try:
                    with st.spinner(
                        "AI is reviewing the complaint and preparing recommendations..."
                    ):
                        result = analyze_complaint(complaint.strip())
                        save_complaint(complaint.strip(), result)
                    st.session_state["latest_result"] = result
                    st.session_state["latest_complaint"] = complaint.strip()
                    st.success("Complaint analyzed and saved.")
                except Exception as exc:
                    st.error(
                        "Analysis failed. Check your API key, internet connection, "
                        "model availability, and terminal logs."
                    )
                    st.caption(f"Technical details: {exc}")

    with right:
        st.markdown(
            '<div class="panel-heading">'
            '<div class="panel-icon">✧</div><div>'
            '<div class="panel-title">Analysis Results</div>'
            '<div class="panel-subtitle">AI-generated findings and recommended next steps.</div>'
            '</div></div>',
            unsafe_allow_html=True,
        )
        result = st.session_state.get("latest_result")

        if result:
            st.markdown(
                '<span class="status-ok">● Analyzed Successfully</span>',
                unsafe_allow_html=True,
            )
            st.markdown("")
            m1, m2, m3 = st.columns(3)
            metrics = [
                (m1, "CATEGORY", result["category"], ""),
                (m2, "SENTIMENT", result["sentiment"], "red"),
                (m3, "RECOMMENDED PRIORITY", result["priority"], "amber"),
            ]
            for col, label, value, extra_class in metrics:
                with col:
                    st.markdown(
                        f'<div class="metric-card {extra_class}">'
                        f'<div class="metric-label">{html.escape(str(label))}</div>'
                        f'<div class="metric-value">{html.escape(str(value))}</div>'
                        "</div>",
                        unsafe_allow_html=True,
                    )

            for icon, title, key in [
                ("▤", "Complaint Summary", "summary"),
                ("💡", "Recommended Resolution", "resolution"),
            ]:
                st.markdown(
                    f'<div class="result-card"><div class="result-title">'
                    f'{icon} {title}</div><div class="result-body">'
                    f'{html.escape(str(result[key]))}</div></div>',
                    unsafe_allow_html=True,
                )

            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.markdown(
                '<div class="result-title">💬 Suggested Customer Reply</div>',
                unsafe_allow_html=True,
            )
            st.write(result["reply"])
            st.markdown("</div>", unsafe_allow_html=True)

            st.download_button(
                "↓  Download Analysis",
                data=(
                    f"CATEGORY: {result['category']}\n"
                    f"SENTIMENT: {result['sentiment']}\n"
                    f"PRIORITY: {result['priority']}\n\n"
                    f"COMPLAINT:\n{st.session_state.get('latest_complaint', '')}\n\n"
                    f"SUMMARY:\n{result['summary']}\n\n"
                    f"RESOLUTION:\n{result['resolution']}\n\n"
                    f"SUGGESTED CUSTOMER REPLY:\n{result['reply']}\n"
                ),
                file_name="complaint_analysis.txt",
                mime="text/plain",
                use_container_width=True,
            )
            st.caption(
                "Review the suggested resolution and reply before using them. "
                "The AI does not execute refunds or other business actions."
            )
        else:
            st.markdown(
                """
                <div class="empty-state">
                  <div class="empty-emoji">✨</div>
                  <div class="empty-title">Your analysis will appear here</div>
                  <div class="empty-copy">
                    Submit a complaint to see its category, sentiment, priority,
                    recommended resolution, and a customer-ready reply draft.
                  </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

with tab_history:
    st.markdown(
        '<div class="panel-heading">'
        '<div class="panel-icon">◷</div><div>'
        '<div class="panel-title">Complaint History</div>'
        '<div class="panel-subtitle">Review previous complaints and AI-generated results saved in your local database.</div>'
        '</div></div>',
        unsafe_allow_html=True,
    )

    history = get_complaint_history()
    if not history:
        st.info(
            "No complaints have been saved yet. Analyze a complaint to build your history."
        )
    else:
        filter_col, category_col = st.columns([2, 1])
        with filter_col:
            search_text = st.text_input(
                "Search complaints",
                placeholder="Search complaint, category, or summary...",
            )
        with category_col:
            categories = sorted({item["category"] for item in history})
            selected_category = st.selectbox(
                "Category filter", ["All Categories"] + categories
            )

        filtered = []
        for item in history:
            searchable = (
                f'{item["complaint"]} {item["category"]} {item["summary"]}'
            ).lower()
            matches_search = search_text.lower() in searchable
            matches_category = (
                selected_category == "All Categories"
                or item["category"] == selected_category
            )
            if matches_search and matches_category:
                filtered.append(item)

        st.caption(f"Showing {len(filtered)} of {len(history)} saved complaints")
        for item in filtered:
            title = (
                f'#{item["id"]} · {item["category"]} · '
                f'{item["priority"]} priority'
            )
            with st.expander(title):
                st.caption(
                    f'Created: {item["created_at"]} | Sentiment: {item["sentiment"]}'
                )
                st.markdown("**Original complaint**")
                st.write(item["complaint"])
                st.markdown("**Complaint summary**")
                st.write(item["summary"])
                st.markdown("**Recommended resolution**")
                st.write(item["resolution"])
                st.markdown("**Suggested customer reply**")
                st.write(item["reply"])
