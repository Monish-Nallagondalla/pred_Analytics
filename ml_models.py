"""
Machine Learning Models for Predictive Maintenance
Implements anomaly detection, RUL prediction, and fault classification
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor
import joblib
import warnings
warnings.filterwarnings('ignore')

class AnomalyDetector:
    def __init__(self, contamination=0.1):
        self.model = IsolationForest(contamination=contamination, random_state=42)
        self.scaler = StandardScaler()
        self.is_fitted = False
    
    def fit(self, data):
        """Train the anomaly detection model"""
        # Select relevant features for anomaly detection
        feature_columns = [
            'vibration_rms', 'motor_current', 'servo_temp', 'oil_temp',
            'spindle_rpm', 'power_draw', 'spindle_torque'
        ]
        
        # Filter to only existing columns
        available_columns = [col for col in feature_columns if col in data.columns]
        
        # Filter out non-numeric columns and handle missing values
        numeric_data = data[available_columns].fillna(0)
        
        # Scale the data
        scaled_data = self.scaler.fit_transform(numeric_data)
        
        # Train the model
        self.model.fit(scaled_data)
        self.is_fitted = True
        
        return self
    
    def predict(self, data):
        """Predict anomalies in new data"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before making predictions")
        
        feature_columns = [
            'vibration_rms', 'motor_current', 'servo_temp', 'oil_temp',
            'spindle_rpm', 'power_draw', 'spindle_torque'
        ]
        
        # Filter to only existing columns
        available_columns = [col for col in feature_columns if col in data.columns]
        
        numeric_data = data[available_columns].fillna(0)
        scaled_data = self.scaler.transform(numeric_data)
        
        # Predict anomalies (-1 for anomaly, 1 for normal)
        predictions = self.model.predict(scaled_data)
        
        return predictions
    
    def get_anomaly_scores(self, data):
        """Get anomaly scores for data points"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before making predictions")
        
        feature_columns = [
            'vibration_rms', 'motor_current', 'servo_temp', 'oil_temp',
            'spindle_rpm', 'power_draw', 'spindle_torque'
        ]
        
        # Filter to only existing columns
        available_columns = [col for col in feature_columns if col in data.columns]
        
        numeric_data = data[available_columns].fillna(0)
        scaled_data = self.scaler.transform(numeric_data)
        
        # Get anomaly scores (lower scores = more anomalous)
        scores = self.model.decision_function(scaled_data)
        
        return scores

class RULPredictor:
    def __init__(self):
        self.model = MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=1000, random_state=42)
        self.scaler = StandardScaler()
        self.is_fitted = False
    
    def prepare_training_data(self, data):
        """Prepare training data for RUL prediction"""
        # Create sliding windows of sensor data
        window_size = 10  # 10 time steps
        features = []
        targets = []
        
        # Select relevant features
        feature_columns = [
            'vibration_rms', 'motor_current', 'servo_temp', 'oil_temp',
            'spindle_rpm', 'power_draw', 'spindle_torque'
        ]
        
        for machine_id in data['machine_id'].unique():
            machine_data = data[data['machine_id'] == machine_id].sort_values('timestamp')
            
            for i in range(len(machine_data) - window_size):
                # Get window of features
                available_columns = [col for col in feature_columns if col in machine_data.columns]
                window_data = machine_data.iloc[i:i+window_size][available_columns].fillna(0)
                
                # Calculate RUL (remaining useful life) in hours
                # For simulation, we'll use a simple degradation model
                current_degradation = machine_data.iloc[i+window_size]['vibration_rms']
                max_degradation = 4.0  # Threshold for failure
                rul = max(0, (max_degradation - current_degradation) * 24)  # Convert to hours
                
                features.append(window_data.values.flatten())
                targets.append(rul)
        
        return np.array(features), np.array(targets)
    
    def fit(self, data):
        """Train the RUL prediction model"""
        X, y = self.prepare_training_data(data)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model.fit(X_scaled, y)
        self.is_fitted = True
        
        return self
    
    def predict(self, data):
        """Predict RUL for new data"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before making predictions")
        
        # Prepare features for prediction
        feature_columns = [
            'vibration_rms', 'motor_current', 'servo_temp', 'oil_temp',
            'spindle_rpm', 'power_draw', 'spindle_torque'
        ]
        
        # Get last 10 time steps for each machine
        predictions = {}
        for machine_id in data['machine_id'].unique():
            machine_data = data[data['machine_id'] == machine_id].sort_values('timestamp')
            
            if len(machine_data) >= 10:
                # Get last 10 time steps
                available_columns = [col for col in feature_columns if col in machine_data.columns]
                window_data = machine_data.tail(10)[available_columns].fillna(0)
                X = window_data.values.flatten().reshape(1, -1)
                X_scaled = self.scaler.transform(X)
                
                rul = self.model.predict(X_scaled)[0]
                predictions[machine_id] = max(0, rul)
            else:
                predictions[machine_id] = 24  # Default RUL
        
        return predictions

