"""
Predictive Maintenance Models
Main orchestrator for all ML models in the JR Manufacturing system
"""

import pandas as pd
import numpy as np
import os
import json
from datetime import datetime
from .anomaly_detector import AnomalyDetector
from .rul_predictor import RULPredictor
from .fault_classifier import FaultClassifier

class PredictiveMaintenanceModels:
    """
    Main orchestrator for all predictive maintenance models
    """
    
    def __init__(self):
        """Initialize the predictive maintenance system"""
        self.anomaly_detector = AnomalyDetector()
        self.rul_predictor = RULPredictor()
        self.fault_classifier = FaultClassifier()
        
        self.models_trained = False
        
    def train_all_models(self, telemetry_data, events_data):
        """
        Train all predictive maintenance models
        """
        print("=" * 60)
        print("TRAINING PREDICTIVE MAINTENANCE MODELS")
        print("=" * 60)
        
        # Train anomaly detection model
        print("\nTraining anomaly detection model...")
        self.anomaly_detector.fit(telemetry_data)
        self.anomaly_detector.save_model()
        
        # Train RUL prediction model
        print("\nTraining RUL prediction model...")
        self.rul_predictor.fit(telemetry_data)
        self.rul_predictor.save_model()
        
        # Train fault classification model
        print("\nTraining fault classification model...")
        self.fault_classifier.fit(telemetry_data)
        self.fault_classifier.save_model()
        
        self.models_trained = True
        
        # Save training metadata
        self._save_training_metadata(telemetry_data, events_data)
        
        print("\nAll models trained successfully!")
        print("Models saved to artifacts/models/")
        
        return True
    
    def load_all_models(self):
        """Load all trained models"""
        try:
            print("Loading predictive maintenance models...")
            
            self.anomaly_detector.load_model()
            self.rul_predictor.load_model()
            self.fault_classifier.load_model()
            
            self.models_trained = True
            print("All models loaded successfully!")
            
            return True
            
        except Exception as e:
            print(f"Error loading models: {e}")
            return False
    
    def predict_anomalies(self, data):
        """Predict anomalies in data"""
        if not self.models_trained:
            raise ValueError("Models must be trained before prediction")
        
        predictions, scores = self.anomaly_detector.predict(data)
        return predictions, scores
    
    def predict_rul(self, data):
        """Predict remaining useful life"""
        if not self.models_trained:
            raise ValueError("Models must be trained before prediction")
        
        predictions = self.rul_predictor.predict(data)
        return predictions
    
    def predict_faults(self, data):
        """Predict fault types"""
        if not self.models_trained:
            raise ValueError("Models must be trained before prediction")
        
        predictions, probabilities = self.fault_classifier.predict(data)
        return predictions, probabilities
    
    def get_machine_health_scores(self, data):
        """Get comprehensive machine health scores"""
        if not self.models_trained:
            raise ValueError("Models must be trained before prediction")
        
        health_scores = []
        
        for machine_id in data['machine_id'].unique():
            machine_data = data[data['machine_id'] == machine_id]
            
            # Get predictions for this machine
            anomaly_preds, anomaly_scores = self.predict_anomalies(machine_data)
            rul_preds = self.predict_rul(machine_data)
            fault_preds, fault_probs = self.predict_faults(machine_data)
            
            # Calculate health score
            health_score = self._calculate_health_score(
                anomaly_scores, rul_preds, fault_probs
            )
            
            health_scores.append({
                'machine_id': machine_id,
                'health_score': health_score,
                'anomaly_score': np.mean(anomaly_scores),
                'rul_hours': np.mean(rul_preds) if len(rul_preds) > 0 else 0,
                'fault_probability': np.mean(fault_probs) if len(fault_probs) > 0 else 0,
                'last_update': machine_data['timestamp'].max()
            })
        
        return pd.DataFrame(health_scores)
    
    def _calculate_health_score(self, anomaly_scores, rul_preds, fault_probs):
        """Calculate overall health score for a machine"""
        # Normalize anomaly scores (higher is better)
        anomaly_score = np.mean(anomaly_scores) if len(anomaly_scores) > 0 else 0
        anomaly_normalized = max(0, min(1, (anomaly_score + 0.5) / 1.0))
        
        # Normalize RUL (higher is better)
        rul_score = np.mean(rul_preds) if len(rul_preds) > 0 else 500
        rul_normalized = max(0, min(1, rul_score / 500))
        
        # Normalize fault probability (lower is better)
        fault_score = np.mean(fault_probs) if len(fault_probs) > 0 else 0
        fault_normalized = max(0, min(1, 1 - fault_score))
        
        # Weighted average
        health_score = (
            0.4 * anomaly_normalized +
            0.4 * rul_normalized +
            0.2 * fault_normalized
        )
        
        return health_score
    
    def _save_training_metadata(self, telemetry_data, events_data):
        """Save metadata about model training"""
        metadata = {
            'training_date': datetime.now().isoformat(),
            'data_summary': {
                'telemetry_records': len(telemetry_data),
                'event_records': len(events_data),
                'machines': telemetry_data['machine_id'].nunique(),
                'date_range': {
                    'start': str(telemetry_data['timestamp'].min()),
                    'end': str(telemetry_data['timestamp'].max())
                }
            },
            'model_parameters': {
                'anomaly_contamination': self.anomaly_detector.contamination,
                'rul_sequence_length': self.rul_predictor.sequence_length,
                'rul_prediction_horizon': self.rul_predictor.prediction_horizon,
                'fault_n_estimators': self.fault_classifier.n_estimators
            },
            'model_files': [
                'artifacts/models/anomaly_detector.joblib',
                'artifacts/models/rul_predictor.joblib',
                'artifacts/models/fault_classifier.joblib'
            ]
        }
        
        with open('artifacts/metadata/model_training_metadata.json', 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print("Training metadata saved to artifacts/metadata/")
    
    def get_model_summary(self):
        """Get summary of all models"""
        if not self.models_trained:
            return {'status': 'Models not trained'}
        
        summary = {
            'status': 'Models trained and ready',
            'anomaly_detector': {
                'contamination': self.anomaly_detector.contamination,
                'is_fitted': self.anomaly_detector.is_fitted
            },
            'rul_predictor': {
                'sequence_length': self.rul_predictor.sequence_length,
                'prediction_horizon': self.rul_predictor.prediction_horizon,
                'is_fitted': self.rul_predictor.is_fitted
            },
            'fault_classifier': {
                'n_estimators': self.fault_classifier.n_estimators,
                'is_fitted': self.fault_classifier.is_fitted
            }
        }
        
        return summary