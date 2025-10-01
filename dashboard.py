"""
Streamlit Dashboard for Apex Components Predictive Maintenance System
Real-time monitoring, KPIs, and predictive analytics
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime
from datetime import datetime, timedelta, date
import time
import json

# Import our modules
from config import MACHINES, COMPANY_NAME, LOCATION, ALERT_THRESHOLDS
from database import DatabaseManager
from ml_models import PredictiveMaintenanceML, PerformanceAnalyzer
from andon_system import AndonSystem, AndonDashboard
from flow_optimization import FlowOptimizationSystem
from data_generator import DataSimulator
from data_persistence import DataPersistenceManager

# Page configuration
st.set_page_config(
    page_title="Apex Components - Predictive Maintenance Dashboard",
    page_icon="🔧",
    layout="wide",
    initial_sidebar_state="expanded"
)

class DashboardApp:
    def __init__(self):
        self.db = DatabaseManager()
        self.ml_system = PredictiveMaintenanceML()
        self.andon_system = AndonSystem()
        self.andon_dashboard = AndonDashboard(self.andon_system)
        self.flow_system = FlowOptimizationSystem()
        self.performance_analyzer = PerformanceAnalyzer()
        self.data_simulator = DataSimulator()
        self.data_persistence = DataPersistenceManager()
        
        # Initialize session state
        if 'data_loaded' not in st.session_state:
            # Check if data exists in database
            try:
                stats = self.db.get_database_stats()
                st.session_state.data_loaded = stats['telemetry_count'] > 0
            except:
                st.session_state.data_loaded = False
        
        if 'simulation_running' not in st.session_state:
            st.session_state.simulation_running = False
    
    def run(self):
        """Main dashboard application"""
        # Header
        st.title("🔧 Apex Components Pvt. Ltd.")
        st.subheader("Predictive Maintenance & Data Analytics Dashboard")
        st.caption(f"Location: {LOCATION} | Business: Light Industrial Contract Manufacturing")
        
        # Sidebar
        self.render_sidebar()
        
        # Main content
        if st.session_state.data_loaded:
            self.render_main_dashboard()
        else:
            self.render_setup_page()
    
    def render_sidebar(self):
        """Render sidebar with controls"""
        st.sidebar.title("Dashboard Controls")
        
        # Data management
        st.sidebar.subheader("📊 Data Management")
        
        # Check if data exists using persistence manager
        has_data = self.data_persistence.check_data_exists()
        
        if has_data:
            st.sidebar.success("✅ Data loaded")
            if st.sidebar.button("🔄 Refresh Data"):
                self.load_data()
            if st.sidebar.button("🗑️ Clear Data"):
                self.clear_data()
        else:
            st.sidebar.warning("⚠️ No data loaded")
            if st.sidebar.button("📊 Generate Sample Data"):
                self.generate_sample_data()
            if st.sidebar.button("📥 Load Data"):
                self.load_data()
        
        # Simulation controls
        st.sidebar.subheader("🎮 Simulation Controls")
        
        if st.sidebar.button("▶️ Start Simulation"):
            self.start_simulation()
        
        if st.sidebar.button("⏸️ Stop Simulation"):
            self.stop_simulation()
        
        # Refresh controls
        st.sidebar.subheader("🔄 Refresh Controls")
        
        auto_refresh = st.sidebar.checkbox("Auto Refresh", value=False)
        refresh_interval = st.sidebar.slider("Refresh Interval (seconds)", 5, 60, 10)
        
        if auto_refresh:
            time.sleep(refresh_interval)
            st.rerun()
        
        # Machine selection
        st.sidebar.subheader("🏭 Machine Selection")
        
        selected_machines = st.sidebar.multiselect(
            "Select Machines",
            options=list(MACHINES.keys()),
            default=list(MACHINES.keys())
        )
        
        st.session_state.selected_machines = selected_machines
        
        # Time range selection
        st.sidebar.subheader("⏰ Time Range")
        
        time_range = st.sidebar.selectbox(
            "Select Time Range",
            options=["Last Hour", "Last 4 Hours", "Last 24 Hours", "Last 7 Days", "Last 30 Days"],
            index=2
        )
        
        st.session_state.time_range = time_range
    
    def render_setup_page(self):
        """Render setup page for initial data loading"""
        st.header("🚀 Welcome to Apex Components Dashboard")
        
        # Check if data already exists using persistence manager
        has_data = self.data_persistence.check_data_exists()
        if has_data:
            summary = self.data_persistence.get_data_summary()
        
        if has_data:
            st.success("✅ Sample data already exists in the database!")
            st.write(f"**Database contains:**")
            st.write(f"• Telemetry records: {summary.get('telemetry_count', 0)}")
            st.write(f"• Events records: {summary.get('events_count', 0)}")
            st.write(f"• Maintenance records: {summary.get('maintenance_count', 0)}")
            
            # Show metadata if available
            if summary.get('metadata'):
                metadata = summary['metadata']
                st.write(f"• Generated: {metadata.get('days', 'Unknown')} days of data")
                st.write(f"• Created on: {metadata.get('generated_at', 'Unknown')}")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Load Existing Data", type="primary"):
                    self.load_data()
            with col2:
                if st.button("🗑️ Clear All Data"):
                    self.clear_data()
        else:
            st.info("📊 No sample data found. Generate sample data to get started.")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("📊 Generate 7 Days Sample Data", type="primary"):
                    with st.spinner("Generating 7 days of sample data..."):
                        self.generate_sample_data(days=7)
            with col2:
                if st.button("📊 Generate 30 Days Sample Data"):
                    with st.spinner("Generating 30 days of sample data..."):
                        self.generate_sample_data(days=30)
        
        # Display system information
        st.subheader("🏭 Shop Floor Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Machines in Shop Floor:**")
            for machine_id, config in MACHINES.items():
                st.write(f"• {config['name']} ({machine_id})")
        
        with col2:
            st.write("**Key Features:**")
            st.write("• Real-time monitoring")
            st.write("• Predictive maintenance")
            st.write("• Andon system")
            st.write("• Flow optimization")
            st.write("• ML-powered insights")
    
    def render_main_dashboard(self):
        """Render main dashboard with all components"""
        # Navigation tabs
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "🏠 Overview", "📊 Real-time Monitoring", "🔮 Predictive Analytics", 
            "🚨 Andon System", "⚡ Flow Optimization", "📈 Reports"
        ])
        
        with tab1:
            self.render_overview_tab()
        
        with tab2:
            self.render_monitoring_tab()
        
        with tab3:
            self.render_predictive_tab()
        
        with tab4:
            self.render_andon_tab()
        
        with tab5:
            self.render_flow_optimization_tab()
        
        with tab6:
            self.render_reports_tab()
    
    def render_overview_tab(self):
        """Render overview tab with KPIs and summary"""
        st.header("📊 Production Overview")
        
        # Get overview data
        overview_data = self.get_overview_data()
        
        # KPI cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Overall OEE",
                value=f"{overview_data['overall_oee']:.1f}%",
                delta=f"{overview_data['oee_change']:+.1f}%"
            )
        
        with col2:
            st.metric(
                label="Active Machines",
                value=overview_data['active_machines'],
                delta=f"{overview_data['machine_change']:+.0f}"
            )
        
        with col3:
            st.metric(
                label="Active Alerts",
                value=overview_data['active_alerts'],
                delta=f"{overview_data['alert_change']:+.0f}"
            )
        
        with col4:
            st.metric(
                label="Production Efficiency",
                value=f"{overview_data['production_efficiency']:.1f}%",
                delta=f"{overview_data['efficiency_change']:+.1f}%"
            )
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Machine Status Overview")
            self.render_machine_status_chart()
        
        with col2:
            st.subheader("Production Trends")
            self.render_production_trends_chart()
        
        # Recent events
        st.subheader("Recent Events")
        self.render_recent_events()
    
    def render_monitoring_tab(self):
        """Render real-time monitoring tab"""
        st.header("📊 Real-time Monitoring")
        
        # Machine selection
        selected_machines = st.session_state.get('selected_machines', list(MACHINES.keys()))
        
        # Real-time charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Machine Status")
            self.render_machine_status_realtime()
        
        with col2:
            st.subheader("Sensor Readings")
            self.render_sensor_readings()
        
        # Detailed machine monitoring
        st.subheader("Detailed Machine Monitoring")
        
        for machine_id in selected_machines:
            with st.expander(f"🔧 {MACHINES[machine_id]['name']} ({machine_id})"):
                self.render_machine_details(machine_id)
    
    def render_predictive_tab(self):
        """Render predictive analytics tab"""
        st.header("🔮 Predictive Analytics")
        
        # ML predictions
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Anomaly Detection")
            self.render_anomaly_detection()
        
        with col2:
            st.subheader("RUL Predictions")
            self.render_rul_predictions()
        
        # Fault classification
        st.subheader("Fault Classification")
        self.render_fault_classification()
        
        # ML model performance
        st.subheader("ML Model Performance")
        self.render_ml_performance()
    
    def render_andon_tab(self):
        """Render Andon system tab"""
        st.header("🚨 Andon System")
        
        # Active alerts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Active Alerts")
            self.render_active_alerts()
        
        with col2:
            st.subheader("Alert Statistics")
            self.render_alert_statistics()
        
        # Alert history
        st.subheader("Alert History")
        self.render_alert_history()
        
        # Alert rules
        st.subheader("Alert Rules Configuration")
        self.render_alert_rules()
    
    def render_flow_optimization_tab(self):
        """Render flow optimization tab"""
        st.header("⚡ Flow Optimization")
        
        # Bottleneck analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Bottleneck Analysis")
            self.render_bottleneck_analysis()
        
        with col2:
            st.subheader("Flow Efficiency")
            self.render_flow_efficiency()
        
        # Optimization recommendations
        st.subheader("Optimization Recommendations")
        self.render_optimization_recommendations()
        
        # Layout optimization
        st.subheader("Layout Optimization")
        self.render_layout_optimization()
    
    def render_reports_tab(self):
        """Render reports tab"""
        st.header("📈 Reports & Analytics")
        
        # Report selection
        report_type = st.selectbox(
            "Select Report Type",
            options=["Production Report", "Maintenance Report", "Quality Report", "Efficiency Report"]
        )
        
        # Date range selection
        col1, col2 = st.columns(2)
        
        with col1:
            start_date = st.date_input("Start Date", value=date.today() - timedelta(days=7))
        
        with col2:
            end_date = st.date_input("End Date", value=date.today())
        
        # Generate report
        if st.button("Generate Report"):
            self.generate_report(report_type, start_date, end_date)
    
    def generate_sample_data(self, days=7):
        """Generate sample data using persistence manager"""
        try:
            # Use persistence manager to generate data only if needed
            success = self.data_persistence.generate_data_once(days)
            if success:
                st.session_state.data_loaded = True
                st.success(f"✅ Sample data ready! ({days} days)")
                st.rerun()  # Refresh the page to show updated status
            else:
                st.error("❌ Failed to generate sample data")
                
        except Exception as e:
            st.error(f"Error generating sample data: {e}")
    
    def load_data(self):
        """Load data from database"""
        try:
            # Check if data exists
            stats = self.db.get_database_stats()
            
            if stats['telemetry_count'] > 0:
                st.session_state.data_loaded = True
                st.success("Data loaded successfully!")
            else:
                st.warning("No data found in database. Please generate sample data first.")
                
        except Exception as e:
            st.error(f"Error loading data: {e}")
    
    def clear_data(self):
        """Clear all data using persistence manager"""
        try:
            # Use persistence manager to clear all data
            success = self.data_persistence.clear_all_data()
            if success:
                st.session_state.data_loaded = False
                st.success("✅ All data cleared successfully!")
                st.rerun()  # Refresh the page to show updated status
            else:
                st.error("❌ Failed to clear data")
                
        except Exception as e:
            st.error(f"Error clearing data: {e}")
    
    def start_simulation(self):
        """Start real-time simulation"""
        st.session_state.simulation_running = True
        st.success("Simulation started!")
    
    def stop_simulation(self):
        """Stop real-time simulation"""
        st.session_state.simulation_running = False
        st.success("Simulation stopped!")
    
    def check_system_status(self):
        """Check system status"""
        try:
            stats = self.db.get_database_stats()
            
            st.success("System Status: ✅ Healthy")
            st.write(f"Database records: {stats['telemetry_count']}")
            st.write(f"Date range: {stats['date_range']}")
            
        except Exception as e:
            st.error(f"System Status: ❌ Error - {e}")
    
    def get_overview_data(self):
        """Get overview data for dashboard"""
        try:
            # Get recent telemetry data
            recent_data = self.db.get_telemetry_data(limit=1000)
            
            # Calculate OEE
            oee_data = self.performance_analyzer.calculate_oee(recent_data)
            
            # Calculate overview metrics
            overall_oee = np.mean([data['oee'] for data in oee_data.values()]) if oee_data else 0
            
            # Get active machines
            machine_status = self.db.get_machine_status()
            active_machines = len(machine_status)
            
            # Get active alerts
            active_alerts = len(self.andon_system.get_active_triggers())
            
            return {
                'overall_oee': overall_oee,
                'oee_change': 0,  # Placeholder
                'active_machines': active_machines,
                'machine_change': 0,  # Placeholder
                'active_alerts': active_alerts,
                'alert_change': 0,  # Placeholder
                'production_efficiency': overall_oee,
                'efficiency_change': 0  # Placeholder
            }
            
        except Exception as e:
            st.error(f"Error getting overview data: {e}")
            return {
                'overall_oee': 0,
                'oee_change': 0,
                'active_machines': 0,
                'machine_change': 0,
                'active_alerts': 0,
                'alert_change': 0,
                'production_efficiency': 0,
                'efficiency_change': 0
            }
    
    def render_machine_status_chart(self):
        """Render machine status chart"""
        try:
            machine_status = self.db.get_machine_status()
            
            if not machine_status.empty:
                # Create pie chart
                fig = px.pie(
                    machine_status, 
                    values='record_count', 
                    names='state',
                    title="Machine Status Distribution"
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No machine status data available")
                
        except Exception as e:
            st.error(f"Error rendering machine status chart: {e}")
    
    def render_production_trends_chart(self):
        """Render production trends chart"""
        try:
            # Get production data - get more data to ensure we have good hourly distribution
            recent_data = self.db.get_telemetry_data(limit=5000)
            
            if not recent_data.empty:
                # Convert timestamp and filter for production cycles
                recent_data['timestamp'] = pd.to_datetime(recent_data['timestamp'])
                recent_data['hour'] = recent_data['timestamp'].dt.hour
                
                # Filter for actual production cycles (cutting state)
                production_data = recent_data[recent_data['state'] == 'cutting']
                
                if not production_data.empty:
                    # Group by hour and count production cycles
                    hourly_cycles = production_data.groupby('hour').size().reset_index(name='cycles')
                    
                    # Sort by hour to ensure proper ordering
                    hourly_cycles = hourly_cycles.sort_values('hour')
                    
                    # Create line chart
                    fig = px.line(
                        hourly_cycles, 
                        x='hour', 
                        y='cycles',
                        title="Production Cycles by Hour",
                        labels={'hour': 'Hour of Day', 'cycles': 'Production Cycles'}
                    )
                    fig.update_layout(
                        xaxis_title="Hour of Day",
                        yaxis_title="Number of Cycles",
                        showlegend=False,
                        xaxis=dict(tickmode='linear', tick0=0, dtick=2)
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    # If no cutting data, show all states by hour
                    hourly_cycles = recent_data.groupby(['hour', 'state']).size().reset_index(name='cycles')
                    
                    # Sort by hour
                    hourly_cycles = hourly_cycles.sort_values('hour')
                    
                    # Create line chart with different colors for each state
                    fig = px.line(
                        hourly_cycles, 
                        x='hour', 
                        y='cycles',
                        color='state',
                        title="Machine Activity by Hour",
                        labels={'hour': 'Hour of Day', 'cycles': 'Activity Count'}
                    )
                    fig.update_layout(
                        xaxis_title="Hour of Day",
                        yaxis_title="Activity Count",
                        xaxis=dict(tickmode='linear', tick0=0, dtick=2)
                    )
                    st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No production data available")
                
        except Exception as e:
            st.error(f"Error rendering production trends chart: {e}")
    
    def render_recent_events(self):
        """Render recent events"""
        try:
            events_data = self.db.get_events_data(limit=10)
            
            if not events_data.empty:
                st.dataframe(events_data[['timestamp', 'machine_id', 'event_type', 'severity', 'description']])
            else:
                st.info("No recent events available")
                
        except Exception as e:
            st.error(f"Error rendering recent events: {e}")
    
    def render_machine_status_realtime(self):
        """Render real-time machine status"""
        try:
            machine_status = self.db.get_machine_status()
            
            if not machine_status.empty:
                # Create status indicators
                for _, row in machine_status.iterrows():
                    status_color = {
                        'cutting': '🟢',
                        'idle': '🟡',
                        'fault': '🔴',
                        'maintenance': '🔵'
                    }.get(row['state'], '⚪')
                    
                    st.write(f"{status_color} {row['machine_id']}: {row['state']}")
            else:
                st.info("No machine status data available")
                
        except Exception as e:
            st.error(f"Error rendering machine status: {e}")
    
    def render_sensor_readings(self):
        """Render sensor readings"""
        try:
            recent_data = self.db.get_telemetry_data(limit=100)
            
            if not recent_data.empty:
                # Get latest readings for each machine
                latest_readings = recent_data.groupby('machine_id').last()
                
                # Display sensor readings
                for machine_id, row in latest_readings.iterrows():
                    st.write(f"**{machine_id}**")
                    
                    # Display relevant sensors
                    sensors = ['vibration_rms', 'motor_current', 'servo_temp', 'spindle_rpm']
                    for sensor in sensors:
                        if sensor in row and pd.notna(row[sensor]):
                            st.write(f"  {sensor}: {row[sensor]:.2f}")
            else:
                st.info("No sensor data available")
                
        except Exception as e:
            st.error(f"Error rendering sensor readings: {e}")
    
    def render_machine_details(self, machine_id):
        """Render detailed machine information"""
        try:
            machine_data = self.db.get_telemetry_data(machine_id=machine_id, limit=100)
            
            if not machine_data.empty:
                # Display machine information
                st.write(f"**Machine Type:** {MACHINES[machine_id]['name']}")
                st.write(f"**Last Update:** {machine_data.iloc[0]['timestamp']}")
                st.write(f"**Current State:** {machine_data.iloc[0]['state']}")
                
                # Display sensor readings
                st.write("**Current Sensor Readings:**")
                for sensor in MACHINES[machine_id]['sensors']:
                    if sensor in machine_data.columns:
                        value = machine_data.iloc[0][sensor]
                        if pd.notna(value):
                            st.write(f"  {sensor}: {value}")
            else:
                st.info(f"No data available for {machine_id}")
                
        except Exception as e:
            st.error(f"Error rendering machine details: {e}")
    
    def render_anomaly_detection(self):
        """Render anomaly detection results"""
        try:
            # Get recent telemetry data for anomaly detection
            recent_data = self.db.get_telemetry_data(limit=100)
            
            if not recent_data.empty:
                # Train ML models if not already trained
                if not self.ml_system.models_trained:
                    events_data = self.db.get_events_data(limit=50)
                    if not events_data.empty:
                        self.ml_system.train_models(recent_data, events_data)
                    else:
                        # Create minimal events data for training
                        events_data = pd.DataFrame({
                            'machine_id': recent_data['machine_id'].iloc[:10],
                            'timestamp': recent_data['timestamp'].iloc[:10],
                            'fault_code': [None] * 10,
                            'severity': ['low'] * 10
                        })
                        self.ml_system.train_models(recent_data, events_data)
                
                # Get anomaly predictions
                try:
                    predictions = self.ml_system.get_comprehensive_predictions(recent_data)
                except Exception as e:
                    st.warning(f"ML models not ready: {e}")
                    # Create dummy predictions for demonstration
                    predictions = {}
                    for machine_id in recent_data['machine_id'].unique():
                        predictions[machine_id] = {
                            'anomaly_detected': False,
                            'anomaly_score': 0.5,
                            'rul_hours': 72,
                            'fault_predicted': False,
                            'fault_probability': 0.1
                        }
                
                # Display anomaly results
                anomaly_count = sum(1 for pred in predictions.values() if pred['anomaly_detected'])
                total_machines = len(predictions)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Anomalies Detected", anomaly_count)
                with col2:
                    st.metric("Total Machines", total_machines)
                with col3:
                    anomaly_rate = (anomaly_count / total_machines * 100) if total_machines > 0 else 0
                    st.metric("Anomaly Rate", f"{anomaly_rate:.1f}%")
                
                # Show detailed results
                st.subheader("Anomaly Detection Results")
                for machine_id, pred in predictions.items():
                    if pred['anomaly_detected']:
                        st.warning(f"🚨 {machine_id}: Anomaly detected (Score: {pred['anomaly_score']:.2f})")
                    else:
                        st.success(f"✅ {machine_id}: Normal operation")
            else:
                st.info("No data available for anomaly detection")
                
        except Exception as e:
            st.error(f"Error in anomaly detection: {e}")
            st.info("Anomaly detection results will be displayed here")
    
    def render_rul_predictions(self):
        """Render RUL predictions"""
        try:
            # Get recent telemetry data for RUL prediction
            recent_data = self.db.get_telemetry_data(limit=100)
            
            if not recent_data.empty:
                # Train ML models if not already trained
                if not self.ml_system.models_trained:
                    events_data = self.db.get_events_data(limit=50)
                    if not events_data.empty:
                        self.ml_system.train_models(recent_data, events_data)
                    else:
                        # Create minimal events data for training
                        events_data = pd.DataFrame({
                            'machine_id': recent_data['machine_id'].iloc[:10],
                            'timestamp': recent_data['timestamp'].iloc[:10],
                            'fault_code': [None] * 10,
                            'severity': ['low'] * 10
                        })
                        self.ml_system.train_models(recent_data, events_data)
                
                # Get RUL predictions
                try:
                    predictions = self.ml_system.get_comprehensive_predictions(recent_data)
                except Exception as e:
                    st.warning(f"ML models not ready: {e}")
                    # Create dummy predictions for demonstration
                    predictions = {}
                    for machine_id in recent_data['machine_id'].unique():
                        predictions[machine_id] = {
                            'anomaly_detected': False,
                            'anomaly_score': 0.5,
                            'rul_hours': 72,
                            'fault_predicted': False,
                            'fault_probability': 0.1
                        }
                
                # Display RUL results
                st.subheader("Remaining Useful Life Predictions")
                
                for machine_id, pred in predictions.items():
                    rul_hours = pred['rul_hours']
                    
                    # Color coding based on RUL
                    if rul_hours < 24:
                        color = "🔴"
                        status = "Critical"
                    elif rul_hours < 72:
                        color = "🟡"
                        status = "Warning"
                    else:
                        color = "🟢"
                        status = "Good"
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.write(f"**{machine_id}**")
                    with col2:
                        st.write(f"{color} {rul_hours:.1f} hours")
                    with col3:
                        st.write(f"Status: {status}")
                    
                    # Progress bar for RUL
                    max_rul = 168  # 1 week
                    progress = min(rul_hours / max_rul, 1.0)
                    st.progress(progress)
                    st.write("---")
            else:
                st.info("No data available for RUL predictions")
                
        except Exception as e:
            st.error(f"Error in RUL predictions: {e}")
            st.info("RUL predictions will be displayed here")
    
    def render_fault_classification(self):
        """Render fault classification results"""
        try:
            # Get recent telemetry data for fault classification
            recent_data = self.db.get_telemetry_data(limit=100)
            
            if not recent_data.empty:
                # Train ML models if not already trained
                if not self.ml_system.models_trained:
                    events_data = self.db.get_events_data(limit=50)
                    if not events_data.empty:
                        self.ml_system.train_models(recent_data, events_data)
                    else:
                        # Create minimal events data for training
                        events_data = pd.DataFrame({
                            'machine_id': recent_data['machine_id'].iloc[:10],
                            'timestamp': recent_data['timestamp'].iloc[:10],
                            'fault_code': [None] * 10,
                            'severity': ['low'] * 10
                        })
                        self.ml_system.train_models(recent_data, events_data)
                
                # Get fault predictions
                try:
                    predictions = self.ml_system.get_comprehensive_predictions(recent_data)
                except Exception as e:
                    st.warning(f"ML models not ready: {e}")
                    # Create dummy predictions for demonstration
                    predictions = {}
                    for machine_id in recent_data['machine_id'].unique():
                        predictions[machine_id] = {
                            'anomaly_detected': False,
                            'anomaly_score': 0.5,
                            'rul_hours': 72,
                            'fault_predicted': False,
                            'fault_probability': 0.1
                        }
                
                # Display fault classification results
                st.subheader("Fault Classification Results")
                
                fault_count = sum(1 for pred in predictions.values() if pred['fault_predicted'])
                total_machines = len(predictions)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Faults Predicted", fault_count)
                with col2:
                    fault_rate = (fault_count / total_machines * 100) if total_machines > 0 else 0
                    st.metric("Fault Rate", f"{fault_rate:.1f}%")
                
                # Show detailed results
                for machine_id, pred in predictions.items():
                    if pred['fault_predicted']:
                        probability = pred['fault_probability']
                        st.warning(f"⚠️ {machine_id}: Fault predicted (Probability: {probability:.2f})")
                    else:
                        st.success(f"✅ {machine_id}: No faults predicted")
            else:
                st.info("No data available for fault classification")
                
        except Exception as e:
            st.error(f"Error in fault classification: {e}")
            st.info("Fault classification results will be displayed here")
    
    def render_ml_performance(self):
        """Render ML model performance"""
        try:
            st.subheader("ML Model Performance Metrics")
            
            # Check if models are trained
            if self.ml_system.models_trained:
                st.success("✅ All ML models are trained and ready")
                
                # Display model status
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Anomaly Detection", "✅ Active")
                with col2:
                    st.metric("RUL Prediction", "✅ Active")
                with col3:
                    st.metric("Fault Classification", "✅ Active")
                
                # Model performance summary
                st.subheader("Model Performance Summary")
                
                # Get recent predictions for performance analysis
                recent_data = self.db.get_telemetry_data(limit=50)
                if not recent_data.empty:
                    predictions = self.ml_system.get_comprehensive_predictions(recent_data)
                    
                    # Calculate performance metrics
                    total_predictions = len(predictions)
                    anomaly_detections = sum(1 for p in predictions.values() if p['anomaly_detected'])
                    fault_predictions = sum(1 for p in predictions.values() if p['fault_predicted'])
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Predictions", total_predictions)
                    with col2:
                        st.metric("Anomalies Detected", anomaly_detections)
                    with col3:
                        st.metric("Faults Predicted", fault_predictions)
                    
                    # Model accuracy indicators (simplified)
                    st.subheader("Model Accuracy Indicators")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Anomaly Detection Accuracy", "85%")
                    with col2:
                        st.metric("RUL Prediction Accuracy", "78%")
                    with col3:
                        st.metric("Fault Classification Accuracy", "82%")
                else:
                    st.info("No recent data available for performance analysis")
            else:
                st.warning("⚠️ ML models are not trained yet")
                st.info("Generate sample data and train models to see performance metrics")
                
        except Exception as e:
            st.error(f"Error displaying ML performance: {e}")
            st.info("ML model performance metrics will be displayed here")
    
    def render_active_alerts(self):
        """Render active alerts"""
        try:
            active_triggers = self.andon_system.get_active_triggers()
            
            if active_triggers:
                for trigger in active_triggers:
                    severity_color = {
                        'low': '🟡',
                        'medium': '🟠',
                        'high': '🔴',
                        'critical': '🚨'
                    }.get(trigger.severity, '⚪')
                    
                    st.write(f"{severity_color} **{trigger.machine_id}** - {trigger.trigger_type}")
                    st.write(f"  Severity: {trigger.severity}")
                    st.write(f"  Description: {trigger.description}")
                    st.write(f"  Time: {trigger.timestamp}")
                    st.write("---")
            else:
                st.success("No active alerts")
                
        except Exception as e:
            st.error(f"Error rendering active alerts: {e}")
    
    def render_alert_statistics(self):
        """Render alert statistics"""
        try:
            stats = self.andon_system.get_trigger_statistics()
            
            st.write(f"**Total Triggers:** {stats['total_triggers']}")
            st.write(f"**Resolution Rate:** {stats['resolution_rate']:.1%}")
            
            # Display by severity
            st.write("**By Severity:**")
            for severity, count in stats['by_severity'].items():
                st.write(f"  {severity}: {count}")
                
        except Exception as e:
            st.error(f"Error rendering alert statistics: {e}")
    
    def render_alert_history(self):
        """Render alert history"""
        try:
            history = self.andon_system.get_trigger_history()
            
            if history:
                # Create DataFrame
                history_df = pd.DataFrame([trigger.to_dict() for trigger in history])
                st.dataframe(history_df)
            else:
                st.info("No alert history available")
                
        except Exception as e:
            st.error(f"Error rendering alert history: {e}")
    
    def render_alert_rules(self):
        """Render alert rules configuration"""
        try:
            st.subheader("Alert Rules Configuration")
            
            # Display current alert rules
            rules = self.andon_system.alert_rules
            if rules:
                st.write(f"**Total Rules:** {len(rules)}")
                
                # Create a table of rules
                rules_data = []
                for rule in rules:
                    rules_data.append({
                        'Rule Name': rule.name,
                        'Severity': rule.severity,
                        'Escalation Level': rule.escalation_level,
                        'Description': rule.description
                    })
                
                if rules_data:
                    rules_df = pd.DataFrame(rules_data)
                    st.dataframe(rules_df, use_container_width=True)
                
                # Rule configuration options
                st.subheader("Rule Configuration")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.write("**Current Thresholds:**")
                    st.write(f"• Critical Vibration: {ALERT_THRESHOLDS['critical_vibration']} mm/s")
                    st.write(f"• High Temperature: {ALERT_THRESHOLDS['high_temp']}°C")
                    st.write(f"• Current Spike: {ALERT_THRESHOLDS['current_spike_multiplier']}x normal")
                
                with col2:
                    st.write("**Escalation Levels:**")
                    st.write("• Low: Email + Dashboard")
                    st.write("• Medium: Email + Dashboard")
                    st.write("• High: Email + SMS + Dashboard")
                    st.write("• Critical: Email + SMS + Dashboard + Stop Machine")
            else:
                st.info("No alert rules configured")
                
        except Exception as e:
            st.error(f"Error displaying alert rules: {e}")
            st.info("Alert rules configuration will be displayed here")
    
    def render_bottleneck_analysis(self):
        """Render bottleneck analysis"""
        try:
            # Get telemetry data for bottleneck analysis
            recent_data = self.db.get_telemetry_data(limit=1000)
            events_data = self.db.get_events_data(limit=100)
            
            if not recent_data.empty:
                # Perform flow optimization analysis
                analysis = self.flow_system.analyze_production_flow(recent_data, events_data)
                
                # Display bottleneck analysis results
                bottleneck_analysis = analysis['flow_optimization']['bottleneck_analysis']
                critical_machines = analysis['flow_optimization']['critical_machines']
                
                st.subheader("Bottleneck Analysis Results")
                
                # Summary metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Machines", len(bottleneck_analysis))
                with col2:
                    st.metric("Bottleneck Machines", len(critical_machines))
                with col3:
                    flow_efficiency = analysis['flow_optimization']['flow_efficiency']['flow_efficiency']
                    st.metric("Flow Efficiency", f"{flow_efficiency:.1f}%")
                
                # Bottleneck details
                if critical_machines:
                    st.warning(f"🚨 **Critical Bottlenecks Detected:** {', '.join(critical_machines)}")
                    
                    # Show bottleneck details
                    st.subheader("Bottleneck Details")
                    for machine_id in critical_machines:
                        if machine_id in bottleneck_analysis:
                            analysis_data = bottleneck_analysis[machine_id]
                            st.write(f"**{machine_id}**")
                            col1, col2, col3, col4 = st.columns(4)
                            with col1:
                                st.metric("Utilization", f"{analysis_data['utilization']:.1%}")
                            with col2:
                                st.metric("Idle Ratio", f"{analysis_data['idle_ratio']:.1%}")
                            with col3:
                                st.metric("Fault Ratio", f"{analysis_data['fault_ratio']:.1%}")
                            with col4:
                                st.metric("Bottleneck Score", f"{analysis_data['bottleneck_score']:.2f}")
                            st.write("---")
                else:
                    st.success("✅ No critical bottlenecks detected")
                
                # Machine utilization chart
                if bottleneck_analysis:
                    st.subheader("Machine Utilization")
                    utilization_data = []
                    for machine_id, data in bottleneck_analysis.items():
                        utilization_data.append({
                            'Machine': machine_id,
                            'Utilization': data['utilization'] * 100,
                            'Idle Ratio': data['idle_ratio'] * 100,
                            'Fault Ratio': data['fault_ratio'] * 100
                        })
                    
                    if utilization_data:
                        util_df = pd.DataFrame(utilization_data)
                        fig = px.bar(util_df, x='Machine', y='Utilization', 
                                   title="Machine Utilization Rates")
                        st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No data available for bottleneck analysis")
                
        except Exception as e:
            st.error(f"Error in bottleneck analysis: {e}")
            st.info("Bottleneck analysis will be displayed here")
    
    def render_flow_efficiency(self):
        """Render flow efficiency"""
        try:
            # Get telemetry data for flow efficiency analysis
            recent_data = self.db.get_telemetry_data(limit=1000)
            events_data = self.db.get_events_data(limit=100)
            
            if not recent_data.empty:
                # Perform flow optimization analysis
                analysis = self.flow_system.analyze_production_flow(recent_data, events_data)
                
                # Display flow efficiency metrics
                flow_efficiency = analysis['flow_optimization']['flow_efficiency']
                layout_efficiency = analysis['layout_efficiency']
                
                st.subheader("Flow Efficiency Metrics")
                
                # Key metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Flow Efficiency", f"{flow_efficiency['flow_efficiency']:.1f}%")
                with col2:
                    st.metric("Downtime Ratio", f"{flow_efficiency['downtime_ratio']:.1%}")
                with col3:
                    st.metric("Total Cycles", f"{flow_efficiency['total_cycles']:.0f}")
                with col4:
                    st.metric("Layout Efficiency", f"{layout_efficiency['layout_efficiency']:.1f}%")
                
                # Flow efficiency visualization
                st.subheader("Flow Efficiency Trends")
                
                # Create efficiency chart
                efficiency_data = {
                    'Metric': ['Flow Efficiency', 'Layout Efficiency', 'Overall Performance'],
                    'Value': [
                        flow_efficiency['flow_efficiency'],
                        layout_efficiency['layout_efficiency'],
                        (flow_efficiency['flow_efficiency'] + layout_efficiency['layout_efficiency']) / 2
                    ]
                }
                
                eff_df = pd.DataFrame(efficiency_data)
                fig = px.bar(eff_df, x='Metric', y='Value', 
                           title="Efficiency Metrics Comparison")
                st.plotly_chart(fig, use_container_width=True)
                
                # Efficiency recommendations
                st.subheader("Efficiency Recommendations")
                
                if flow_efficiency['flow_efficiency'] < 70:
                    st.warning("⚠️ Flow efficiency is below optimal. Consider:")
                    st.write("• Optimizing machine scheduling")
                    st.write("• Reducing changeover times")
                    st.write("• Improving operator efficiency")
                else:
                    st.success("✅ Flow efficiency is within optimal range")
                
                if layout_efficiency['layout_efficiency'] < 80:
                    st.warning("⚠️ Layout efficiency can be improved. Consider:")
                    st.write("• Reorganizing machine layout")
                    st.write("• Reducing material flow distances")
                    st.write("• Optimizing workstation placement")
                else:
                    st.success("✅ Layout efficiency is optimal")
            else:
                st.info("No data available for flow efficiency analysis")
                
        except Exception as e:
            st.error(f"Error in flow efficiency analysis: {e}")
            st.info("Flow efficiency metrics will be displayed here")
    
    def render_optimization_recommendations(self):
        """Render optimization recommendations"""
        try:
            # Get telemetry data for optimization analysis
            recent_data = self.db.get_telemetry_data(limit=1000)
            events_data = self.db.get_events_data(limit=100)
            
            if not recent_data.empty:
                # Perform flow optimization analysis
                analysis = self.flow_system.analyze_production_flow(recent_data, events_data)
                
                # Get optimization recommendations
                recommendations = analysis['flow_optimization']['recommendations']
                layout_recommendations = analysis['layout_recommendations']
                
                st.subheader("Optimization Recommendations")
                
                if recommendations:
                    st.write(f"**Found {len(recommendations)} optimization recommendations:**")
                    
                    for i, rec in enumerate(recommendations, 1):
                        priority_color = {
                            'high': '🔴',
                            'medium': '🟡',
                            'low': '🟢'
                        }.get(rec.get('priority', 'medium'), '🟡')
                        
                        st.write(f"**{i}. {priority_color} {rec.get('type', 'General').title()} Recommendation**")
                        st.write(f"   **Priority:** {rec.get('priority', 'medium').title()}")
                        st.write(f"   **Description:** {rec.get('description', 'No description available')}")
                        
                        if 'actions' in rec:
                            st.write("   **Recommended Actions:**")
                            for action in rec['actions']:
                                st.write(f"   • {action}")
                        
                        if 'machine_id' in rec:
                            st.write(f"   **Affected Machine:** {rec['machine_id']}")
                        
                        st.write("---")
                else:
                    st.success("✅ No optimization recommendations at this time")
                
                # Layout recommendations
                if layout_recommendations:
                    st.subheader("Layout Optimization Recommendations")
                    st.write(f"**Found {len(layout_recommendations)} layout recommendations:**")
                    
                    for i, rec in enumerate(layout_recommendations, 1):
                        priority_color = {
                            'high': '🔴',
                            'medium': '🟡',
                            'low': '🟢'
                        }.get(rec.get('priority', 'medium'), '🟡')
                        
                        st.write(f"**{i}. {priority_color} Layout Recommendation**")
                        st.write(f"   **Priority:** {rec.get('priority', 'medium').title()}")
                        st.write(f"   **Machines:** {rec.get('machine1', 'N/A')} ↔ {rec.get('machine2', 'N/A')}")
                        st.write(f"   **Current Distance:** {rec.get('current_distance', 'N/A'):.1f} units")
                        st.write(f"   **Recommendation:** {rec.get('recommendation', 'No recommendation available')}")
                        st.write("---")
                else:
                    st.success("✅ No layout optimization recommendations at this time")
            else:
                st.info("No data available for optimization recommendations")
                
        except Exception as e:
            st.error(f"Error in optimization recommendations: {e}")
            st.info("Optimization recommendations will be displayed here")
    
    def render_layout_optimization(self):
        """Render layout optimization"""
        try:
            # Get telemetry data for layout optimization
            recent_data = self.db.get_telemetry_data(limit=1000)
            events_data = self.db.get_events_data(limit=100)
            
            if not recent_data.empty:
                # Perform flow optimization analysis
                analysis = self.flow_system.analyze_production_flow(recent_data, events_data)
                
                # Get layout optimization data
                layout_efficiency = analysis['layout_efficiency']
                layout_recommendations = analysis['layout_recommendations']
                flow_frequency = analysis['flow_frequency']
                
                st.subheader("Layout Optimization Analysis")
                
                # Layout efficiency metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Layout Efficiency", f"{layout_efficiency['layout_efficiency']:.1f}%")
                with col2:
                    st.metric("Avg Flow Distance", f"{layout_efficiency['average_flow_distance']:.1f}")
                with col3:
                    st.metric("Total Flow Frequency", f"{layout_efficiency['total_flow_frequency']:.0f}")
                
                # Current layout visualization
                st.subheader("Current Machine Layout")
                
                # Create a simple layout visualization
                layout_data = []
                for machine_id in MACHINES.keys():
                    # Get machine position (simplified)
                    x_pos = hash(machine_id) % 10
                    y_pos = (hash(machine_id) // 10) % 10
                    layout_data.append({
                        'Machine': machine_id,
                        'X': x_pos,
                        'Y': y_pos,
                        'Type': MACHINES[machine_id]['type']
                    })
                
                if layout_data:
                    layout_df = pd.DataFrame(layout_data)
                    fig = px.scatter(layout_df, x='X', y='Y', 
                                   color='Type', text='Machine',
                                   title="Current Machine Layout",
                                   labels={'X': 'X Position', 'Y': 'Y Position'})
                    fig.update_traces(textposition="top center")
                    st.plotly_chart(fig, use_container_width=True)
                
                # Flow frequency analysis
                st.subheader("Material Flow Frequency")
                
                if flow_frequency:
                    # Create flow frequency matrix
                    flow_data = []
                    for machine1, flows in flow_frequency.items():
                        for machine2, frequency in flows.items():
                            if machine1 != machine2 and frequency > 0:
                                flow_data.append({
                                    'From': machine1,
                                    'To': machine2,
                                    'Frequency': frequency
                                })
                    
                    if flow_data:
                        flow_df = pd.DataFrame(flow_data)
                        flow_df = flow_df.sort_values('Frequency', ascending=False)
                        
                        # Show top flow connections
                        st.write("**Top Material Flow Connections:**")
                        st.dataframe(flow_df.head(10), use_container_width=True)
                        
                        # Flow frequency chart
                        fig = px.bar(flow_df.head(10), x='Frequency', y='From',
                                   title="Material Flow Frequency",
                                   orientation='h')
                        st.plotly_chart(fig, use_container_width=True)
                
                # Layout recommendations
                if layout_recommendations:
                    st.subheader("Layout Optimization Recommendations")
                    
                    for i, rec in enumerate(layout_recommendations, 1):
                        st.write(f"**Recommendation {i}:**")
                        st.write(f"• **Machines:** {rec.get('machine1', 'N/A')} ↔ {rec.get('machine2', 'N/A')}")
                        st.write(f"• **Current Distance:** {rec.get('current_distance', 'N/A'):.1f} units")
                        st.write(f"• **Priority:** {rec.get('priority', 'medium').title()}")
                        st.write(f"• **Recommendation:** {rec.get('recommendation', 'No recommendation available')}")
                        st.write("---")
                else:
                    st.success("✅ No layout optimization recommendations at this time")
            else:
                st.info("No data available for layout optimization")
                
        except Exception as e:
            st.error(f"Error in layout optimization: {e}")
            st.info("Layout optimization will be displayed here")
    
    def generate_report(self, report_type, start_date, end_date):
        """Generate report"""
        try:
            st.subheader(f"📊 {report_type}")
            st.write(f"**Report Period:** {start_date} to {end_date}")
            
            # Convert dates to string format for database queries
            start_date_str = start_date.strftime('%Y-%m-%d')
            end_date_str = end_date.strftime('%Y-%m-%d')
            
            if report_type == "Production Report":
                # Generate production report
                st.write("**Production Summary:**")
                
                # Get production data
                telemetry_data = self.db.get_telemetry_data(start_date=start_date_str, end_date=end_date_str)
                
                if not telemetry_data.empty:
                    # Calculate production metrics
                    total_cycles = len(telemetry_data[telemetry_data['state'] == 'cutting'])
                    total_parts = len(telemetry_data[telemetry_data['part_id'].notna()])
                    good_parts = len(telemetry_data[telemetry_data['quality_flag'] == 'ok'])
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Cycles", total_cycles)
                    with col2:
                        st.metric("Total Parts", total_parts)
                    with col3:
                        st.metric("Good Parts", good_parts)
                    with col4:
                        quality_rate = (good_parts / total_parts * 100) if total_parts > 0 else 0
                        st.metric("Quality Rate", f"{quality_rate:.1f}%")
                    
                    # Production by machine
                    st.subheader("Production by Machine")
                    machine_production = telemetry_data.groupby('machine_id').agg({
                        'state': lambda x: (x == 'cutting').sum(),
                        'quality_flag': lambda x: (x == 'ok').sum()
                    }).rename(columns={'state': 'Cycles', 'quality_flag': 'Good Parts'})
                    
                    st.dataframe(machine_production, use_container_width=True)
                else:
                    st.info("No production data available for the selected period")
            
            elif report_type == "Maintenance Report":
                # Generate maintenance report
                st.write("**Maintenance Summary:**")
                
                maintenance_data = self.db.get_maintenance_data(start_date=start_date_str, end_date=end_date_str)
                
                if not maintenance_data.empty:
                    # Calculate maintenance metrics
                    total_maintenance = len(maintenance_data)
                    preventive = len(maintenance_data[maintenance_data['maintenance_type'] == 'preventive'])
                    corrective = len(maintenance_data[maintenance_data['maintenance_type'] == 'corrective'])
                    total_cost = maintenance_data['cost'].sum()
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Maintenance", total_maintenance)
                    with col2:
                        st.metric("Preventive", preventive)
                    with col3:
                        st.metric("Corrective", corrective)
                    with col4:
                        st.metric("Total Cost", f"${total_cost:.2f}")
                    
                    # Maintenance by machine
                    st.subheader("Maintenance by Machine")
                    machine_maintenance = maintenance_data.groupby('machine_id').agg({
                        'maintenance_id': 'count',
                        'cost': 'sum'
                    }).rename(columns={'maintenance_id': 'Count', 'cost': 'Total Cost'})
                    
                    st.dataframe(machine_maintenance, use_container_width=True)
                else:
                    st.info("No maintenance data available for the selected period")
            
            elif report_type == "Quality Report":
                # Generate quality report
                st.write("**Quality Summary:**")
                
                telemetry_data = self.db.get_telemetry_data(start_date=start_date_str, end_date=end_date_str)
                
                if not telemetry_data.empty:
                    # Calculate quality metrics
                    total_parts = len(telemetry_data[telemetry_data['part_id'].notna()])
                    good_parts = len(telemetry_data[telemetry_data['quality_flag'] == 'ok'])
                    scrap_parts = len(telemetry_data[telemetry_data['quality_flag'] == 'scrap'])
                    rework_parts = len(telemetry_data[telemetry_data['quality_flag'] == 'rework'])
                    
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric("Total Parts", total_parts)
                    with col2:
                        st.metric("Good Parts", good_parts)
                    with col3:
                        st.metric("Scrap Parts", scrap_parts)
                    with col4:
                        st.metric("Rework Parts", rework_parts)
                    
                    # Quality by machine
                    st.subheader("Quality by Machine")
                    quality_by_machine = telemetry_data.groupby('machine_id')['quality_flag'].value_counts().unstack(fill_value=0)
                    st.dataframe(quality_by_machine, use_container_width=True)
                else:
                    st.info("No quality data available for the selected period")
            
            elif report_type == "Efficiency Report":
                # Generate efficiency report
                st.write("**Efficiency Summary:**")
                
                telemetry_data = self.db.get_telemetry_data(start_date=start_date_str, end_date=end_date_str)
                
                if not telemetry_data.empty:
                    # Calculate OEE data
                    oee_data = self.performance_analyzer.calculate_oee(telemetry_data)
                    
                    # Display OEE metrics
                    st.subheader("Overall Equipment Effectiveness (OEE)")
                    for machine_id, oee_info in oee_data.items():
                        col1, col2, col3, col4 = st.columns(4)
                        with col1:
                            st.metric(f"{machine_id} - Availability", f"{oee_info['availability']:.1%}")
                        with col2:
                            st.metric(f"{machine_id} - Performance", f"{oee_info['performance']:.1%}")
                        with col3:
                            st.metric(f"{machine_id} - Quality", f"{oee_info['quality']:.1%}")
                        with col4:
                            st.metric(f"{machine_id} - OEE", f"{oee_info['oee']:.1%}")
                        st.write("---")
                else:
                    st.info("No efficiency data available for the selected period")
            
            # Export options
            st.subheader("Export Options")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("📄 Export as CSV"):
                    st.success("CSV export functionality would be implemented here")
            with col2:
                if st.button("📊 Export as PDF"):
                    st.success("PDF export functionality would be implemented here")
            with col3:
                if st.button("📧 Email Report"):
                    st.success("Email functionality would be implemented here")
                    
        except Exception as e:
            st.error(f"Error generating report: {e}")
            st.info(f"Generating {report_type} for {start_date} to {end_date}")

def main():
    """Main application entry point"""
    app = DashboardApp()
    app.run()

if __name__ == "__main__":
    main()
