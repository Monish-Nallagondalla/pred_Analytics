# Apex Components Predictive Maintenance System

## Overview
A comprehensive predictive maintenance and data analytics system for Apex Components Pvt. Ltd., a light industrial contract manufacturer. The system provides real-time monitoring, predictive analytics, flow optimization, and machine layout planning for 8 different types of manufacturing equipment.

## System Architecture

### Core Components

1. **Dashboard Application** (`dashboard.py`)
   - Streamlit-based web interface
   - Real-time monitoring and KPIs
   - Interactive charts and visualizations
   - Multi-tab interface for different functionalities

2. **Andon System** (`andon_system.py`)
   - Real-time alerting and escalation
   - Automated trigger detection
   - Email/SMS notifications
   - Machine status monitoring

3. **Machine Learning Models** (`ml_models.py`)
   - Anomaly detection using Isolation Forest
   - RUL (Remaining Useful Life) prediction
   - Fault classification using Random Forest
   - Performance analysis and OEE calculation

4. **Flow Optimization** (`flow_optimization.py`)
   - Bottleneck detection and analysis
   - Production flow optimization
   - Machine layout optimization
   - Buffer size recommendations

5. **Data Management** (`database.py`)
   - SQLite database operations
   - Data storage and retrieval
   - Historical data analysis
   - Database statistics

6. **Data Generation** (`data_generator.py`)
   - Synthetic data generation for testing
   - Realistic sensor data simulation
   - Failure pattern modeling
   - Maintenance event simulation

## Machine Configuration

The system monitors 8 different types of manufacturing equipment:

1. **VF2_01** - Haas VF-2 CNC Mill
2. **ST10_01** - Haas ST-10 CNC Lathe  
3. **KUKA_01** - KUKA KR-6 Robot
4. **COMPRESSOR_01** - Atlas Copco GA11 Compressor
5. **LASER_01** - Trotec Speedy 100 Laser
6. **PRESS_01** - Amada HFE Press Brake
7. **DRILL_01** - Bosch PBD 40 Drill
8. **GRINDER_01** - Okuma Surface Grinder

## Key Features

### 1. Data Persistence & Management
- **One-Time Data Generation**: Sample data is generated only once and reused
- **Automatic Data Detection**: System detects existing data and loads it automatically
- **Data Metadata Tracking**: Tracks when and how much data was generated
- **Smart Caching**: Avoids unnecessary data regeneration

### 2. Real-time Monitoring
- Live sensor data visualization
- Machine status tracking
- Performance metrics (OEE, MTBF, MTTR)
- Quality monitoring

### 2. Predictive Analytics
- **Anomaly Detection**: Identifies unusual patterns in sensor data
- **RUL Prediction**: Estimates remaining useful life of components
- **Fault Classification**: Categorizes different types of failures
- **Performance Analysis**: Calculates OEE and other KPIs

### 3. Andon System
- **Alert Rules**: Configurable thresholds for different conditions
- **Escalation Levels**: Automatic escalation based on severity
- **Notification System**: Email and SMS alerts
- **Machine Control**: Automatic machine stopping for critical issues

### 4. Flow Optimization
- **Bottleneck Analysis**: Identifies production bottlenecks
- **Flow Efficiency**: Calculates overall production flow efficiency
- **Layout Optimization**: Recommends machine layout improvements
- **Scheduling Optimization**: Optimizes machine scheduling

### 5. Data Analytics
- **Historical Analysis**: Trend analysis and pattern recognition
- **Report Generation**: Automated report generation
- **KPI Tracking**: Real-time KPI monitoring
- **Performance Benchmarking**: Compare performance across machines

## Installation and Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd optimax
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run startup script (recommended)**
   ```bash
   python startup.py
   ```
   This will check system requirements and generate sample data if needed.

4. **Run the application**
   ```bash
   streamlit run main.py
   ```

5. **Access the dashboard**
   - Open your browser and go to `http://localhost:8501`
   - The dashboard will load with the main interface

## Usage Guide

### 1. Initial Setup
- **Automatic Data Detection**: The system automatically detects if sample data already exists
- **One-Time Generation**: Sample data is generated only once and reused across sessions
- **Data Persistence**: Data is saved to the database and persists between runs
- **Smart Loading**: The system automatically loads existing data if available

### 2. Dashboard Navigation

#### Overview Tab
- **KPI Cards**: Overall OEE, Active Machines, Active Alerts, Production Efficiency
- **Machine Status Chart**: Distribution of machine states
- **Production Trends**: Production cycles over time
- **Recent Events**: Latest system events

#### Real-time Monitoring Tab
- **Machine Status**: Live status of all machines
- **Sensor Readings**: Current sensor values
- **Detailed Monitoring**: Individual machine details