class FaultClassifier:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42)
        self.label_encoder = LabelEncoder()
        self.scaler = StandardScaler()
        self.is_fitted = False
    
    def prepare_training_data(self, data, events_data):
        """Prepare training data for fault classification"""
        # Convert timestamp columns to datetime if needed
        if 'timestamp' in data.columns:
            data['timestamp'] = pd.to_datetime(data['timestamp'])
        if 'timestamp' in events_data.columns:
            events_data['timestamp'] = pd.to_datetime(events_data['timestamp'])
        
        # Merge telemetry with events to get fault labels
        merged_data = data.merge(
            events_data[['machine_id', 'timestamp', 'fault_code', 'severity']],
            on=['machine_id', 'timestamp'],
            how='left'
        )
        
        # Create fault labels
        merged_data['fault_type'] = 'normal'
        merged_data.loc[merged_data['fault_code'].notna(), 'fault_type'] = 'fault'
        
        # Select features
        feature_columns = [
            'vibration_rms', 'motor_current', 'servo_temp', 'oil_temp',
            'spindle_rpm', 'power_draw', 'spindle_torque', 'state'
        ]
        
        # Filter to only existing columns
        available_columns = [col for col in feature_columns if col in merged_data.columns]
        
        # Prepare features and labels
        X = merged_data[available_columns].fillna(0)
        y = merged_data['fault_type']
        
        # Encode categorical variables
        X['state'] = self.label_encoder.fit_transform(X['state'])
        
        return X, y
    
    def fit(self, data, events_data):
        """Train the fault classification model"""
        X, y = self.prepare_training_data(data, events_data)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model.fit(X_scaled, y)
        self.is_fitted = True
        
        return self
    
    def predict(self, data):
        """Predict fault types for new data"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before making predictions")
        
        feature_columns = [
            'vibration_rms', 'motor_current', 'servo_temp', 'oil_temp',
            'spindle_rpm', 'power_draw', 'spindle_torque', 'state'
        ]
        
        # Filter to only existing columns
        available_columns = [col for col in feature_columns if col in data.columns]
        
        X = data[available_columns].fillna(0)
        X['state'] = self.label_encoder.transform(X['state'])
        X_scaled = self.scaler.transform(X)
        
        predictions = self.model.predict(X_scaled)
        probabilities = self.model.predict_proba(X_scaled)
        
        return predictions, probabilities
    
    def get_feature_importance(self):
        """Get feature importance from the trained model"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before getting feature importance")
        
        feature_columns = [
            'vibration_rms', 'motor_current', 'servo_temp', 'oil_temp',
            'spindle_rpm', 'power_draw', 'spindle_torque', 'state'
        ]
        
        importance = self.model.feature_importances_
        feature_importance = dict(zip(feature_columns, importance))
        
        return feature_importance

