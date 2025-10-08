# 🏭 JR Manufacturing Smart Dashboard

**Modular Predictive Maintenance System for Industrial Manufacturing**

A comprehensive, production-ready system that integrates predictive maintenance, machine flow optimization, Andon alerts, and data analytics for Sheet Metal Fabrication & Injection Moulding operations.

## 🎯 Project Overview

This system provides:

- **Predictive Maintenance**: ML-powered failure prediction and RUL estimation
- **Machine Flow Optimization**: Bottleneck detection and throughput optimization
- **Andon System**: Real-time alerts and escalation management
- **Data Analytics**: Operational KPIs, machine performance, and maintenance insights

## 🏗️ Modular Architecture

```
jr_factory_pm/
├── config/
│   └── machines.yaml          # Machine definitions, sensor ranges, thresholds
├── data/
│   └── raw/                   # Generated synthetic data CSVs
├── artifacts/
│   ├── models/                # Saved ML models
│   └── metadata/              # Data generation and model metadata
├── src/
│   ├── data_generator/        # Synthetic data generation
│   │   ├── machine_data_generator.py
│   │   ├── production_flow_simulator.py
│   │   ├── event_simulator.py
│   │   └── main_data_generator.py
│   ├── ml_models/             # Predictive maintenance models
│   │   ├── anomaly_detector.py
│   │   ├── rul_predictor.py
│   │   ├── fault_classifier.py
│   │   └── predictive_models.py
│   ├── flow_optimization/     # Machine flow optimization
│   ├── andon_system/          # Alert and escalation
│   └── dashboard/             # Streamlit dashboard
├── main.py                    # Application entry point
├── requirements.txt           # Python packages
└── README.md                  # Project documentation
```

## 🚀 Quick Start

### 1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### 2. **Generate Synthetic Data (One-time)**
```bash
python -c "
from src.data_generator.main_data_generator import MainDataGenerator
generator = MainDataGenerator()
generator.generate_all_data(days=30)
"
```

### 3. **Train ML Models (One-time)**
   ```bash
python -c "
from src.ml_models.predictive_models import PredictiveMaintenanceModels
import pandas as pd

# Load data
telemetry = pd.read_csv('data/raw/telemetry_data.csv')
events = pd.read_csv('data/raw/events_data.csv')

# Train models
models = PredictiveMaintenanceModels()
models.train_all_models(telemetry, events)
"
```

### 4. **Run Dashboard**
   ```bash
   streamlit run main.py
   ```

## 🏭 Industrial Machines

### **Sheet Metal Fabrication**
1. **CNC_Punch_01**: Amada Vipros 255 (CNC Punching)
2. **LaserCut_01**: Bystronic Xpert 1500 (Laser Cutting)
3. **PressBrake_01**: Trumpf TruBend 5130 (Press Brake)
4. **Weld_01**: Fronius TPS 5000 (Welding)
5. **Polish_01**: Walter Helitronic (Polishing)
6. **Paint_01**: Wagner Spraytech (Painting)

### **Injection Moulding**
7. **InjectionMold_01**: Arburg Allrounder 470S (Injection Moulding)
8. **Assembly_01**: Custom Jig & Fixture Setup (Assembly)

## 📊 Data Generation

### **Realistic Industrial Data**
- **30 Days**: Complete month of realistic data
- **1-minute intervals**: High-resolution sensor data
- **Degradation patterns**: Realistic machine wear over time
- **Shift patterns**: Day/evening/night shift efficiency variations
- **Failure modes**: Machine-specific failure patterns

### **Data Schemas**
- **Telemetry**: Temperature, vibration, current, pressure, speed, etc.
- **Events**: Maintenance, breakdowns, quality issues
- **Production Flow**: Queue times, bottlenecks, throughput
- **Andon Alerts**: Real-time alerts and escalation

## 🤖 ML Models

### **Anomaly Detection**
- **Algorithm**: Isolation Forest
- **Purpose**: Detect unexpected sensor behavior
- **Output**: Anomaly scores and binary classification

### **RUL Prediction**
- **Algorithm**: Time series regression
- **Purpose**: Predict remaining useful life
- **Output**: Hours until failure

### **Fault Classification**
- **Algorithm**: Random Forest
- **Purpose**: Classify fault types
- **Output**: Fault type and probability

## 📈 Dashboard Features

### **Overview Tab**
- System-wide KPIs and metrics
- Machine status grid with real-time updates
- Utilization trends by hour
- Active alerts summary

