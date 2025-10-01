"""
Database Fix Script for Apex Components Predictive Maintenance System
Fixes identified database issues
"""

import sqlite3
import pandas as pd
from datetime import datetime
import shutil
import os

class DatabaseFixer:
    def __init__(self, db_path="apex_components.db"):
        self.db_path = db_path
        self.backup_path = f"{db_path}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    def create_backup(self):
        """Create backup of the database before making changes"""
        try:
            shutil.copy2(self.db_path, self.backup_path)
            print(f"✅ Database backup created: {self.backup_path}")
            return True
        except Exception as e:
            print(f"❌ Error creating backup: {e}")
            return False
    
    def fix_invalid_states(self):
        """Fix invalid states in telemetry table"""
        print("\n🔧 Fixing invalid states in telemetry...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check current invalid states
        cursor.execute("SELECT DISTINCT state FROM telemetry WHERE state NOT IN ('idle', 'cutting', 'fault', 'maintenance', 'setup')")
        invalid_states = [row[0] for row in cursor.fetchall()]
        
        if invalid_states:
            print(f"Found invalid states: {invalid_states}")
            
            # Fix 'toolchange' state - map to 'maintenance' as it's a maintenance activity
            cursor.execute("UPDATE telemetry SET state = 'maintenance' WHERE state = 'toolchange'")
            updated_count = cursor.rowcount
            print(f"✅ Updated {updated_count} records from 'toolchange' to 'maintenance'")
            
            # Add CHECK constraint to prevent future invalid states
            try:
                cursor.execute("""
                    ALTER TABLE telemetry ADD CONSTRAINT check_valid_state 
                    CHECK (state IN ('idle', 'cutting', 'fault', 'maintenance', 'setup'))
                """)
                print("✅ Added CHECK constraint for valid states")
            except sqlite3.OperationalError as e:
                if "duplicate constraint name" in str(e):
                    print("✅ CHECK constraint already exists")
                else:
                    print(f"⚠️ Could not add CHECK constraint: {e}")
        else:
            print("✅ No invalid states found")
        
        conn.commit()
        conn.close()
    
    def fix_maintenance_time_issues(self):
        """Fix maintenance records with start_time > end_time"""
        print("\n🔧 Fixing maintenance time issues...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Find records with start_time > end_time
        cursor.execute("""
            SELECT maintenance_id, machine_id, start_time, end_time 
            FROM maintenance 
            WHERE start_time > end_time
        """)
        invalid_records = cursor.fetchall()
        
        if invalid_records:
            print(f"Found {len(invalid_records)} records with start_time > end_time:")
            for record in invalid_records:
                print(f"  - {record[0]} ({record[1]}): {record[2]} > {record[3]}")
            
            # Fix by swapping start_time and end_time
            cursor.execute("""
                UPDATE maintenance 
                SET start_time = end_time, end_time = start_time 
                WHERE start_time > end_time
            """)
            updated_count = cursor.rowcount
            print(f"✅ Fixed {updated_count} maintenance records by swapping start/end times")
        else:
            print("✅ No maintenance time issues found")
        
        conn.commit()
        conn.close()
    
    def add_data_validation_constraints(self):
        """Add constraints to prevent future data quality issues"""
        print("\n🔧 Adding data validation constraints...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        constraints_added = []
        
        # Add constraints for telemetry table
        try:
            # Quality flag constraint
            cursor.execute("""
                ALTER TABLE telemetry ADD CONSTRAINT check_quality_flag 
                CHECK (quality_flag IN ('ok', 'scrap', 'rework'))
            """)
            constraints_added.append("quality_flag constraint")
        except sqlite3.OperationalError as e:
            if "duplicate constraint name" not in str(e):
                print(f"⚠️ Could not add quality_flag constraint: {e}")
        
        try:
            # Non-negative numeric values
            cursor.execute("""
                ALTER TABLE telemetry ADD CONSTRAINT check_non_negative_values 
                CHECK (spindle_rpm >= 0 AND motor_current >= 0 AND vibration_rms >= 0 
                       AND servo_temp >= 0 AND power_draw >= 0)
            """)
            constraints_added.append("non-negative values constraint")
        except sqlite3.OperationalError as e:
            if "duplicate constraint name" not in str(e):
                print(f"⚠️ Could not add non-negative values constraint: {e}")
        
        # Add constraints for events table
        try:
            cursor.execute("""
                ALTER TABLE events ADD CONSTRAINT check_severity 
                CHECK (severity IN ('low', 'medium', 'high', 'critical'))
            """)
            constraints_added.append("severity constraint")
        except sqlite3.OperationalError as e:
            if "duplicate constraint name" not in str(e):
                print(f"⚠️ Could not add severity constraint: {e}")
        
        try:
            cursor.execute("""
                ALTER TABLE events ADD CONSTRAINT check_non_negative_downtime 
                CHECK (downtime_minutes >= 0)
            """)
            constraints_added.append("non-negative downtime constraint")
        except sqlite3.OperationalError as e:
            if "duplicate constraint name" not in str(e):
                print(f"⚠️ Could not add downtime constraint: {e}")
        
        # Add constraints for maintenance table
        try:
            cursor.execute("""
                ALTER TABLE maintenance ADD CONSTRAINT check_non_negative_cost 
                CHECK (cost >= 0)
            """)
            constraints_added.append("non-negative cost constraint")
        except sqlite3.OperationalError as e:
            if "duplicate constraint name" not in str(e):
                print(f"⚠️ Could not add cost constraint: {e}")
        
        try:
            cursor.execute("""
                ALTER TABLE maintenance ADD CONSTRAINT check_valid_time_sequence 
                CHECK (start_time <= end_time)
            """)
            constraints_added.append("valid time sequence constraint")
        except sqlite3.OperationalError as e:
            if "duplicate constraint name" not in str(e):
                print(f"⚠️ Could not add time sequence constraint: {e}")
        
        if constraints_added:
            print(f"✅ Added constraints: {', '.join(constraints_added)}")
        else:
            print("✅ All constraints already exist")
        
        conn.commit()
        conn.close()
    
    def create_indexes_for_performance(self):
        """Create indexes to improve query performance"""
        print("\n🔧 Creating performance indexes...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        indexes = [
            ("idx_telemetry_timestamp", "telemetry", "timestamp"),
            ("idx_telemetry_machine_id", "telemetry", "machine_id"),
            ("idx_telemetry_state", "telemetry", "state"),
            ("idx_events_timestamp", "events", "timestamp"),
            ("idx_events_machine_id", "events", "machine_id"),
            ("idx_events_severity", "events", "severity"),
            ("idx_maintenance_machine_id", "maintenance", "machine_id"),
            ("idx_maintenance_start_time", "maintenance", "start_time")
        ]
        
        indexes_created = []
        for index_name, table, column in indexes:
            try:
                cursor.execute(f"CREATE INDEX IF NOT EXISTS {index_name} ON {table} ({column})")
                indexes_created.append(index_name)
            except sqlite3.OperationalError as e:
                print(f"⚠️ Could not create index {index_name}: {e}")
        
        if indexes_created:
            print(f"✅ Created indexes: {', '.join(indexes_created)}")
        else:
            print("✅ All indexes already exist")
        
        conn.commit()
        conn.close()
    
    def verify_fixes(self):
        """Verify that all fixes were applied correctly"""
        print("\n🔍 Verifying fixes...")
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Check for remaining invalid states
        cursor.execute("SELECT COUNT(*) FROM telemetry WHERE state NOT IN ('idle', 'cutting', 'fault', 'maintenance', 'setup')")
        invalid_states_count = cursor.fetchone()[0]
        
        # Check for remaining time issues
        cursor.execute("SELECT COUNT(*) FROM maintenance WHERE start_time > end_time")
        time_issues_count = cursor.fetchone()[0]
        
        # Check for negative values
        cursor.execute("SELECT COUNT(*) FROM telemetry WHERE spindle_rpm < 0 OR motor_current < 0 OR vibration_rms < 0")
        negative_values_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM events WHERE downtime_minutes < 0")
        negative_downtime_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM maintenance WHERE cost < 0")
        negative_cost_count = cursor.fetchone()[0]
        
        print(f"Invalid states remaining: {invalid_states_count}")
        print(f"Time sequence issues remaining: {time_issues_count}")
        print(f"Negative values in telemetry: {negative_values_count}")
        print(f"Negative downtime values: {negative_downtime_count}")
        print(f"Negative cost values: {negative_cost_count}")
        
        if all(count == 0 for count in [invalid_states_count, time_issues_count, negative_values_count, negative_downtime_count, negative_cost_count]):
            print("✅ All fixes verified successfully!")
            return True
        else:
            print("⚠️ Some issues may still remain")
            return False
        
        conn.close()
    
    def run_all_fixes(self):
        """Run all database fixes"""
        print("🔧 DATABASE FIX SCRIPT")
        print("=" * 50)
        
        # Create backup first
        if not self.create_backup():
            print("❌ Cannot proceed without backup. Exiting.")
            return False
        
        # Apply fixes
        self.fix_invalid_states()
        self.fix_maintenance_time_issues()
        self.add_data_validation_constraints()
        self.create_indexes_for_performance()
        
        # Verify fixes
        success = self.verify_fixes()
        
        print("\n" + "=" * 50)
        if success:
            print("✅ DATABASE FIXES COMPLETED SUCCESSFULLY!")
            print(f"📁 Backup created at: {self.backup_path}")
        else:
            print("⚠️ Some issues may require manual intervention")
        
        return success

if __name__ == "__main__":
    fixer = DatabaseFixer()
    success = fixer.run_all_fixes()
    
    if success:
        print("\n🎉 Database is now clean and optimized!")
    else:
        print("\n⚠️ Please review any remaining issues manually.")
