"""
Startup Script for JR Manufacturing Smart Dashboard
One-time data generation and model training
"""

import os
import sys
from datetime import datetime

def main():
    """Main startup function"""
    print("=" * 60)
    print("JR Manufacturing Smart Dashboard")
    print("Modular Predictive Maintenance System")
    print("=" * 60)
    print(f"Startup Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Check if data exists
    if os.path.exists('data/raw/machine_telemetry.csv'):
        print("SUCCESS: Data already exists")
        print("System ready! Run: streamlit run main.py")
        return True
    
    print("\nGenerating synthetic data...")
    print("This will create 30 days of realistic manufacturing data")
    
    try:
        # Generate data
        sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
        from data_generator.simple_main_generator import SimpleMainDataGenerator
        generator = SimpleMainDataGenerator()
        generator.generate_all_data(days=30)
        
        print("\nTraining ML models...")
        from ml_models.predictive_models import PredictiveMaintenanceModels
        import pandas as pd
        
        # Load data
        telemetry = pd.read_csv('data/raw/machine_telemetry.csv')
        events = pd.read_csv('data/raw/andon_alerts.csv')
        
        # Train models
        models = PredictiveMaintenanceModels()
        models.train_all_models(telemetry, events)
        
        print("\nSUCCESS: System initialization completed!")
        print("Generated 30 days of realistic industrial data")
        print("Trained all ML models")
        print("System ready! Run: streamlit run main.py")
        
        return True
        
    except Exception as e:
        print(f"\nERROR: Error during initialization: {e}")
        return False

if __name__ == "__main__":
    main()
