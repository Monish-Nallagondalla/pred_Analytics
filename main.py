"""
Main Application Entry Point for Apex Components Predictive Maintenance System
"""

import streamlit as st
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import dashboard
from dashboard import DashboardApp

def main():
    """Main application entry point"""
    try:
        # Create and run dashboard
        app = DashboardApp()
        app.run()
        
    except Exception as e:
        st.error(f"Application error: {e}")
        st.write("Please check the logs for more details.")

if __name__ == "__main__":
    main()
