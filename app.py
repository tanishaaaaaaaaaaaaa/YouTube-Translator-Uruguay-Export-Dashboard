"""
YouTube Speech Translator + Uruguay Export Data Dashboard
Combined web application with video translation and data visualization
NO PYDUB DEPENDENCY VERSION
"""

import streamlit as st
import os
import time
from pathlib import Path
import logging

# Import our modules
from youtube_translator import FixedYouTubeTranslatorNoPyAudio
from uruguay_data import UruguayExportData
from utils import (
    create_language_options, validate_youtube_url, format_file_size,
    create_export_treemap, create_trade_partners_chart, create_export_trends_chart,
    create_complexity_scatter, create_trade_balance_chart, display_summary_metrics
)

# Page configuration
st.set_page_config(
    page_title="YouTube Translator & Uruguay Export Dashboard",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-bottom: 2rem;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .section-header {
        font-size: 1.8rem;
        font-weight: bold;
        margin: 2rem 0 1rem 0;
        color: #2c3e50;
        border-bottom: 2px solid #3498db;
        padding-bottom: 0.5rem;
    }
    
    .info-box {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3498db;
        margin: 1rem 0;
    }
    
    .success-box {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    
    .error-box {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Main header
    st.markdown('<h1 class="main-header">🎬 YouTube Translator & 🇺🇾 Uruguay Export Dashboard</h1>', unsafe_allow_html=True)
    
    # Sidebar navigation
    st.sidebar.title("Navigation")
    app_mode = st.sidebar.selectbox(
        "Choose Application Mode",
        ["🏠 Home", "🎥 YouTube Translator", "📊 Uruguay Export Data", "ℹ️ About"]
    )
    
    if app_mode == "🏠 Home":
        show_home_page()
    elif app_mode == "🎥 YouTube Translator":
        show_translator_page()
    elif app_mode == "📊 Uruguay Export Data":
        show_export_dashboard()
    elif app_mode == "ℹ️ About":
        show_about_page()

def show_home_page():
    """Display the home page with overview of both applications"""
    st.markdown('<div class="section-header">Welcome to the Integrated Platform</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🎥 YouTube Speech Translator
        
        Transform any YouTube video by translating its speech into different languages:
        
        - **Download** YouTube videos automatically
        - **Transcribe** speech using OpenAI Whisper
        - **Translate** to 12+ languages
        - **Generate** new audio with translated speech
        - **Create** final video with translated audio
        
        **Supported Languages:**
        Spanish, English, Portuguese, French, German, Italian, Hindi, Chinese, Japanese, Korean, Russian, Arabic
        """)
        
        if st.button("🚀 Start Translating Videos", type="primary"):
            st.switch_page("app.py")
    
    with col2:
        st.markdown("""
        ### 📊 Uruguay Export Dashboard
        
        Explore Uruguay's international trade data with interactive visualizations:
        
        - **Export Products** analysis with treemap visualization
        - **Trade Partners** ranking and relationships
        - **Trends Analysis** over time (2010-2023)
        - **Product Complexity** vs opportunity mapping
        - **Trade Balance** with major partners
        
        **Key Insights:**
        - Agricultural products dominate exports
        - China and Brazil are top partners
        - Growing services sector exports
        """)
        
        if st.button("📈 Explore Export Data", type="primary"):
            st.switch_page("app.py")
    
    # Quick stats
    st.markdown('<div class="section-header">Platform Statistics</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Supported Languages", "12+", "Translation")
    
    with col2:
        st.metric("Data Years", "2010-2023", "Export Data")
    
    with col3:
        st.metric("Export Products", "18+", "Categories")
    
    with col4:
        st.metric("Trade Partners", "15+", "Countries")

def show_translator_page():
    """Display the YouTube translator interface"""
    st.markdown('<div class="section-header">🎥 YouTube Speech Translator</div>', unsafe_allow_html=True)
    
    # Information box
    st.markdown("""
    <div class="info-box">
        <strong>How it works:</strong> Enter a YouTube URL, select target language, and get a translated video with new audio track.
        Processing time depends on video length (typically 2-5 minutes for short videos).
        <br><br>
        <strong>Note:</strong> This version uses FFmpeg directly for audio processing to avoid dependency issues.
    </div>
    """, unsafe_allow_html=True)
    
    # Input form
    with st.form("translation_form"):
        col1, col2 = st.columns([2, 1])
        
        with col1:
            youtube_url = st.text_input(
                "YouTube URL",
                placeholder="https://www.youtube.com/watch?v=...",
                help="Paste the full YouTube video URL here"
            )
        
        with col2:
            language_options = create_language_options()
            target_language = st.selectbox(
                "Target Language",
                options=list(language_options.keys()),
                index=0
            )
        
        video_name = st.text_input(
            "Custom Video Name (Optional)",
            placeholder="my_translated_video",
            help="Leave empty for auto-generated name"
        )
        
        submit_button = st.form_submit_button("🚀 Start Translation", type="primary")
    
    # Process translation
    if submit_button:
        if not youtube_url:
            st.error("Please enter a YouTube URL")
            return
        
        if not validate_youtube_url(youtube_url):
            st.error("Please enter a valid YouTube URL")
            return
        
        # Initialize translator
        try:
            with st.spinner("Initializing translator (FFmpeg-based audio processing)..."):
                translator = FixedYouTubeTranslatorNoPyAudio(
                    output_dir="output",
                    temp_dir="temp"
                )
            
            st.success("✅ Translator initialized successfully!")
            
            # Start translation process
            language_code = language_options[target_language]
            
            with st.spinner(f"Translating video to {target_language}... This may take several minutes."):
                # Create progress placeholder
                progress_placeholder = st.empty()
                status_placeholder = st.empty()
                
                # Show progress updates
                progress_placeholder.progress(0.1, "Downloading video...")
                time.sleep(1)
                
                progress_placeholder.progress(0.3, "Extracting audio with FFmpeg...")
                time.sleep(1)
                
                progress_placeholder.progress(0.5, "Transcribing speech...")
                time.sleep(1)
                
                progress_placeholder.progress(0.7, "Translating text...")
                time.sleep(1)
                
                progress_placeholder.progress(0.9, "Generating final video...")
                
                # Run actual translation
                result = translator.translate_video(
                    url=youtube_url,
                    target_language=language_code,
                    video_name=video_name
                )
                
                progress_placeholder.progress(1.0, "Complete!")
            
            if result:
                st.markdown("""
                <div class="success-box">
                    <strong>🎉 Translation completed successfully!</strong><br>
                    Your translated video is ready for download.
                </div>
                """, unsafe_allow_html=True)
                
                # Display file info
                if os.path.exists(result):
                    file_size = os.path.getsize(result)
                    st.info(f"📁 **File:** {os.path.basename(result)}")
                    st.info(f"📊 **Size:** {format_file_size(file_size)}")
                    st.info(f"🎯 **Language:** {target_language}")
                    
                    # Download button
                    with open(result, "rb") as file:
                        st.download_button(
                            label="⬇️ Download Translated Video",
                            data=file.read(),
                            file_name=os.path.basename(result),
                            mime="video/mp4",
                            type="primary"
                        )
                else:
                    st.error("Output file not found. Please try again.")
            else:
                st.markdown("""
                <div class="error-box">
                    <strong>❌ Translation failed!</strong><br>
                    Please check the video URL and try again. Some videos may not be available for processing.
                </div>
                """, unsafe_allow_html=True)
        
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.info("Please try again or contact support if the problem persists.")
    
    # Recent translations (if any)
    output_dir = Path("output")
    if output_dir.exists():
        video_files = list(output_dir.glob("*.mp4"))
        if video_files:
            st.markdown('<div class="section-header">Recent Translations</div>', unsafe_allow_html=True)
            
            for video_file in sorted(video_files, key=lambda x: x.stat().st_mtime, reverse=True)[:5]:
                col1, col2, col3 = st.columns([2, 1, 1])
                
                with col1:
                    st.text(video_file.name)
                
                with col2:
                    st.text(format_file_size(video_file.stat().st_size))
                
                with col3:
                    with open(video_file, "rb") as file:
                        st.download_button(
                            label="⬇️ Download",
                            data=file.read(),
                            file_name=video_file.name,
                            mime="video/mp4",
                            key=f"download_{video_file.name}"
                        )

def show_export_dashboard():
    """Display the Uruguay export data dashboard"""
    st.markdown('<div class="section-header">📊 Uruguay Export Data Dashboard</div>', unsafe_allow_html=True)
    
    # Load data
    @st.cache_data
    def load_data():
        data_loader = UruguayExportData()
        return data_loader.load_all_data()
    
    try:
        with st.spinner("Loading Uruguay export data..."):
            data = load_data()
        
        export_data = data['exports']
        trade_partners = data['trade_partners']
        trends_data = data['trends']
        complexity_data = data['complexity']
        
        # Summary metrics
        display_summary_metrics(export_data, trade_partners)
        
        # Main dashboard tabs
        tab1, tab2, tab3, tab4 = st.tabs([
            "🌳 Export Products", 
            "🌍 Trade Partners", 
            "📈 Trends Analysis", 
            "🎯 Product Complexity"
        ])
        
        with tab1:
            st.subheader("Export Products Overview")
            
            # Year selector
            years = sorted(export_data['Year'].unique(), reverse=True)
            selected_year = st.selectbox("Select Year", years, index=0)
            
            # Treemap visualization
            treemap_fig = create_export_treemap(export_data, selected_year)
            st.plotly_chart(treemap_fig, use_container_width=True)
            
            # Top products table
            year_data = export_data[export_data['Year'] == selected_year].nlargest(10, 'Export_Value_USD_Millions')
            
            st.subheader(f"Top 10 Export Products - {selected_year}")
            st.dataframe(
                year_data[['Product', 'Export_Value_USD_Millions', 'Market_Share_Percent']].rename(columns={
                    'Product': 'Product',
                    'Export_Value_USD_Millions': 'Export Value (USD Millions)',
                    'Market_Share_Percent': 'Market Share (%)'
                }),
                use_container_width=True
            )
        
        with tab2:
            st.subheader("Trade Partners Analysis")
            
            # Trade partners chart
            partners_fig = create_trade_partners_chart(trade_partners)
            st.plotly_chart(partners_fig, use_container_width=True)
            
            # Trade balance chart
            balance_fig = create_trade_balance_chart(trade_partners)
            st.plotly_chart(balance_fig, use_container_width=True)
            
            # Partners table
            st.subheader("Trade Partners Details")
            st.dataframe(
                trade_partners.rename(columns={
                    'Country': 'Country',
                    'Export_Value_USD_Millions': 'Exports (USD Millions)',
                    'Import_Value_USD_Millions': 'Imports (USD Millions)',
                    'Trade_Balance_USD_Millions': 'Trade Balance (USD Millions)'
                }),
                use_container_width=True
            )
        
        with tab3:
            st.subheader("Export Trends Over Time")
            
            # Trends chart
            trends_fig = create_export_trends_chart(trends_data)
            st.plotly_chart(trends_fig, use_container_width=True)
            
            # Category analysis
            st.subheader("Growth Analysis by Category")
            
            # Calculate growth rates
            latest_year = trends_data['Year'].max()
            previous_year = latest_year - 1
            
            latest_data = trends_data[trends_data['Year'] == latest_year].set_index('Category')
            previous_data = trends_data[trends_data['Year'] == previous_year].set_index('Category')
            
            growth_data = []
            for category in latest_data.index:
                if category in previous_data.index:
                    latest_value = latest_data.loc[category, 'Export_Value_USD_Millions']
                    previous_value = previous_data.loc[category, 'Export_Value_USD_Millions']
                    growth_rate = ((latest_value - previous_value) / previous_value) * 100
                    
                    growth_data.append({
                        'Category': category,
                        f'{latest_year} Value (USD Millions)': latest_value,
                        f'{previous_year} Value (USD Millions)': previous_value,
                        'Growth Rate (%)': round(growth_rate, 2)
                    })
            
            if growth_data:
                st.dataframe(growth_data, use_container_width=True)
        
        with tab4:
            st.subheader("Product Complexity Analysis")
            
            st.markdown("""
            This chart shows the relationship between product complexity and export opportunity:
            - **X-axis**: Product Complexity Index (higher = more complex products)
            - **Y-axis**: Opportunity Gain Index (higher = better growth potential)
            - **Bubble size**: Revealed Comparative Advantage (RCA)
            """)
            
            # Complexity scatter plot
            complexity_fig = create_complexity_scatter(complexity_data)
            st.plotly_chart(complexity_fig, use_container_width=True)
            
            # Complexity table
            st.subheader("Product Complexity Details")
            complexity_display = complexity_data.copy()
            complexity_display = complexity_display.sort_values('rca', ascending=False)
            
            st.dataframe(
                complexity_display.rename(columns={
                    'name': 'Product',
                    'complexity': 'Complexity Index',
                    'opportunity': 'Opportunity Index',
                    'rca': 'RCA Index'
                }),
                use_container_width=True
            )
        
        # Data source information
        st.markdown("---")
        st.markdown("""
        **Data Sources:**
        - Export data based on Uruguay's trade statistics
        - Product complexity data derived from international trade patterns
        - Trade partner information from bilateral trade records
        
        **Note:** This dashboard uses representative sample data for demonstration purposes.
        """)
    
    except Exception as e:
        st.error(f"Error loading export data: {str(e)}")
        st.info("Please refresh the page or contact support if the problem persists.")

def show_about_page():
    """Display information about the application"""
    st.markdown('<div class="section-header">ℹ️ About This Platform</div>', unsafe_allow_html=True)
    
    st.markdown("""
    ## 🎬 YouTube Speech Translator (FFmpeg Version)
    
    This application provides automated video translation services using cutting-edge AI technologies:
    
    ### 🔧 Technical Stack
    - **yt-dlp**: Robust YouTube video downloading
    - **OpenAI Whisper**: State-of-the-art speech recognition
    - **Google Translate API**: Accurate text translation
    - **Google Text-to-Speech**: Natural voice synthesis
    - **FFmpeg**: Professional video/audio processing (no pydub dependency)
    - **Streamlit**: Modern web interface
    
    ### 🚀 Features
    - Automatic video download from YouTube
    - Multi-language speech recognition
    - High-quality text translation
    - Natural voice synthesis
    - Professional video merging
    - Progress tracking and error handling
    - **No pyaudioop dependency** - uses FFmpeg directly
    
    ---
    
    ## 📊 Uruguay Export Dashboard
    
    Interactive visualization platform for Uruguay's international trade data:
    
    ### 📈 Visualizations
    - **Treemap**: Export products by value
    - **Bar Charts**: Trade partner rankings
    - **Line Charts**: Trends over time
    - **Scatter Plot**: Product complexity analysis
    - **Trade Balance**: Import/export comparison
    
    ### 🔍 Data Insights
    - Agricultural products dominate exports
    - China and Brazil are key trade partners
    - Services sector showing growth
    - Product diversification opportunities
    
    ---
    
    ## 🛠️ System Requirements
    
    ### For Video Translation:
    - FFmpeg installed on system
    - Sufficient disk space for video processing
    - Stable internet connection
    - Modern web browser
    
    ### Supported Languages:
    Spanish, English, Portuguese, French, German, Italian, Hindi, Chinese, Japanese, Korean, Russian, Arabic
    
    ---
    
    ## 📞 Support & Contact
    
    For technical support or feature requests:
    - Check the error messages for troubleshooting
    - Ensure all system requirements are met
    - Try refreshing the page for temporary issues
    
    **Version:** 1.1.0 (FFmpeg Direct Processing)  
    **Last Updated:** 2024
    """)

if __name__ == "__main__":
    main()