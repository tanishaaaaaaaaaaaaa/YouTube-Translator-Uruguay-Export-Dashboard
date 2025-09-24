"""
Uruguay Export Data Processing
Handles data fetching and processing for Uruguay export visualizations
"""

import pandas as pd
import numpy as np
import requests
from typing import Dict, List, Optional
import streamlit as st

class UruguayExportData:
    def __init__(self):
        self.base_url = "https://oec.world/olap-proxy/data"
        self.country_code = "ury"  # Uruguay
        
    def get_sample_export_data(self) -> pd.DataFrame:
        """Generate sample Uruguay export data for demonstration"""
        # Sample data based on Uruguay's actual major exports
        products = [
            "Beef", "Soybeans", "Rice", "Wheat", "Dairy Products",
            "Wool", "Leather", "Pulp", "Fish", "Citrus Fruits",
            "Software Services", "Tourism Services", "Electricity",
            "Chemicals", "Textiles", "Wine", "Honey", "Lumber"
        ]
        
        years = list(range(2018, 2024))
        
        # Generate realistic export values (in millions USD)
        np.random.seed(42)  # For reproducible data
        
        data = []
        for year in years:
            for i, product in enumerate(products):
                # Base values with some realistic variation
                base_values = {
                    "Beef": 1500, "Soybeans": 1200, "Rice": 400, "Wheat": 300,
                    "Dairy Products": 600, "Wool": 200, "Leather": 150, "Pulp": 800,
                    "Fish": 100, "Citrus Fruits": 80, "Software Services": 500,
                    "Tourism Services": 300, "Electricity": 150, "Chemicals": 200,
                    "Textiles": 120, "Wine": 50, "Honey": 30, "Lumber": 100
                }
                
                base_value = base_values.get(product, 100)
                # Add year-over-year growth/decline
                year_factor = 1 + (year - 2018) * 0.02  # 2% annual growth
                # Add random variation
                random_factor = np.random.uniform(0.8, 1.2)
                
                value = base_value * year_factor * random_factor
                
                data.append({
                    'Year': year,
                    'Product': product,
                    'Export_Value_USD_Millions': round(value, 2),
                    'Market_Share_Percent': round(np.random.uniform(0.1, 15.0), 2)
                })
        
        return pd.DataFrame(data)
    
    def get_trade_partners_data(self) -> pd.DataFrame:
        """Generate sample trade partners data"""
        partners = [
            "China", "Brazil", "Argentina", "United States", "Germany",
            "Netherlands", "Italy", "Spain", "Russia", "India",
            "Turkey", "Egypt", "Saudi Arabia", "Japan", "South Korea"
        ]
        
        np.random.seed(42)
        data = []
        
        for partner in partners:
            # Generate realistic trade values
            base_values = {
                "China": 2000, "Brazil": 1500, "Argentina": 1200, "United States": 800,
                "Germany": 600, "Netherlands": 500, "Italy": 400, "Spain": 350,
                "Russia": 300, "India": 250, "Turkey": 200, "Egypt": 180,
                "Saudi Arabia": 150, "Japan": 120, "South Korea": 100
            }
            
            export_value = base_values.get(partner, 50) * np.random.uniform(0.8, 1.2)
            import_value = export_value * np.random.uniform(0.3, 1.5)
            
            data.append({
                'Country': partner,
                'Export_Value_USD_Millions': round(export_value, 2),
                'Import_Value_USD_Millions': round(import_value, 2),
                'Trade_Balance_USD_Millions': round(export_value - import_value, 2)
            })
        
        return pd.DataFrame(data).sort_values('Export_Value_USD_Millions', ascending=False)
    
    def get_export_trends_data(self) -> pd.DataFrame:
        """Generate export trends over time"""
        years = list(range(2010, 2024))
        
        # Major export categories
        categories = {
            'Agricultural Products': 3500,
            'Livestock Products': 2000,
            'Manufacturing': 1500,
            'Services': 1000,
            'Mining & Energy': 500
        }
        
        np.random.seed(42)
        data = []
        
        for year in years:
            for category, base_value in categories.items():
                # Simulate growth trends
                year_factor = 1 + (year - 2010) * 0.03  # 3% annual growth
                
                # Add economic cycles
                cycle_factor = 1 + 0.1 * np.sin((year - 2010) * 0.5)
                
                # Random variation
                random_factor = np.random.uniform(0.9, 1.1)
                
                value = base_value * year_factor * cycle_factor * random_factor
                
                data.append({
                    'Year': year,
                    'Category': category,
                    'Export_Value_USD_Millions': round(value, 2)
                })
        
        return pd.DataFrame(data)
    
    def get_product_complexity_data(self) -> pd.DataFrame:
        """Generate product complexity and opportunity data"""
        products = [
            {"name": "Beef", "complexity": 0.2, "opportunity": 0.3, "rca": 8.5},
            {"name": "Soybeans", "complexity": -0.1, "opportunity": 0.4, "rca": 12.3},
            {"name": "Software", "complexity": 1.8, "opportunity": 0.8, "rca": 2.1},
            {"name": "Rice", "complexity": 0.1, "opportunity": 0.2, "rca": 15.2},
            {"name": "Dairy", "complexity": 0.5, "opportunity": 0.5, "rca": 6.8},
            {"name": "Pulp", "complexity": 0.3, "opportunity": 0.3, "rca": 4.2},
            {"name": "Wool", "complexity": -0.2, "opportunity": 0.1, "rca": 25.6},
            {"name": "Leather", "complexity": 0.4, "opportunity": 0.2, "rca": 7.9},
            {"name": "Fish", "complexity": 0.1, "opportunity": 0.4, "rca": 3.2},
            {"name": "Wine", "complexity": 0.6, "opportunity": 0.6, "rca": 1.8},
            {"name": "Chemicals", "complexity": 1.2, "opportunity": 0.7, "rca": 1.5},
            {"name": "Machinery", "complexity": 1.5, "opportunity": 0.9, "rca": 0.8}
        ]
        
        return pd.DataFrame(products)
    
    @st.cache_data
    def load_all_data(_self) -> Dict[str, pd.DataFrame]:
        """Load all Uruguay export data"""
        return {
            'exports': _self.get_sample_export_data(),
            'trade_partners': _self.get_trade_partners_data(),
            'trends': _self.get_export_trends_data(),
            'complexity': _self.get_product_complexity_data()
        }