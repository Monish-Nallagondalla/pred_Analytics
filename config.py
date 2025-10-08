"""
Configuration for JR Manufacturing Smart Dashboard
Sheet Metal Fabrication & Injection Moulding SME
"""

import os
from datetime import datetime as dt, timedelta

# Company Information
COMPANY_NAME = "JR Manufacturing"
LOCATION = "Industrial Zone, Manufacturing City"
BUSINESS_TYPE = "Sheet Metal Fabrication & Injection Moulding SME"

# Shop Floor Configuration
SHIFT_1_START = "08:00"
SHIFT_1_END = "16:00"
SHIFT_2_START = "16:00"
SHIFT_2_END = "00:00"

# Machine Configuration with Real Specifications
MACHINES = {
    "LASER_01": {
        "name": "TRUMPF TruLaser 3030",
        "type": "Laser_Cutting",
        "manufacturer": "TRUMPF GmbH",
        "specs": {
            "power": 4000,  # 4kW fiber laser
            "bed_size": "3000x1500mm",
            "max_speed": 100,  # m/min
            "rated_temp": 60,  # °C
            "rated_vibration": 2.0,  # mm/s
            "rated_current": 15,  # A
            "rated_pressure": 6  # bar
        },
        "sensors": ["spindle_speed", "laser_temp", "cutting_time", "power_usage", "vibration", "current", "pressure"],
        "process_time": 2.5,  # minutes per part
        "capacity": 24  # parts per hour
    },
    "PUNCH_01": {
        "name": "Amada EM-2510NT",
        "type": "CNC_Punching",
        "manufacturer": "Amada",
        "specs": {
            "tonnage": 20,  # 20-ton press
            "stations": 58,
            "rated_temp": 45,
            "rated_vibration": 1.5,
            "rated_current": 25,
            "rated_pressure": 150
        },
        "sensors": ["punch_force", "cycle_time", "hydraulic_pressure", "x_servo_torque", "y_servo_torque", "temp", "vibration"],
        "process_time": 1.8,
        "capacity": 33
    },
    "BEND_01": {
        "name": "Bystronic Xpert 150",
        "type": "Press_Brake",
        "manufacturer": "Bystronic",
        "specs": {
            "tonnage": 150,  # 150-ton
            "length": 3000,  # 3m length
            "rated_temp": 50,
            "rated_vibration": 2.5,
            "rated_current": 30,
            "rated_pressure": 200
        },
        "sensors": ["pressure", "bending_angle", "oil_temp", "stroke_count", "motor_temp", "vibration", "current"],
        "process_time": 3.2,
        "capacity": 19
    },
    "WELD_01": {
        "name": "Lincoln Electric i400",
        "type": "Spot_Welding",
        "manufacturer": "Lincoln Electric",
        "specs": {
            "current": 400,  # 400A inverter
            "phase": "3-phase",
            "rated_temp": 40,
            "rated_vibration": 1.0,
            "rated_current": 400,
            "rated_voltage": 220
        },
        "sensors": ["current", "electrode_temp", "duty_cycle", "weld_duration", "voltage", "vibration", "temp"],
        "process_time": 0.8,
        "capacity": 75
    },
    "POLISH_01": {
        "name": "3M Polishing Unit Pro",
        "type": "Surface_Polisher",
        "manufacturer": "3M",
        "specs": {
            "motor_power": 2,  # 2HP motor
            "heads": 2,  # Dual-head
            "rated_temp": 35,
            "rated_vibration": 3.0,
            "rated_current": 8,
            "max_rpm": 3000
        },
        "sensors": ["motor_temp", "vibration", "rpm", "belt_wear", "current", "power", "speed"],
        "process_time": 4.5,
        "capacity": 13
    },
    "COAT_01": {
        "name": "Nordson Encore HD",
        "type": "Powder_Coating",
        "manufacturer": "Nordson",
        "specs": {
            "voltage": 100,  # 100kV electrostatic
            "rated_temp": 55,
            "rated_vibration": 1.8,
            "rated_current": 12,
            "rated_pressure": 4
        },
        "sensors": ["booth_pressure", "spray_time", "coating_thickness", "voltage", "temp", "vibration", "current"],
        "process_time": 5.0,
        "capacity": 12
    },
    "INJECT_01": {
        "name": "Arburg Allrounder 470C",
        "type": "Injection_Moulding",
        "manufacturer": "Arburg",
        "specs": {
            "clamping_force": 100,  # 100-ton clamping
            "barrel_temp": 230,  # 230°C barrel
            "rated_temp": 230,
            "rated_vibration": 2.2,
            "rated_current": 40,
            "rated_pressure": 1500
        },
        "sensors": ["barrel_temp", "injection_pressure", "screw_torque", "cycle_time", "mould_temp", "vibration", "current"],
        "process_time": 1.2,
        "capacity": 50
    },
    "ASSEMBLY_01": {
        "name": "Custom Jig & Fixture Setup",
        "type": "Assembly_Station",
        "manufacturer": "JR Automation",
        "specs": {
            "operation": "Manual/Auto",
            "rated_temp": 30,
            "rated_vibration": 0.5,
            "rated_current": 5,
            "max_torque": 50
        },
        "sensors": ["cycle_time", "tool_torque", "rework_count", "temp", "vibration", "current", "power"],
        "process_time": 6.0,
        "capacity": 10
    },
    "INSPECT_01": {
        "name": "Mitutoyo QV-Active Vision",
        "type": "Quality_Inspection",
        "manufacturer": "Mitutoyo",
        "specs": {
            "precision": "micrometer",
            "scanning": "3D",
            "rated_temp": 25,
            "rated_vibration": 0.2,
            "rated_current": 3,
            "accuracy": 0.001
        },
        "sensors": ["measurement_deviation", "inspection_time", "temp", "vibration", "current", "accuracy", "defect_count"],
        "process_time": 2.0,
        "capacity": 30
    },
    "PACK_01": {
        "name": "FlexLink X85",
        "type": "Packaging_Conveyor",
        "manufacturer": "FlexLink",
        "specs": {
            "speed": "variable",
            "control": "PLC",
            "rated_temp": 40,
            "rated_vibration": 1.5,
            "rated_current": 10,
            "max_speed": 50
        },
        "sensors": ["conveyor_speed", "stoppage_time", "package_count", "temp", "vibration", "current", "power"],
        "process_time": 0.5,
        "capacity": 120
    }
}

