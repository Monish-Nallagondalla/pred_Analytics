# JR Manufacturing Smart Dashboard - Deployment Guide

## 🚀 Quick Start

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the application
streamlit run main.py
```

### Streamlit Cloud Deployment
1. **Upload to GitHub**: Push your code to a GitHub repository
2. **Connect to Streamlit Cloud**: Link your repository
3. **Set Main File**: Set `main.py` as the main file
4. **Install Dependencies**: Streamlit Cloud will automatically install from `requirements.txt`

## 🔧 Troubleshooting Import Errors

### Common Issues & Solutions

#### 1. ModuleNotFoundError: 'plotly'
**Solution**: Install plotly
```bash
pip install plotly>=5.15.0
```

#### 2. ModuleNotFoundError: 'dashboard'
**Solution**: Ensure file structure is correct
```
project/
├── main.py
├── requirements.txt
└── src/
    └── dashboard/
        └── industrial_dashboard.py
```

#### 3. ImportError: No module named 'sklearn'
**Solution**: Install scikit-learn
```bash
pip install scikit-learn>=1.3.0
```

#### 4. YAML Import Error
**Solution**: Install PyYAML
```bash
pip install PyYAML>=6.0
```

## 📁 File Structure Requirements

Ensure your project has this exact structure:
```
pred_Analytics/
├── main.py                          # Main entry point
├── requirements.txt                  # Dependencies
├── config/
│   └── machines.yaml                # Machine configuration
├── src/
│   ├── dashboard/
│   │   └── industrial_dashboard.py  # Main dashboard
│   ├── data_generator/
│   │   ├── __init__.py
│   │   ├── simple_main_generator.py
│   │   └── schema_compliant_generator.py
│   ├── ml_models/
│   │   ├── __init__.py
│   │   ├── predictive_models.py
│   │   ├── anomaly_detector.py
│   │   ├── rul_predictor.py
│   │   └── fault_classifier.py
│   ├── andon_system/
│   │   └── andon_manager.py
│   └── flow_optimization/
│       └── machine_flow_optimizer.py
└── data/                            # Generated data (created at runtime)
    └── raw/
```

## 🐍 Python Version Requirements

- **Python 3.8+** required
- **Python 3.9+** recommended for best compatibility

## 📦 Dependencies

### Core Dependencies
- `streamlit>=1.28.0` - Web framework
- `pandas>=1.5.0` - Data manipulation
- `numpy>=1.24.0` - Numerical computing
- `plotly>=5.15.0` - Interactive visualizations
- `scikit-learn>=1.3.0` - Machine learning
- `joblib>=1.3.0` - Model persistence
- `PyYAML>=6.0` - Configuration files

### Additional Dependencies
- `openpyxl>=3.1.0` - Excel file support
- `kaleido>=0.2.1` - Static image export
- `python-dateutil>=2.8.0` - Date utilities
- `pytz>=2023.3` - Timezone support

## 🔍 Debugging Steps

### 1. Check Python Version
```bash
python --version
# Should be 3.8 or higher
```

### 2. Check Dependencies
```bash
pip list | grep -E "(streamlit|pandas|plotly|scikit-learn)"
```

### 3. Test Imports
```python
# Test in Python console
import streamlit as st
import pandas as pd
import plotly.express as px
import sklearn
import yaml
```

### 4. Check File Structure
```bash
# Ensure all files exist
ls -la src/dashboard/industrial_dashboard.py
ls -la config/machines.yaml
```

## 🚀 Deployment Checklist

- [ ] All dependencies in `requirements.txt`
- [ ] Correct file structure
- [ ] Python 3.8+ installed
- [ ] All `__init__.py` files present
- [ ] No syntax errors in Python files
- [ ] Test locally before deployment

## 📞 Support

If you encounter issues:

1. **Check the logs** for specific error messages
2. **Verify file structure** matches the requirements
3. **Test dependencies** individually
4. **Check Python version** compatibility
5. **Review import paths** in the code

## 🔧 Common Fixes

### Fix 1: Missing __init__.py files
```bash
# Create missing __init__.py files
touch src/__init__.py
touch src/dashboard/__init__.py
touch src/data_generator/__init__.py
touch src/ml_models/__init__.py
```

### Fix 2: Path issues
```python
# Add to main.py if needed
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'src'))
```

### Fix 3: Dependency conflicts
```bash
# Create fresh environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

This guide should help resolve most deployment and import issues!
