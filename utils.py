"""
Utility functions for the YouTube Translator and Uruguay Export Dashboard
"""

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Dict, List, Optional
import os

def create_language_options() -> Dict[str, str]:
    """Create language options for translation"""
    return {
        "Spanish": "es",
        "English": "en", 
        "Portuguese": "pt",
        "French": "fr",
        "German": "de",
        "Italian": "it",
        "Hindi": "hi",
        "Chinese": "zh",
        "Japanese": "ja",
        "Korean": "ko",
        "Russian": "ru",
        "Arabic": "ar"
    }

def validate_youtube_url(url: str) -> bool:
    """Validate YouTube URL"""
    youtube_patterns = [
        "youtube.com/watch?v=",
        "youtu.be/",
        "youtube.com/embed/",
        "m.youtube.com/watch?v="
    ]
    return any(pattern in url for pattern in youtube_patterns)

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes == 0:
        return "0B"
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    return f"{size_bytes:.1f} {size_names[i]}"

def create_export_treemap(df: pd.DataFrame, year: int = 2023) -> go.Figure:
    """Create treemap visualization for export products"""
    year_data = df[df['Year'] == year].nlargest(15, 'Export_Value_USD_Millions')
    
    fig = go.Figure(go.Treemap(
        labels=year_data['Product'],
        values=year_data['Export_Value_USD_Millions'],
        parents=[""] * len(year_data),
        textinfo="label+value",
        texttemplate="<b>%{label}</b><br>$%{value:.0f}M",
        hovertemplate="<b>%{label}</b><br>Export Value: $%{value:.0f}M<br>Market Share: %{customdata:.1f}%<extra></extra>",
        customdata=year_data['Market_Share_Percent']
    ))
    
    fig.update_layout(
        title=f"Uruguay Export Products - {year}",
        font_size=12,
        height=600
    )
    
    return fig

def create_trade_partners_chart(df: pd.DataFrame) -> go.Figure:
    """Create horizontal bar chart for trade partners"""
    top_partners = df.head(10)
    
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        y=top_partners['Country'],
        x=top_partners['Export_Value_USD_Millions'],
        name='Exports',
        orientation='h',
        marker_color='lightblue',
        text=top_partners['Export_Value_USD_Millions'],
        texttemplate='$%{text:.0f}M',
        textposition='inside'
    ))
    
    fig.update_layout(
        title="Top 10 Export Partners",
        xaxis_title="Export Value (USD Millions)",
        yaxis_title="Country",
        height=500,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig

def create_export_trends_chart(df: pd.DataFrame) -> go.Figure:
    """Create line chart for export trends over time"""
    fig = go.Figure()
    
    categories = df['Category'].unique()
    colors = px.colors.qualitative.Set3
    
    for i, category in enumerate(categories):
        category_data = df[df['Category'] == category]
        fig.add_trace(go.Scatter(
            x=category_data['Year'],
            y=category_data['Export_Value_USD_Millions'],
            mode='lines+markers',
            name=category,
            line=dict(color=colors[i % len(colors)], width=3),
            marker=dict(size=6)
        ))
    
    fig.update_layout(
        title="Uruguay Export Trends by Category (2010-2023)",
        xaxis_title="Year",
        yaxis_title="Export Value (USD Millions)",
        height=500,
        hovermode='x unified'
    )
    
    return fig

def create_complexity_scatter(df: pd.DataFrame) -> go.Figure:
    """Create product complexity vs opportunity scatter plot"""
    fig = go.Figure()
    
    # Size bubbles by RCA (Revealed Comparative Advantage)
    fig.add_trace(go.Scatter(
        x=df['complexity'],
        y=df['opportunity'],
        mode='markers+text',
        text=df['name'],
        textposition='top center',
        marker=dict(
            size=df['rca'] * 3,  # Scale RCA for bubble size
            color=df['rca'],
            colorscale='Viridis',
            showscale=True,
            colorbar=dict(title="RCA Index"),
            line=dict(width=1, color='black')
        ),
        hovertemplate="<b>%{text}</b><br>" +
                      "Complexity: %{x:.2f}<br>" +
                      "Opportunity: %{y:.2f}<br>" +
                      "RCA: %{marker.color:.1f}<extra></extra>"
    ))
    
    fig.update_layout(
        title="Product Complexity vs Export Opportunity",
        xaxis_title="Product Complexity Index",
        yaxis_title="Opportunity Gain Index",
        height=600,
        showlegend=False
    )
    
    # Add quadrant lines
    fig.add_hline(y=0.5, line_dash="dash", line_color="gray", opacity=0.5)
    fig.add_vline(x=0.5, line_dash="dash", line_color="gray", opacity=0.5)
    
    return fig

def create_trade_balance_chart(df: pd.DataFrame) -> go.Figure:
    """Create trade balance visualization"""
    top_partners = df.head(10)
    
    fig = go.Figure()
    
    # Exports
    fig.add_trace(go.Bar(
        name='Exports',
        x=top_partners['Country'],
        y=top_partners['Export_Value_USD_Millions'],
        marker_color='lightgreen'
    ))
    
    # Imports (negative for visual effect)
    fig.add_trace(go.Bar(
        name='Imports',
        x=top_partners['Country'],
        y=-top_partners['Import_Value_USD_Millions'],
        marker_color='lightcoral'
    ))
    
    fig.update_layout(
        title="Trade Balance with Top Partners",
        xaxis_title="Country",
        yaxis_title="Trade Value (USD Millions)",
        barmode='relative',
        height=500,
        xaxis_tickangle=-45
    )
    
    return fig

def display_summary_metrics(export_data: pd.DataFrame, trade_data: pd.DataFrame):
    """Display key summary metrics"""
    latest_year = export_data['Year'].max()
    latest_data = export_data[export_data['Year'] == latest_year]
    
    total_exports = latest_data['Export_Value_USD_Millions'].sum()
    top_product = latest_data.loc[latest_data['Export_Value_USD_Millions'].idxmax(), 'Product']
    top_partner = trade_data.iloc[0]['Country']
    trade_balance = trade_data['Trade_Balance_USD_Millions'].sum()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="Total Exports (2023)",
            value=f"${total_exports:,.0f}M",
            delta="2.3%"
        )
    
    with col2:
        st.metric(
            label="Top Export Product",
            value=top_product,
            delta="Leading sector"
        )
    
    with col3:
        st.metric(
            label="Top Trade Partner",
            value=top_partner,
            delta="Main destination"
        )
    
    with col4:
        st.metric(
            label="Trade Balance",
            value=f"${trade_balance:,.0f}M",
            delta="Surplus" if trade_balance > 0 else "Deficit"
        )

def create_progress_bar(current: int, total: int, text: str = ""):
    """Create a progress bar for long operations"""
    progress = current / total if total > 0 else 0
    st.progress(progress, text=f"{text} ({current}/{total})")