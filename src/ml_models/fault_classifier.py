"""
Fault Classifier
Multi-class fault classification using Random Forest for industrial machines
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import os

class FaultClassifier:
    """
    Fault classification using Random Forest for industrial machines
    """
    
    def __init__(self, n_estimators=100, random_state=42):
        """Initialize fault classifier"""
        self.n_estimators = n_estimators
        self.random_state = random_state
        self.model = RandomForestClassifier(
            n_estimators=n_estimators,
            random_state=random_state,
            max_depth=10,
            min_samples_split=5
        )
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.is_fitted = False
        
    def fit(self, data):
        """Train the fault classification model"""
        print("Training fault classification model...")
        
        # Prepare features and labels
        X, y = self._prepare_data(data)
        
        if len(X) == 0:
            print("⚠️ No valid data found for fault classification training")
            return self
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Encode labels
        y_encoded = self.label_encoder.fit_transform(y)
        
        # Train model
        self.model.fit(X_scaled, y_encoded)
        self.is_fitted = True
        
        print(f"Fault classification model trained on {len(X)} samples")
        print(f"Features used: {X.shape[1]}")
        print(f"Classes: {len(self.label_encoder.classes_)}")
        
        return self
    
    def predict(self, data):
        """Predict fault types for data"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")
        
        X, _ = self._prepare_data(data)
        
        if len(X) == 0:
            return np.array([])
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        # Predict fault types
        predictions_encoded = self.model.predict(X_scaled)
        predictions = self.label_encoder.inverse_transform(predictions_encoded)
        
        # Get prediction probabilities
        probabilities = self.model.predict_proba(X_scaled)
        
        return predictions, probabilities
    
    def _prepare_data(self, data):
        """Prepare features and labels for training"""
        # Get feature columns
        feature_columns = self._get_feature_columns(data)
        X = data[feature_columns].fillna(0)
        
        # Create fault labels based on machine state and sensor values
        y = self._create_fault_labels(data)
        
        return X, y
    
    def _get_feature_columns(self, data):
        """Get relevant feature columns for fault classification"""
        sensor_columns = [
            'temperature', 'vibration', 'current', 'rpm', 'hydraulic_pressure',
            'bending_force', 'tool_wear', 'coolant_flow', 'arc_voltage',
            'injection_pressure', 'clamping_force', 'throughput'
        ]
        
        # Filter to existing columns
        available_columns = [col for col in sensor_columns if col in data.columns]
        
        return available_columns
    
    def _create_fault_labels(self, data):
        """Create fault labels based on machine state and sensor values"""
        fault_labels = []
        
        for _, row in data.iterrows():
            # Use status_flag column from new schema, fallback to state for legacy data
            status_col = 'status_flag' if 'status_flag' in data.columns else 'state'
            
            if row[status_col] == 'Fault':
                # Determine fault type based on sensor values
                fault_type = self._determine_fault_type(row)
                fault_labels.append(fault_type)
            elif row[status_col] == 'Anomaly':
                fault_labels.append('anomaly_detected')
            else:
                fault_labels.append('normal')
        
        return fault_labels
    
    def _determine_fault_type(self, row):
        """Determine fault type based on sensor values"""
        fault_types = []
        
        # Temperature-based faults
        if 'temperature' in row and row['temperature'] > 80:
            fault_types.append('overheating')
        
        # Vibration-based faults
        if 'vibration' in row and row['vibration'] > 3.0:
            fault_types.append('vibration_anomaly')
        
        # Current-based faults
        if 'current' in row and row['current'] > 15:
            fault_types.append('electrical_fault')
        
        # Tool wear faults
        if 'tool_wear' in row and row['tool_wear'] > 80:
            fault_types.append('tool_wear')
        
        # Hydraulic faults
        if 'hydraulic_pressure' in row and row['hydraulic_pressure'] > 250:
            fault_types.append('hydraulic_fault')
        
        # Return the first fault type found, or 'general_fault'
        return fault_types[0] if fault_types else 'general_fault'
    
    def save_model(self, filepath="artifacts/models/fault_classifier.joblib"):
        """Save the trained model"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before saving")
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'label_encoder': self.label_encoder,
            'n_estimators': self.n_estimators,
            'random_state': self.random_state
        }
        
        joblib.dump(model_data, filepath)
        print(f"Fault classification model saved to {filepath}")
    
    def load_model(self, filepath="artifacts/models/fault_classifier.joblib"):
        """Load a trained model"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found: {filepath}")
        
        model_data = joblib.load(filepath)
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.label_encoder = model_data['label_encoder']
        self.n_estimators = model_data['n_estimators']
        self.random_state = model_data['random_state']
        self.is_fitted = True
        
        print(f"Fault classification model loaded from {filepath}")
        return self
    
    def get_classification_summary(self, data):
        """Get summary of fault classifications"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before analysis")
        
        predictions, probabilities = self.predict(data)
        
        if len(predictions) == 0:
            return {'total_predictions': 0}
        
        # Count fault types
        fault_counts = pd.Series(predictions).value_counts()
        
        summary = {
            'total_predictions': len(predictions),
            'fault_types': fault_counts.to_dict(),
            'avg_confidence': np.mean(np.max(probabilities, axis=1)),
            'high_confidence_predictions': np.sum(np.max(probabilities, axis=1) > 0.8)
        }
        
        return summary
