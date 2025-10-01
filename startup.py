#!/usr/bin/env python3
"""
Startup script for Apex Components Predictive Maintenance System
Ensures data is generated only once and system is ready for use
"""

import os
import sys
from data_persistence import DataPersistenceManager

def check_system_requirements():
    """Check if all required files exist"""
    required_files = [
        'main.py',
        'dashboard.py',
        'database.py',
        'ml_models.py',
        'andon_system.py',
        'flow_optimization.py',
        'data_generator.py',
        'config.py',
        'requirements.txt'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing required files: {', '.join(missing_files)}")
        return False
    
    print("✅ All required files present")
    return True

def ensure_sample_data():
    """Ensure sample data exists, generate if needed"""
    print("📊 Checking for sample data...")
    
    manager = DataPersistenceManager()
    
    if manager.check_data_exists():
        summary = manager.get_data_summary()
        if summary:
            print(f"✅ Sample data already exists:")
            print(f"   • Telemetry: {summary['telemetry_count']} records")
            print(f"   • Events: {summary['events_count']} records")
            print(f"   • Maintenance: {summary['maintenance_count']} records")
            
            if summary.get('metadata'):
                metadata = summary['metadata']
                print(f"   • Generated: {metadata.get('days', 'Unknown')} days")
                print(f"   • Created: {metadata.get('generated_at', 'Unknown')}")
        return True
    else:
        print("📊 No sample data found. Generating 7 days of sample data...")
        success = manager.generate_data_once(7)
        if success:
            print("✅ Sample data generated successfully!")
            return True
        else:
            print("❌ Failed to generate sample data")
            return False

def main():
    """Main startup function"""
    print("=" * 60)
    print("APEX COMPONENTS PREDICTIVE MAINTENANCE SYSTEM - STARTUP")
    print("=" * 60)
    
    # Check system requirements
    if not check_system_requirements():
        print("❌ System requirements not met. Please check missing files.")
        return 1
    
    # Ensure sample data exists
    if not ensure_sample_data():
        print("❌ Failed to ensure sample data. Please check system.")
        return 1
    
    print("\n🎉 System is ready!")
    print("\nTo start the dashboard, run:")
    print("streamlit run main.py")
    print("\nOr to run the test suite:")
    print("python test_system.py")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
