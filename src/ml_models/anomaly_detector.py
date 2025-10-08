"""
Anomaly Detector
Isolation Forest-based anomaly detection for industrial machines
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import os

class AnomalyDetector:
    """
    Anomaly detection using Isolation Forest for industrial machines
    """
    
    def __init__(self, contamination=0.1):
        """Initialize anomaly detector"""
        self.contamination = contamination
        self.model = IsolationForest(
            contamination=contamination,
            random_state=42,
            n_estimators=100
        )
        self.scaler = StandardScaler()
        self.is_fitted = False
        
    def fit(self, data):
        """Train the anomaly detection model"""
        print("Training anomaly detection model...")
        
        # Select relevant features
        feature_columns = self._get_feature_columns(data)
        X = data[feature_columns].fillna(0)
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train model
        self.model.fit(X_scaled)
        self.is_fitted = True
        
        print(f"Anomaly detection model trained on {len(data)} samples")
        print(f"Features used: {len(feature_columns)}")
        
        return self
    
    def predict(self, data):
        """Predict anomalies in data"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")
        
        feature_columns = self._get_feature_columns(data)
        X = data[feature_columns].fillna(0)
        X_scaled = self.scaler.transform(X)
        
        # Predict anomalies (-1 for anomaly, 1 for normal)
        predictions = self.model.predict(X_scaled)
        anomaly_scores = self.model.decision_function(X_scaled)
        
        return predictions, anomaly_scores
    
    def _get_feature_columns(self, data):
        """Get relevant feature columns for anomaly detection"""
        sensor_columns = [
            'temperature', 'vibration', 'current', 'rpm', 'hydraulic_pressure',
            'bending_force', 'tool_wear', 'coolant_flow', 'arc_voltage',
            'injection_pressure', 'clamping_force', 'throughput'
        ]
        
        # Filter to existing columns
        available_columns = [col for col in sensor_columns if col in data.columns]
        
        return available_columns
    
    def save_model(self, filepath="artifacts/models/anomaly_detector.joblib"):
        """Save the trained model"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before saving")
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'contamination': self.contamination
        }
        
        joblib.dump(model_data, filepath)
        print(f"Anomaly detection model saved to {filepath}")
    
    def load_model(self, filepath="artifacts/models/anomaly_detector.joblib"):
        """Load a trained model"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found: {filepath}")
        
        model_data = joblib.load(filepath)
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.contamination = model_data['contamination']
        self.is_fitted = True
        
        print(f"Anomaly detection model loaded from {filepath}")
        return self
    
    def get_anomaly_summary(self, data):
        """Get summary of anomalies in data"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before analysis")
        
        predictions, scores = self.predict(data)
        
        anomaly_count = np.sum(predictions == -1)
        normal_count = np.sum(predictions == 1)
        anomaly_rate = anomaly_count / len(predictions)
        
        summary = {
            'total_samples': len(data),
            'anomalies': anomaly_count,
            'normal': normal_count,
            'anomaly_rate': anomaly_rate,
            'avg_anomaly_score': np.mean(scores),
            'min_anomaly_score': np.min(scores),
            'max_anomaly_score': np.max(scores)
        }
        
        return summary