# Production Flow Sequence
PRODUCTION_FLOW = [
    "LASER_01",    # Laser Cutting
    "PUNCH_01",    # CNC Punching
    "BEND_01",     # Press Brake Bending
    "WELD_01",     # Spot Welding
    "COAT_01",     # Powder Coating
    "ASSEMBLY_01", # Assembly Station
    "INSPECT_01",  # Quality Inspection
    "PACK_01"      # Packaging
]

# Andon Trigger Rules
ANDON_RULES = {
    "high_temperature": {
        "condition": "temp > rated_temp + 20",
        "severity": "yellow",
        "description": "High Temperature Alert"
    },
    "vibration_anomaly": {
        "condition": "z_score > 3",
        "severity": "red",
        "description": "Vibration Anomaly Detected"
    },
    "cycle_delay": {
        "condition": "cycle_time > mean_cycle_time * 1.2",
        "severity": "yellow",
        "description": "Cycle Time Delay"
    },
    "power_spike": {
        "condition": "power > rated_power * 1.3",
        "severity": "red",
        "description": "Power Spike Detected"
    },
    "maintenance_due": {
        "condition": "hours_since_maintenance > 500",
        "severity": "yellow",
        "description": "Maintenance Due"
    }
}

# Alert Thresholds
ALERT_THRESHOLDS = {
    "critical_vibration": 4.0,  # mm/s
    "high_temp": 80,  # °C
    "power_spike_multiplier": 1.3,
    "cycle_delay_threshold": 1.2,
    "maintenance_hours": 500,
    "andon_trigger_duration": 60  # seconds
}

# Database Configuration
DATABASE_PATH = "jr_manufacturing.db"

# Simulation Configuration
SIMULATION_START_DATE = dt(2025, 1, 1)
SIMULATION_DAYS = 14  # 2 weeks
SAMPLE_RATE_SECONDS = 5  # 5-second intervals
LOW_FREQ_SAMPLE_RATE = 30  # 30-second intervals for some sensors

# Dashboard Configuration
DASHBOARD_REFRESH_RATE = 5  # seconds
KPI_WINDOW_DAYS = 7

# Machine Flow Optimization
FLOW_OPTIMIZATION = {
    "bottleneck_threshold": 0.8,  # 80% utilization
    "queue_time_threshold": 30,  # 30 minutes
    "efficiency_target": 85,  # 85% efficiency target
    "parallel_machines": ["LASER_01", "PUNCH_01", "BEND_01"]  # Machines that can have parallel units
}

# Quality Metrics
QUALITY_METRICS = {
    "defect_threshold": 0.05,  # 5% defect rate
    "rework_threshold": 0.02,  # 2% rework rate
    "scrap_threshold": 0.01,   # 1% scrap rate
    "quality_target": 99.5     # 99.5% quality target
}

# Maintenance Schedule
MAINTENANCE_SCHEDULE = {
    "preventive_interval": 500,  # hours
    "predictive_interval": 250,  # hours
    "emergency_threshold": 0.1,  # 10% failure probability
    "spare_parts_lead_time": 7   # days
}