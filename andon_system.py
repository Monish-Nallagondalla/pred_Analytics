"""
Andon System for Real-time Alerts and Escalation
Implements automated alerting based on sensor thresholds and ML predictions
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from config import ALERT_THRESHOLDS, MACHINES

class AndonTrigger:
    def __init__(self, machine_id, trigger_type, severity, description, timestamp=None):
        self.machine_id = machine_id
        self.trigger_type = trigger_type
        self.severity = severity
        self.description = description
        self.timestamp = timestamp or datetime.now()
        self.resolved = False
        self.resolution_time = None
        self.resolution_action = None
    
    def resolve(self, action="Manual resolution"):
        """Mark the Andon trigger as resolved"""
        self.resolved = True
        self.resolution_time = datetime.now()
        self.resolution_action = action
    
    def to_dict(self):
        """Convert to dictionary for storage"""
        return {
            'machine_id': self.machine_id,
            'trigger_type': self.trigger_type,
            'severity': self.severity,
            'description': self.description,
            'timestamp': self.timestamp.isoformat(),
            'resolved': self.resolved,
            'resolution_time': self.resolution_time.isoformat() if self.resolution_time else None,
            'resolution_action': self.resolution_action
        }

class AlertRule:
    def __init__(self, name, condition, severity, escalation_level, description):
        self.name = name
        self.condition = condition  # Function that takes sensor data and returns boolean
        self.severity = severity
        self.escalation_level = escalation_level
        self.description = description
    
    def evaluate(self, data):
        """Evaluate the rule against sensor data"""
        try:
            return self.condition(data)
        except Exception as e:
            logging.error(f"Error evaluating rule {self.name}: {e}")
            return False

class AndonSystem:
    def __init__(self):
        self.active_triggers = []
        self.alert_rules = []
        self.escalation_config = {
            'low': {'email': True, 'sms': False, 'dashboard': True},
            'medium': {'email': True, 'sms': False, 'dashboard': True},
            'high': {'email': True, 'sms': True, 'dashboard': True},
            'critical': {'email': True, 'sms': True, 'dashboard': True, 'stop_machine': True}
        }
        self.setup_logging()
        self.setup_default_rules()
    
    def setup_logging(self):
        """Setup logging for the Andon system"""
        # Check if logger already exists to prevent duplicate handlers
        if not hasattr(self, 'logger') or not self.logger.handlers:
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler('andon_system.log'),
                    logging.StreamHandler()
                ]
            )
        self.logger = logging.getLogger('AndonSystem')
    
    def setup_default_rules(self):
        """Setup default alert rules"""
        # Critical vibration rule
        self.add_rule(
            name="Critical Vibration",
            condition=lambda data: data.get('vibration_rms', 0) > ALERT_THRESHOLDS['critical_vibration'],
            severity="critical",
            escalation_level=4,
            description="Vibration exceeds critical threshold"
        )
        
        # High temperature rule
        self.add_rule(
            name="High Temperature",
            condition=lambda data: any(data.get(temp_key, 0) > ALERT_THRESHOLDS['high_temp'] 
                                    for temp_key in ['servo_temp', 'oil_temp', 'head_temp', 'coolant_temp']),
            severity="high",
            escalation_level=3,
            description="Temperature exceeds safe operating limits"
        )
        
        # Current spike rule
        self.add_rule(
            name="Current Spike",
            condition=lambda data: any(data.get(current_key, 0) > 15 
                                    for current_key in ['motor_current', 'spindle_current', 'spindle_torque']),
            severity="high",
            escalation_level=3,
            description="Motor current exceeds normal operating range"
        )
        
        # Quality issue rule
        self.add_rule(
            name="Quality Issue",
            condition=lambda data: data.get('quality_flag') in ['scrap', 'rework'],
            severity="medium",
            escalation_level=2,
            description="Quality issue detected in production"
        )
        
        # Machine fault rule
        self.add_rule(
            name="Machine Fault",
            condition=lambda data: data.get('state') == 'fault',
            severity="critical",
            escalation_level=4,
            description="Machine fault detected"
        )
        
        # Anomaly detection rule
        self.add_rule(
            name="ML Anomaly",
            condition=lambda data: data.get('anomaly_detected', False),
            severity="medium",
            escalation_level=2,
            description="ML model detected anomalous behavior"
        )
        
        # RUL prediction rule
        self.add_rule(
            name="Low RUL",
            condition=lambda data: data.get('rul_hours', 24) < 24,
            severity="high",
            escalation_level=3,
            description="Remaining useful life is critically low"
        )
    
    def add_rule(self, name, condition, severity, escalation_level, description):
        """Add a new alert rule"""
        # Check if rule already exists to prevent duplicates
        existing_rule = next((rule for rule in self.alert_rules if rule.name == name), None)
        if existing_rule is None:
            rule = AlertRule(name, condition, severity, escalation_level, description)
            self.alert_rules.append(rule)
            self.logger.info(f"Added alert rule: {name}")
    
    def evaluate_sensor_data(self, data):
        """Evaluate sensor data against all rules"""
        triggered_rules = []
        
        for rule in self.alert_rules:
            if rule.evaluate(data):
                triggered_rules.append(rule)
        
        return triggered_rules
    
    def create_andon_trigger(self, machine_id, trigger_type, severity, description):
        """Create a new Andon trigger"""
        trigger = AndonTrigger(machine_id, trigger_type, severity, description)
        self.active_triggers.append(trigger)
        
        self.logger.info(f"Created Andon trigger: {trigger_type} for {machine_id}")
        return trigger
    
    def process_sensor_data(self, data):
        """Process sensor data and create triggers as needed"""
        triggers_created = []
        
        # Evaluate all rules
        triggered_rules = self.evaluate_sensor_data(data)
        
        for rule in triggered_rules:
            # Check if trigger already exists for this machine and rule
            existing_trigger = self.get_active_trigger(data['machine_id'], rule.name)
            
            if not existing_trigger:
                # Create new trigger
                trigger = self.create_andon_trigger(
                    machine_id=data['machine_id'],
                    trigger_type=rule.name,
                    severity=rule.severity,
                    description=rule.description
                )
                triggers_created.append(trigger)
                
                # Send alerts
                self.send_alerts(trigger)
        
        return triggers_created
    
    def get_active_trigger(self, machine_id, trigger_type):
        """Get active trigger for a machine and trigger type"""
        for trigger in self.active_triggers:
            if (trigger.machine_id == machine_id and 
                trigger.trigger_type == trigger_type and 
                not trigger.resolved):
                return trigger
        return None
    
    def resolve_trigger(self, machine_id, trigger_type, action="Manual resolution"):
        """Resolve an active trigger"""
        trigger = self.get_active_trigger(machine_id, trigger_type)
        if trigger:
            trigger.resolve(action)
            self.logger.info(f"Resolved trigger: {trigger_type} for {machine_id}")
            return True
        return False
    
    def send_alerts(self, trigger):
        """Send alerts based on trigger severity"""
        severity = trigger.severity
        escalation_config = self.escalation_config.get(severity, {})
        
        # Send email alert
        if escalation_config.get('email', False):
            self.send_email_alert(trigger)
        
        # Send SMS alert
        if escalation_config.get('sms', False):
            self.send_sms_alert(trigger)
        
        # Update dashboard
        if escalation_config.get('dashboard', True):
            self.update_dashboard_alert(trigger)
        
        # Stop machine if critical
        if escalation_config.get('stop_machine', False):
            self.stop_machine(trigger.machine_id)
    
    def send_email_alert(self, trigger):
        """Send email alert"""
        try:
            # Email configuration (replace with actual SMTP settings)
            smtp_server = "smtp.gmail.com"
            smtp_port = 587
            sender_email = "alerts@apexcomponents.com"
            sender_password = "your_password"
            
            # Recipients based on severity
            recipients = {
                'low': ['operator@apexcomponents.com'],
                'medium': ['operator@apexcomponents.com', 'supervisor@apexcomponents.com'],
                'high': ['operator@apexcomponents.com', 'supervisor@apexcomponents.com', 'manager@apexcomponents.com'],
                'critical': ['operator@apexcomponents.com', 'supervisor@apexcomponents.com', 'manager@apexcomponents.com', 'maintenance@apexcomponents.com']
            }
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = ', '.join(recipients.get(trigger.severity, recipients['low']))
            msg['Subject'] = f"ALERT: {trigger.trigger_type} - {trigger.machine_id}"
            
            body = f"""
            Andon Alert Details:
            
            Machine ID: {trigger.machine_id}
            Trigger Type: {trigger.trigger_type}
            Severity: {trigger.severity.upper()}
            Description: {trigger.description}
            Timestamp: {trigger.timestamp}
            
            Please take appropriate action immediately.
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email (commented out for demo)
            # server = smtplib.SMTP(smtp_server, smtp_port)
            # server.starttls()
            # server.login(sender_email, sender_password)
            # server.send_message(msg)
            # server.quit()
            
            self.logger.info(f"Email alert sent for {trigger.machine_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to send email alert: {e}")
    
    def send_sms_alert(self, trigger):
        """Send SMS alert"""
        try:
            # SMS configuration (replace with actual SMS service)
            # This is a placeholder for SMS service integration
            self.logger.info(f"SMS alert sent for {trigger.machine_id}")
            
        except Exception as e:
            self.logger.error(f"Failed to send SMS alert: {e}")
    
    def update_dashboard_alert(self, trigger):
        """Update dashboard with alert information"""
        # This would update the dashboard in real-time
        self.logger.info(f"Dashboard alert updated for {trigger.machine_id}")
    
    def stop_machine(self, machine_id):
        """Stop machine operation"""
        self.logger.warning(f"STOPPING MACHINE: {machine_id}")
        # This would send stop command to the machine
        # In a real system, this would interface with machine controllers
    
    def get_active_triggers(self, machine_id=None):
        """Get all active triggers"""
        if machine_id:
            return [t for t in self.active_triggers if t.machine_id == machine_id and not t.resolved]
        else:
            return [t for t in self.active_triggers if not t.resolved]
    
    def get_trigger_history(self, machine_id=None, days=7):
        """Get trigger history for the last N days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        
        if machine_id:
            return [t for t in self.active_triggers if t.machine_id == machine_id and t.timestamp >= cutoff_date]
        else:
            return [t for t in self.active_triggers if t.timestamp >= cutoff_date]
    
    def get_trigger_statistics(self, days=7):
        """Get trigger statistics"""
        history = self.get_trigger_history(days=days)
        
        stats = {
            'total_triggers': len(history),
            'by_severity': {},
            'by_machine': {},
            'by_type': {},
            'resolution_rate': 0
        }
        
        # Count by severity
        for trigger in history:
            severity = trigger.severity
            stats['by_severity'][severity] = stats['by_severity'].get(severity, 0) + 1
        
        # Count by machine
        for trigger in history:
            machine_id = trigger.machine_id
            stats['by_machine'][machine_id] = stats['by_machine'].get(machine_id, 0) + 1
        
        # Count by type
        for trigger in history:
            trigger_type = trigger.trigger_type
            stats['by_type'][trigger_type] = stats['by_type'].get(trigger_type, 0) + 1
        
        # Calculate resolution rate
        resolved_count = len([t for t in history if t.resolved])
        stats['resolution_rate'] = resolved_count / len(history) if history else 0
        
        return stats
    
    def export_triggers(self, filepath="andon_triggers.json"):
        """Export triggers to JSON file"""
        triggers_data = [trigger.to_dict() for trigger in self.active_triggers]
        
        with open(filepath, 'w') as f:
            json.dump(triggers_data, f, indent=2)
        
        self.logger.info(f"Triggers exported to {filepath}")
    
    def import_triggers(self, filepath="andon_triggers.json"):
        """Import triggers from JSON file"""
        try:
            with open(filepath, 'r') as f:
                triggers_data = json.load(f)
            
            for trigger_data in triggers_data:
                trigger = AndonTrigger(
                    machine_id=trigger_data['machine_id'],
                    trigger_type=trigger_data['trigger_type'],
                    severity=trigger_data['severity'],
                    description=trigger_data['description'],
                    timestamp=datetime.fromisoformat(trigger_data['timestamp'])
                )
                
                if trigger_data['resolved']:
                    trigger.resolved = True
                    trigger.resolution_time = datetime.fromisoformat(trigger_data['resolution_time'])
                    trigger.resolution_action = trigger_data['resolution_action']
                
                self.active_triggers.append(trigger)
            
            self.logger.info(f"Triggers imported from {filepath}")
            
        except Exception as e:
            self.logger.error(f"Failed to import triggers: {e}")

class AndonDashboard:
    def __init__(self, andon_system):
        self.andon_system = andon_system
    
    def get_dashboard_data(self):
        """Get data for the Andon dashboard"""
        active_triggers = self.andon_system.get_active_triggers()
        trigger_stats = self.andon_system.get_trigger_statistics()
        
        # Group triggers by machine
        machine_status = {}
        for machine_id in MACHINES.keys():
            machine_triggers = [t for t in active_triggers if t.machine_id == machine_id]
            
            if machine_triggers:
                # Get highest severity trigger
                severity_levels = {'low': 1, 'medium': 2, 'high': 3, 'critical': 4}
                highest_severity = max(machine_triggers, key=lambda t: severity_levels.get(t.severity, 0))
                
                machine_status[machine_id] = {
                    'status': 'alert',
                    'severity': highest_severity.severity,
                    'trigger_count': len(machine_triggers),
                    'latest_trigger': highest_severity.trigger_type,
                    'timestamp': highest_severity.timestamp
                }
            else:
                machine_status[machine_id] = {
                    'status': 'normal',
                    'severity': None,
                    'trigger_count': 0,
                    'latest_trigger': None,
                    'timestamp': None
                }
        
        return {
            'machine_status': machine_status,
            'trigger_statistics': trigger_stats,
            'active_triggers': active_triggers
        }

if __name__ == "__main__":
    # Test Andon system
    print("Testing Andon System...")
    
    # Create Andon system
    andon_system = AndonSystem()
    
    # Test sensor data
    test_data = {
        'machine_id': 'VF2_01',
        'vibration_rms': 5.0,  # Above threshold
        'servo_temp': 45.0,
        'motor_current': 8.0,
        'quality_flag': 'ok',
        'state': 'cutting'
    }
    
    # Process sensor data
    triggers = andon_system.process_sensor_data(test_data)
    print(f"Created {len(triggers)} triggers")
    
    # Get active triggers
    active_triggers = andon_system.get_active_triggers()
    print(f"Active triggers: {len(active_triggers)}")
    
    # Get statistics
    stats = andon_system.get_trigger_statistics()
    print(f"Trigger statistics: {stats}")
    
    # Test dashboard
    dashboard = AndonDashboard(andon_system)
    dashboard_data = dashboard.get_dashboard_data()
    print(f"Dashboard data: {dashboard_data}")
