import streamlit as st
import textwrap

def render_html(html_code: str):
    st.html(textwrap.dedent(html_code).strip())

def test_render_html_snippets():
    # Hero snippet
    hero = """
    <div class="hero-wrapper">
        <div class="hero-content">
            <div class="hero-badge">🧠 AI-POWERED VALIDATION</div>
            <h1 class="hero-title">Turn startup ideas into<br><span>data-driven decisions.</span></h1>
            <div class="hero-description">Analyze your startup idea using market research, competitor intelligence, SWOT analysis and AI-powered strategy recommendations.</div>
            <div class="hero-pills">
                <div class="hero-pill">🧠 AI Analysis</div>
                <div class="hero-pill">🌐 Live Web Research</div>
                <div class="hero-pill">🏢 Competitor Intelligence</div>
                <div class="hero-pill">🎯 Smart Recommendations</div>
            </div>
        </div>
    </div>
    """
    render_html(hero)

    # Sidebar status snippet
    status = """
    <div class="card">
        <div class="card-title">System Status</div>
        <div style="color:#57f287;font-size:13px;font-weight:800;margin-top:10px;">● API Connected</div>
        <div style="color:#949ba4;font-size:10px;margin-top:8px;">FastAPI + Ollama + AI Pipeline</div>
    </div>
    """
    render_html(status)

    # Stat card snippet
    stat = """
    <div class="stat-card">
        <div class="stat-icon">🧠</div>
        <div class="stat-label">AI Analysis</div>
        <div class="stat-value">7+</div>
        <div class="stat-description">Analysis stages</div>
    </div>
    """
    render_html(stat)

    # Verdict card snippet
    verdict = """
    <div class="verdict-card">
        <div class="card-text">FINAL VERDICT</div>
        <div class="verdict verdict-go">GO</div>
        <div class="card-text">Confidence: <strong>8/10</strong></div>
    </div>
    """
    render_html(verdict)
