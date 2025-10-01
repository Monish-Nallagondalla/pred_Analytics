"""
Database management for Apex Components Predictive Maintenance System
Handles SQLite database operations for telemetry, events, and maintenance data
"""

import sqlite3
import pandas as pd
from datetime import datetime
import json
from config import DATABASE_PATH

class DatabaseManager:
    def __init__(self, db_path=DATABASE_PATH):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with required tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Telemetry table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS telemetry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                machine_id TEXT NOT NULL,
                machine_type TEXT NOT NULL,
                shift INTEGER NOT NULL,
                state TEXT NOT NULL,
                cycle_id TEXT,
                part_id TEXT,
                quality_flag TEXT NOT NULL,
                andon_trigger INTEGER NOT NULL,
                spindle_rpm REAL,
                motor_current REAL,
                vibration_rms REAL,
                axis_x REAL,
                axis_y REAL,
                axis_z REAL,
                servo_temp REAL,
                power_draw REAL,
                spindle_torque REAL,
                chuck_status TEXT,
                turret_index INTEGER,
                oil_temp REAL,
                joint_pos_1 REAL,
                joint_pos_2 REAL,
                joint_pos_3 REAL,
                joint_pos_4 REAL,
                joint_pos_5 REAL,
                joint_pos_6 REAL,
                joint_current_1 REAL,
                joint_current_2 REAL,
                joint_current_3 REAL,
                joint_current_4 REAL,
                joint_current_5 REAL,
                joint_current_6 REAL,
                tcp_force REAL,
                controller_temp REAL,
                suction_pressure REAL,
                discharge_pressure REAL,
                runtime_hours REAL,
                duty_cycle REAL,
                condensate_level REAL,
                laser_power REAL,
                head_temp REAL,
                exhaust_flow REAL,
                focal_height REAL,
                position_x REAL,
                position_y REAL,
                interlocks TEXT,
                ram_position REAL,
                hydraulic_pressure REAL,
                load_cell REAL,
                cycle_time REAL,
                crowning_actuator REAL,
                back_gauge REAL,
                drill_feed REAL,
                chuck_state TEXT,
                stroke_count INTEGER,
                wheel_rpm REAL,
                spindle_current REAL,
                coolant_temp REAL,
                coolant_flow REAL,
                table_feed REAL
            )
        ''')
        
        # Events table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                event_id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                machine_id TEXT NOT NULL,
                event_type TEXT NOT NULL,
                fault_code TEXT,
                severity TEXT NOT NULL,
                description TEXT NOT NULL,
                resolved_timestamp TEXT,
                resolution_action TEXT,
                downtime_minutes INTEGER DEFAULT 0
            )
        ''')
        
        # Maintenance table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS maintenance (
                maintenance_id TEXT PRIMARY KEY,
                machine_id TEXT NOT NULL,
                start_time TEXT NOT NULL,
                end_time TEXT NOT NULL,
                maintenance_type TEXT NOT NULL,
                parts_replaced TEXT,
                technician_id TEXT NOT NULL,
                cost REAL NOT NULL,
                notes TEXT
            )
        ''')
        
        # Production flow table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS production_flow (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                workstation_id TEXT NOT NULL,
                queue_length INTEGER NOT NULL,
                throughput_per_hour REAL NOT NULL,
                avg_cycle_time REAL NOT NULL,
                downtime_minutes REAL NOT NULL,
                operator_on_station INTEGER NOT NULL
            )
        ''')
        
        # Spares and MTTR table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS spares_mttr (
                machine_id TEXT NOT NULL,
                component TEXT NOT NULL,
                part_number TEXT NOT NULL,
                lead_time_days INTEGER NOT NULL,
                mean_time_to_replace_minutes INTEGER NOT NULL,
                cost REAL NOT NULL,
                PRIMARY KEY (machine_id, component)
            )
        ''')
        
        # KPIs table for caching
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS kpis (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT NOT NULL,
                machine_id TEXT NOT NULL,
                oee REAL NOT NULL,
                availability REAL NOT NULL,
                performance REAL NOT NULL,
                quality REAL NOT NULL,
                mtbf_hours REAL,
                mttr_hours REAL,
                next_failure_probability REAL,
                rul_hours REAL
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def insert_telemetry(self, data):
        """Insert telemetry data into database"""
        conn = sqlite3.connect(self.db_path)
        
        # Convert DataFrame to list of tuples
        data_list = data.to_dict('records')
        
        # Prepare insert statement
        columns = list(data.columns)
        placeholders = ', '.join(['?' for _ in columns])
        query = f"INSERT INTO telemetry ({', '.join(columns)}) VALUES ({placeholders})"
        
        # Insert data
        cursor = conn.cursor()
        for record in data_list:
            values = []
            for col in columns:
                value = record.get(col, None)
                # Convert numpy types to Python native types
                if value is not None:
                    if hasattr(value, 'item'):  # numpy scalar
                        value = value.item()
                    elif hasattr(value, 'isoformat'):  # datetime object
                        value = value.isoformat()
                    elif isinstance(value, (list, dict)):  # complex types
                        value = str(value)
                values.append(value)
            cursor.execute(query, values)
        
        conn.commit()
        conn.close()
    
    def insert_events(self, data):
        """Insert events data into database"""
        conn = sqlite3.connect(self.db_path)
        
        data_list = data.to_dict('records')
        
        columns = list(data.columns)
        placeholders = ', '.join(['?' for _ in columns])
        query = f"INSERT INTO events ({', '.join(columns)}) VALUES ({placeholders})"
        
        cursor = conn.cursor()
        for record in data_list:
            values = []
            for col in columns:
                value = record.get(col, None)
                # Convert numpy types to Python native types
                if value is not None:
                    if hasattr(value, 'item'):  # numpy scalar
                        value = value.item()
                    elif hasattr(value, 'isoformat'):  # datetime object
                        value = value.isoformat()
                    elif isinstance(value, (list, dict)):  # complex types
                        value = str(value)
                values.append(value)
            cursor.execute(query, values)
        
        conn.commit()
        conn.close()
    
    def insert_maintenance(self, data):
        """Insert maintenance data into database"""
        conn = sqlite3.connect(self.db_path)
        
        data_list = data.to_dict('records')
        
        columns = list(data.columns)
        placeholders = ', '.join(['?' for _ in columns])
        query = f"INSERT INTO maintenance ({', '.join(columns)}) VALUES ({placeholders})"
        
        cursor = conn.cursor()
        for record in data_list:
            values = []
            for col in columns:
                value = record.get(col, None)
                # Convert numpy types to Python native types
                if value is not None:
                    if hasattr(value, 'item'):  # numpy scalar
                        value = value.item()
                    elif hasattr(value, 'isoformat'):  # datetime object
                        value = value.isoformat()
                    elif isinstance(value, (list, dict)):  # complex types
                        value = str(value)
                values.append(value)
            cursor.execute(query, values)
        
        conn.commit()
        conn.close()
    
    def get_telemetry_data(self, machine_id=None, start_date=None, end_date=None, limit=None):
        """Retrieve telemetry data with optional filters"""
        conn = sqlite3.connect(self.db_path)
        
        query = "SELECT * FROM telemetry WHERE 1=1"
        params = []
        
        if machine_id:
            query += " AND machine_id = ?"
            params.append(machine_id)
        
        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date)
        
        query += " ORDER BY timestamp DESC"
        
        if limit:
            query += " LIMIT ?"
            params.append(limit)
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        
        return df
    
    def get_events_data(self, machine_id=None, start_date=None, end_date=None, limit=None):
        """Retrieve events data with optional filters"""
        conn = sqlite3.connect(self.db_path)
        
        query = "SELECT * FROM events WHERE 1=1"
        params = []
        
        if machine_id:
            query += " AND machine_id = ?"
            params.append(machine_id)
        
        if start_date:
            query += " AND timestamp >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND timestamp <= ?"
            params.append(end_date)
        
        query += " ORDER BY timestamp DESC"
        
        if limit:
            query += " LIMIT ?"
            params.append(limit)
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        
        return df
    
    def get_maintenance_data(self, machine_id=None, start_date=None, end_date=None, limit=None):
        """Retrieve maintenance data with optional filters"""
        conn = sqlite3.connect(self.db_path)
        
        query = "SELECT * FROM maintenance WHERE 1=1"
        params = []
        
        if machine_id:
            query += " AND machine_id = ?"
            params.append(machine_id)
        
        if start_date:
            query += " AND start_time >= ?"
            params.append(start_date)
        
        if end_date:
            query += " AND start_time <= ?"
            params.append(end_date)
        
        query += " ORDER BY start_time DESC"
        
        if limit:
            query += " LIMIT ?"
            params.append(limit)
        
        df = pd.read_sql_query(query, conn, params=params)
        conn.close()
        
        return df
    
    def get_machine_status(self):
        """Get current status of all machines"""
        conn = sqlite3.connect(self.db_path)
        
        # First try to get data from the last hour (for real-time data)
        query = '''
            SELECT 
                machine_id,
                machine_type,
                state,
                MAX(timestamp) as last_update,
                COUNT(*) as record_count
            FROM telemetry 
            WHERE timestamp >= datetime('now', '-1 hour')
            GROUP BY machine_id, machine_type, state
            ORDER BY machine_id
        '''
        
        df = pd.read_sql_query(query, conn)
        
        # If no recent data, get the latest data available (for sample data)
        if df.empty:
            query = '''
                SELECT 
                    machine_id,
                    machine_type,
                    state,
                    MAX(timestamp) as last_update,
                    COUNT(*) as record_count
                FROM telemetry 
                GROUP BY machine_id, machine_type, state
                ORDER BY machine_id
            '''
            df = pd.read_sql_query(query, conn)
        
        conn.close()
        
        return df
    
    def get_oee_data(self, machine_id=None, days=7):
        """Calculate OEE (Overall Equipment Effectiveness) data"""
        conn = sqlite3.connect(self.db_path)
        
        # Try to get data for the last N days
        query = '''
            SELECT 
                machine_id,
                machine_type,
                state,
                COUNT(*) as state_count,
                SUM(CASE WHEN quality_flag = 'ok' THEN 1 ELSE 0 END) as good_parts,
                SUM(CASE WHEN quality_flag = 'scrap' THEN 1 ELSE 0 END) as scrap_parts,
                SUM(CASE WHEN quality_flag = 'rework' THEN 1 ELSE 0 END) as rework_parts
            FROM telemetry 
            WHERE timestamp >= date('now', '-{} days')
        '''.format(days)
        
        if machine_id:
            query += " AND machine_id = ?"
            params = [machine_id]
        else:
            params = []
        
        query += " GROUP BY machine_id, machine_type, state"
        
        df = pd.read_sql_query(query, conn, params=params)
        
        # If no recent data, get all available data (for sample data)
        if df.empty:
            query = '''
                SELECT 
                    machine_id,
                    machine_type,
                    state,
                    COUNT(*) as state_count,
                    SUM(CASE WHEN quality_flag = 'ok' THEN 1 ELSE 0 END) as good_parts,
                    SUM(CASE WHEN quality_flag = 'scrap' THEN 1 ELSE 0 END) as scrap_parts,
                    SUM(CASE WHEN quality_flag = 'rework' THEN 1 ELSE 0 END) as rework_parts
                FROM telemetry 
            '''
            
            if machine_id:
                query += " WHERE machine_id = ?"
                params = [machine_id]
            else:
                params = []
            
            query += " GROUP BY machine_id, machine_type, state"
            df = pd.read_sql_query(query, conn, params=params)
        
        conn.close()
        
        return df
    
    def get_downtime_data(self, machine_id=None, days=7):
        """Get downtime analysis data"""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT 
                machine_id,
                event_type,
                severity,
                COUNT(*) as event_count,
                SUM(downtime_minutes) as total_downtime
            FROM events 
            WHERE timestamp >= date('now', '-{} days')
        '''.format(days)
        
        if machine_id:
            query += " AND machine_id = ?"
            params = [machine_id]
        else:
            params = []
        
        query += " GROUP BY machine_id, event_type, severity ORDER BY total_downtime DESC"
        
        df = pd.read_sql_query(query, conn, params=params)
        
        # If no recent data, get all available data (for sample data)
        if df.empty:
            query = '''
                SELECT 
                    machine_id,
                    event_type,
                    severity,
                    COUNT(*) as event_count,
                    SUM(downtime_minutes) as total_downtime
                FROM events 
            '''
            
            if machine_id:
                query += " WHERE machine_id = ?"
                params = [machine_id]
            else:
                params = []
            
            query += " GROUP BY machine_id, event_type, severity ORDER BY total_downtime DESC"
            df = pd.read_sql_query(query, conn, params=params)
        
        conn.close()
        
        return df
    
    def get_bottleneck_analysis(self, days=7):
        """Analyze production bottlenecks"""
        conn = sqlite3.connect(self.db_path)
        
        query = '''
            SELECT 
                machine_id,
                machine_type,
                AVG(CASE WHEN state = 'idle' THEN 1 ELSE 0 END) as idle_ratio,
                AVG(CASE WHEN state = 'cutting' THEN 1 ELSE 0 END) as cutting_ratio,
                AVG(CASE WHEN state = 'fault' THEN 1 ELSE 0 END) as fault_ratio,
                COUNT(DISTINCT cycle_id) as total_cycles,
                AVG(CASE WHEN quality_flag = 'ok' THEN 1 ELSE 0 END) as quality_ratio
            FROM telemetry 
            WHERE timestamp >= date('now', '-{} days')
            GROUP BY machine_id, machine_type
            ORDER BY idle_ratio DESC
        '''.format(days)
        
        df = pd.read_sql_query(query, conn)
        
        # If no recent data, get all available data (for sample data)
        if df.empty:
            query = '''
                SELECT 
                    machine_id,
                    machine_type,
                    AVG(CASE WHEN state = 'idle' THEN 1 ELSE 0 END) as idle_ratio,
                    AVG(CASE WHEN state = 'cutting' THEN 1 ELSE 0 END) as cutting_ratio,
                    AVG(CASE WHEN state = 'fault' THEN 1 ELSE 0 END) as fault_ratio,
                    COUNT(DISTINCT cycle_id) as total_cycles,
                    AVG(CASE WHEN quality_flag = 'ok' THEN 1 ELSE 0 END) as quality_ratio
                FROM telemetry 
                GROUP BY machine_id, machine_type
                ORDER BY idle_ratio DESC
            '''
            df = pd.read_sql_query(query, conn)
        
        conn.close()
        
        return df
    
    def get_predictive_insights(self, machine_id=None):
        """Get predictive maintenance insights"""
        conn = sqlite3.connect(self.db_path)
        
        # Get recent vibration and temperature trends
        query = '''
            SELECT 
                machine_id,
                timestamp,
                vibration_rms,
                servo_temp,
                motor_current,
                state,
                quality_flag
            FROM telemetry 
            WHERE timestamp >= datetime('now', '-24 hours')
        '''
        
        if machine_id:
            query += " AND machine_id = ?"
            params = [machine_id]
        else:
            params = []
        
        query += " ORDER BY timestamp DESC"
        
        df = pd.read_sql_query(query, conn, params=params)
        
        # If no recent data, get the latest data available (for sample data)
        if df.empty:
            query = '''
                SELECT 
                    machine_id,
                    timestamp,
                    vibration_rms,
                    servo_temp,
                    motor_current,
                    state,
                    quality_flag
                FROM telemetry 
            '''
            
            if machine_id:
                query += " WHERE machine_id = ?"
                params = [machine_id]
            else:
                params = []
            
            query += " ORDER BY timestamp DESC LIMIT 1000"
            df = pd.read_sql_query(query, conn, params=params)
        
        conn.close()
        
        return df
    
    def clear_old_data(self, days_to_keep=30):
        """Clear old data to manage database size"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cutoff_date = datetime.now().strftime('%Y-%m-%d')
        
        # Clear old telemetry data
        cursor.execute("DELETE FROM telemetry WHERE timestamp < ?", (cutoff_date,))
        
        # Clear old events data
        cursor.execute("DELETE FROM events WHERE timestamp < ?", (cutoff_date,))
        
        # Clear old maintenance data
        cursor.execute("DELETE FROM maintenance WHERE start_time < ?", (cutoff_date,))
        
        conn.commit()
        conn.close()
    
    def get_database_stats(self):
        """Get database statistics"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        stats = {}
        
        # Count records in each table
        tables = ['telemetry', 'events', 'maintenance', 'production_flow', 'spares_mttr', 'kpis']
        for table in tables:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            stats[f"{table}_count"] = cursor.fetchone()[0]
        
        # Get date range
        cursor.execute("SELECT MIN(timestamp), MAX(timestamp) FROM telemetry")
        date_range = cursor.fetchone()
        stats['date_range'] = date_range
        
        conn.close()
        
        return stats

if __name__ == "__main__":
    # Test database operations
    db = DatabaseManager()
    
    print("Database initialized successfully")
    print("Database statistics:")
    stats = db.get_database_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
