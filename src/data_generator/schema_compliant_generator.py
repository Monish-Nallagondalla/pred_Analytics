"""
Schema-Compliant Data Generator
Generates data exactly matching the project_plan.md schema specifications
"""

import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import yaml
import os
from typing import Dict, List, Tuple

class SchemaCompliantDataGenerator:
    """
    Data generator that follows project_plan.md schema exactly
    """
    
    def __init__(self, config_path="config/machines.yaml"):
        """Initialize the schema-compliant data generator"""
        self.config_path = config_path
        self.load_config()
        
    def load_config(self):
        """Load machine configuration"""
        try:
            with open(self.config_path, 'r') as file:
                self.config = yaml.safe_load(file)
            self.machines = self.config['machines']
        except Exception as e:
            print(f"Error loading config: {e}")
            self.config = {}
            self.machines = {}
    
    def generate_all_data(self, start_date=None, days=30):
        """Generate all data according to project plan schema"""
        if start_date is None:
            start_date = datetime.now() - timedelta(days=days)
        
        print("=" * 60)
        print("SCHEMA-COMPLIANT DATA GENERATION")
        print("=" * 60)
        print(f"Start Date: {start_date.strftime('%Y-%m-%d')}")
        print(f"Days: {days}")
        print("=" * 60)
        
        # Generate all required tables as per project plan
        orders_data = self.generate_orders_batch_data(start_date, days)
        machine_inventory = self.generate_machine_inventory()
        telemetry_data = self.generate_machine_telemetry(start_date, days)
        process_flow = self.generate_process_flow_data(start_date, days)
        maintenance_data = self.generate_maintenance_data(start_date, days)
        quality_inspection = self.generate_quality_inspection_data(start_date, days)
        kpis_data = self.generate_kpis_data(telemetry_data)
        material_inventory = self.generate_material_inventory_data(start_date, days)
        packaging_shipment = self.generate_packaging_shipment_data(start_date, days)
        alerts_data = self.generate_alerts_data(telemetry_data)
        
        # Save all data
        self.save_all_data({
            'orders_batch': orders_data,
            'machine_inventory': machine_inventory,
            'machine_telemetry': telemetry_data,
            'process_flow': process_flow,
            'maintenance': maintenance_data,
            'quality_inspection': quality_inspection,
            'kpis': kpis_data,
            'material_inventory': material_inventory,
            'packaging_shipment': packaging_shipment,
            'andon_alerts': alerts_data
        })
        
        print("\n✅ All data generated successfully!")
        return {
            'orders_batch': orders_data,
            'machine_inventory': machine_inventory,
            'machine_telemetry': telemetry_data,
            'process_flow': process_flow,
            'maintenance': maintenance_data,
            'quality_inspection': quality_inspection,
            'kpis': kpis_data,
            'material_inventory': material_inventory,
            'packaging_shipment': packaging_shipment,
            'andon_alerts': alerts_data
        }
    
    def generate_orders_batch_data(self, start_date, days):
        """Generate Orders/Batch Table as per project plan schema"""
        print("Generating Orders/Batch data...")
        
        orders_data = []
        order_counter = 1
        batch_counter = 1
        
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            
            # Generate 5-15 orders per day
            num_orders = random.randint(5, 15)
            
            for order in range(num_orders):
                order_id = f"ORD_{order_counter:04d}"
                batch_id = f"BATCH_{batch_counter:04d}"
                
                # Product types as per project plan
                product_types = [
                    "SheetMetalBox_A", "SheetMetalBox_B", "InjectionMoldPart_A", 
                    "InjectionMoldPart_B", "AssemblyComponent_A"
                ]
                
                # Material types as per project plan
                material_types = [
                    "Stainless Steel 304", "Aluminum 6061", "Carbon Steel", 
                    "Plastic ABS", "Plastic PP"
                ]
                
                order_date = current_date + timedelta(hours=random.randint(8, 16))
                planned_start = order_date + timedelta(hours=random.randint(1, 4))
                planned_end = planned_start + timedelta(hours=random.randint(4, 12))
                
                order_data = {
                    'order_id': order_id,
                    'product_type': random.choice(product_types),
                    'batch_id': batch_id,
                    'batch_size': random.randint(50, 500),
                    'material_type': random.choice(material_types),
                    'material_thickness': round(random.uniform(1.0, 5.0), 2),
                    'order_date': order_date,
                    'planned_start': planned_start,
                    'planned_end': planned_end,
                    'assigned_engineer': f"Engineer_{random.randint(1, 10)}",
                    'status': random.choice(['planned', 'in-progress', 'completed'])
                }
                
                orders_data.append(order_data)
                order_counter += 1
                batch_counter += 1
        
        return pd.DataFrame(orders_data)
    
    def generate_machine_inventory(self):
        """Generate Machine Inventory Table as per project plan schema"""
        print("Generating Machine Inventory data...")
        
        machine_inventory = []
        
        # Machine types as per project plan
        machine_types = [
            "CNC Punch", "Laser Cutter", "Bender", "Welder", 
            "Polisher", "Injection Moulding"
        ]
        
        manufacturers = ["Trumpf", "Amada", "Mazak", "Bosch", "Fronius", "Arburg"]
        
        for machine_id, machine_config in self.machines.items():
            machine_data = {
                'machine_id': machine_id,
                'machine_type': machine_config.get('type', 'Unknown'),
                'manufacturer': machine_config.get('manufacturer', 'Unknown'),
                'model': machine_config.get('model', 'Unknown'),
                'max_capacity': random.randint(50, 200),
                'power_rating': random.uniform(5, 50),
                'location': machine_config.get('location', 'Unknown'),
                'installation_date': datetime(2022, 1, 1) + timedelta(days=random.randint(0, 1000)),
                'last_service_date': datetime.now() - timedelta(days=random.randint(1, 90)),
                'sensor_list': list(machine_config.get('sensors', {}).keys())
            }
            machine_inventory.append(machine_data)
        
        return pd.DataFrame(machine_inventory)
    
    def generate_machine_telemetry(self, start_date, days):
        """Generate Machine Telemetry Table as per project plan schema"""
        print("Generating Machine Telemetry data...")
        
        telemetry_data = []
        
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            
            # Generate data for each machine every 5 minutes
            for hour in range(24):
                for minute in range(0, 60, 5):  # Every 5 minutes
                    timestamp = current_date + timedelta(hours=hour, minutes=minute)
                    
                    for machine_id, machine_config in self.machines.items():
                        # Generate telemetry record
                        telemetry_record = self._generate_telemetry_record(
                            timestamp, machine_id, machine_config
                        )
                        telemetry_data.append(telemetry_record)
        
        return pd.DataFrame(telemetry_data)
    
    def _generate_telemetry_record(self, timestamp, machine_id, machine_config):
        """Generate a single telemetry record following project plan schema"""
        
        # Base fields as per project plan
        record = {
            'timestamp': timestamp,
            'machine_id': machine_id,
            'batch_id': f"BATCH_{random.randint(1000, 9999)}",
            'spindle_rpm': random.uniform(500, 3000) if 'rpm' in machine_config.get('sensors', {}) else None,
            'feed_rate': random.uniform(50, 500) if machine_id.startswith('CNC') else None,
            'cutting_force': random.uniform(200, 2000) if machine_id.startswith('CNC') else None,
            'vibration_x': random.uniform(0, 5),
            'vibration_y': random.uniform(0, 5),
            'vibration_z': random.uniform(0, 5),
            'motor_current': random.uniform(5, 25),
            'motor_voltage': random.uniform(380, 480),
            'temperature': random.uniform(30, 90),
            'hydraulic_pressure': random.uniform(50, 250) if 'hydraulic_pressure' in machine_config.get('sensors', {}) else None,
            'coolant_flow': random.uniform(0, 20),
            'tool_wear': random.uniform(0, 100),
            'cycle_time': random.uniform(10, 300),
            'status_flag': self._get_status_flag()
        }
        
        # Machine-specific sensors as per project plan
        if machine_id.startswith('CNC'):
            record.update({
                'spindle_rpm': random.uniform(500, 3000),
                'feed_rate': random.uniform(50, 500),
                'cutting_force': random.uniform(200, 2000)
            })
        elif machine_id.startswith('Laser'):
            record.update({
                'laser_power': random.uniform(1000, 5000),
                'cutting_speed': random.uniform(100, 1000),
                'head_temp': random.uniform(40, 80),
                'lens_status': random.choice(['Good', 'Worn', 'Dirty'])
            })
        elif machine_id.startswith('Press') or machine_id.startswith('Bend'):
            record.update({
                'hydraulic_pressure': random.uniform(50, 250),
                'angle': random.uniform(0, 180),
                'bend_force': random.uniform(100, 1000)
            })
        elif machine_id.startswith('Weld'):
            record.update({
                'current': random.uniform(50, 200),
                'voltage': random.uniform(15, 30),
                'arc_length': random.uniform(1, 5),
                'cooling_flow': random.uniform(5, 15)
            })
        elif machine_id.startswith('Polish'):
            record.update({
                'spindle_rpm': random.uniform(1000, 5000),
                'vibration': random.uniform(0, 5),
                'temperature': random.uniform(30, 60)
            })
        elif machine_id.startswith('Injection'):
            record.update({
                'barrel_temp': random.uniform(150, 300),
                'screw_rpm': random.uniform(50, 200),
                'injection_pressure': random.uniform(50, 250),
                'mold_temp': random.uniform(40, 80)
            })
        
        return record
    
    def _get_status_flag(self):
        """Get status flag as per project plan"""
        rand = random.random()
        if rand < 0.85:
            return 'Normal'
        elif rand < 0.95:
            return 'Anomaly'
        else:
            return 'Fault'
    
    def generate_process_flow_data(self, start_date, days):
        """Generate Process Flow/Material Tracking Table as per project plan schema"""
        print("Generating Process Flow data...")
        
        process_flow = []
        
        # Process steps as per project plan
        process_steps = [
            'Material Application', 'Blanking', 'Laser Cutting', 'CNC Punching',
            'Press Brake Bending', 'Fitter Riveting', 'Welding', 'Polishing',
            'Surface Treatment', 'Semi-finished Inspection', 'Silk Printing',
            'Final Assembly', 'Quality Inspection', 'Warehousing', 'Shipment'
        ]
        
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            
            # Generate flow for each batch
            for batch_num in range(random.randint(10, 20)):
                batch_id = f"BATCH_{random.randint(1000, 9999)}"
                
                for step_num, process_step in enumerate(process_steps):
                    start_time = current_date + timedelta(hours=8 + step_num * 0.5)
                    duration = random.uniform(5, 60)
                    end_time = start_time + timedelta(minutes=duration)
                    
                    flow_record = {
                        'batch_id': batch_id,
                        'process_step': process_step,
                        'machine_id': f"MACHINE_{step_num + 1:02d}",
                        'start_time': start_time,
                        'end_time': end_time,
                        'duration': duration,
                        'operator': f"Operator_{random.randint(1, 20)}",
                        'quality_flag': random.choice(['Pass', 'Fail', 'Scrap']),
                        'defect_type': random.choice(['None', 'Burr', 'Crack', 'Misalignment']) if random.random() < 0.1 else 'None',
                        'remarks': random.choice(['Normal', 'Tool change', 'Power surge', 'Material issue']) if random.random() < 0.05 else '',
                        'material_moved': random.choice([True, False])
                    }
                    
                    process_flow.append(flow_record)
        
        return pd.DataFrame(process_flow)
    
    def generate_maintenance_data(self, start_date, days):
        """Generate Maintenance Table as per project plan schema"""
        print("Generating Maintenance data...")
        
        maintenance_data = []
        failure_counter = 1
        
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            
            # Generate maintenance events (0-3 per day)
            num_events = random.randint(0, 3)
            
            for event in range(num_events):
                failure_id = f"F_{failure_counter:03d}"
                machine_id = random.choice(list(self.machines.keys()))
                
                start_time = current_date + timedelta(hours=random.randint(8, 20))
                downtime = random.uniform(5, 120)
                end_time = start_time + timedelta(minutes=downtime)
                
                maintenance_record = {
                    'machine_id': machine_id,
                    'failure_id': failure_id,
                    'failure_type': random.choice(['Wear', 'Breakdown', 'Sensor Fault', 'Electrical']),
                    'start_time': start_time,
                    'end_time': end_time,
                    'downtime': downtime,
                    'maintenance_type': random.choice(['Corrective', 'Preventive']),
                    'parts_replaced': random.choice(['Tool Bit', 'Hydraulic Hose', 'Sensor', 'Motor']) if random.random() < 0.7 else 'None',
                    'notes': random.choice(['Minor spindle misalignment', 'Routine maintenance', 'Emergency repair'])
                }
                
                maintenance_data.append(maintenance_record)
                failure_counter += 1
        
        return pd.DataFrame(maintenance_data)
    
    def generate_quality_inspection_data(self, start_date, days):
        """Generate Quality Inspection Table as per project plan schema"""
        print("Generating Quality Inspection data...")
        
        quality_data = []
        
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            
            # Generate inspection records
            num_inspections = random.randint(20, 50)
            
            for inspection in range(num_inspections):
                inspection_time = current_date + timedelta(hours=random.randint(8, 20))
                
                quality_record = {
                    'batch_id': f"BATCH_{random.randint(1000, 9999)}",
                    'inspection_step': random.choice(['Punching', 'Welding', 'Final Assembly', 'Quality Check']),
                    'inspector': f"Inspector_{random.randint(1, 10)}",
                    'dimension_ok': random.choice([True, False]),
                    'surface_ok': random.choice([True, False]),
                    'assembly_ok': random.choice([True, False]),
                    'defects_found': random.choice(['None', 'Burr', 'Scratch', 'Crack']) if random.random() < 0.1 else 'None',
                    'rework_required': random.choice([True, False]) if random.random() < 0.05 else False,
                    'inspection_time': inspection_time
                }
                
                quality_data.append(quality_record)
        
        return pd.DataFrame(quality_data)
    
    def generate_kpis_data(self, telemetry_data):
        """Generate KPIs/Performance Metrics Table as per project plan schema"""
        print("Generating KPIs data...")
        
        kpis_data = []
        
        for machine_id in telemetry_data['machine_id'].unique():
            machine_data = telemetry_data[telemetry_data['machine_id'] == machine_id]
            
            for batch_id in machine_data['batch_id'].unique():
                batch_data = machine_data[machine_data['batch_id'] == batch_id]
                
                kpi_record = {
                    'machine_id': machine_id,
                    'batch_id': batch_id,
                    'utilization': random.uniform(70, 100),
                    'availability': random.uniform(85, 100),
                    'OEE': random.uniform(65, 95),
                    'avg_cycle_time': random.uniform(10, 300),
                    'defect_rate': random.uniform(0, 5),
                    'maintenance_count': random.randint(0, 5),
                    'downtime': random.uniform(0, 120)
                }
                
                kpis_data.append(kpi_record)
        
        return pd.DataFrame(kpis_data)
    
    def generate_material_inventory_data(self, start_date, days):
        """Generate Material & Inventory Tracking Table as per project plan schema"""
        print("Generating Material Inventory data...")
        
        material_data = []
        
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            
            # Generate material usage records
            num_records = random.randint(5, 15)
            
            for record in range(num_records):
                material_record = {
                    'material_id': f"MAT_{random.randint(1, 10):03d}",
                    'material_type': random.choice(['Stainless Steel', 'Aluminum', 'Carbon Steel', 'Plastic ABS', 'Plastic PP']),
                    'thickness': round(random.uniform(1, 5), 2),
                    'batch_id': f"BATCH_{random.randint(1000, 9999)}",
                    'quantity_used': random.uniform(10, 500),
                    'inventory_before': random.uniform(800, 1200),
                    'inventory_after': random.uniform(300, 1000)
                }
                
                material_data.append(material_record)
        
        return pd.DataFrame(material_data)
    
    def generate_packaging_shipment_data(self, start_date, days):
        """Generate Packaging & Shipment Table as per project plan schema"""
        print("Generating Packaging & Shipment data...")
        
        packaging_data = []
        
        for day in range(days):
            current_date = start_date + timedelta(days=day)
            
            # Generate packaging records
            num_shipments = random.randint(5, 15)
            
            for shipment in range(num_shipments):
                shipping_date = current_date + timedelta(hours=random.randint(8, 20))
                
                packaging_record = {
                    'batch_id': f"BATCH_{random.randint(1000, 9999)}",
                    'packed_units': random.randint(50, 500),
                    'packaging_type': random.choice(['Box', 'Foam', 'Tray', 'Box + Foam']),
                    'shipper': random.choice(['FedEx', 'DHL', 'UPS', 'Local']),
                    'shipping_date': shipping_date,
                    'logistics_no': f"TRK_{random.randint(1000, 9999)}",
                    'shipment_status': random.choice(['In-transit', 'Delivered', 'Pending'])
                }
                
                packaging_data.append(packaging_record)
        
        return pd.DataFrame(packaging_data)
    
    def generate_alerts_data(self, telemetry_data):
        """Generate Andon Alerts data"""
        print("Generating Alerts data...")
        
        alerts_data = []
        alert_counter = 1
        
        for _, row in telemetry_data.iterrows():
            # Generate alerts based on sensor thresholds
            if row['status_flag'] in ['Anomaly', 'Fault']:
                alert_record = {
                    'alert_id': f"ALERT_{alert_counter:06d}",
                    'timestamp': row['timestamp'],
                    'machine_id': row['machine_id'],
                    'alert_type': self._get_alert_type(row),
                    'severity': self._get_alert_severity(row),
                    'description': self._get_alert_description(row),
                    'triggered_by': self._get_triggered_by(row),
                    'resolved': random.choice([True, False]),
                    'resolution_time': random.uniform(5, 120) if random.random() < 0.7 else None
                }
                
                alerts_data.append(alert_record)
                alert_counter += 1
        
        return pd.DataFrame(alerts_data)
    
    def _get_alert_type(self, row):
        """Get alert type based on sensor data"""
        if row['temperature'] > 80:
            return 'High Temperature'
        elif row['vibration_x'] > 4:
            return 'High Vibration'
        elif row['motor_current'] > 20:
            return 'High Current'
        else:
            return 'General Alert'
    
    def _get_alert_severity(self, row):
        """Get alert severity"""
        if row['status_flag'] == 'Fault':
            return 'Critical'
        elif row['status_flag'] == 'Anomaly':
            return 'High'
        else:
            return 'Medium'
    
    def _get_alert_description(self, row):
        """Get alert description"""
        return f"Alert detected on {row['machine_id']} - {row['status_flag']}"
    
    def _get_triggered_by(self, row):
        """Get what triggered the alert"""
        if row['temperature'] > 80:
            return 'Temperature Sensor'
        elif row['vibration_x'] > 4:
            return 'Vibration Sensor'
        else:
            return 'System Monitor'
    
    def save_all_data(self, data_dict):
        """Save all generated data to files"""
        print("Saving all data to files...")
        
        # Ensure data directory exists
        os.makedirs('data/raw', exist_ok=True)
        
        # Save each dataset
        for name, data in data_dict.items():
            filename = f"data/raw/{name}.csv"
            data.to_csv(filename, index=False)
            print(f"✅ Saved {name}: {len(data)} records to {filename}")
        
        # Save metadata
        metadata = {
            'generation_date': datetime.now().isoformat(),
            'data_summary': {name: len(data) for name, data in data_dict.items()},
            'schema_compliant': True,
            'project_plan_version': '1.0'
        }
        
        import json
        with open('artifacts/metadata/schema_compliant_metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print("✅ Metadata saved")

def main():
    """Main function for testing"""
    generator = SchemaCompliantDataGenerator()
    generator.generate_all_data(days=7)  # Generate 7 days of data for testing

if __name__ == "__main__":
    main()