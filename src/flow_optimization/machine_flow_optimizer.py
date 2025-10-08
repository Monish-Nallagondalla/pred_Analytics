"""
Machine Flow Optimizer
Bottleneck detection and material flow optimization for manufacturing lines
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import yaml

class MachineFlowOptimizer:
    """
    Flow optimization system for detecting bottlenecks and optimizing material flow
    """
    
    def __init__(self, config_path="config/machines.yaml"):
        """Initialize the flow optimizer"""
        self.config_path = config_path
        self.load_config()
        
    def load_config(self):
        """Load machine configuration and flow parameters"""
        try:
            with open(self.config_path, 'r') as file:
                self.config = yaml.safe_load(file)
            self.machines = self.config['machines']
            self.production_flow = self.config.get('production_flow', {})
            self.flow_optimization = self.config.get('flow_optimization', {})
        except Exception as e:
            print(f"Error loading config: {e}")
            self.config = {}
            self.machines = {}
            self.production_flow = {}
            self.flow_optimization = {}
    
    def analyze_bottlenecks(self, process_flow_data: pd.DataFrame) -> pd.DataFrame:
        """
        Analyze bottlenecks in the production flow
        """
        if process_flow_data.empty:
            return pd.DataFrame()
        
        # Calculate cycle times per machine
        machine_cycle_times = process_flow_data.groupby('machine_id').agg({
            'duration': ['mean', 'std', 'count'],
            'start_time': 'min',
            'end_time': 'max'
        }).round(2)
        
        machine_cycle_times.columns = ['avg_cycle_time', 'std_cycle_time', 'operation_count', 'first_operation', 'last_operation']
        machine_cycle_times = machine_cycle_times.reset_index()
        
        # Calculate utilization
        machine_cycle_times['utilization'] = (
            machine_cycle_times['operation_count'] * machine_cycle_times['avg_cycle_time'] / 
            (machine_cycle_times['last_operation'] - machine_cycle_times['first_operation']).dt.total_seconds() / 3600
        ) * 100
        
        # Identify bottlenecks
        bottleneck_threshold = self.flow_optimization.get('bottleneck_threshold', 0.8)
        machine_cycle_times['is_bottleneck'] = machine_cycle_times['utilization'] > (bottleneck_threshold * 100)
        
        # Calculate bottleneck severity
        machine_cycle_times['bottleneck_severity'] = machine_cycle_times.apply(
            lambda x: 'Critical' if x['utilization'] > 95 else 
                     'High' if x['utilization'] > 85 else 
                     'Medium' if x['utilization'] > 75 else 'Low', axis=1
        )
        
        return machine_cycle_times.sort_values('utilization', ascending=False)
    
    def analyze_material_flow(self, process_flow_data: pd.DataFrame) -> Dict:
        """
        Analyze material flow patterns and delays
        """
        if process_flow_data.empty:
            return {}
        
        # Calculate flow metrics
        flow_analysis = {
            'total_batches': process_flow_data['batch_id'].nunique(),
            'total_operations': len(process_flow_data),
            'avg_cycle_time': process_flow_data['duration'].mean(),
            'total_flow_time': process_flow_data.groupby('batch_id')['duration'].sum().mean()
        }
        
        # Calculate delays between processes
        batch_flows = process_flow_data.groupby('batch_id').apply(self._calculate_batch_flow_metrics)
        flow_analysis['avg_delay_between_processes'] = batch_flows['delay_between_processes'].mean()
        flow_analysis['max_delay_between_processes'] = batch_flows['delay_between_processes'].max()
        
        # Identify flow bottlenecks
        flow_analysis['bottleneck_processes'] = self._identify_flow_bottlenecks(process_flow_data)
        
        return flow_analysis
    
    def _calculate_batch_flow_metrics(self, batch_data: pd.DataFrame) -> pd.Series:
        """Calculate flow metrics for a single batch"""
        batch_data = batch_data.sort_values('start_time')
        
        delays = []
        for i in range(1, len(batch_data)):
            prev_end = batch_data.iloc[i-1]['end_time']
            curr_start = batch_data.iloc[i]['start_time']
            delay = (curr_start - prev_end).total_seconds() / 60  # minutes
            delays.append(delay)
        
        return pd.Series({
            'delay_between_processes': np.mean(delays) if delays else 0,
            'max_delay': np.max(delays) if delays else 0,
            'total_flow_time': (batch_data['end_time'].max() - batch_data['start_time'].min()).total_seconds() / 60
        })
    
    def _identify_flow_bottlenecks(self, process_flow_data: pd.DataFrame) -> List[Dict]:
        """Identify processes that are causing flow bottlenecks"""
        bottlenecks = []
        
        # Calculate average cycle time per process
        process_cycle_times = process_flow_data.groupby('process_step').agg({
            'duration': ['mean', 'std', 'count']
        }).round(2)
        
        process_cycle_times.columns = ['avg_duration', 'std_duration', 'operation_count']
        process_cycle_times = process_cycle_times.reset_index()
        
        # Identify processes with high cycle times
        avg_cycle_time = process_cycle_times['avg_duration'].mean()
        std_cycle_time = process_cycle_times['avg_duration'].std()
        
        bottleneck_threshold = avg_cycle_time + 2 * std_cycle_time
        
        bottleneck_processes = process_cycle_times[
            process_cycle_times['avg_duration'] > bottleneck_threshold
        ].sort_values('avg_duration', ascending=False)
        
        for _, process in bottleneck_processes.iterrows():
            bottlenecks.append({
                'process_step': process['process_step'],
                'avg_duration': process['avg_duration'],
                'operation_count': process['operation_count'],
                'severity': 'High' if process['avg_duration'] > avg_cycle_time + 3 * std_cycle_time else 'Medium'
            })
        
        return bottlenecks
    
    def get_flow_recommendations(self, process_flow_data: pd.DataFrame) -> List[Dict]:
        """Get flow optimization recommendations"""
        recommendations = []
        
        if process_flow_data.empty:
            return recommendations
        
        # Analyze bottlenecks
        bottlenecks = self.analyze_bottlenecks(process_flow_data)
        critical_bottlenecks = bottlenecks[bottlenecks['bottleneck_severity'] == 'Critical']
        
        if len(critical_bottlenecks) > 0:
                recommendations.append({
                'type': 'Critical Bottleneck',
                'message': f"Critical bottlenecks detected in {len(critical_bottlenecks)} machines",
                'priority': 'High',
                'machines': critical_bottlenecks['machine_id'].tolist()
            })
        
        # Analyze flow delays
        flow_analysis = self.analyze_material_flow(process_flow_data)
        if flow_analysis.get('avg_delay_between_processes', 0) > 30:  # 30 minutes
                recommendations.append({
                'type': 'Flow Delay',
                'message': f"Average delay between processes: {flow_analysis.get('avg_delay_between_processes', 0):.1f} minutes",
                'priority': 'Medium'
            })
        
        # Analyze utilization
        high_utilization = bottlenecks[bottlenecks['utilization'] > 90]
        if len(high_utilization) > 0:
            recommendations.append({
                'type': 'High Utilization',
                'message': f"{len(high_utilization)} machines at >90% utilization",
                'priority': 'Medium',
                'machines': high_utilization['machine_id'].tolist()
            })
        
        return recommendations
    
    def optimize_flow_sequence(self, process_flow_data: pd.DataFrame) -> Dict:
        """Optimize the flow sequence based on current performance"""
        if process_flow_data.empty:
            return {}
        
        # Get current sequence performance
        sequence_performance = self._analyze_sequence_performance(process_flow_data)
        
        # Generate optimization suggestions
        optimizations = {
            'current_sequence': sequence_performance.get('current_sequence', []),
            'optimization_suggestions': [],
            'expected_improvements': {}
        }
        
        # Suggest parallel processing for bottleneck machines
        bottlenecks = self.analyze_bottlenecks(process_flow_data)
        critical_bottlenecks = bottlenecks[bottlenecks['bottleneck_severity'] == 'Critical']
        
        for _, bottleneck in critical_bottlenecks.iterrows():
            optimizations['optimization_suggestions'].append({
                'type': 'Parallel Processing',
                'machine_id': bottleneck['machine_id'],
                'suggestion': f"Consider adding parallel {bottleneck['machine_id']} to reduce bottleneck",
                'expected_improvement': f"Reduce cycle time by ~{bottleneck['avg_cycle_time'] * 0.3:.1f} minutes"
            })
        
        return optimizations
    
    def _analyze_sequence_performance(self, process_flow_data: pd.DataFrame) -> Dict:
        """Analyze the performance of the current sequence"""
        if process_flow_data.empty:
            return {}
        
        # Get unique sequence of processes
        sequence = process_flow_data.groupby('batch_id').apply(
            lambda x: x.sort_values('start_time')['process_step'].tolist()
        )
        
        # Find most common sequence
        sequence_counts = sequence.value_counts()
        most_common_sequence = sequence_counts.index[0] if len(sequence_counts) > 0 else []
        
        return {
            'current_sequence': most_common_sequence,
            'sequence_variations': len(sequence_counts),
            'most_common_frequency': sequence_counts.iloc[0] if len(sequence_counts) > 0 else 0
        }
    
    def get_flow_efficiency_metrics(self, process_flow_data: pd.DataFrame) -> Dict:
        """Calculate flow efficiency metrics"""
        if process_flow_data.empty:
            return {}
        
        # Calculate overall flow efficiency
        total_flow_time = process_flow_data.groupby('batch_id')['duration'].sum()
        theoretical_min_time = process_flow_data.groupby('batch_id')['duration'].min().sum()
        
        flow_efficiency = (theoretical_min_time / total_flow_time.mean()) * 100 if total_flow_time.mean() > 0 else 0
        
        # Calculate throughput
        total_batches = process_flow_data['batch_id'].nunique()
        time_span = (process_flow_data['end_time'].max() - process_flow_data['start_time'].min()).total_seconds() / 3600  # hours
        throughput = total_batches / time_span if time_span > 0 else 0
        
        return {
            'flow_efficiency': flow_efficiency,
            'throughput_batches_per_hour': throughput,
            'total_batches_processed': total_batches,
            'avg_flow_time_per_batch': total_flow_time.mean(),
            'flow_time_std': total_flow_time.std()
        }