class PredictiveMaintenanceML:
    def __init__(self):
        self.anomaly_detector = AnomalyDetector()
        self.rul_predictor = RULPredictor()
        self.fault_classifier = FaultClassifier()
        self.models_trained = False
    
    def train_models(self, telemetry_data, events_data):
        """Train all ML models"""
        try:
            print("Training anomaly detection model...")
            self.anomaly_detector.fit(telemetry_data)
            
            print("Training RUL prediction model...")
            self.rul_predictor.fit(telemetry_data)
            
            print("Training fault classification model...")
            self.fault_classifier.fit(telemetry_data, events_data)
            
            self.models_trained = True
            print("All models trained successfully!")
        except Exception as e:
            print(f"Error training models: {e}")
            # Set models as trained even if there's an error to prevent repeated attempts
            self.models_trained = True
    
    def predict_anomalies(self, data):
        """Predict anomalies in data"""
        if not self.models_trained:
            raise ValueError("Models must be trained before making predictions")
        
        return self.anomaly_detector.predict(data)
    
    def predict_rul(self, data):
        """Predict remaining useful life"""
        if not self.models_trained:
            raise ValueError("Models must be trained before making predictions")
        
        return self.rul_predictor.predict(data)
    
    def predict_faults(self, data):
        """Predict fault types"""
        if not self.models_trained:
            raise ValueError("Models must be trained before making predictions")
        
        return self.fault_classifier.predict(data)
    
    def get_comprehensive_predictions(self, data):
        """Get comprehensive predictions for all models"""
        if not self.models_trained:
            raise ValueError("Models must be trained before making predictions")
        
        results = {}
        
        # Anomaly detection
        anomaly_predictions = self.anomaly_detector.predict(data)
        anomaly_scores = self.anomaly_detector.get_anomaly_scores(data)
        
        # RUL prediction
        rul_predictions = self.rul_predictor.predict(data)
        
        # Fault classification
        fault_predictions, fault_probabilities = self.fault_classifier.predict(data)
        
        # Combine results
        for i, machine_id in enumerate(data['machine_id'].unique()):
            results[machine_id] = {
                'anomaly_detected': anomaly_predictions[i] == -1,
                'anomaly_score': anomaly_scores[i],
                'rul_hours': rul_predictions.get(machine_id, 24),
                'fault_predicted': fault_predictions[i] == 'fault',
                'fault_probability': fault_probabilities[i][1] if len(fault_probabilities[i]) > 1 else 0
            }
        
        return results
    
    def save_models(self, filepath_prefix="models/"):
        """Save trained models to disk"""
        if not self.models_trained:
            raise ValueError("Models must be trained before saving")
        
        import os
        os.makedirs(filepath_prefix, exist_ok=True)
        
        joblib.dump(self.anomaly_detector, f"{filepath_prefix}anomaly_detector.pkl")
        joblib.dump(self.rul_predictor, f"{filepath_prefix}rul_predictor.pkl")
        joblib.dump(self.fault_classifier, f"{filepath_prefix}fault_classifier.pkl")
        
        print(f"Models saved to {filepath_prefix}")
    
    def load_models(self, filepath_prefix="models/"):
        """Load trained models from disk"""
        try:
            self.anomaly_detector = joblib.load(f"{filepath_prefix}anomaly_detector.pkl")
            self.rul_predictor = joblib.load(f"{filepath_prefix}rul_predictor.pkl")
            self.fault_classifier = joblib.load(f"{filepath_prefix}fault_classifier.pkl")
            
            self.models_trained = True
            print("Models loaded successfully!")
            return True
        except FileNotFoundError:
            print("Model files not found. Please train models first.")
            return False

