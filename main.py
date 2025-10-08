"""
JR Manufacturing Smart Dashboard - Main Entry Point
Industrial predictive maintenance system for Sheet Metal Fabrication & Injection Moulding
"""

import streamlit as st
import sys
import os
from datetime import datetime

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))

# Import the modular dashboard from src
from dashboard.industrial_dashboard import JRManufacturingDashboard

def main():
    """Main application entry point"""
    try:
        # Initialize and run the modular dashboard
        app = JRManufacturingDashboard()
        app.run()
    except Exception as e:
        st.error(f"Application error: {e}")
        st.error("Please check the logs and try again.")

if __name__ == "__main__":
    main()