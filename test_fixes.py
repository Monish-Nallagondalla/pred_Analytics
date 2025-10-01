#!/usr/bin/env python3
"""
Test script to verify the fixes for the dashboard issues
"""

import sys
import pandas as pd
from database import DatabaseManager
from data_persistence import DataPersistenceManager

def test_database_fixes():
    """Test that database methods accept limit parameter"""
    print("Testing database fixes...")
    
    try:
        db = DatabaseManager()
        
        # Test get_events_data with limit
        events_data = db.get_events_data(limit=10)
        print(f"[OK] get_events_data with limit works: {len(events_data)} records")
        
        # Test get_maintenance_data with limit
        maintenance_data = db.get_maintenance_data(limit=5)
        print(f"[OK] get_maintenance_data with limit works: {len(maintenance_data)} records")
        
        return True
    except Exception as e:
        print(f"[ERROR] Database test failed: {e}")
        return False

def test_data_persistence():
    """Test data persistence manager"""
    print("Testing data persistence...")
    
    try:
        manager = DataPersistenceManager()
        
        # Check if data exists
        has_data = manager.check_data_exists()
        print(f"[OK] Data exists check: {has_data}")
        
        if has_data:
            summary = manager.get_data_summary()
            if summary:
                print(f"[OK] Data summary: {summary['telemetry_count']} telemetry records")
        
        return True
    except Exception as e:
        print(f"[ERROR] Data persistence test failed: {e}")
        return False

def test_ml_models():
    """Test ML models with minimal data"""
    print("Testing ML models...")
    
    try:
        from ml_models import PredictiveMaintenanceML
        
        # Create minimal test data
        test_data = pd.DataFrame({
            'machine_id': ['VF2_01'] * 10,
            'timestamp': pd.date_range('2025-01-01', periods=10, freq='1H'),
            'vibration_rms': [0.5] * 10,
            'motor_current': [5.0] * 10,
            'servo_temp': [40.0] * 10,
            'state': ['cutting'] * 10,
            'quality_flag': ['ok'] * 10
        })
        
        test_events = pd.DataFrame({
            'machine_id': ['VF2_01'] * 5,
            'timestamp': pd.date_range('2025-01-01', periods=5, freq='2H'),
            'fault_code': [None] * 5,
            'severity': ['low'] * 5
        })
        
        ml_system = PredictiveMaintenanceML()
        
        # Test training
        ml_system.train_models(test_data, test_events)
        print(f"[OK] ML models trained: {ml_system.models_trained}")
        
        # Test predictions
        predictions = ml_system.get_comprehensive_predictions(test_data)
        print(f"[OK] ML predictions generated: {len(predictions)} predictions")
        
        return True
    except Exception as e:
        print(f"[ERROR] ML models test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("TESTING FIXES FOR DASHBOARD ISSUES")
    print("=" * 60)
    
    tests = [
        ("Database Fixes", test_database_fixes),
        ("Data Persistence", test_data_persistence),
        ("ML Models", test_ml_models)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- Testing {test_name} ---")
        if test_func():
            passed += 1
        print("-" * 40)
    
    print(f"\n{'=' * 60}")
    print(f"TEST RESULTS: {passed}/{total} tests passed")
    print(f"{'=' * 60}")
    
    if passed == total:
        print("[SUCCESS] All fixes working correctly!")
        print("The dashboard should now work without the previous errors.")
    else:
        print("[FAILED] Some tests failed. Please check the issues.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
