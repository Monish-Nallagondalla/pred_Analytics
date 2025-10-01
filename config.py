"""
Configuration file for Apex Components Predictive Maintenance System
"""

import os
from datetime import datetime as dt, timedelta

# Company Information
COMPANY_NAME = "Apex Components Pvt. Ltd."
LOCATION = "Bengaluru, India"
BUSINESS_TYPE = "Light industrial contract manufacturer"

# Shop Floor Configuration
SHIFT_1_START = "08:00"
SHIFT_1_END = "16:00"
SHIFT_2_START = "16:00"
SHIFT_2_END = "00:00"

# Machine Configuration
MACHINES = {
    "VF2_01": {
        "name": "Haas VF-2 CNC Mill",
        "type": "CNC_Mill",
        "max_rpm": 7500,
        "max_current": 20,
        "normal_temp_range": (25, 80),
        "normal_vibration": 2.0,
        "sensors": ["spindle_rpm", "motor_current", "vibration_rms", "axis_x", "axis_y", "axis_z", "servo_temp", "power_draw"]
    },
    "ST10_01": {
        "name": "Haas ST-10 CNC Lathe",
        "type": "CNC_Lathe",
        "max_rpm": 6000,
        "max_current": 25,
        "normal_temp_range": (25, 80),
        "normal_vibration": 2.0,
        "sensors": ["spindle_rpm", "spindle_torque", "chuck_status", "turret_index", "vibration_rms", "oil_temp"]
    },
    "KUKA_01": {
        "name": "KUKA KR-6 Robot",
        "type": "Robot",
        "max_payload": 6,
        "reach": 1570,
        "normal_temp_range": (25, 60),
        "sensors": ["joint_pos_1", "joint_pos_2", "joint_pos_3", "joint_pos_4", "joint_pos_5", "joint_pos_6", "joint_current_1", "joint_current_2", "joint_current_3", "joint_current_4", "joint_current_5", "joint_current_6", "tcp_force", "controller_temp"]
    },
    "COMPRESSOR_01": {
        "name": "Atlas Copco GA11 Compressor",
        "type": "Compressor",
        "max_pressure": 10,
        "max_power": 11,
        "normal_temp_range": (30, 90),
        "sensors": ["suction_pressure", "discharge_pressure", "motor_current", "oil_temp", "vibration", "runtime_hours", "duty_cycle", "condensate_level"]
    },
    "LASER_01": {
        "name": "Trotec Speedy 100 Laser",
        "type": "Laser_Cutter",
        "max_power": 60,
        "max_speed": 2.8,
        "normal_temp_range": (25, 60),
        "sensors": ["laser_power", "head_temp", "exhaust_flow", "focal_height", "position_x", "position_y", "interlocks"]
    },
    "PRESS_01": {
        "name": "Amada HFE Press Brake",
        "type": "Press_Brake",
        "max_tonnage": 100,
        "normal_temp_range": (25, 60),
        "sensors": ["ram_position", "hydraulic_pressure", "load_cell", "cycle_time", "crowning_actuator", "motor_current", "back_gauge"]
    },
    "DRILL_01": {
        "name": "Bosch PBD 40 Drill",
        "type": "Bench_Drill",
        "max_rpm": 2500,
        "max_power": 0.71,
        "normal_temp_range": (25, 50),
        "sensors": ["spindle_rpm", "motor_current", "drill_feed", "chuck_state", "stroke_count"]
    },
    "GRINDER_01": {
        "name": "Okuma Surface Grinder",
        "type": "Grinder",
        "max_rpm": 3000,
        "normal_temp_range": (25, 60),
        "sensors": ["wheel_rpm", "spindle_current", "coolant_temp", "coolant_flow", "table_feed", "vibration"]
    }
}

# Alert Thresholds
ALERT_THRESHOLDS = {
    "critical_vibration": 4.0,  # mm/s
    "high_temp": 85,  # °C
    "current_spike_multiplier": 2.0,
    "quality_scrap_threshold": 1,
    "andon_trigger_duration": 60  # seconds
}

# Database Configuration
DATABASE_PATH = "apex_components.db"

# Simulation Configuration
SIMULATION_START_DATE = dt(2025, 1, 1)
SIMULATION_DAYS = 7  # Changed to 7 days as requested
SAMPLE_RATE_SECONDS = 5  # For high-frequency sensors (reduced from 1 second)
LOW_FREQ_SAMPLE_RATE = 30  # For low-frequency sensors (reduced from 10 seconds)

# Dashboard Configuration
DASHBOARD_REFRESH_RATE = 5  # seconds
KPI_WINDOW_DAYS = 7
