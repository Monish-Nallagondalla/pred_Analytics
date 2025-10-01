#!/usr/bin/env python3
"""
Test script for Apex Components Predictive Maintenance System
Verifies all components are working correctly for prototyping
"""

import sys
import os
import traceback

def test_imports():
    """Test all module imports"""
    print("Testing imports...")
    try:
        # Test core imports
        import streamlit as st
        import pandas as pd
        import numpy as np
        import plotly.express as px
        import plotly.graph_objects as go
        from sklearn.ensemble import IsolationForest, RandomForestClassifier
        from sklearn.preprocessing import StandardScaler, LabelEncoder
        import sqlite3
        import networkx as nx
        
        # Test custom module imports
        from config import MACHINES, COMPANY_NAME, LOCATION, ALERT_THRESHOLDS
        from database import DatabaseManager
        from ml_models import PredictiveMaintenanceML, PerformanceAnalyzer
        from andon_system import AndonSystem, AndonDashboard
        from flow_optimization import FlowOptimizationSystem
        from data_generator import DataSimulator
        from dashboard import DashboardApp
        
        print("[OK] All imports successful")
        return True
    except Exception as e:
        print(f"[ERROR] Import error: {e}")
        traceback.print_exc()
        return False

def test_database():
    """Test database functionality"""
    print("Testing database...")
    try:
        db = DatabaseManager()
        stats = db.get_database_stats()
        print(f"[OK] Database initialized successfully")
        print(f"   Database stats: {stats}")
        return True
    except Exception as e:
        print(f"[ERROR] Database error: {e}")
        traceback.print_exc()
        return False

def test_andon_system():
    """Test Andon system"""
    print("Testing Andon system...")
    try:
        andon = AndonSystem()
        print(f"[OK] Andon system initialized with {len(andon.alert_rules)} rules")
        return True
    except Exception as e:
        print(f"[ERROR] Andon system error: {e}")
        traceback.print_exc()
        return False

def test_ml_models():
    """Test ML models"""
    print("Testing ML models...")
    try:
        ml_system = PredictiveMaintenanceML()
        print("[OK] ML models initialized successfully")
        return True
    except Exception as e:
        print(f"[ERROR] ML models error: {e}")
        traceback.print_exc()
        return False

def test_flow_optimization():
    """Test flow optimization"""
    print("Testing flow optimization...")
    try:
        flow_system = FlowOptimizationSystem()
        print("[OK] Flow optimization system initialized successfully")
        return True
    except Exception as e:
        print(f"[ERROR] Flow optimization error: {e}")
        traceback.print_exc()
        return False

def test_data_generator():
    """Test data generator"""
    print("Testing data generator...")
    try:
        data_simulator = DataSimulator()
        print("[OK] Data simulator initialized successfully")
        return True
    except Exception as e:
        print(f"[ERROR] Data generator error: {e}")
        traceback.print_exc()
        return False

def test_dashboard():
    """Test dashboard initialization"""
    print("Testing dashboard...")
    try:
        app = DashboardApp()
        print("[OK] Dashboard app initialized successfully")
        return True
    except Exception as e:
        print(f"[ERROR] Dashboard error: {e}")
        traceback.print_exc()
        return False

def test_configuration():
    """Test configuration"""
    print("Testing configuration...")
    try:
        from config import MACHINES, ALERT_THRESHOLDS, SIMULATION_DAYS
        
        print(f"[OK] Configuration loaded successfully")
        print(f"   Machines: {len(MACHINES)}")
        print(f"   Alert thresholds: {len(ALERT_THRESHOLDS)}")
        print(f"   Simulation days: {SIMULATION_DAYS}")
        
        # Test machine configuration
        for machine_id, config in MACHINES.items():
            print(f"   {machine_id}: {config['name']} ({config['type']})")
        
        return True
    except Exception as e:
        print(f"[ERROR] Configuration error: {e}")
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("=" * 60)
    print("APEX COMPONENTS PREDICTIVE MAINTENANCE SYSTEM - TEST SUITE")
    print("=" * 60)
    
    tests = [
        ("Configuration", test_configuration),
        ("Imports", test_imports),
        ("Database", test_database),
        ("Andon System", test_andon_system),
        ("ML Models", test_ml_models),
        ("Flow Optimization", test_flow_optimization),
        ("Data Generator", test_data_generator),
        ("Dashboard", test_dashboard)
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
        print("[SUCCESS] ALL TESTS PASSED! System is ready for prototyping.")
        print("\nTo start the dashboard, run:")
        print("streamlit run main.py")
    else:
        print("[FAILED] Some tests failed. Please fix the issues before prototyping.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