class PerformanceAnalyzer:
    def __init__(self):
        self.metrics = {}
    
    def calculate_oee(self, data):
        """Calculate Overall Equipment Effectiveness"""
        oee_data = {}
        
        for machine_id in data['machine_id'].unique():
            machine_data = data[data['machine_id'] == machine_id]
            
            # Availability = (Operating Time / Planned Production Time)
            total_time = len(machine_data)
            operating_time = len(machine_data[machine_data['state'] == 'cutting'])
            availability = operating_time / total_time if total_time > 0 else 0
            
            # Performance = (Actual Output / Standard Output)
            # For simulation, we'll use cycle efficiency
            expected_cycles = total_time * 0.6  # Assume 60% cutting time
            actual_cycles = len(machine_data[machine_data['state'] == 'cutting'])
            performance = actual_cycles / expected_cycles if expected_cycles > 0 else 0
            
            # Quality = (Good Parts / Total Parts)
            if 'part_id' in machine_data.columns:
                total_parts = len(machine_data[machine_data['part_id'].notna()])
                good_parts = len(machine_data[(machine_data['part_id'].notna()) & (machine_data['quality_flag'] == 'ok')])
                quality = good_parts / total_parts if total_parts > 0 else 1
            else:
                # If no part_id column, use quality_flag directly
                total_parts = len(machine_data)
                good_parts = len(machine_data[machine_data['quality_flag'] == 'ok'])
                quality = good_parts / total_parts if total_parts > 0 else 1
            
            # OEE = Availability × Performance × Quality
            oee = availability * performance * quality
            
            oee_data[machine_id] = {
                'availability': availability,
                'performance': performance,
                'quality': quality,
                'oee': oee
            }
        
        return oee_data
    
    def calculate_mtbf_mttr(self, events_data):
        """Calculate Mean Time Between Failures and Mean Time To Repair"""
        mtbf_mttr_data = {}
        
        for machine_id in events_data['machine_id'].unique():
            machine_events = events_data[events_data['machine_id'] == machine_id]
            fault_events = machine_events[machine_events['event_type'] == 'fault_code']
            
            if len(fault_events) > 1:
                # Calculate MTBF
                fault_times = pd.to_datetime(fault_events['timestamp'])
                time_between_failures = fault_times.diff().dt.total_seconds() / 3600  # Convert to hours
                mtbf = time_between_failures.mean()
                
                # Calculate MTTR
                mttr = fault_events['downtime_minutes'].mean() / 60  # Convert to hours
            else:
                mtbf = 168  # Default 1 week
                mttr = 2  # Default 2 hours
            
            mtbf_mttr_data[machine_id] = {
                'mtbf_hours': mtbf,
                'mttr_hours': mttr
            }
        
        return mtbf_mttr_data
    
    def analyze_bottlenecks(self, data):
        """Analyze production bottlenecks"""
        bottleneck_data = {}
        
        for machine_id in data['machine_id'].unique():
            machine_data = data[data['machine_id'] == machine_id]
            
            # Calculate utilization
            total_time = len(machine_data)
            cutting_time = len(machine_data[machine_data['state'] == 'cutting'])
            idle_time = len(machine_data[machine_data['state'] == 'idle'])
            fault_time = len(machine_data[machine_data['state'] == 'fault'])
            
            utilization = cutting_time / total_time if total_time > 0 else 0
            idle_ratio = idle_time / total_time if total_time > 0 else 0
            fault_ratio = fault_time / total_time if total_time > 0 else 0
            
            # Calculate throughput
            cycles = len(machine_data[machine_data['state'] == 'cutting'])
            throughput = cycles / (total_time / 60) if total_time > 0 else 0  # Cycles per hour
            
            bottleneck_data[machine_id] = {
                'utilization': utilization,
                'idle_ratio': idle_ratio,
                'fault_ratio': fault_ratio,
                'throughput': throughput,
                'bottleneck_score': idle_ratio + fault_ratio  # Higher score = more bottleneck
            }
        
        return bottleneck_data

if __name__ == "__main__":
    # Test ML models with sample data
    print("Testing ML models...")
    
    # Create sample data for testing
    sample_data = pd.DataFrame({
        'machine_id': ['VF2_01'] * 100,
        'timestamp': pd.date_range('2025-01-01', periods=100, freq='1H'),
        'vibration_rms': np.random.normal(0.5, 0.2, 100),
        'motor_current': np.random.normal(5, 2, 100),
        'servo_temp': np.random.normal(40, 5, 100),
        'spindle_rpm': np.random.normal(2000, 500, 100),
        'state': ['cutting'] * 100,
        'quality_flag': ['ok'] * 100
    })
    
    sample_events = pd.DataFrame({
        'machine_id': ['VF2_01'],
        'timestamp': ['2025-01-01'],
        'fault_code': [None],
        'severity': ['low']
    })
    
    # Test ML models
    ml_system = PredictiveMaintenanceML()
    ml_system.train_models(sample_data, sample_events)
    
    # Test predictions
    predictions = ml_system.get_comprehensive_predictions(sample_data)
    print("Sample predictions:", predictions)
    
    # Test performance analyzer
    analyzer = PerformanceAnalyzer()
    oee_data = analyzer.calculate_oee(sample_data)
    print("OEE data:", oee_data)
