# Apex Components Predictive Maintenance System - Complete Code Documentation

## Table of Contents
1. [System Architecture Overview](#system-architecture-overview)
2. [Core Components Deep Dive](#core-components-deep-dive)
3. [Data Flow Architecture](#data-flow-architecture)
4. [Machine Learning Pipeline](#machine-learning-pipeline)
5. [Database Schema & Operations](#database-schema--operations)
6. [User Interface Logic](#user-interface-logic)
7. [Error Handling & Fallbacks](#error-handling--fallbacks)
8. [Configuration Management](#configuration-management)
9. [Deployment & Testing](#deployment--testing)

---

## System Architecture Overview

### High-Level Architecture
The system follows a modular architecture with clear separation of concerns:

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Streamlit     │    │   Database      │    │   ML Models     │
│   Dashboard     │◄──►│   Manager       │◄──►│   Pipeline      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Andon System  │    │   Data          │    │   Flow          │
│   (Alerts)      │    │   Generator     │    │   Optimization  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### Key Design Principles
1. **Modularity**: Each component has a single responsibility
2. **Data Persistence**: One-time data generation with smart caching
3. **Error Resilience**: Graceful degradation when components fail
4. **User Experience**: Intuitive interface with clear status indicators

---

## Core Components Deep Dive

### 1. Main Application Entry Point (`main.py`)

**Purpose**: Application bootstrap and error handling
**Key Logic**:
- Imports the `DashboardApp` class from `dashboard.py`
- Implements global exception handling with user-friendly error messages
- Sets up the application entry point for Streamlit

**Error Handling Strategy**:
- Catches all exceptions at the top level
- Displays error messages in the Streamlit interface
- Provides guidance for troubleshooting

### 2. Dashboard Application (`dashboard.py`)

**Purpose**: Central Streamlit application orchestrating all components
**Architecture Pattern**: MVC (Model-View-Controller) with Streamlit as the view layer

#### Class Structure: `DashboardApp`
- **Initialization Logic**:
  - Creates instances of all subsystem managers
  - Initializes session state for data persistence
  - Checks for existing data automatically

- **Session State Management**:
  - `data_loaded`: Tracks if sample data exists
  - `simulation_running`: Controls real-time simulation state
  - `selected_machines`: User's machine selection preferences

#### Rendering Logic Hierarchy:
1. **Setup Page**: Data initialization and system status
2. **Main Dashboard**: Six-tab interface with different functionalities
3. **Sidebar**: Control panel with data management and simulation controls

#### Data Management Strategy:
- **Smart Data Detection**: Automatically checks database for existing data
- **One-Time Generation**: Prevents unnecessary data regeneration
- **Persistence Integration**: Uses `DataPersistenceManager` for data lifecycle

### 3. Database Management (`database.py`)

**Purpose**: SQLite database operations and data persistence
**Architecture**: Repository pattern with connection management

#### Class: `DatabaseManager`
**Core Responsibilities**:
- Database schema initialization
- CRUD operations for all data types
- Connection lifecycle management
- Data type conversion and validation

#### Schema Design:
- **Telemetry Table**: Sensor data with 50+ columns for different machine types
- **Events Table**: Alert and event logging with resolution tracking
- **Maintenance Table**: Maintenance history with cost tracking
- **Production Flow Table**: Workflow optimization data
- **KPIs Table**: Cached performance metrics

#### Query Optimization Strategy:
- Uses parameterized queries to prevent SQL injection
- Implements LIMIT clauses for performance
- Orders results by timestamp for chronological analysis
- Handles NULL values gracefully

### 4. Machine Learning Pipeline (`ml_models.py`)

**Purpose**: Predictive analytics and anomaly detection
**Architecture**: Pipeline pattern with separate model classes

#### Model Classes:

##### `AnomalyDetector`
- **Algorithm**: Isolation Forest for unsupervised anomaly detection
- **Feature Engineering**: Standardizes sensor data across different machine types
- **Training Logic**: Fits on normal operational data, flags outliers
- **Output**: Binary classification (-1 for anomaly, 1 for normal)

##### `RULPredictor`
- **Algorithm**: Multi-layer Perceptron for regression
- **Data Preparation**: Creates sliding windows of sensor data
- **Training Logic**: Uses degradation patterns to predict remaining useful life
- **Output**: Hours until predicted failure

##### `FaultClassifier`
- **Algorithm**: Random Forest for multi-class classification
- **Feature Engineering**: Combines sensor data with categorical variables
- **Training Logic**: Supervised learning on historical fault data
- **Output**: Fault type predictions with probability scores

#### Training Pipeline:
1. **Data Validation**: Ensures sufficient data for training
2. **Feature Selection**: Automatically selects relevant sensor columns
3. **Model Fitting**: Trains each model with appropriate data
4. **Error Handling**: Graceful degradation if training fails
5. **Persistence**: Models can be saved/loaded for reuse

### 5. Andon System (`andon_system.py`)

**Purpose**: Real-time alerting and escalation management
**Architecture**: Rule-based system with configurable thresholds

#### Core Classes:

##### `AndonTrigger`
- **State Management**: Tracks trigger lifecycle (created → active → resolved)
- **Metadata**: Stores machine ID, severity, description, timestamps
- **Resolution Tracking**: Records resolution actions and timing

##### `AlertRule`
- **Rule Engine**: Lambda functions for condition evaluation
- **Severity Levels**: Four-tier escalation (low, medium, high, critical)
- **Escalation Logic**: Different notification channels per severity

##### `AndonSystem`
- **Rule Management**: Dynamic rule addition with duplicate prevention
- **Alert Processing**: Evaluates sensor data against all rules
- **Notification System**: Email/SMS/Dashboard integration
- **Machine Control**: Automatic machine stopping for critical alerts

#### Alert Rule Types:
1. **Critical Vibration**: Exceeds 4.0 mm/s threshold
2. **High Temperature**: Any temperature sensor > 85°C
3. **Current Spike**: Motor current > 15A
4. **Quality Issues**: Scrap/rework detection
5. **Machine Faults**: State-based fault detection
6. **ML Anomalies**: AI-detected unusual patterns
7. **Low RUL**: Remaining useful life < 24 hours

### 6. Flow Optimization (`flow_optimization.py`)

**Purpose**: Production flow analysis and bottleneck detection
**Architecture**: Graph-based optimization with network analysis

#### Core Classes:

##### `ProductionFlow`
- **Capacity Modeling**: Parts per hour calculations
- **Queue Management**: Job queuing and processing simulation
- **Utilization Tracking**: Real-time capacity utilization

##### `BottleneckDetector`
- **Graph Analysis**: Uses NetworkX for flow network modeling
- **Bottleneck Scoring**: Combines idle time, fault time, and utilization
- **Critical Path Analysis**: Identifies production constraints

##### `FlowOptimizer`
- **Optimization Strategies**: Multiple approaches for flow improvement
- **Recommendation Engine**: Generates actionable optimization suggestions
- **Scheduling Logic**: Optimizes machine scheduling based on demand

##### `LayoutOptimizer`
- **Distance Calculations**: Euclidean distance between machine positions
- **Flow Frequency Analysis**: Tracks material movement patterns
- **Layout Recommendations**: Suggests machine repositioning for efficiency

### 7. Data Generation (`data_generator.py`)

**Purpose**: Synthetic data generation for testing and simulation
**Architecture**: Factory pattern with machine-specific generators

#### Class: `MachineDataGenerator`
**Per-Machine Logic**:
- **State Simulation**: Realistic machine state transitions
- **Sensor Data**: Machine-specific sensor value generation
- **Degradation Modeling**: Progressive wear simulation over time
- **Failure Patterns**: Realistic failure probability modeling

#### Data Generation Strategy:
- **Temporal Patterns**: Shift-based operation (8-16h, 16-24h)
- **Weekend Operations**: Reduced activity on weekends
- **Maintenance Windows**: Scheduled maintenance every 4 hours
- **Failure Simulation**: Probability-based fault generation
- **Quality Variation**: Realistic quality flag distribution

#### Machine-Specific Generators:
1. **CNC Mill**: Spindle RPM, axis positions, cutting forces
2. **CNC Lathe**: Chuck status, turret indexing, oil temperature
3. **Robot**: Joint positions, TCP forces, controller temperature
4. **Compressor**: Pressure levels, duty cycle, condensate
5. **Laser**: Power levels, head temperature, exhaust flow
6. **Press Brake**: Ram position, hydraulic pressure, load cells
7. **Drill**: Spindle RPM, feed rates, stroke counts
8. **Grinder**: Wheel RPM, coolant flow, table feed

### 8. Data Persistence (`data_persistence.py`)

**Purpose**: Smart data lifecycle management
**Architecture**: Singleton pattern with metadata tracking

#### Class: `DataPersistenceManager`
**Core Logic**:
- **Existence Checking**: Verifies data presence before generation
- **Metadata Tracking**: Stores generation parameters and timestamps
- **Smart Caching**: Prevents unnecessary data regeneration
- **Data Summary**: Provides comprehensive data statistics

#### Persistence Strategy:
- **One-Time Generation**: Generates data only if not exists
- **Metadata Storage**: JSON file with generation details
- **Data Validation**: Ensures data integrity before use
- **Cleanup Operations**: Safe data deletion with confirmation

---

## Data Flow Architecture

### 1. Data Generation Flow
```
User Request → DataPersistenceManager → DataSimulator → DatabaseManager → SQLite
```

**Logic**:
- Check if data exists using metadata
- Generate telemetry, events, and maintenance data
- Insert into database with transaction safety
- Update metadata for future reference

### 2. Real-Time Data Flow
```
Sensor Data → AndonSystem → Alert Rules → Notifications → Dashboard
```

**Logic**:
- Continuous sensor data evaluation
- Rule-based alert triggering
- Multi-channel notification dispatch
- Dashboard real-time updates

### 3. ML Pipeline Flow
```
Historical Data → Feature Engineering → Model Training → Predictions → Dashboard
```

**Logic**:
- Data preprocessing and feature selection
- Model training with error handling
- Prediction generation with fallbacks
- Results visualization in dashboard

### 4. Optimization Flow
```
Production Data → Flow Analysis → Bottleneck Detection → Recommendations → Dashboard
```

**Logic**:
- Production flow graph construction
- Bottleneck identification algorithms
- Optimization recommendation generation
- Layout improvement suggestions

---

## Machine Learning Pipeline

### 1. Data Preprocessing
**Feature Selection Logic**:
- Automatically identifies relevant sensor columns
- Handles missing values with zero-filling
- Standardizes data across different machine types
- Creates sliding windows for time-series analysis

### 2. Model Training Strategy
**Training Sequence**:
1. **Anomaly Detection**: Unsupervised learning on normal data
2. **RUL Prediction**: Regression on degradation patterns
3. **Fault Classification**: Supervised learning on labeled data

**Error Handling**:
- Graceful degradation when training fails
- Fallback to dummy predictions for demonstration
- User-friendly error messages in dashboard

### 3. Prediction Pipeline
**Inference Logic**:
- Real-time data preprocessing
- Model prediction with confidence scores
- Result aggregation across machines
- Dashboard visualization with color coding

### 4. Model Performance
**Metrics Tracking**:
- Accuracy indicators for each model type
- Performance comparison across machines
- Training status monitoring
- Prediction confidence scoring

---

## Database Schema & Operations

### 1. Table Relationships
```
Telemetry (1) ←→ (N) Events
Telemetry (1) ←→ (N) Maintenance
Telemetry (1) ←→ (N) Production_Flow
```

### 2. Query Optimization
**Performance Strategies**:
- Indexed timestamp columns for time-based queries
- LIMIT clauses for large dataset handling
- Parameterized queries for security
- Connection pooling for concurrent access

### 3. Data Integrity
**Validation Logic**:
- Type conversion for numpy/pandas compatibility
- NULL value handling in sensor data
- Timestamp standardization across tables
- Foreign key relationship maintenance

### 4. Backup & Recovery
**Data Management**:
- Automatic old data cleanup
- Metadata preservation
- Transaction safety for data operations
- Database statistics tracking

---

## User Interface Logic

### 1. Streamlit Architecture
**Page Structure**:
- **Setup Page**: Initial data loading and system status
- **Main Dashboard**: Six-tab interface with different functionalities
- **Sidebar**: Control panel with data management options

### 2. State Management
**Session State Logic**:
- `data_loaded`: Tracks data availability
- `simulation_running`: Controls real-time features
- `selected_machines`: User preferences
- `time_range`: Data filtering options

### 3. Component Rendering
**Rendering Hierarchy**:
1. **Header**: Company branding and system status
2. **Sidebar**: Control panel with data management
3. **Main Content**: Tab-based interface
4. **Footer**: System information and status

### 4. User Experience
**UX Patterns**:
- **Progressive Disclosure**: Show relevant options based on data state
- **Status Indicators**: Clear visual feedback for system state
- **Error Handling**: User-friendly error messages
- **Loading States**: Spinner animations for long operations

---

## Error Handling & Fallbacks

### 1. Database Errors
**Handling Strategy**:
- Connection failure recovery
- Query timeout handling
- Data type conversion errors
- Transaction rollback on failures

### 2. ML Model Errors
**Fallback Logic**:
- Dummy predictions when models fail
- Graceful degradation messages
- Training error recovery
- Model persistence issues

### 3. Data Generation Errors
**Recovery Mechanisms**:
- Partial data generation handling
- Database insertion failures
- Memory management for large datasets
- File system errors

### 4. UI Errors
**User Experience**:
- Streamlit rendering errors
- Chart generation failures
- Data loading timeouts
- Session state corruption

---

## Configuration Management

### 1. Machine Configuration (`config.py`)
**Configuration Structure**:
- Machine definitions with sensor specifications
- Alert thresholds for different conditions
- Simulation parameters for data generation
- Dashboard settings for user interface

### 2. Environment Variables
**System Settings**:
- Database path configuration
- Logging levels and destinations
- Email/SMS notification settings
- ML model parameters

### 3. User Preferences
**Customization Options**:
- Machine selection preferences
- Time range filtering
- Refresh rate settings
- Display options

---

## Deployment & Testing

### 1. System Requirements
**Dependencies**:
- Python 3.8+ with specific package versions
- SQLite database for data storage
- Streamlit for web interface
- Machine learning libraries (scikit-learn, pandas, numpy)

### 2. Testing Strategy
**Test Coverage**:
- Unit tests for individual components
- Integration tests for data flow
- End-to-end tests for user workflows
- Performance tests for large datasets

### 3. Deployment Process
**Deployment Steps**:
1. **Environment Setup**: Python environment with dependencies
2. **Data Initialization**: Run startup script for data generation
3. **System Validation**: Test all components functionality
4. **User Training**: Documentation and usage guidelines

### 4. Monitoring & Maintenance
**Operational Aspects**:
- Log file management and rotation
- Database cleanup and optimization
- Performance monitoring
- Error tracking and resolution

---

## Key Design Decisions

### 1. Why SQLite?
- **Lightweight**: No server setup required
- **Portable**: Single file database
- **Reliable**: ACID compliance for data integrity
- **Performance**: Sufficient for prototype scale

### 2. Why Streamlit?
- **Rapid Development**: Quick prototype creation
- **Python Native**: Seamless integration with ML libraries
- **Interactive**: Real-time dashboard capabilities
- **Deployment**: Easy web application deployment

### 3. Why Modular Architecture?
- **Maintainability**: Easy to modify individual components
- **Testability**: Isolated testing of each module
- **Scalability**: Easy to add new features
- **Reusability**: Components can be used independently

### 4. Why Data Persistence?
- **User Experience**: No repeated data generation
- **Performance**: Faster application startup
- **Reliability**: Consistent data across sessions
- **Development**: Faster iteration cycles

---

## Future Enhancement Opportunities

### 1. Real-Time Data Integration
- **IoT Connectivity**: Direct sensor data integration
- **Edge Computing**: Local data processing
- **Real-Time Streaming**: Live data pipeline

### 2. Advanced Analytics
- **Deep Learning**: Neural networks for complex patterns
- **Time Series**: Advanced forecasting models
- **Computer Vision**: Image-based quality inspection

### 3. Scalability Improvements
- **Database Migration**: PostgreSQL for production scale
- **Microservices**: Distributed architecture
- **Cloud Deployment**: AWS/Azure integration

### 4. User Experience
- **Mobile Interface**: Responsive design
- **Offline Capability**: Local data processing
- **Advanced Visualization**: 3D layouts and AR/VR

---

This documentation provides a comprehensive understanding of the entire system architecture, data flow, and implementation logic without repeating the actual code. It serves as a reference for understanding, maintaining, and extending the Apex Components Predictive Maintenance System.
