"""
Simple Main Data Generator
Uses schema-compliant generator to match project plan exactly
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import json
from .schema_compliant_generator import SchemaCompliantDataGenerator

class SimpleMainDataGenerator:
    """
    Simple main data generator using schema-compliant approach
    """
    
    def __init__(self, config_path="config/machines.yaml"):
        """Initialize the simple main data generator"""
        self.config_path = config_path
        self.schema_generator = SchemaCompliantDataGenerator(config_path)
        
        # Create output directories
        self.create_directories()
    
    def create_directories(self):
        """Create necessary directories"""
        directories = [
            "data/raw",
            "artifacts/models",
            "artifacts/metadata"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def generate_all_data(self, start_date=None, days=30):
        """
        Generate all synthetic data using schema-compliant generator
        """
        if start_date is None:
            start_date = datetime.now() - timedelta(days=days)
        
        print("=" * 60)
        print("JR Manufacturing Schema-Compliant Data Generation")
        print("=" * 60)
        print(f"Start Date: {start_date.strftime('%Y-%m-%d')}")
        print(f"Days: {days}")
        print(f"Output Directory: data/raw/")
        print("=" * 60)
        
        # Generate schema-compliant data
        print("\nGenerating schema-compliant data...")
        schema_data = self.schema_generator.generate_all_data(start_date, days)
        
        print("\n✅ All schema-compliant data generated successfully!")
        print("📁 Data saved to data/raw/")
        
        return schema_data

def main():
    """Main function for testing"""
    generator = SimpleMainDataGenerator()
    generator.generate_all_data(days=7)

if __name__ == "__main__":
    main()
