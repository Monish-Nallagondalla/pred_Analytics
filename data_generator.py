"""
Synthetic Data Generator for Apex Components Predictive Maintenance System
Generates realistic sensor data, failure patterns, and maintenance events
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import json
import sqlite3
from config import MACHINES, ALERT_THRESHOLDS, SIMULATION_START_DATE, SIMULATION_DAYS, SAMPLE_RATE_SECONDS, LOW_FREQ_SAMPLE_RATE

class MachineDataGenerator:
    def __init__(self, machine_id, machine_config):
        self.machine_id = machine_id
        self.config = machine_config
        self.degradation_factor = 0.0  # Will increase over time
        self.failure_probability = 0.001  # Base failure probability
        self.current_cycle_id = None
        self.part_count = 0
        
    def generate_normal_cycle(self, timestamp):
        """Generate normal operational data for a cycle"""
        cycle_data = {
            'timestamp': timestamp,
            'machine_id': self.machine_id,
            'machine_type': self.config['type'],
            'shift': self._get_shift(timestamp),
            'state': self._get_machine_state(timestamp),
            'cycle_id': self._get_cycle_id(),
            'part_id': f"PART_{self.part_count:06d}" if self._is_production_time(timestamp) else None,
            'quality_flag': 'ok'
        }
        
        # Add sensor data based on machine type
        if self.config['type'] == 'CNC_Mill':
            cycle_data.update(self._generate_cnc_mill_data(timestamp))
        elif self.config['type'] == 'CNC_Lathe':
            cycle_data.update(self._generate_cnc_lathe_data(timestamp))
        elif self.config['type'] == 'Robot':
            cycle_data.update(self._generate_robot_data(timestamp))
        elif self.config['type'] == 'Compressor':
            cycle_data.update(self._generate_compressor_data(timestamp))
        elif self.config['type'] == 'Laser_Cutter':
            cycle_data.update(self._generate_laser_data(timestamp))
        elif self.config['type'] == 'Press_Brake':
            cycle_data.update(self._generate_press_brake_data(timestamp))
        elif self.config['type'] == 'Bench_Drill':
            cycle_data.update(self._generate_drill_data(timestamp))
        elif self.config['type'] == 'Grinder':
            cycle_data.update(self._generate_grinder_data(timestamp))
            
        # Add degradation effects
        cycle_data = self._apply_degradation(cycle_data, timestamp)
        
        # Check for failures
        cycle_data = self._check_failures(cycle_data, timestamp)
        
        return cycle_data
    
    def _generate_cnc_mill_data(self, timestamp):
        """Generate CNC Mill specific sensor data"""
        state = self._get_machine_state(timestamp)
        
        if state == 'idle':
            return {
                'spindle_rpm': 0,
                'motor_current': 0.1 + random.uniform(-0.05, 0.05),
                'vibration_rms': 0.1 + random.uniform(-0.05, 0.05),
                'axis_x': 0,
                'axis_y': 0,
                'axis_z': 0,
                'servo_temp': 30 + random.uniform(-2, 2),
                'power_draw': 0.5 + random.uniform(-0.1, 0.1)
            }
        elif state == 'cutting':
            rpm = random.uniform(500, 4500)
            current = 2 + (rpm / 7500) * 8 + random.uniform(-1, 1)
            vibration = 0.5 + (rpm / 7500) * 1.5 + random.uniform(-0.2, 0.2)
            
            return {
                'spindle_rpm': int(rpm),
                'motor_current': max(0, current),
                'vibration_rms': max(0.1, vibration),
                'axis_x': random.uniform(0, 914),
                'axis_y': random.uniform(0, 305),
                'axis_z': random.uniform(0, 305),
                'servo_temp': 40 + (rpm / 7500) * 20 + random.uniform(-3, 3),
                'power_draw': 5 + (rpm / 7500) * 8 + random.uniform(-1, 1)
            }
        else:  # fault or maintenance
            return {
                'spindle_rpm': 0,
                'motor_current': 0,
                'vibration_rms': random.uniform(3, 8) if state == 'fault' else 0.1,
                'axis_x': 0,
                'axis_y': 0,
                'axis_z': 0,
                'servo_temp': 60 + random.uniform(-5, 5) if state == 'fault' else 30,
                'power_draw': 0
            }
    
    def _generate_cnc_lathe_data(self, timestamp):
        """Generate CNC Lathe specific sensor data"""
        state = self._get_machine_state(timestamp)
        
        if state == 'idle':
            return {
                'spindle_rpm': 0,
                'spindle_torque': 0,
                'chuck_status': 'open',
                'turret_index': 0,
                'vibration_rms': 0.1 + random.uniform(-0.05, 0.05),
                'oil_temp': 30 + random.uniform(-2, 2)
            }
        elif state == 'cutting':
            rpm = random.uniform(300, 4000)
            torque = 2 + (rpm / 6000) * 10 + random.uniform(-1, 1)
            vibration = 0.5 + (rpm / 6000) * 1.5 + random.uniform(-0.2, 0.2)
            
            return {
                'spindle_rpm': int(rpm),
                'spindle_torque': max(0, torque),
                'chuck_status': 'closed',
                'turret_index': random.randint(1, 8),
                'vibration_rms': max(0.1, vibration),
                'oil_temp': 35 + (rpm / 6000) * 15 + random.uniform(-2, 2)
            }
        else:
            return {
                'spindle_rpm': 0,
                'spindle_torque': 0,
                'chuck_status': 'open',
                'turret_index': 0,
                'vibration_rms': random.uniform(3, 8) if state == 'fault' else 0.1,
                'oil_temp': 60 + random.uniform(-5, 5) if state == 'fault' else 30
            }
    
    def _generate_robot_data(self, timestamp):
        """Generate Robot specific sensor data"""
        state = self._get_machine_state(timestamp)
        
        if state == 'idle':
            return {
                'joint_pos_1': 0, 'joint_pos_2': 0, 'joint_pos_3': 0,
                'joint_pos_4': 0, 'joint_pos_5': 0, 'joint_pos_6': 0,
                'joint_current_1': 0.1, 'joint_current_2': 0.1, 'joint_current_3': 0.1,
                'joint_current_4': 0.1, 'joint_current_5': 0.1, 'joint_current_6': 0.1,
                'tcp_force': 0, 'controller_temp': 30
            }
        elif state == 'cutting':
            # Simulate pick and place cycle
            cycle_time = random.uniform(1, 6)
            joint_positions = [random.uniform(-180, 180) for _ in range(6)]
            joint_currents = [random.uniform(0.5, 3) for _ in range(6)]
            
            return {
                'joint_pos_1': joint_positions[0], 'joint_pos_2': joint_positions[1], 'joint_pos_3': joint_positions[2],
                'joint_pos_4': joint_positions[3], 'joint_pos_5': joint_positions[4], 'joint_pos_6': joint_positions[5],
                'joint_current_1': joint_currents[0], 'joint_current_2': joint_currents[1], 'joint_current_3': joint_currents[2],
                'joint_current_4': joint_currents[3], 'joint_current_5': joint_currents[4], 'joint_current_6': joint_currents[5],
                'tcp_force': random.uniform(0, 6), 'controller_temp': 35 + random.uniform(-2, 2)
            }
        else:
            return {
                'joint_pos_1': 0, 'joint_pos_2': 0, 'joint_pos_3': 0,
                'joint_pos_4': 0, 'joint_pos_5': 0, 'joint_pos_6': 0,
                'joint_current_1': 0, 'joint_current_2': 0, 'joint_current_3': 0,
                'joint_current_4': 0, 'joint_current_5': 0, 'joint_current_6': 0,
                'tcp_force': 0, 'controller_temp': 30
            }
    
    def _generate_compressor_data(self, timestamp):
        """Generate Compressor specific sensor data"""
        state = self._get_machine_state(timestamp)
        
        if state == 'idle':
            return {
                'suction_pressure': 0,
                'discharge_pressure': 0,
                'motor_current': 0,
                'oil_temp': 30,
                'vibration_rms': 0.1,
                'runtime_hours': self._get_runtime_hours(timestamp),
                'duty_cycle': 0,
                'condensate_level': random.uniform(0, 10)
            }
        elif state == 'cutting':
            suction = random.uniform(0.5, 1.5)
            discharge = random.uniform(6, 8.5)
            current = 5 + (discharge / 8.5) * 6 + random.uniform(-1, 1)
            vibration = 0.5 + random.uniform(-0.2, 0.2)
            
            return {
                'suction_pressure': suction,
                'discharge_pressure': discharge,
                'motor_current': max(0, current),
                'oil_temp': 50 + (current / 11) * 20 + random.uniform(-3, 3),
                'vibration_rms': max(0.1, vibration),
                'runtime_hours': self._get_runtime_hours(timestamp),
                'duty_cycle': random.uniform(60, 90),
                'condensate_level': random.uniform(5, 15)
            }
        else:
            return {
                'suction_pressure': 0,
                'discharge_pressure': 0,
                'motor_current': 0,
                'oil_temp': 30,
                'vibration_rms': random.uniform(3, 8) if state == 'fault' else 0.1,
                'runtime_hours': self._get_runtime_hours(timestamp),
                'duty_cycle': 0,
                'condensate_level': random.uniform(0, 10)
            }
    
    def _generate_laser_data(self, timestamp):
        """Generate Laser Cutter specific sensor data"""
        state = self._get_machine_state(timestamp)
        
        if state == 'idle':
            return {
                'laser_power': 0,
                'head_temp': 25,
                'exhaust_flow': 0,
                'focal_height': 0,
                'position_x': 0,
                'position_y': 0,
                'interlocks': 'ok'
            }
        elif state == 'cutting':
            power = random.uniform(30, 60)
            head_temp = 30 + (power / 60) * 20 + random.uniform(-2, 2)
            exhaust_flow = 100 + (power / 60) * 200 + random.uniform(-20, 20)
            
            return {
                'laser_power': power,
                'head_temp': max(25, head_temp),
                'exhaust_flow': max(50, exhaust_flow),
                'focal_height': random.uniform(0, 10),
                'position_x': random.uniform(0, 610),
                'position_y': random.uniform(0, 305),
                'interlocks': 'ok'
            }
        else:
            return {
                'laser_power': 0,
                'head_temp': 25,
                'exhaust_flow': 0,
                'focal_height': 0,
                'position_x': 0,
                'position_y': 0,
                'interlocks': 'fault' if state == 'fault' else 'ok'
            }
    
    def _generate_press_brake_data(self, timestamp):
        """Generate Press Brake specific sensor data"""
        state = self._get_machine_state(timestamp)
        
        if state == 'idle':
            return {
                'ram_position': 0,
                'hydraulic_pressure': 0,
                'load_cell': 0,
                'cycle_time': 0,
                'crowning_actuator': 0,
                'motor_current': 0,
                'back_gauge': 0
            }
        elif state == 'cutting':
            ram_pos = random.uniform(0, 100)
            pressure = 50 + (ram_pos / 100) * 50 + random.uniform(-5, 5)
            load = 20 + (ram_pos / 100) * 80 + random.uniform(-10, 10)
            
            return {
                'ram_position': ram_pos,
                'hydraulic_pressure': max(0, pressure),
                'load_cell': max(0, load),
                'cycle_time': random.uniform(10, 30),
                'crowning_actuator': random.uniform(-5, 5),
                'motor_current': 5 + (pressure / 100) * 10 + random.uniform(-1, 1),
                'back_gauge': random.uniform(0, 1000)
            }
        else:
            return {
                'ram_position': 0,
                'hydraulic_pressure': 0,
                'load_cell': 0,
                'cycle_time': 0,
                'crowning_actuator': 0,
                'motor_current': 0,
                'back_gauge': 0
            }
    
    def _generate_drill_data(self, timestamp):
        """Generate Bench Drill specific sensor data"""
        state = self._get_machine_state(timestamp)
        
        if state == 'idle':
            return {
                'spindle_rpm': 0,
                'motor_current': 0,
                'drill_feed': 0,
                'chuck_state': 'open',
                'stroke_count': 0
            }
        elif state == 'cutting':
            rpm = random.uniform(200, 2500)
            current = 0.2 + (rpm / 2500) * 0.5 + random.uniform(-0.1, 0.1)
            feed = random.uniform(0, 50)
            
            return {
                'spindle_rpm': int(rpm),
                'motor_current': max(0, current),
                'drill_feed': feed,
                'chuck_state': 'closed',
                'stroke_count': random.randint(1, 10)
            }
        else:
            return {
                'spindle_rpm': 0,
                'motor_current': 0,
                'drill_feed': 0,
                'chuck_state': 'open',
                'stroke_count': 0
            }
    
    def _generate_grinder_data(self, timestamp):
        """Generate Surface Grinder specific sensor data"""
        state = self._get_machine_state(timestamp)
        
        if state == 'idle':
            return {
                'wheel_rpm': 0,
                'spindle_current': 0,
                'coolant_temp': 25,
                'coolant_flow': 0,
                'table_feed': 0,
                'vibration_rms': 0.1
            }
        elif state == 'cutting':
            rpm = random.uniform(1000, 3000)
            current = 2 + (rpm / 3000) * 8 + random.uniform(-1, 1)
            coolant_temp = 30 + (rpm / 3000) * 15 + random.uniform(-2, 2)
            coolant_flow = 50 + (rpm / 3000) * 100 + random.uniform(-10, 10)
            
            return {
                'wheel_rpm': int(rpm),
                'spindle_current': max(0, current),
                'coolant_temp': max(25, coolant_temp),
                'coolant_flow': max(10, coolant_flow),
                'table_feed': random.uniform(10, 50),
                'vibration_rms': 0.5 + (rpm / 3000) * 1.5 + random.uniform(-0.2, 0.2)
            }
        else:
            return {
                'wheel_rpm': 0,
                'spindle_current': 0,
                'coolant_temp': 25,
                'coolant_flow': 0,
                'table_feed': 0,
                'vibration_rms': random.uniform(3, 8) if state == 'fault' else 0.1
            }
    
    def _get_shift(self, timestamp):
        """Determine which shift based on timestamp"""
        hour = timestamp.hour
        if 8 <= hour < 16:
            return 1
        elif 16 <= hour < 24 or 0 <= hour < 8:
            return 2
        else:
            return 1
    
    def _get_machine_state(self, timestamp):
        """Determine machine state based on time and degradation"""
        hour = timestamp.hour
        minute = timestamp.minute
        
        # Weekend limited operations
        if timestamp.weekday() >= 5:  # Saturday = 5, Sunday = 6
            if random.random() < 0.3:  # 30% chance of weekend operation
                return 'idle'
            else:
                return 'idle'
        
        # Check for maintenance windows (every 4 hours for 30 minutes)
        if minute >= 0 and minute < 30 and hour % 4 == 0:
            return 'maintenance'
        
        # Check for failures
        if random.random() < self.failure_probability:
            return 'fault'
        
        # Normal operation states
        if 8 <= hour < 16 or 16 <= hour < 24:
            states = ['idle', 'cutting', 'toolchange']
            weights = [0.2, 0.6, 0.2]
            return random.choices(states, weights=weights)[0]
        else:
            return 'idle'
    
    def _get_cycle_id(self):
        """Generate cycle ID"""
        if self.current_cycle_id is None:
            self.current_cycle_id = f"CYC_{self.machine_id}_{int(datetime.now().timestamp())}"
        return self.current_cycle_id
    
    def _is_production_time(self, timestamp):
        """Check if it's production time"""
        hour = timestamp.hour
        return (8 <= hour < 16 or 16 <= hour < 24) and timestamp.weekday() < 5
    
    def _get_runtime_hours(self, timestamp):
        """Calculate runtime hours for the machine"""
        # Simplified calculation - in reality would track actual runtime
        days_since_start = (timestamp - SIMULATION_START_DATE).days
        return days_since_start * 16  # 16 hours per day
    
    def _apply_degradation(self, data, timestamp):
        """Apply degradation effects to sensor data"""
        days_since_start = (timestamp - SIMULATION_START_DATE).days
        
        # Increase degradation factor over time
        self.degradation_factor = min(1.0, days_since_start / 30.0)  # Max degradation after 30 days
        
        # Apply degradation to vibration and temperature
        if 'vibration_rms' in data:
            data['vibration_rms'] *= (1 + self.degradation_factor * 0.5)
        
        if 'servo_temp' in data:
            data['servo_temp'] += self.degradation_factor * 10
        
        if 'oil_temp' in data:
            data['oil_temp'] += self.degradation_factor * 5
        
        # Increase failure probability with degradation
        self.failure_probability = 0.001 + (self.degradation_factor * 0.01)
        
        return data
    
    def _check_failures(self, data, timestamp):
        """Check for failure conditions and update data accordingly"""
        # Check vibration threshold
        if 'vibration_rms' in data and data['vibration_rms'] > ALERT_THRESHOLDS['critical_vibration']:
            data['state'] = 'fault'
            data['quality_flag'] = 'scrap'
            data['andon_trigger'] = 1
            return data
        
        # Check temperature threshold
        temp_keys = ['servo_temp', 'oil_temp', 'head_temp', 'coolant_temp']
        for key in temp_keys:
            if key in data and data[key] > ALERT_THRESHOLDS['high_temp']:
                data['state'] = 'fault'
                data['quality_flag'] = 'scrap'
                data['andon_trigger'] = 1
                return data
        
        # Check current spike
        current_keys = ['motor_current', 'spindle_current', 'spindle_torque']
        for key in current_keys:
            if key in data and data[key] > 15:  # High current threshold
                data['state'] = 'fault'
                data['quality_flag'] = 'scrap'
                data['andon_trigger'] = 1
                return data
        
        # Random quality issues
        if random.random() < 0.01:  # 1% chance of quality issue
            data['quality_flag'] = 'rework'
            data['andon_trigger'] = 1
        
        # Add andon trigger flag
        data['andon_trigger'] = 0
        
        return data

