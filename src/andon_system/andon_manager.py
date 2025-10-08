"""
Andon System Manager
Alert generation based on thresholds for industrial machines
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import yaml

class AndonManager:
    """
    Andon system for generating alerts based on machine thresholds
    """
    
    def __init__(self, config_path="config/machines.yaml"):
        """Initialize the andon system"""
        self.config_path = config_path
        self.load_config()
        self.active_alerts = []
        
    def load_config(self):
        """Load machine configuration and alert thresholds"""
        try:
            with open(self.config_path, 'r') as file:
                self.config = yaml.safe_load(file)
            self.machines = self.config['machines']
            self.andon_thresholds = self.config.get('andon_thresholds', {})
        except Exception as e:
            print(f"Error loading config: {e}")
            self.config = {}
            self.machines = {}
            self.andon_thresholds = {}
    
    def generate_alerts(self, telemetry_data: pd.DataFrame) -> pd.DataFrame:
        """
        Generate andon alerts based on telemetry data and thresholds
        """
        alerts = []
        
        for _, row in telemetry_data.iterrows():
            machine_id = row['machine_id']
            timestamp = row['timestamp']
            
            if machine_id not in self.machines:
                continue
                
            machine_config = self.machines[machine_id]
            sensors = machine_config.get('sensors', {})
            
            # Check each sensor for threshold violations
            for sensor_name, sensor_config in sensors.items():
                if sensor_name not in row or pd.isna(row[sensor_name]):
                    continue
                    
                sensor_value = row[sensor_name]
                threshold_warning = sensor_config.get('threshold_warning')
                threshold_critical = sensor_config.get('threshold_critical')
                
                if threshold_warning is None or threshold_critical is None:
                    continue
                
                # Determine alert severity
                severity = None
                if sensor_value >= threshold_critical:
                    severity = 'Critical'
                elif sensor_value >= threshold_warning:
                    severity = 'High'
                
                if severity:
                    alert = {
                        'timestamp': timestamp,
                        'machine_id': machine_id,
                        'sensor_name': sensor_name,
                        'sensor_value': sensor_value,
                        'threshold_warning': threshold_warning,
                        'threshold_critical': threshold_critical,
                        'severity': severity,
                        'description': f"{sensor_name} {severity} Alert: {sensor_value:.2f} {sensor_config.get('unit', '')}",
                        'status': 'Active'
                    }
                    alerts.append(alert)
        
        return pd.DataFrame(alerts)
    
    def get_active_alerts(self, alerts_data: pd.DataFrame) -> pd.DataFrame:
        """Get currently active alerts"""
        if alerts_data.empty:
            return pd.DataFrame()
        
        # Filter for recent alerts (last 24 hours)
        cutoff_time = datetime.now() - timedelta(hours=24)
        recent_alerts = alerts_data[alerts_data['timestamp'] >= cutoff_time]
        
        return recent_alerts.sort_values('timestamp', ascending=False)
    
    def get_alert_summary(self, alerts_data: pd.DataFrame) -> Dict:
        """Get alert summary statistics"""
        if alerts_data.empty:
            return {
                'total_alerts': 0,
                'critical_alerts': 0,
                'high_alerts': 0,
                'active_machines': 0
            }
        
        summary = {
            'total_alerts': len(alerts_data),
            'critical_alerts': len(alerts_data[alerts_data['severity'] == 'Critical']),
            'high_alerts': len(alerts_data[alerts_data['severity'] == 'High']),
            'active_machines': alerts_data['machine_id'].nunique()
        }
        
        return summary
    
    def get_machine_alert_history(self, alerts_data: pd.DataFrame, machine_id: str) -> pd.DataFrame:
        """Get alert history for a specific machine"""
        if alerts_data.empty:
            return pd.DataFrame()
        
        machine_alerts = alerts_data[alerts_data['machine_id'] == machine_id]
        return machine_alerts.sort_values('timestamp', ascending=False)
    
    def get_alert_trends(self, alerts_data: pd.DataFrame, days: int = 7) -> pd.DataFrame:
        """Get alert trends over time"""
        if alerts_data.empty:
            return pd.DataFrame()
        
        # Filter for last N days
        cutoff_time = datetime.now() - timedelta(days=days)
        recent_alerts = alerts_data[alerts_data['timestamp'] >= cutoff_time]
        
        # Group by date and severity
        recent_alerts['date'] = pd.to_datetime(recent_alerts['timestamp']).dt.date
        trends = recent_alerts.groupby(['date', 'severity']).size().reset_index(name='count')
        
        return trends
    
    def get_top_alerting_machines(self, alerts_data: pd.DataFrame, limit: int = 10) -> pd.DataFrame:
        """Get machines with most alerts"""
        if alerts_data.empty:
            return pd.DataFrame()
        
        machine_alert_counts = alerts_data.groupby('machine_id').agg({
            'severity': 'count',
            'timestamp': 'max'
        }).rename(columns={'severity': 'alert_count'})
        
        machine_alert_counts = machine_alert_counts.sort_values('alert_count', ascending=False)
        return machine_alert_counts.head(limit)
    
    def get_sensor_alert_frequency(self, alerts_data: pd.DataFrame) -> pd.DataFrame:
        """Get sensor alert frequency"""
        if alerts_data.empty:
            return pd.DataFrame()
        
        sensor_counts = alerts_data.groupby(['machine_id', 'sensor_name']).size().reset_index(name='alert_count')
        sensor_counts = sensor_counts.sort_values('alert_count', ascending=False)
        
        return sensor_counts
    
    def resolve_alert(self, alert_id: str, resolution_notes: str = "") -> bool:
        """Resolve an alert"""
        # This would typically update a database
        # For now, we'll just return True
        return True
    
    def get_alert_recommendations(self, alerts_data: pd.DataFrame) -> List[Dict]:
        """Get recommendations based on alert patterns"""
        recommendations = []
        
        if alerts_data.empty:
            return recommendations
        
        # Analyze patterns
        critical_alerts = alerts_data[alerts_data['severity'] == 'Critical']
        
        if len(critical_alerts) > 0:
            recommendations.append({
                'type': 'Critical Alert',
                'message': f"{len(critical_alerts)} critical alerts require immediate attention",
                'priority': 'High'
            })
        
        # Check for repeated alerts from same machine
        machine_alert_counts = alerts_data.groupby('machine_id').size()
        repeated_alert_machines = machine_alert_counts[machine_alert_counts > 5]
        
        for machine_id, count in repeated_alert_machines.items():
            recommendations.append({
                'type': 'Repeated Alerts',
                'message': f"Machine {machine_id} has {count} alerts - consider maintenance",
                'priority': 'Medium'
            })
        
        return recommendations
