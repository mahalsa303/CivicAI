"""
Hero and Onboarding Component for CivicAI.

Provides a client-side auto-rotating campaign spotlight carousel, a premium glassmorphic
landing experience block with custom illustration, and modern feature card highlights.
"""

import base64
import os
import streamlit as st


def get_base64_image(image_path: str) -> str:
    """
    Encodes a local file to a base64 string for inline HTML rendering.
    """
    if os.path.exists(image_path):
        try:
            with open(image_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode("utf-8")
        except Exception:
            return ""
    return ""


def render_hero():
    """
    Renders the dynamic auto-rotating campaign spotlight banners and the premium onboarding hero card.
    """
    # 1. RENDER AUTO-ROTATING SPOTLIGHT CAROUSEL WITH 5 SLIDES & 5 DOTS
    st.markdown("""
        <div class="hero-banner-carousel" id="heroCarousel">
            <div class="slides-container">
                <div class="hero-slide active" style="background: linear-gradient(135deg, #10B981 0%, #059669 100%);">
                    <h2>Clean City Campaign 🌱</h2>
                    <p>Help keep our streets clean! Report uncollected waste and overflowing garbage bins instantly.</p>
                </div>
                <div class="hero-slide" style="background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);">
                    <h2>Road Safety Week 🚦</h2>
                    <p>Potholes and broken lights pose immediate risks. File reports to alert municipal road services.</p>
                </div>
                <div class="hero-slide" style="background: linear-gradient(135deg, #3B82F6 0%, #2563EB 100%);">
                    <h2>Water Conservation Drive 💧</h2>
                    <p>Report leaking pipelines. Help us conserve community water resources.</p>
                </div>
                <div class="hero-slide" style="background: linear-gradient(135deg, #6D28D9 0%, #4F46E5 100%);">
                    <h2>Citizen Awareness Portal 📢</h2>
                    <p>Leverage Gemini AI to file formal complaints and track local government resolutions.</p>
                </div>
                <div class="hero-slide" style="background: linear-gradient(135deg, #EC4899 0%, #BE185D 100%);">
                    <h2>Green Campus Initiative 🌳</h2>
                    <p>Plant trees and keep parks clear. Submit maintenance logs to sustain local community gardens.</p>
                </div>
            </div>
            
            <div class="carousel-indicators">
                <span class="dot active" data-slide="0"></span>
                <span class="dot" data-slide="1"></span>
                <span class="dot" data-slide="2"></span>
                <span class="dot" data-slide="3"></span>
                <span class="dot" data-slide="4"></span>
            </div>
        </div>

        <script>
        (function() {
            const container = window.parent.document.getElementById("heroCarousel");
            if (!container) return;
            
            // Prevent multiple initializations
            if (container.dataset.initialized) return;
            container.dataset.initialized = "true";

            const slides = container.querySelectorAll(".hero-slide");
            const dots = container.querySelectorAll(".dot");
            let currentIndex = 0;
            let timer = null;

            function showSlide(index) {
                slides[currentIndex].classList.remove("active");
                dots[currentIndex].classList.remove("active");
                currentIndex = index;
                slides[currentIndex].classList.add("active");
                dots[currentIndex].classList.add("active");
            }

            function nextSlide() {
                let nextIndex = (currentIndex + 1) % slides.length;
                showSlide(nextIndex);
            }

            function startAutoScroll() {
                if (timer === null) {
                    timer = setInterval(nextSlide, 3000);
                }
            }

            function stopAutoScroll() {
                if (timer !== null) {
                    clearInterval(timer);
                    timer = null;
                }
            }

            dots.forEach((dot, idx) => {
                dot.addEventListener("click", () => {
                    showSlide(idx);
                });
            });

            container.addEventListener("mouseenter", stopAutoScroll);
            container.addEventListener("mouseleave", startAutoScroll);

            startAutoScroll();
        })();
        </script>
    """, unsafe_allow_html=True)

    # 2. RENDER PREMIUM GLASSMORPHIC HERO SECTION
    st.markdown('<div class="premium-hero-anchor"></div>', unsafe_allow_html=True)
    
    col_hero_left, col_hero_right = st.columns([1.4, 1.0])
    
    with col_hero_left:
        st.markdown('<h1 class="hero-title">Report Smarter.<br>Resolve Faster.</h1>', unsafe_allow_html=True)
        st.markdown(
            '<p class="hero-desc">CivicAI uses Gemini AI to help citizens report, verify, analyze and resolve civic issues faster than traditional reporting systems.</p>',
            unsafe_allow_html=True
        )
        
        # Primary & Secondary styled buttons using sub-columns and anchors
        btn_col1, btn_col2 = st.columns([1, 1.2])
        with btn_col1:
            st.markdown('<div class="hero-btn-primary-anchor"></div>', unsafe_allow_html=True)
            if st.button("🚨 Report Issue", key="hero_report_btn", use_container_width=True):
                st.switch_page("pages/report_issue.py")
        with btn_col2:
            st.markdown('<div class="hero-btn-secondary-anchor"></div>', unsafe_allow_html=True)
            if st.button("📊 Explore Dashboard", key="hero_explore_btn", use_container_width=True):
                st.switch_page("pages/analytics.py")

    with col_hero_right:
        # Load and render base64 illustration with floating smart city icons
        illustration_b64 = get_base64_image("assets/hero_illustration.png")
        if illustration_b64:
            st.markdown(f"""
                <div style="position: relative; width: 100%; height: 100%; min-height: 240px; display: flex; justify-content: center; align-items: center; overflow: visible;">
                    <div class="floating-icon icon-road">🛣️</div>
                    <div class="floating-icon icon-tree">🌳</div>
                    <div class="floating-icon icon-lamp">💡</div>
                    <div class="floating-icon icon-building">🏢</div>
                    <div class="floating-icon icon-water">💧</div>
                    <div class="floating-icon icon-ai">🤖</div>
                    <img src="data:image/png;base64,{illustration_b64}" style="max-height: 240px; max-width: 100%; object-fit: contain; z-index: 1;" alt="Smart City AI illustration"/>
                </div>
            """, unsafe_allow_html=True)
        else:
            # Fallback illustration placeholder
            st.markdown("""
                <div style="display: flex; justify-content: center; align-items: center; height: 100%; min-height: 240px; color: var(--text-muted); font-size: 80px;">
                    🏙️
                </div>
            """, unsafe_allow_html=True)

    # 3. ONBOARDING FEATURE CARDS Highlight
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            <div class="saas-card glass-panel" style="text-align: center; height: 100%;">
                <div style="font-size: 36px; margin-bottom: 12px;">🤖</div>
                <h4 style="font-weight:700; color: var(--text-main); margin-bottom:8px; font-size: 16px;">AI Issue Analysis</h4>
                <p style="color: var(--text-muted); font-size:13px; line-height:1.45; margin-bottom: 0;">
                    Gemini AI automatically parses descriptions and images, assessing priority, estimating repair cost, and routing to the proper department.
                </p>
            </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
            <div class="saas-card glass-panel" style="text-align: center; height: 100%;">
                <div style="font-size: 36px; margin-bottom: 12px;">🗺</div>
                <h4 style="font-weight:700; color: var(--text-main); margin-bottom:8px; font-size: 16px;">Real-Time Map</h4>
                <p style="color: var(--text-muted); font-size:13px; line-height:1.45; margin-bottom: 0;">
                    Visualise active reports geographically. Markers are colored dynamically based on severity: Red (High), Orange (Medium), Green (Low).
                </p>
            </div>
        """, unsafe_allow_html=True)
        
    with col3:
        st.markdown("""
            <div class="saas-card glass-panel" style="text-align: center; height: 100%;">
                <div style="font-size: 36px; margin-bottom: 12px;">📊</div>
                <h4 style="font-weight:700; color: var(--text-main); margin-bottom:8px; font-size: 16px;">Smart Insights</h4>
                <p style="color: var(--text-muted); font-size:13px; line-height:1.45; margin-bottom: 0;">
                    Dynamic analytics distributions, risk levels, coordinate hotspots clustering, and weekly/monthly trends for local planning.
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