class DataSimulator:
    def __init__(self):
        self.generators = {}
        for machine_id, config in MACHINES.items():
            self.generators[machine_id] = MachineDataGenerator(machine_id, config)
    
    def generate_data(self, start_date, days):
        """Generate synthetic data for all machines"""
        all_data = []
        
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            
            for hour in range(24):
                for minute in range(0, 60, 5):  # 5-minute intervals to reduce data volume
                    timestamp = current_date.replace(hour=hour, minute=minute, second=0)
                    
                    for machine_id, generator in self.generators.items():
                        data = generator.generate_normal_cycle(timestamp)
                        all_data.append(data)
        
        return pd.DataFrame(all_data)
    
    def generate_events(self, start_date, days):
        """Generate event log data"""
        events = []
        event_id = 1
        
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            
            # Generate random events
            for _ in range(random.randint(0, 5)):  # 0-5 events per day
                event = {
                    'event_id': f"EVT_{event_id:06d}",
                    'timestamp': current_date + timedelta(hours=random.randint(8, 22)),
                    'machine_id': random.choice(list(MACHINES.keys())),
                    'event_type': random.choice(['toolchange', 'fault_code', 'manual_andon', 'operator_note']),
                    'fault_code': f"FC_{random.randint(100, 999)}" if random.random() < 0.3 else None,
                    'severity': random.choice(['low', 'medium', 'high', 'critical']),
                    'description': f"Event description {event_id}",
                    'resolved_timestamp': None,
                    'resolution_action': None,
                    'downtime_minutes': 0
                }
                
                # Add resolution for some events
                if random.random() < 0.7:  # 70% of events are resolved
                    event['resolved_timestamp'] = event['timestamp'] + timedelta(minutes=random.randint(5, 120))
                    event['resolution_action'] = random.choice(['replaced_part', 'adjusted_settings', 'cleaned_machine', 'software_update'])
                    event['downtime_minutes'] = random.randint(5, 120)
                
                events.append(event)
                event_id += 1
        
        return pd.DataFrame(events)
    
    def generate_maintenance_history(self, start_date, days):
        """Generate maintenance history data"""
        maintenance = []
        maintenance_id = 1
        
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            
            # Scheduled maintenance every 7 days
            if day % 7 == 0:
                for machine_id in MACHINES.keys():
                    maint = {
                        'maintenance_id': f"MAINT_{maintenance_id:06d}",
                        'machine_id': machine_id,
                        'start_time': current_date + timedelta(hours=8),
                        'end_time': current_date + timedelta(hours=10),
                        'maintenance_type': 'preventive',
                        'parts_replaced': random.choice(['bearing', 'belt', 'filter', 'oil']),
                        'technician_id': f"TECH_{random.randint(1, 3)}",
                        'cost': random.uniform(100, 1000),
                        'notes': f"Preventive maintenance for {machine_id}"
                    }
                    maintenance.append(maint)
                    maintenance_id += 1
            
            # Unscheduled maintenance (repairs)
            if random.random() < 0.1:  # 10% chance per day
                machine_id = random.choice(list(MACHINES.keys()))
                maint = {
                    'maintenance_id': f"MAINT_{maintenance_id:06d}",
                    'machine_id': machine_id,
                    'start_time': current_date + timedelta(hours=random.randint(8, 20)),
                    'end_time': current_date + timedelta(hours=random.randint(8, 20)) + timedelta(minutes=random.randint(30, 180)),
                    'maintenance_type': 'corrective',
                    'parts_replaced': random.choice(['spindle', 'motor', 'sensor', 'controller']),
                    'technician_id': f"TECH_{random.randint(1, 3)}",
                    'cost': random.uniform(500, 5000),
                    'notes': f"Emergency repair for {machine_id}"
                }
                maintenance.append(maint)
                maintenance_id += 1
        
        return pd.DataFrame(maintenance)

if __name__ == "__main__":
    # Generate sample data
    simulator = DataSimulator()
    
    print("Generating synthetic data...")
    telemetry_data = simulator.generate_data(SIMULATION_START_DATE, 7)  # 7 days for testing
    events_data = simulator.generate_events(SIMULATION_START_DATE, 7)
    maintenance_data = simulator.generate_maintenance_history(SIMULATION_START_DATE, 7)
    
    print(f"Generated {len(telemetry_data)} telemetry records")
    print(f"Generated {len(events_data)} event records")
    print(f"Generated {len(maintenance_data)} maintenance records")
    
    # Save to CSV for inspection
    telemetry_data.to_csv('sample_telemetry.csv', index=False)
    events_data.to_csv('sample_events.csv', index=False)
    maintenance_data.to_csv('sample_maintenance.csv', index=False)
    
    print("Sample data saved to CSV files")
