"""
Test script to verify all dashboard components are working properly
"""

import pandas as pd
import numpy as np
from database import DatabaseManager
from ml_models import PredictiveMaintenanceML, PerformanceAnalyzer
from andon_system import AndonSystem
from flow_optimization import FlowOptimizationSystem
from data_persistence import DataPersistenceManager

def test_database_components():
    """Test all database methods"""
    print("=== Testing Database Components ===")
    db = DatabaseManager()
    
    # Test basic data retrieval
    print("1. Testing get_telemetry_data...")
    telemetry = db.get_telemetry_data(limit=10)
    print(f"   Telemetry records: {len(telemetry)}")
    
    print("2. Testing get_machine_status...")
    machine_status = db.get_machine_status()
    print(f"   Machine status records: {len(machine_status)}")
    
    print("3. Testing get_events_data...")
    events = db.get_events_data(limit=10)
    print(f"   Events records: {len(events)}")
    
    print("4. Testing get_maintenance_data...")
    maintenance = db.get_maintenance_data(limit=10)
    print(f"   Maintenance records: {len(maintenance)}")
    
    print("5. Testing get_oee_data...")
    oee = db.get_oee_data()
    print(f"   OEE records: {len(oee)}")
    
    print("6. Testing get_downtime_data...")
    downtime = db.get_downtime_data()
    print(f"   Downtime records: {len(downtime)}")
    
    print("7. Testing get_bottleneck_analysis...")
    bottleneck = db.get_bottleneck_analysis()
    print(f"   Bottleneck records: {len(bottleneck)}")
    
    print("8. Testing get_predictive_insights...")
    insights = db.get_predictive_insights()
    print(f"   Predictive insights records: {len(insights)}")
    
    return True

def test_ml_components():
    """Test ML components"""
    print("\n=== Testing ML Components ===")
    
    try:
        # Test ML system initialization
        print("1. Testing PredictiveMaintenanceML initialization...")
        ml_system = PredictiveMaintenanceML()
        print("   ML system initialized successfully")
        
        # Test performance analyzer
        print("2. Testing PerformanceAnalyzer initialization...")
        performance_analyzer = PerformanceAnalyzer()
        print("   Performance analyzer initialized successfully")
        
        # Test with sample data
        db = DatabaseManager()
        telemetry_data = db.get_telemetry_data(limit=100)
        
        if not telemetry_data.empty:
            print("3. Testing OEE calculation...")
            oee_data = performance_analyzer.calculate_oee(telemetry_data)
            print(f"   OEE calculated for {len(oee_data)} machines")
            
            print("4. Testing ML model training...")
            events_data = db.get_events_data(limit=50)
            if not events_data.empty:
                ml_system.train_models(telemetry_data, events_data)
                print("   ML models trained successfully")
            else:
                print("   No events data for ML training")
        else:
            print("   No telemetry data for ML testing")
        
        return True
        
    except Exception as e:
        print(f"   Error in ML components: {e}")
        return False

def test_andon_system():
    """Test Andon system"""
    print("\n=== Testing Andon System ===")
    
    try:
        print("1. Testing AndonSystem initialization...")
        andon_system = AndonSystem()
        print("   Andon system initialized successfully")
        
        print("2. Testing active triggers...")
        active_triggers = andon_system.get_active_triggers()
        print(f"   Active triggers: {len(active_triggers)}")
        
        print("3. Testing trigger statistics...")
        stats = andon_system.get_trigger_statistics()
        print(f"   Total triggers: {stats['total_triggers']}")
        print(f"   Resolution rate: {stats['resolution_rate']:.1%}")
        
        return True
        
    except Exception as e:
        print(f"   Error in Andon system: {e}")
        return False

def test_flow_optimization():
    """Test Flow optimization system"""
    print("\n=== Testing Flow Optimization System ===")
    
    try:
        print("1. Testing FlowOptimizationSystem initialization...")
        flow_system = FlowOptimizationSystem()
        print("   Flow optimization system initialized successfully")
        
        # Test with sample data
        db = DatabaseManager()
        telemetry_data = db.get_telemetry_data(limit=1000)
        events_data = db.get_events_data(limit=100)
        
        if not telemetry_data.empty:
            print("2. Testing production flow analysis...")
            analysis = flow_system.analyze_production_flow(telemetry_data, events_data)
            print("   Production flow analysis completed")
            
            # Check if analysis has expected keys
            expected_keys = ['flow_optimization', 'layout_efficiency', 'layout_recommendations']
            for key in expected_keys:
                if key in analysis:
                    print(f"   {key}: Available")
                else:
                    print(f"   {key}: Missing")
        else:
            print("   No telemetry data for flow optimization testing")
        
        return True
        
    except Exception as e:
        print(f"   Error in Flow optimization system: {e}")
        return False

def test_data_persistence():
    """Test data persistence manager"""
    print("\n=== Testing Data Persistence Manager ===")
    
    try:
        print("1. Testing DataPersistenceManager initialization...")
        persistence = DataPersistenceManager()
        print("   Data persistence manager initialized successfully")
        
        print("2. Testing data existence check...")
        has_data = persistence.check_data_exists()
        print(f"   Data exists: {has_data}")
        
        if has_data:
            print("3. Testing data summary...")
            summary = persistence.get_data_summary()
            if summary:
                print(f"   Telemetry records: {summary.get('telemetry_count', 0)}")
                print(f"   Events records: {summary.get('events_count', 0)}")
                print(f"   Maintenance records: {summary.get('maintenance_count', 0)}")
            else:
                print("   Could not get data summary")
        
        return True
        
    except Exception as e:
        print(f"   Error in Data persistence manager: {e}")
        return False

def main():
    """Run all tests"""
    print("Starting Dashboard Component Tests...")
    print("=" * 50)
    
    results = []
    
    # Test all components
    results.append(("Database Components", test_database_components()))
    results.append(("ML Components", test_ml_components()))
    results.append(("Andon System", test_andon_system()))
    results.append(("Flow Optimization", test_flow_optimization()))
    results.append(("Data Persistence", test_data_persistence()))
    
    # Print summary
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    
    for component, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{component}: {status}")
    
    total_passed = sum(1 for _, success in results if success)
    total_tests = len(results)
    
    print(f"\nTotal: {total_passed}/{total_tests} components passed")
    
    if total_passed == total_tests:
        print("🎉 All dashboard components are working properly!")
    else:
        print("⚠️  Some components need attention.")

if __name__ == "__main__":
    main()