#### Predictive Analytics Tab
- **Anomaly Detection**: ML-based anomaly detection results
- **RUL Predictions**: Remaining useful life estimates
- **Fault Classification**: Predicted fault types
- **ML Performance**: Model performance metrics

#### Andon System Tab
- **Active Alerts**: Current active alerts and their severity
- **Alert Statistics**: Historical alert statistics
- **Alert History**: Complete alert history
- **Alert Rules**: Configuration of alert rules

#### Flow Optimization Tab
- **Bottleneck Analysis**: Production bottleneck identification
- **Flow Efficiency**: Overall flow efficiency metrics
- **Optimization Recommendations**: AI-generated recommendations
- **Layout Optimization**: Machine layout suggestions

#### Reports Tab
- **Report Generation**: Generate various types of reports
- **Date Range Selection**: Customize report time periods
- **Export Options**: Export reports in different formats

### 3. Simulation Controls
- **Start Simulation**: Begin real-time data simulation
- **Stop Simulation**: Stop the simulation
- **Auto Refresh**: Enable/disable automatic dashboard refresh
- **Refresh Interval**: Set refresh rate (5-60 seconds)

## Configuration

### Alert Thresholds
The system uses configurable thresholds for different alert conditions:
- **Critical Vibration**: 4.0 mm/s
- **High Temperature**: 85°C
- **Current Spike**: 2x normal current
- **Quality Issues**: Scrap/rework detection

### Machine Configuration
Each machine has specific sensor configurations and operating parameters defined in `config.py`.

### Database Configuration
- **Database Path**: `apex_components.db`
- **Data Retention**: Configurable data retention periods
- **Backup**: Automatic database backup options

## Troubleshooting

### Common Issues

1. **Continuous Logging**
   - **Issue**: Logs are generated continuously even without stopping
   - **Solution**: Auto-refresh is disabled by default. Enable only when needed.

2. **High Data Volume**
   - **Issue**: Too much data being generated
   - **Solution**: Data generation interval increased to 5 minutes

3. **Performance Issues**
   - **Issue**: Dashboard running slowly
   - **Solution**: Reduce refresh rate or disable auto-refresh

4. **Database Issues**
   - **Issue**: Database connection problems
   - **Solution**: Check database file permissions and path

### Performance Optimization

1. **Data Management**
   - Regular cleanup of old data
   - Optimized database queries
   - Efficient data storage

2. **Dashboard Performance**
   - Disable auto-refresh when not needed
   - Use appropriate refresh intervals
   - Limit data visualization scope

3. **ML Model Performance**
   - Model caching and persistence
   - Efficient feature extraction
   - Optimized prediction algorithms

## Development

### Code Structure
```
optimax/
├── main.py                 # Application entry point
├── dashboard.py            # Streamlit dashboard
├── andon_system.py        # Alert and notification system
├── ml_models.py           # Machine learning models
├── flow_optimization.py   # Production flow optimization
├── database.py            # Database management
├── data_generator.py      # Synthetic data generation
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
└── README.md             # This file
```

### Adding New Features

1. **New Machine Types**
   - Add machine configuration in `config.py`
   - Implement sensor data generation in `data_generator.py`
   - Update dashboard visualization

2. **New Alert Rules**
   - Add rules in `andon_system.py`
   - Configure thresholds in `config.py`
   - Update notification system

3. **New ML Models**
   - Implement in `ml_models.py`
   - Add training and prediction methods
   - Update dashboard integration

### Testing
- Use synthetic data generation for testing
- Test with different machine configurations
- Validate ML model performance
- Test alert system functionality

## Future Enhancements

1. **Advanced ML Models**
   - Deep learning for complex pattern recognition
   - Time series forecasting
   - Multi-variate analysis

2. **IoT Integration**
   - Real sensor data integration
   - Edge computing capabilities
   - Real-time data streaming

3. **Mobile Application**
   - Mobile dashboard
   - Push notifications
   - Offline capabilities

4. **Advanced Analytics**
   - Digital twin simulation
   - Advanced optimization algorithms
   - Predictive scheduling

## Support and Maintenance

### Regular Maintenance
- Database cleanup and optimization
- Model retraining and updates
- System performance monitoring
- Security updates

### Monitoring
- System health monitoring
- Performance metrics tracking
- Error logging and analysis
- User activity monitoring

## License
This project is proprietary software for Apex Components Pvt. Ltd.

## Contact
For technical support or questions, contact the development team.

---

**Note**: This system is designed for manufacturing environments and requires proper setup and configuration for production use. Always test thoroughly before deploying in production environments.