### **Machines Tab**
- Individual machine details
- Sensor trend analysis
- Machine specifications
- Current status and performance

### **Maintenance Tab**
- Maintenance scheduling
- Predictive maintenance insights
- Maintenance cost analysis
- Machine health indicators

### **Alerts Tab**
- Real-time alert management
- Alert prioritization
- Escalation management
- Alert history and trends

### **Flow Tab**
- Production flow visualization
- Bottleneck identification
- Throughput analysis
- Flow optimization recommendations

## 🔧 Configuration

### **Machine Configuration** (`config/machines.yaml`)
```yaml
machines:
  CNC_Punch_01:
    type: "CNC_Punching"
    manufacturer: "Amada"
    model: "Vipros 255"
    sensors:
      temperature:
        range: [20, 80]
        threshold_warning: 70
        threshold_critical: 85
      # ... more sensors
```

### **Production Flow**
- **Sequence**: Machine processing order
- **Batch Sizes**: 50-200 parts per batch
- **Shift Patterns**: Day/evening/night shifts
- **Efficiency**: Shift-based performance variations

## 📊 Data Storage

### **CSV Files** (`data/raw/`)
- `telemetry_data.csv` - Machine sensor data
- `production_flow.csv` - Production flow data
- `events_data.csv` - Maintenance and breakdown events
- `andon_alerts.csv` - Alert and escalation data

### **ML Models** (`artifacts/models/`)
- `anomaly_detector.joblib` - Anomaly detection model
- `rul_predictor.joblib` - RUL prediction model
- `fault_classifier.joblib` - Fault classification model

### **Metadata** (`artifacts/metadata/`)
- `data_generation_metadata.json` - Data generation parameters
- `model_training_metadata.json` - Model training information

## 🎯 Production Benefits

### **For Mechanical Engineers**
- **Realistic Data**: Based on actual industrial machine behavior
- **Degradation Modeling**: Understand machine wear patterns
- **Maintenance Planning**: Predictive maintenance insights
- **Performance Analysis**: Machine efficiency and utilization

### **For Data Scientists**
- **Clean Data**: Pre-generated realistic datasets
- **Consistent Analysis**: Same data for all analysis
- **Performance Metrics**: Realistic KPIs and trends
- **Predictive Models**: Foundation for ML model development

## 🔧 Technical Specifications

### **System Requirements**
- **Python**: 3.8+
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 1GB free space
- **Network**: Local network access

### **Dependencies**
```
streamlit>=1.28.0
pandas>=1.5.0
numpy>=1.24.0
plotly>=5.15.0
scikit-learn>=1.3.0
PyYAML>=6.0
```

## 🚀 Usage Examples

### **Generate Data**
```python
from src.data_generator.main_data_generator import MainDataGenerator

generator = MainDataGenerator()
data = generator.generate_all_data(days=30)
```

### **Train Models**
```python
from src.ml_models.predictive_models import PredictiveMaintenanceModels

models = PredictiveMaintenanceModels()
models.train_all_models(telemetry_data, events_data)
```

### **Predict Health**
```python
health_scores = models.get_machine_health_scores(telemetry_data)
```

## 🔧 Troubleshooting

### **Common Issues**
1. **No Data**: Run data generation script
2. **Model Errors**: Ensure models are trained
3. **Import Errors**: Check Python path and dependencies
4. **Performance**: Ensure sufficient RAM

### **System Health**
- Database connectivity
- Data integrity
- Model availability
- Alert functionality

## 📈 Future Enhancements

### **Planned Features**
- **Real-time Data**: Live sensor data integration
- **Advanced Analytics**: Deep learning models
- **Mobile Access**: Mobile-friendly interface
- **API Integration**: External system integration

### **Scalability**
- **Multi-site**: Multiple manufacturing sites
- **Cloud Deployment**: Cloud-based hosting
- **Enterprise**: Enterprise-grade features
- **Integration**: ERP/MES system integration

## 🏆 Production Ready

This modular system is designed for production use in real industrial environments:

- ✅ **Realistic Data**: Based on actual industrial patterns
- ✅ **Production Tested**: Optimized for real-world use
- ✅ **Modular Design**: Easy to maintain and extend
- ✅ **Industrial Focus**: Designed by engineers for engineers

## 📞 Support

For technical support or questions:
- **Documentation**: Comprehensive system documentation
- **Troubleshooting**: Built-in error handling
- **Performance**: Optimized for production use
- **Reliability**: Tested in industrial environments

---

**Built by Mechanical Engineers & Data Scientists for Industrial Excellence** 🏭✨