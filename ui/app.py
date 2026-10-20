import streamlit as st
import requests
import time
import textwrap
from datetime import datetime


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Startup Validator",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# SESSION STATE
# ============================================================

if "result" not in st.session_state:
    st.session_state.result = None

if "current_page" not in st.session_state:
    st.session_state.current_page = "🏠 Dashboard"

if "validating" not in st.session_state:
    st.session_state.validating = False


# ============================================================
# GLOBAL CSS
# ============================================================

st.markdown(
    """
    <style>

    /* ========================================================
       GLOBAL
       ======================================================== */

    html, body, [class*="css"] {
        font-family:
            Inter,
            "gg sans",
            "Noto Sans",
            "Helvetica Neue",
            Arial,
            sans-serif;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 15% 10%,
                rgba(88, 101, 242, 0.12),
                transparent 28%
            ),
            radial-gradient(
                circle at 85% 20%,
                rgba(114, 137, 218, 0.08),
                transparent 30%
            ),
            #111214;
        color: #f2f3f5;
    }

    .main {
        padding-top: 1rem;
    }

    section[data-testid="stSidebar"] {
        background: #18191c;
        border-right: 1px solid #292b2f;
    }

    section[data-testid="stSidebar"] > div {
        padding-top: 1rem;
    }

    /* Hide Streamlit branding */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header[data-testid="stHeader"] {
        background: transparent;
    }


    /* ========================================================
       SIDEBAR
       ======================================================== */

    .brand {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 8px 4px 22px 4px;
    }

    .brand-icon {
        width: 38px;
        height: 38px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, #5865f2, #7289da);
        font-size: 20px;
        box-shadow: 0 8px 25px rgba(88, 101, 242, 0.25);
    }

    .brand-title {
        font-weight: 800;
        font-size: 15px;
        color: #ffffff;
    }

    .brand-subtitle {
        font-size: 10px;
        color: #949ba4;
        margin-top: 2px;
    }

    .sidebar-heading {
        color: #b5bac1;
        font-size: 11px;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin: 8px 4px 8px;
    }


    /* ========================================================
       HERO
       ======================================================== */

    .hero-wrapper {
        position: relative;
        overflow: hidden;
        min-height: 360px;
        border-radius: 18px;
        border: 1px solid #2b2d31;
        background:
            radial-gradient(
                circle at 15% 30%,
                rgba(88, 101, 242, 0.22),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 10%,
                rgba(114, 137, 218, 0.15),
                transparent 28%
            ),
            linear-gradient(
                135deg,
                #202225,
                #18191c
            );
        padding: 52px;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.28);
        margin-bottom: 32px;
    }

    .hero-wrapper::before {
        content: "";
        position: absolute;
        width: 280px;
        height: 280px;
        right: -100px;
        bottom: -130px;
        border-radius: 50%;
        background: rgba(88, 101, 242, 0.13);
        filter: blur(20px);
    }

    .hero-content {
        position: relative;
        z-index: 2;
        max-width: 850px;
    }

    .hero-badge {
        display: inline-block;
        padding: 7px 13px;
        margin-bottom: 18px;
        border-radius: 999px;
        background: rgba(88, 101, 242, 0.14);
        border: 1px solid rgba(88, 101, 242, 0.32);
        color: #aeb7ff;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.08em;
    }

    .hero-title {
        margin: 0;
        font-size: 44px;
        line-height: 1.12;
        font-weight: 850;
        color: #ffffff;
        letter-spacing: -0.03em;
    }

    .hero-title span {
        color: #7289da;
    }

    .hero-description {
        margin-top: 20px;
        max-width: 720px;
        color: #b5bac1;
        font-size: 16px;
        line-height: 1.7;
    }

    .hero-pills {
        display: flex;
        gap: 10px;
        flex-wrap: wrap;
        margin-top: 25px;
    }

    .hero-pill {
        padding: 8px 13px;
        border-radius: 8px;
        background: #2b2d31;
        border: 1px solid #3a3d43;
        color: #dbdee1;
        font-size: 12px;
    }


    /* ========================================================
       SECTION TITLES
       ======================================================== */

    .section-title {
        color: #ffffff;
        font-size: 21px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .section-subtitle {
        color: #949ba4;
        font-size: 13px;
        margin-bottom: 20px;
    }


    /* ========================================================
       CARDS
       ======================================================== */

    .card {
        background: #1e1f22;
        border: 1px solid #2b2d31;
        border-radius: 14px;
        padding: 22px;
        margin-bottom: 16px;
        transition:
            transform 0.2s ease,
            border-color 0.2s ease,
            box-shadow 0.2s ease;
    }

    .card:hover {
        transform: translateY(-2px);
        border-color: #41444b;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.18);
    }

    .card-title {
        font-size: 14px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 8px;
    }

    .card-text {
        color: #b5bac1;
        font-size: 13px;
        line-height: 1.65;
    }


    /* ========================================================
       STAT CARDS
       ======================================================== */

    .stat-card {
        background: #1e1f22;
        border: 1px solid #2b2d31;
        border-radius: 14px;
        padding: 22px;
        min-height: 130px;
    }

    .stat-icon {
        font-size: 18px;
        margin-bottom: 10px;
    }

    .stat-label {
        color: #949ba4;
        font-size: 12px;
        font-weight: 600;
    }

    .stat-value {
        color: #ffffff;
        font-size: 24px;
        font-weight: 850;
        margin-top: 5px;
    }

    .stat-description {
        color: #72767d;
        font-size: 10px;
        margin-top: 4px;
    }


    /* ========================================================
       BADGES
       ======================================================== */

    .badge {
        display: inline-block;
        padding: 5px 9px;
        border-radius: 6px;
        font-size: 10px;
        font-weight: 800;
        text-transform: uppercase;
    }

    .badge-green {
        background: rgba(35, 165, 90, 0.15);
        color: #57f287;
    }

    .badge-yellow {
        background: rgba(254, 231, 92, 0.12);
        color: #fee75c;
    }

    .badge-red {
        background: rgba(237, 66, 69, 0.13);
        color: #ed4245;
    }

    .badge-blue {
        background: rgba(88, 101, 242, 0.15);
        color: #aeb7ff;
    }


    /* ========================================================
       VERDICT
       ======================================================== */

    .verdict-card {
        border-radius: 16px;
        padding: 28px;
        background:
            linear-gradient(
                135deg,
                rgba(88, 101, 242, 0.12),
                rgba(30, 31, 34, 0.95)
            );
        border: 1px solid #3b3f73;
        margin-bottom: 22px;
    }

    .verdict {
        font-size: 32px;
        font-weight: 900;
        margin: 5px 0 10px;
    }

    .verdict-go {
        color: #57f287;
    }

    .verdict-change {
        color: #fee75c;
    }

    .verdict-no {
        color: #ed4245;
    }


    /* ========================================================
       PIPELINE
       ======================================================== */

    .pipeline-card {
        background: #1e1f22;
        border: 1px solid #2b2d31;
        border-radius: 14px;
        padding: 20px;
        margin-bottom: 12px;
        display: flex;
        align-items: center;
        gap: 15px;
    }

    .pipeline-number {
        width: 35px;
        height: 35px;
        border-radius: 10px;
        background: #2b2d31;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 800;
        color: #b5bac1;
    }

    .pipeline-name {
        color: #ffffff;
        font-weight: 750;
        font-size: 14px;
    }

    .pipeline-description {
        color: #72767d;
        font-size: 11px;
        margin-top: 3px;
    }


    /* ========================================================
       LISTS
       ======================================================== */

    .result-item {
        background: #18191c;
        border-left: 3px solid #5865f2;
        border-radius: 7px;
        padding: 12px 14px;
        margin-bottom: 9px;
        color: #b5bac1;
        font-size: 13px;
        line-height: 1.55;
    }

    .competitor {
        background: #18191c;
        border: 1px solid #2b2d31;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
    }

    .competitor-name {
        color: #ffffff;
        font-weight: 800;
        font-size: 14px;
    }

    .competitor-description {
        color: #949ba4;
        font-size: 12px;
        line-height: 1.5;
        margin-top: 6px;
    }


    /* ========================================================
       FOOTER
       ======================================================== */

    .footer {
        text-align: center;
        color: #4e5058;
        font-size: 11px;
        padding: 35px 0 15px;
    }


    /* ========================================================
       STREAMLIT BUTTONS
       ======================================================== */

    .stButton > button {
        border-radius: 9px;
        border: 1px solid #4752c4;
        background: #5865f2;
        color: white;
        font-weight: 750;
        padding: 10px 18px;
        transition:
            background 0.2s ease,
            transform 0.2s ease;
    }

    .stButton > button:hover {
        background: #4752c4;
        transform: translateY(-1px);
    }


    /* ========================================================
       INPUTS
       ======================================================== */

    textarea,
    input {
        background: #1e1f22 !important;
        color: #ffffff !important;
        border-color: #2b2d31 !important;
    }

    textarea:focus,
    input:focus {
        border-color: #5865f2 !important;
        box-shadow: 0 0 0 1px #5865f2 !important;
    }


    /* ========================================================
       TABS
       ======================================================== */

    button[data-baseweb="tab"] {
        color: #949ba4 !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #ffffff !important;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# HELPERS
# ============================================================

BACKEND_URL = "http://127.0.0.1:8000"


def render_html(html_code: str):
    st.html(textwrap.dedent(html_code).strip())


def safe_text(value, default="Not available"):
    if value is None:
        return default

    if isinstance(value, str):
        return value

    return str(value)


def render_list(items, empty_message="No information available."):
    if not items:
        render_html(
            f"""
            <div class="result-item">
                {empty_message}
            </div>
            """
        )
        return

    for item in items:
        if isinstance(item, dict):
            text = (
                item.get("detail")
                or item.get("trend")
                or item.get("description")
                or item.get("feature")
                or item.get("stream")
                or item.get("name")
                or str(item)
            )
        else:
            text = str(item)

        render_html(
            f"""
            <div class="result-item">
                {text}
            </div>
            """
        )


def verdict_class(verdict):
    verdict = safe_text(verdict).upper()

    if verdict == "GO":
        return "verdict-go"

    if verdict == "NO-GO":
        return "verdict-no"

    return "verdict-change"


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    render_html(
        """
        <div class="brand">
            <div class="brand-icon">🚀</div>
            <div>
                <div class="brand-title">Startup Validator</div>
                <div class="brand-subtitle">AI Intelligence Platform</div>
            </div>
        </div>
        """
    )

    render_html('<div class="sidebar-heading">Workspace</div>')

    pages = [
        "🏠 Dashboard",
        "🚀 Validate Idea",
        "📈 Market Research",
        "🏢 Competitors",
        "🛡️ SWOT & Risk",
        "🧩 MVP & Strategy",
        "🎯 Recommendation",
        "📄 Full Report",
    ]

    for page in pages:
        if st.button(
            page,
            key=f"nav_{page}",
            use_container_width=True,
        ):
            st.session_state.current_page = page
            st.rerun()

    st.markdown("---")

    render_html(
        """
        <div class="card">
            <div class="card-title">System Status</div>
            <div style="color:#57f287;font-size:13px;font-weight:800;margin-top:10px;">
                ● API Connected
            </div>
            <div style="color:#949ba4;font-size:10px;margin-top:8px;">
                FastAPI + Ollama + AI Pipeline
            </div>
        </div>
        """
    )


# ============================================================
# DASHBOARD
# ============================================================

page = st.session_state.current_page


if page == "🏠 Dashboard":

    render_html(
        """
        <div class="hero-wrapper">
            <div class="hero-content">
                <div class="hero-badge">
                    🧠 AI-POWERED VALIDATION
                </div>
                <h1 class="hero-title">
                    Turn startup ideas into
                    <br>
                    <span>data-driven decisions.</span>
                </h1>
                <div class="hero-description">
                    Analyze your startup idea using market research,
                    competitor intelligence, SWOT analysis and AI-powered
                    strategy recommendations.
                </div>
                <div class="hero-pills">
                    <div class="hero-pill">🧠 AI Analysis</div>
                    <div class="hero-pill">🌐 Live Web Research</div>
                    <div class="hero-pill">🏢 Competitor Intelligence</div>
                    <div class="hero-pill">🎯 Smart Recommendations</div>
                </div>
            </div>
        </div>
        """
    )

    render_html('<div class="section-title">Your validation workspace</div>')
    render_html(
        '<div class="section-subtitle">'
        'Start by entering a startup idea and let the AI pipeline analyze it.'
        '</div>'
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        render_html(
            """
            <div class="stat-card">
                <div class="stat-icon">🧠</div>
                <div class="stat-label">AI Analysis</div>
                <div class="stat-value">7+</div>
                <div class="stat-description">
                    Analysis stages
                </div>
            </div>
            """
        )

    with col2:
        render_html(
            """
            <div class="stat-card">
                <div class="stat-icon">🌐</div>
                <div class="stat-label">Web Research</div>
                <div class="stat-value">Live</div>
                <div class="stat-description">
                    Market & competitor data
                </div>
            </div>
            """
        )

    with col3:
        render_html(
            """
            <div class="stat-card">
                <div class="stat-icon">⚡</div>
                <div class="stat-label">AI Engine</div>
                <div class="stat-value">Ollama</div>
                <div class="stat-description">
                    Local AI inference
                </div>
            </div>
            """
        )

    render_html("<br>")

    render_html(
        """
        <div class="card">
            <div class="card-title">
                🔍 How the validator works
            </div>
            <div class="card-text">
                Your idea passes through idea analysis, market research,
                competitor research, SWOT analysis, strategy generation
                and final recommendation before a complete report is produced.
            </div>
        </div>
        """
    )


# ============================================================
# VALIDATE IDEA
# ============================================================

elif page == "🚀 Validate Idea":

    render_html('<div class="section-title">🚀 Validate Your Startup Idea</div>')
    render_html(
        '<div class="section-subtitle">'
        'Describe your startup idea clearly. The AI pipeline will analyze it.'
        '</div>'
    )

    idea = st.text_area(
        "Startup Idea",
        height=180,
        placeholder=(
            "Example:\n"
            "An AI platform that helps students discover and validate "
            "startup ideas using market research, competitor analysis, "
            "SWOT analysis and personalized recommendations."
        ),
    )

    if st.button(
        "🚀 Validate Startup Idea",
        use_container_width=True,
    ):

        if not idea.strip():
            st.warning("Please enter a startup idea first.")
        else:

            st.session_state.validating = True

            progress = st.progress(0)
            status = st.empty()

            stages = [
                "Analyzing startup idea...",
                "Researching market...",
                "Finding competitors...",
                "Performing SWOT analysis...",
                "Building MVP strategy...",
                "Generating recommendation...",
                "Creating final report...",
            ]

            for i, stage in enumerate(stages):
                status.html(
                    f'<div class="card-text">⚡ {stage}</div>'
                )
                progress.progress(
                    int(((i + 1) / len(stages)) * 80)
                )
                time.sleep(0.15)

            status.info("⚡ Running multi-agent AI pipeline (this may take 2-4 minutes)...")

            try:

                response = requests.post(
                    f"{BACKEND_URL}/validate",
                    json={
                        "startup_idea": idea.strip()
                    },
                    timeout=1800,
                )

                if response.status_code == 200:

                    data = response.json()
                    st.session_state.result = data
                    progress.progress(100)
                    status.success(
                        "Validation completed successfully."
                    )
                    time.sleep(0.5)
                    st.session_state.current_page = "🎯 Recommendation"
                    st.rerun()

                else:
                    status.error(
                        f"Backend returned HTTP {response.status_code}"
                    )
                    st.error(response.text)

            except requests.exceptions.ConnectionError:
                status.error("Cannot connect to FastAPI backend.")
                st.error(
                    "Make sure the backend is running with:\n\n"
                    "`python -m uvicorn app.main:app --reload`"
                )

            except requests.exceptions.Timeout:
                status.error(
                    "The validation request timed out."
                )

            except Exception as e:
                status.error(
                    f"Validation failed: {str(e)}"
                )

            finally:
                st.session_state.validating = False


# ============================================================
# MARKET RESEARCH
# ============================================================

elif page == "📈 Market Research":

    render_html('<div class="section-title">📈 Market Research</div>')

    result = st.session_state.result

    if not result:
        st.info("Run a validation first.")
    else:
        market = result.get("market_research", {})

        col1, col2, col3 = st.columns(3)

        with col1:
            render_html(
                f"""
                <div class="stat-card">
                    <div class="stat-label">
                        Total Addressable Market
                    </div>
                    <div class="stat-value" style="font-size:18px;">
                        {safe_text(market.get("total_addressable_market"))}
                    </div>
                </div>
                """
            )

        with col2:
            render_html(
                f"""
                <div class="stat-card">
                    <div class="stat-label">
                        Market Growth
                    </div>
                    <div class="stat-value" style="font-size:18px;">
                        {safe_text(market.get("market_growth_rate"))}
                    </div>
                </div>
                """
            )

        with col3:
            render_html(
                f"""
                <div class="stat-card">
                    <div class="stat-label">
                        Market Maturity
                    </div>
                    <div class="stat-value" style="font-size:18px;">
                        {safe_text(market.get("market_maturity"))}
                    </div>
                </div>
                """
            )

        render_html(
            f"""
            <div class="card">
                <div class="card-title">Market Summary</div>
                <div class="card-text">{safe_text(market.get("summary"))}</div>
            </div>
            """
        )

        col1, col2 = st.columns(2)

        with col1:
            render_html('<div class="section-title">📊 Key Trends</div>')
            render_list(market.get("key_trends", []))

        with col2:
            render_html('<div class="section-title">💡 Opportunities</div>')
            render_list(market.get("opportunities", []))


# ============================================================
# COMPETITORS
# ============================================================

elif page == "🏢 Competitors":

    render_html('<div class="section-title">🏢 Competitor Analysis</div>')

    result = st.session_state.result

    if not result:
        st.info("Run a validation first.")
    else:
        competitors = result.get("competitor_research", {})
        intensity = safe_text(competitors.get("competitive_intensity"))

        render_html(
            f"""
            <div class="verdict-card">
                <div class="card-text">COMPETITIVE INTENSITY</div>
                <div class="verdict">{intensity}</div>
                <div class="card-text">{safe_text(competitors.get("summary"))}</div>
            </div>
            """
        )

        direct = competitors.get("direct_competitors", [])
        indirect = competitors.get("indirect_competitors", [])

        render_html(f'<div class="section-title">🎯 Direct Competitors ({len(direct)})</div>')

        for competitor in direct:
            render_html(
                f"""
                <div class="competitor">
                    <div class="competitor-name">{safe_text(competitor.get("name"))}</div>
                    <div class="competitor-description">{safe_text(competitor.get("description"))}</div>
                    <div style="margin-top:10px;color:#57f287;font-size:11px;">Strengths:</div>
                    <div class="competitor-description">{", ".join(competitor.get("strengths", [])) or "None listed"}</div>
                    <div style="margin-top:8px;color:#ed4245;font-size:11px;">Weaknesses:</div>
                    <div class="competitor-description">{", ".join(competitor.get("weaknesses", [])) or "None listed"}</div>
                </div>
                """
            )

        render_html(f'<div class="section-title">🔄 Indirect Competitors ({len(indirect)})</div>')

        for competitor in indirect:
            render_html(
                f"""
                <div class="competitor">
                    <div class="competitor-name">{safe_text(competitor.get("name"))}</div>
                    <div class="competitor-description">{safe_text(competitor.get("description"))}</div>
                </div>
                """
            )

        render_html('<div class="section-title">💡 Differentiation Opportunities</div>')
        render_list(competitors.get("differentiation_opportunities", []))

        render_html('<div class="section-title">🔎 Market Gaps</div>')
        render_list(competitors.get("market_gaps", []))


# ============================================================
# SWOT
# ============================================================

elif page == "🛡️ SWOT & Risk":

    render_html('<div class="section-title">🛡️ SWOT & Risk Analysis</div>')

    result = st.session_state.result

    if not result:
        st.info("Run a validation first.")
    else:
        swot = result.get("swot_analysis", {})

        render_html(
            f"""
            <div class="verdict-card">
                <div class="card-text">OVERALL VIABILITY</div>
                <div class="verdict verdict-go">{safe_text(swot.get("overall_viability"))}</div>
                <div class="card-text">{safe_text(swot.get("summary"))}</div>
            </div>
            """
        )

        c1, c2 = st.columns(2)

        with c1:
            render_html('<div class="section-title">💪 Strengths</div>')
            render_list(swot.get("strengths", []))

            render_html('<div class="section-title">⚠️ Weaknesses</div>')
            render_list(swot.get("weaknesses", []))

        with c2:
            render_html('<div class="section-title">🚀 Opportunities</div>')
            render_list(swot.get("opportunities", []))

            render_html('<div class="section-title">🔥 Threats</div>')
            render_list(swot.get("threats", []))

        render_html(
            f"""
            <div class="card">
                <div class="card-title">🚨 Key Risk</div>
                <div style="color:#ed4245;font-size:15px;font-weight:750;line-height:1.6;">
                    {safe_text(swot.get("key_risk"))}
                </div>
            </div>
            """
        )


# ============================================================
# MVP & STRATEGY
# ============================================================

elif page == "🧩 MVP & Strategy":

    render_html('<div class="section-title">🧩 MVP & Business Strategy</div>')

    result = st.session_state.result

    if not result:
        st.info("Run a validation first.")
    else:
        strategy = result.get("strategy", {})

        col1, col2 = st.columns(2)

        with col1:
            render_html(
                f"""
                <div class="stat-card">
                    <div class="stat-label">MVP Timeline</div>
                    <div class="stat-value">{safe_text(strategy.get("mvp_timeline_weeks"))}</div>
                    <div class="stat-description">weeks</div>
                </div>
                """
            )

        with col2:
            render_html(
                f"""
                <div class="stat-card">
                    <div class="stat-label">Burn Rate Estimate</div>
                    <div class="stat-value" style="font-size:18px;">
                        {safe_text(strategy.get("burn_rate_estimate"))}
                    </div>
                </div>
                """
            )

        render_html('<div class="section-title">🛠️ MVP Features</div>')

        for feature in strategy.get("mvp_plan", []):
            render_html(
                f"""
                <div class="card">
                    <div class="card-title">{safe_text(feature.get("feature"))}</div>
                    <span class="badge badge-blue">{safe_text(feature.get("priority"))}</span>
                    <div class="card-text" style="margin-top:10px;">
                        {safe_text(feature.get("rationale"))}
                    </div>
                </div>
                """
            )

        c1, c2 = st.columns(2)

        with c1:
            render_html('<div class="section-title">💰 Revenue Streams</div>')
            for revenue in strategy.get("revenue_streams", []):
                render_html(
                    f"""
                    <div class="result-item">
                        <strong>{safe_text(revenue.get("stream"))}</strong>
                        <br>
                        Model: {safe_text(revenue.get("model"))}
                    </div>
                    """
                )

        with c2:
            render_html('<div class="section-title">📣 Acquisition Channels</div>')
            render_list(strategy.get("customer_acquisition_channels", []))

        render_html(
            f"""
            <div class="card">
                <div class="card-title">🚀 Go-To-Market Strategy</div>
                <div class="card-text">{safe_text(strategy.get("go_to_market_strategy"))}</div>
            </div>
            """
        )

        render_html(
            f"""
            <div class="card">
                <div class="card-title">📈 Growth Plan</div>
                <div class="card-text">{safe_text(strategy.get("growth_plan"))}</div>
            </div>
            """
        )


# ============================================================
# RECOMMENDATION
# ============================================================

elif page == "🎯 Recommendation":

    render_html('<div class="section-title">🎯 Final Recommendation</div>')

    result = st.session_state.result

    if not result:
        st.info("Run a validation first.")
    else:
        recommendation = result.get("final_recommendation", {})
        verdict = safe_text(recommendation.get("verdict"))
        css_class = verdict_class(verdict)

        render_html(
            f"""
            <div class="verdict-card">
                <div class="card-text">FINAL VERDICT</div>
                <div class="verdict {css_class}">{verdict}</div>
                <div class="card-text">
                    Confidence: <strong>{safe_text(recommendation.get("confidence"))}/10</strong>
                </div>
            </div>
            """
        )

        render_html(
            f"""
            <div class="card">
                <div class="card-title">🧠 Rationale</div>
                <div class="card-text">{safe_text(recommendation.get("rationale"))}</div>
            </div>
            """
        )

        render_html('<div class="section-title">🔥 Top 3 Priorities</div>')

        priorities = recommendation.get("top_3_priorities", [])

        for index, priority in enumerate(priorities[:3], start=1):
            render_html(
                f"""
                <div class="pipeline-card">
                    <div class="pipeline-number">{index}</div>
                    <div>
                        <div class="pipeline-name">{safe_text(priority)}</div>
                    </div>
                </div>
                """
            )

        render_html(
            f"""
            <div class="card">
                <div class="card-title">🚨 Biggest Risk</div>
                <div style="color:#ed4245;font-weight:750;font-size:15px;">
                    {safe_text(recommendation.get("biggest_risk"))}
                </div>
            </div>
            """
        )


# ============================================================
# FULL REPORT
# ============================================================

elif page == "📄 Full Report":

    render_html('<div class="section-title">📄 Full Validation Report</div>')

    result = st.session_state.result

    if not result:
        st.info("Run a validation first.")
    else:
        report = result.get("report", "No report available.")

        st.markdown(report)

        st.download_button(
            label="⬇️ Download Report",
            data=report,
            file_name="startup_validation_report.md",
            mime="text/markdown",
            use_container_width=True,
        )


# ============================================================
# FOOTER
# ============================================================

render_html(
    """
    <div class="footer">
        AI Startup Idea Validator
        • FastAPI
        • Ollama
        • Live Web Research
        • Multi-Agent AI Pipeline
    </div>
    """
)