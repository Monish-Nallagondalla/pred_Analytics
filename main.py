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

def main():
    """Main application entry point"""
    try:
        # Import the modular dashboard from src
        from dashboard.industrial_dashboard import JRManufacturingDashboard
        
        # Initialize and run the modular dashboard
        app = JRManufacturingDashboard()
        app.run()
        
    except ImportError as e:
        st.error(f"Import Error: {e}")
        st.error("Please ensure all dependencies are installed:")
        st.code("pip install -r requirements.txt")
        
        # Show requirements
        st.subheader("Required Dependencies:")
        st.code("""
streamlit>=1.28.0
pandas>=1.5.0
numpy>=1.24.0
plotly>=5.15.0
scikit-learn>=1.3.0
joblib>=1.3.0
PyYAML>=6.0
python-dateutil>=2.8.0
pytz>=2023.3
        """)
        
    except Exception as e:
        st.error(f"Application error: {e}")
        st.error("Please check the logs and try again.")
        
        # Show troubleshooting info
        st.subheader("Troubleshooting:")
        st.markdown("""
        1. **Check Dependencies**: Ensure all packages in requirements.txt are installed
        2. **Check File Structure**: Ensure src/dashboard/industrial_dashboard.py exists
        3. **Check Python Version**: Requires Python 3.8+
        4. **Restart Application**: Try restarting the Streamlit app
        """)

if __name__ == "__main__":
    main()