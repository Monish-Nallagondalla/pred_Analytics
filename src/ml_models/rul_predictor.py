"""
RUL Predictor
Remaining Useful Life prediction using MLP (Multi-Layer Perceptron) for industrial machines
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, mean_squared_error
import joblib
import os

class RULPredictor:
    """
    RUL prediction using time series regression
    """
    
    def __init__(self, sequence_length=60, prediction_horizon=24):
        """Initialize RUL predictor"""
        self.sequence_length = sequence_length
        self.prediction_horizon = prediction_horizon
        self.scaler = StandardScaler()
        self.is_fitted = False
        
    def fit(self, data):
        """Train the RUL prediction model"""
        print("Training RUL prediction model...")
        
        # Prepare time series data
        X, y = self._prepare_sequences(data)
        
        if len(X) == 0:
            print("⚠️ No valid sequences found for RUL training")
            return self
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X.reshape(-1, X.shape[-1]))
        X_scaled = X_scaled.reshape(X.shape)
        
        # MLP (Multi-Layer Perceptron) for RUL prediction as per project plan
        from sklearn.neural_network import MLPRegressor
        self.model = MLPRegressor(
            hidden_layer_sizes=(100, 50),
            activation='relu',
            solver='adam',
            max_iter=1000,
            random_state=42
        )
        
        # Flatten sequences for training
        X_flat = X_scaled.reshape(-1, X_scaled.shape[-1])
        y_flat = y.flatten()
        
        # Ensure X and y have the same length
        min_length = min(len(X_flat), len(y_flat))
        X_flat = X_flat[:min_length]
        y_flat = y_flat[:min_length]
        
        # Train model
        self.model.fit(X_flat, y_flat)
        self.is_fitted = True
        
        print(f"RUL prediction model trained on {len(X)} sequences")
        print(f"Sequence length: {self.sequence_length}")
        print(f"Prediction horizon: {self.prediction_horizon} hours")
        
        return self
    
    def predict(self, data):
        """Predict RUL for data"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before prediction")
        
        X, _ = self._prepare_sequences(data)
        
        if len(X) == 0:
            return np.array([])
        
        # Scale features
        X_scaled = self.scaler.transform(X.reshape(-1, X.shape[-1]))
        X_scaled = X_scaled.reshape(X.shape)
        
        # Predict RUL
        X_flat = X_scaled.reshape(-1, X_scaled.shape[-1])
        predictions = self.model.predict(X_flat)
        
        return predictions.reshape(-1, 1)
    
    def _prepare_sequences(self, data):
        """Prepare time series sequences for RUL prediction"""
        # Group by machine
        sequences = []
        targets = []
        
        for machine_id in data['machine_id'].unique():
            machine_data = data[data['machine_id'] == machine_id].sort_values('timestamp')
            
            if len(machine_data) < self.sequence_length + self.prediction_horizon:
                continue
            
            # Get feature columns
            feature_columns = self._get_feature_columns(machine_data)
            X_machine = machine_data[feature_columns].fillna(0).values
            
            # Create sequences with proper bounds checking
            max_sequences = len(X_machine) - self.sequence_length - self.prediction_horizon
            for i in range(max(0, max_sequences)):
                if i + self.sequence_length < len(X_machine):
                    sequence = X_machine[i:i + self.sequence_length]
                    target = self._calculate_rul(machine_data.iloc[i + self.sequence_length:])
                    
                    sequences.append(sequence)
                    targets.append(target)
        
        if len(sequences) == 0:
            return np.array([]), np.array([])
        
        return np.array(sequences), np.array(targets)
    
    def _get_feature_columns(self, data):
        """Get relevant feature columns for RUL prediction"""
        sensor_columns = [
            'temperature', 'vibration', 'current', 'rpm', 'hydraulic_pressure',
            'bending_force', 'tool_wear', 'coolant_flow', 'arc_voltage',
            'injection_pressure', 'clamping_force', 'throughput'
        ]
        
        # Filter to existing columns
        available_columns = [col for col in sensor_columns if col in data.columns]
        
        return available_columns
    
    def _calculate_rul(self, future_data):
        """Calculate RUL based on future data"""
        # Simple RUL calculation based on degradation
        if len(future_data) == 0:
            return 0
        
        # Calculate degradation rate
        degradation_rate = 0.001  # Base degradation rate per hour
        
        # Calculate RUL (simplified)
        rul = max(0, 500 - len(future_data) * degradation_rate)
        
        return rul
    
    def save_model(self, filepath="artifacts/models/rul_predictor.joblib"):
        """Save the trained model"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before saving")
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        model_data = {
            'model': self.model,
            'scaler': self.scaler,
            'sequence_length': self.sequence_length,
            'prediction_horizon': self.prediction_horizon
        }
        
        joblib.dump(model_data, filepath)
        print(f"RUL prediction model saved to {filepath}")
    
    def load_model(self, filepath="artifacts/models/rul_predictor.joblib"):
        """Load a trained model"""
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Model file not found: {filepath}")
        
        model_data = joblib.load(filepath)
        self.model = model_data['model']
        self.scaler = model_data['scaler']
        self.sequence_length = model_data['sequence_length']
        self.prediction_horizon = model_data['prediction_horizon']
        self.is_fitted = True
        
        print(f"RUL prediction model loaded from {filepath}")
        return self
    
    def get_rul_summary(self, data):
        """Get summary of RUL predictions"""
        if not self.is_fitted:
            raise ValueError("Model must be fitted before analysis")
        
        predictions = self.predict(data)
        
        if len(predictions) == 0:
            return {'total_predictions': 0}
        
        summary = {
            'total_predictions': len(predictions),
            'avg_rul': np.mean(predictions),
            'min_rul': np.min(predictions),
            'max_rul': np.max(predictions),
            'std_rul': np.std(predictions),
            'critical_machines': np.sum(predictions < 50),  # RUL < 50 hours
            'warning_machines': np.sum((predictions >= 50) & (predictions < 100))  # 50-100 hours
        }
        
        return summary
