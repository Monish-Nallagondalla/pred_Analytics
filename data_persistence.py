"""
Data Persistence Utility for Apex Components Predictive Maintenance System
Manages data generation and persistence to avoid unnecessary regeneration
"""

import os
import json
from datetime import datetime, timedelta
from database import DatabaseManager
from data_generator import DataSimulator

class DataPersistenceManager:
    def __init__(self):
        self.db = DatabaseManager()
        self.data_simulator = DataSimulator()
        self.metadata_file = "data_metadata.json"
    
    def check_data_exists(self):
        """Check if sample data already exists"""
        try:
            stats = self.db.get_database_stats()
            return stats['telemetry_count'] > 0
        except:
            return False
    
    def get_data_metadata(self):
        """Get metadata about existing data"""
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r') as f:
                return json.load(f)
        return None
    
    def save_data_metadata(self, days, generated_at):
        """Save metadata about generated data"""
        metadata = {
            'days': days,
            'generated_at': generated_at.isoformat(),
            'data_type': 'sample_data'
        }
        with open(self.metadata_file, 'w') as f:
            json.dump(metadata, f)
    
    def generate_data_once(self, days=7):
        """Generate data only if it doesn't exist"""
        if self.check_data_exists():
            metadata = self.get_data_metadata()
            if metadata:
                print(f"✅ Sample data already exists ({metadata['days']} days, generated on {metadata['generated_at']})")
                return True
            else:
                print("✅ Sample data exists but no metadata found")
                return True
        
        print(f"📊 Generating {days} days of sample data...")
        
        # Generate data
        start_date = datetime.now() - timedelta(days=days)
        
        # Generate telemetry data
        telemetry_data = self.data_simulator.generate_data(start_date, days)
        
        # Generate events data
        events_data = self.data_simulator.generate_events(start_date, days)
        
        # Generate maintenance data
        maintenance_data = self.data_simulator.generate_maintenance_history(start_date, days)
        
        # Insert into database
        self.db.insert_telemetry(telemetry_data)
        self.db.insert_events(events_data)
        self.db.insert_maintenance(maintenance_data)
        
        # Save metadata
        self.save_data_metadata(days, datetime.now())
        
        print(f"✅ Successfully generated {days} days of sample data!")
        return True
    
    def clear_all_data(self):
        """Clear all data and metadata"""
        try:
            # Clear database
            self.db.clear_old_data(days_to_keep=0)
            
            # Remove metadata file
            if os.path.exists(self.metadata_file):
                os.remove(self.metadata_file)
            
            print("✅ All data cleared successfully!")
            return True
        except Exception as e:
            print(f"❌ Error clearing data: {e}")
            return False
    
    def get_data_summary(self):
        """Get summary of existing data"""
        try:
            stats = self.db.get_database_stats()
            metadata = self.get_data_metadata()
            
            summary = {
                'telemetry_count': stats.get('telemetry_count', 0),
                'events_count': stats.get('events_count', 0),
                'maintenance_count': stats.get('maintenance_count', 0),
                'date_range': stats.get('date_range', 'Unknown'),
                'metadata': metadata
            }
            
            return summary
        except Exception as e:
            print(f"❌ Error getting data summary: {e}")
            return None

if __name__ == "__main__":
    # Test data persistence
    manager = DataPersistenceManager()
    
    print("=== Data Persistence Manager Test ===")
    
    # Check if data exists
    if manager.check_data_exists():
        print("✅ Data exists")
        summary = manager.get_data_summary()
        if summary:
            print(f"   Telemetry: {summary['telemetry_count']} records")
            print(f"   Events: {summary['events_count']} records")
            print(f"   Maintenance: {summary['maintenance_count']} records")
    else:
        print("❌ No data found")
        print("Generating sample data...")
        manager.generate_data_once(7)
