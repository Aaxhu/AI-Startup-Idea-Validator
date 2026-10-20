import streamlit as st
import textwrap

def test_imports():
    assert hasattr(st, "html")
    assert hasattr(st, "markdown")

def test_dedent_no_code_block():
    html_block = textwrap.dedent("""
    <div class="hero-wrapper">
        <div class="hero-content">
            <div class="hero-badge">🧠 AI-POWERED VALIDATION</div>
            <h1 class="hero-title">Turn startup ideas into<br><span>data-driven decisions.</span></h1>
            <div class="hero-description">Analyze your startup idea using market research.</div>
            <div class="hero-pills">
                <div class="hero-pill">🧠 AI Analysis</div>
                <div class="hero-pill">🌐 Live Web Research</div>
            </div>
        </div>
    </div>
    """).strip()
    # In dedented HTML without blank lines, tags are not indented code blocks
    assert '<div class="hero-description">' in html_block
    assert '<div class="hero-pill">' in html_block
