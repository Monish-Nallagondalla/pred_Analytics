"""
Database Analysis Script for Apex Components Predictive Maintenance System
Identifies faults and issues in the database
"""

import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

class DatabaseAnalyzer:
    def __init__(self, db_path="apex_components.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
    
    def get_table_info(self):
        """Get information about all tables"""
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in self.cursor.fetchall()]
        
        table_info = {}
        for table in tables:
            self.cursor.execute(f"PRAGMA table_info({table})")
            columns = self.cursor.fetchall()
            self.cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = self.cursor.fetchone()[0]
            
            table_info[table] = {
                'columns': columns,
                'row_count': count
            }
        
        return table_info
    
    def check_data_quality(self):
        """Check data quality issues"""
        issues = []
        
        # Check telemetry data
        print("=== TELEMETRY DATA ANALYSIS ===")
        self.cursor.execute("SELECT COUNT(*) FROM telemetry")
        telemetry_count = self.cursor.fetchone()[0]
        print(f"Total telemetry records: {telemetry_count}")
        
        if telemetry_count > 0:
            # Check for null values in critical fields
            critical_fields = ['timestamp', 'machine_id', 'machine_type', 'state', 'quality_flag']
            for field in critical_fields:
                self.cursor.execute(f"SELECT COUNT(*) FROM telemetry WHERE {field} IS NULL")
                null_count = self.cursor.fetchone()[0]
                if null_count > 0:
                    issues.append(f"Telemetry: {null_count} null values in {field}")
                    print(f"ERROR: {null_count} null values in {field}")
                else:
                    print(f"OK: No null values in {field}")
            
            # Check for invalid states
            self.cursor.execute("SELECT DISTINCT state FROM telemetry")
            states = [row[0] for row in self.cursor.fetchall()]
            valid_states = ['idle', 'cutting', 'fault', 'maintenance', 'setup']
            invalid_states = [s for s in states if s not in valid_states]
            if invalid_states:
                issues.append(f"Telemetry: Invalid states found: {invalid_states}")
                print(f"ERROR: Invalid states: {invalid_states}")
            else:
                print(f"OK: All states are valid: {states}")
            
            # Check for invalid quality flags
            self.cursor.execute("SELECT DISTINCT quality_flag FROM telemetry")
            quality_flags = [row[0] for row in self.cursor.fetchall()]
            valid_flags = ['ok', 'scrap', 'rework']
            invalid_flags = [f for f in quality_flags if f not in valid_flags]
            if invalid_flags:
                issues.append(f"Telemetry: Invalid quality flags: {invalid_flags}")
                print(f"ERROR: Invalid quality flags: {invalid_flags}")
            else:
                print(f"OK: All quality flags are valid: {quality_flags}")
            
            # Check for negative values in numeric fields
            numeric_fields = ['spindle_rpm', 'motor_current', 'vibration_rms', 'servo_temp', 'power_draw']
            for field in numeric_fields:
                self.cursor.execute(f"SELECT COUNT(*) FROM telemetry WHERE {field} < 0")
                negative_count = self.cursor.fetchone()[0]
                if negative_count > 0:
                    issues.append(f"Telemetry: {negative_count} negative values in {field}")
                    print(f"ERROR: {negative_count} negative values in {field}")
                else:
                    print(f"OK: No negative values in {field}")
            
            # Check for unrealistic values
            self.cursor.execute("SELECT COUNT(*) FROM telemetry WHERE spindle_rpm > 10000")
            high_rpm_count = self.cursor.fetchone()[0]
            if high_rpm_count > 0:
                issues.append(f"Telemetry: {high_rpm_count} records with unrealistic spindle_rpm > 10000")
                print(f"ERROR: {high_rpm_count} records with unrealistic spindle_rpm > 10000")
            
            self.cursor.execute("SELECT COUNT(*) FROM telemetry WHERE servo_temp > 150")
            high_temp_count = self.cursor.fetchone()[0]
            if high_temp_count > 0:
                issues.append(f"Telemetry: {high_temp_count} records with unrealistic servo_temp > 150°C")
                print(f"ERROR: {high_temp_count} records with unrealistic servo_temp > 150°C")
        
        # Check events data
        print("\n=== EVENTS DATA ANALYSIS ===")
        self.cursor.execute("SELECT COUNT(*) FROM events")
        events_count = self.cursor.fetchone()[0]
        print(f"Total events records: {events_count}")
        
        if events_count > 0:
            # Check for null values in critical fields
            critical_fields = ['event_id', 'timestamp', 'machine_id', 'event_type', 'severity', 'description']
            for field in critical_fields:
                self.cursor.execute(f"SELECT COUNT(*) FROM events WHERE {field} IS NULL")
                null_count = self.cursor.fetchone()[0]
                if null_count > 0:
                    issues.append(f"Events: {null_count} null values in {field}")
                    print(f"ERROR: {null_count} null values in {field}")
                else:
                    print(f"OK: No null values in {field}")
            
            # Check for invalid severity levels
            self.cursor.execute("SELECT DISTINCT severity FROM events")
            severities = [row[0] for row in self.cursor.fetchall()]
            valid_severities = ['low', 'medium', 'high', 'critical']
            invalid_severities = [s for s in severities if s not in valid_severities]
            if invalid_severities:
                issues.append(f"Events: Invalid severity levels: {invalid_severities}")
                print(f"ERROR: Invalid severity levels: {invalid_severities}")
            else:
                print(f"OK: All severity levels are valid: {severities}")
            
            # Check for negative downtime
            self.cursor.execute("SELECT COUNT(*) FROM events WHERE downtime_minutes < 0")
            negative_downtime = self.cursor.fetchone()[0]
            if negative_downtime > 0:
                issues.append(f"Events: {negative_downtime} records with negative downtime")
                print(f"ERROR: {negative_downtime} records with negative downtime")
            else:
                print(f"OK: No negative downtime values")
        
        # Check maintenance data
        print("\n=== MAINTENANCE DATA ANALYSIS ===")
        self.cursor.execute("SELECT COUNT(*) FROM maintenance")
        maintenance_count = self.cursor.fetchone()[0]
        print(f"Total maintenance records: {maintenance_count}")
        
        if maintenance_count > 0:
            # Check for null values in critical fields
            critical_fields = ['maintenance_id', 'machine_id', 'start_time', 'end_time', 'maintenance_type', 'technician_id', 'cost']
            for field in critical_fields:
                self.cursor.execute(f"SELECT COUNT(*) FROM maintenance WHERE {field} IS NULL")
                null_count = self.cursor.fetchone()[0]
                if null_count > 0:
                    issues.append(f"Maintenance: {null_count} null values in {field}")
                    print(f"ERROR: {null_count} null values in {field}")
                else:
                    print(f"OK: No null values in {field}")
            
            # Check for negative costs
            self.cursor.execute("SELECT COUNT(*) FROM maintenance WHERE cost < 0")
            negative_cost = self.cursor.fetchone()[0]
            if negative_cost > 0:
                issues.append(f"Maintenance: {negative_cost} records with negative cost")
                print(f"ERROR: {negative_cost} records with negative cost")
            else:
                print(f"OK: No negative cost values")
            
            # Check for invalid time sequences
            self.cursor.execute("SELECT COUNT(*) FROM maintenance WHERE start_time > end_time")
            invalid_times = self.cursor.fetchone()[0]
            if invalid_times > 0:
                issues.append(f"Maintenance: {invalid_times} records with start_time > end_time")
                print(f"ERROR: {invalid_times} records with start_time > end_time")
            else:
                print(f"OK: All time sequences are valid")
        
        return issues
    
    def check_referential_integrity(self):
        """Check referential integrity between tables"""
        issues = []
        print("\n=== REFERENTIAL INTEGRITY CHECK ===")
        
        # Check if machine_ids in events exist in telemetry
        self.cursor.execute("""
            SELECT DISTINCT e.machine_id 
            FROM events e 
            LEFT JOIN telemetry t ON e.machine_id = t.machine_id 
            WHERE t.machine_id IS NULL
        """)
        orphaned_events = self.cursor.fetchall()
        if orphaned_events:
            issues.append(f"Events: {len(orphaned_events)} events reference non-existent machines")
            print(f"ERROR: {len(orphaned_events)} events reference non-existent machines: {[row[0] for row in orphaned_events]}")
        else:
            print("OK: All events reference existing machines")
        
        # Check if machine_ids in maintenance exist in telemetry
        self.cursor.execute("""
            SELECT DISTINCT m.machine_id 
            FROM maintenance m 
            LEFT JOIN telemetry t ON m.machine_id = t.machine_id 
            WHERE t.machine_id IS NULL
        """)
        orphaned_maintenance = self.cursor.fetchall()
        if orphaned_maintenance:
            issues.append(f"Maintenance: {len(orphaned_maintenance)} maintenance records reference non-existent machines")
            print(f"ERROR: {len(orphaned_maintenance)} maintenance records reference non-existent machines: {[row[0] for row in orphaned_maintenance]}")
        else:
            print("OK: All maintenance records reference existing machines")
        
        return issues
    
    def check_duplicates(self):
        """Check for duplicate records"""
        issues = []
        print("\n=== DUPLICATE RECORDS CHECK ===")
        
        # Check for duplicate telemetry records
        self.cursor.execute("""
            SELECT timestamp, machine_id, COUNT(*) as count 
            FROM telemetry 
            GROUP BY timestamp, machine_id 
            HAVING COUNT(*) > 1
        """)
        duplicate_telemetry = self.cursor.fetchall()
        if duplicate_telemetry:
            issues.append(f"Telemetry: {len(duplicate_telemetry)} duplicate records found")
            print(f"ERROR: {len(duplicate_telemetry)} duplicate telemetry records")
        else:
            print("OK: No duplicate telemetry records")
        
        # Check for duplicate event_ids
        self.cursor.execute("""
            SELECT event_id, COUNT(*) as count 
            FROM events 
            GROUP BY event_id 
            HAVING COUNT(*) > 1
        """)
        duplicate_events = self.cursor.fetchall()
        if duplicate_events:
            issues.append(f"Events: {len(duplicate_events)} duplicate event_ids found")
            print(f"ERROR: {len(duplicate_events)} duplicate event_ids")
        else:
            print("OK: No duplicate event_ids")
        
        # Check for duplicate maintenance_ids
        self.cursor.execute("""
            SELECT maintenance_id, COUNT(*) as count 
            FROM maintenance 
            GROUP BY maintenance_id 
            HAVING COUNT(*) > 1
        """)
        duplicate_maintenance = self.cursor.fetchall()
        if duplicate_maintenance:
            issues.append(f"Maintenance: {len(duplicate_maintenance)} duplicate maintenance_ids found")
            print(f"ERROR: {len(duplicate_maintenance)} duplicate maintenance_ids")
        else:
            print("OK: No duplicate maintenance_ids")
        
        return issues
    
    def check_data_consistency(self):
        """Check data consistency across tables"""
        issues = []
        print("\n=== DATA CONSISTENCY CHECK ===")
        
        # Check if machine types are consistent
        self.cursor.execute("""
            SELECT t1.machine_id, t1.machine_type, t2.machine_type
            FROM telemetry t1
            JOIN telemetry t2 ON t1.machine_id = t2.machine_id
            WHERE t1.machine_type != t2.machine_type
            LIMIT 5
        """)
        inconsistent_types = self.cursor.fetchall()
        if inconsistent_types:
            issues.append(f"Telemetry: Machine types inconsistent for some machines")
            print(f"ERROR: Machine types inconsistent for some machines")
        else:
            print("OK: Machine types are consistent")
        
        # Check for orphaned records
        self.cursor.execute("SELECT COUNT(*) FROM telemetry WHERE machine_id NOT IN (SELECT DISTINCT machine_id FROM telemetry WHERE machine_id IS NOT NULL)")
        orphaned_telemetry = self.cursor.fetchone()[0]
        if orphaned_telemetry > 0:
            issues.append(f"Telemetry: {orphaned_telemetry} orphaned records")
            print(f"ERROR: {orphaned_telemetry} orphaned telemetry records")
        else:
            print("OK: No orphaned telemetry records")
        
        return issues
    
    def generate_fix_recommendations(self, all_issues):
        """Generate recommendations to fix identified issues"""
        recommendations = []
        
        if not all_issues:
            recommendations.append("OK: No critical issues found in the database!")
            return recommendations
        
        recommendations.append("RECOMMENDED FIXES:")
        recommendations.append("")
        
        for issue in all_issues:
            if "null values" in issue:
                table = issue.split(":")[0]
                field = issue.split("null values in ")[1]
                recommendations.append(f"1. Fix null values in {table}.{field}:")
                recommendations.append(f"   - Update records with NULL {field} to appropriate default values")
                recommendations.append(f"   - Add NOT NULL constraint to prevent future null values")
                recommendations.append("")
            
            elif "Invalid states" in issue:
                recommendations.append("2. Fix invalid states in telemetry:")
                recommendations.append("   - Update invalid states to valid ones (idle, cutting, fault, maintenance, setup)")
                recommendations.append("   - Add CHECK constraint to enforce valid states")
                recommendations.append("")
            
            elif "Invalid quality flags" in issue:
                recommendations.append("3. Fix invalid quality flags in telemetry:")
                recommendations.append("   - Update invalid flags to valid ones (ok, scrap, rework)")
                recommendations.append("   - Add CHECK constraint to enforce valid quality flags")
                recommendations.append("")
            
            elif "negative values" in issue:
                field = issue.split("negative values in ")[1]
                recommendations.append(f"4. Fix negative values in {field}:")
                recommendations.append(f"   - Update negative values to 0 or appropriate positive values")
                recommendations.append(f"   - Add CHECK constraint to prevent negative values")
                recommendations.append("")
            
            elif "unrealistic" in issue:
                recommendations.append("5. Fix unrealistic values:")
                recommendations.append("   - Review and correct unrealistic sensor readings")
                recommendations.append("   - Add validation rules for sensor data ranges")
                recommendations.append("")
            
            elif "duplicate" in issue:
                recommendations.append("6. Fix duplicate records:")
                recommendations.append("   - Remove duplicate records keeping the most recent ones")
                recommendations.append("   - Add UNIQUE constraints to prevent future duplicates")
                recommendations.append("")
            
            elif "orphaned" in issue:
                recommendations.append("7. Fix orphaned records:")
                recommendations.append("   - Delete orphaned records or update references to valid machines")
                recommendations.append("   - Add foreign key constraints to prevent future orphaned records")
                recommendations.append("")
        
        recommendations.append("IMPLEMENTATION STEPS:")
        recommendations.append("1. Backup the database before making changes")
        recommendations.append("2. Create a script to fix data issues")
        recommendations.append("3. Test fixes on a copy of the database")
        recommendations.append("4. Apply fixes to production database")
        recommendations.append("5. Add constraints to prevent future issues")
        
        return recommendations
    
    def run_full_analysis(self):
        """Run complete database analysis"""
        print("DATABASE ANALYSIS REPORT")
        print("=" * 50)
        
        # Get table information
        table_info = self.get_table_info()
        print(f"\nDATABASE OVERVIEW:")
        for table, info in table_info.items():
            print(f"   {table}: {info['row_count']} records")
        
        # Check data quality
        quality_issues = self.check_data_quality()
        
        # Check referential integrity
        integrity_issues = self.check_referential_integrity()
        
        # Check for duplicates
        duplicate_issues = self.check_duplicates()
        
        # Check data consistency
        consistency_issues = self.check_data_consistency()
        
        # Combine all issues
        all_issues = quality_issues + integrity_issues + duplicate_issues + consistency_issues
        
        # Generate recommendations
        recommendations = self.generate_fix_recommendations(all_issues)
        
        print("\n" + "=" * 50)
        print("SUMMARY")
        print("=" * 50)
        
        if all_issues:
            print(f"Found {len(all_issues)} issues:")
            for i, issue in enumerate(all_issues, 1):
                print(f"   {i}. {issue}")
        else:
            print("No issues found in the database!")
        
        print("\n" + "=" * 50)
        for rec in recommendations:
            print(rec)
        
        self.conn.close()
        return all_issues, recommendations

if __name__ == "__main__":
    analyzer = DatabaseAnalyzer()
    issues, recommendations = analyzer.run_full_analysis()
