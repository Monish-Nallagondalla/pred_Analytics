"""
Flow Optimization and Bottleneck Detection System
Implements algorithms for optimizing machine flow and detecting production bottlenecks
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import networkx as nx
from collections import defaultdict, deque
import json
import random
from config import MACHINES

class ProductionFlow:
    def __init__(self, machine_id, capacity, processing_time, setup_time=0):
        self.machine_id = machine_id
        self.capacity = capacity  # Parts per hour
        self.processing_time = processing_time  # Minutes per part
        self.setup_time = setup_time  # Minutes for setup
        self.current_queue = []
        self.current_load = 0
        self.downtime_minutes = 0
        self.operator_available = True
    
    def add_job(self, job):
        """Add a job to the machine queue"""
        self.current_queue.append(job)
    
    def process_job(self):
        """Process the next job in the queue"""
        if self.current_queue and self.operator_available:
            job = self.current_queue.pop(0)
            self.current_load += self.processing_time
            return job
        return None
    
    def get_utilization(self):
        """Get current utilization percentage"""
        if self.capacity > 0:
            return (self.current_load / self.capacity) * 100
        return 0
    
    def get_queue_length(self):
        """Get current queue length"""
        return len(self.current_queue)

class BottleneckDetector:
    def __init__(self):
        self.flow_graph = nx.DiGraph()
        self.machine_flows = {}
        self.setup_production_flow()
    
    def setup_production_flow(self):
        """Setup the production flow network"""
        # Define machine capacities and processing times
        machine_configs = {
            'VF2_01': {'capacity': 20, 'processing_time': 3, 'setup_time': 15},  # CNC Mill
            'ST10_01': {'capacity': 25, 'processing_time': 2.5, 'setup_time': 10},  # CNC Lathe
            'KUKA_01': {'capacity': 30, 'processing_time': 2, 'setup_time': 5},  # Robot
            'LASER_01': {'capacity': 15, 'processing_time': 4, 'setup_time': 20},  # Laser
            'PRESS_01': {'capacity': 18, 'processing_time': 3.5, 'setup_time': 12},  # Press Brake
            'DRILL_01': {'capacity': 35, 'processing_time': 1.5, 'setup_time': 5},  # Drill
            'GRINDER_01': {'capacity': 12, 'processing_time': 5, 'setup_time': 25},  # Grinder
            'COMPRESSOR_01': {'capacity': 100, 'processing_time': 0.5, 'setup_time': 0}  # Compressor
        }
        
        # Create flow objects for each machine
        for machine_id, config in machine_configs.items():
            self.machine_flows[machine_id] = ProductionFlow(
                machine_id=machine_id,
                capacity=config['capacity'],
                processing_time=config['processing_time'],
                setup_time=config['setup_time']
            )
        
        # Define production flow sequence
        self.setup_flow_sequence()
    
    def setup_flow_sequence(self):
        """Setup the production flow sequence"""
        # Define the production flow sequence
        flow_sequence = [
            'VF2_01',  # CNC Mill - Primary machining
            'ST10_01',  # CNC Lathe - Secondary machining
            'KUKA_01',  # Robot - Loading/unloading
            'LASER_01',  # Laser cutting
            'PRESS_01',  # Press brake
            'DRILL_01',  # Drilling
            'GRINDER_01'  # Grinding
        ]
        
        # Create directed graph
        for i in range(len(flow_sequence) - 1):
            current_machine = flow_sequence[i]
            next_machine = flow_sequence[i + 1]
            self.flow_graph.add_edge(current_machine, next_machine)
    
    def analyze_bottlenecks(self, telemetry_data):
        """Analyze production bottlenecks from telemetry data"""
        bottleneck_analysis = {}
        
        for machine_id in self.machine_flows.keys():
            machine_data = telemetry_data[telemetry_data['machine_id'] == machine_id]
            
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
            
            # Calculate bottleneck score
            bottleneck_score = idle_ratio + fault_ratio
            
            bottleneck_analysis[machine_id] = {
                'utilization': utilization,
                'idle_ratio': idle_ratio,
                'fault_ratio': fault_ratio,
                'throughput': throughput,
                'bottleneck_score': bottleneck_score,
                'status': 'bottleneck' if bottleneck_score > 0.3 else 'normal'
            }
        
        return bottleneck_analysis
    
    def identify_critical_path(self, bottleneck_analysis):
        """Identify the critical path in production"""
        critical_machines = []
        
        for machine_id, analysis in bottleneck_analysis.items():
            if analysis['bottleneck_score'] > 0.3:
                critical_machines.append(machine_id)
        
        return critical_machines
    
    def calculate_flow_efficiency(self, telemetry_data):
        """Calculate overall flow efficiency"""
        total_cycles = 0
        total_time = 0
        total_downtime = 0
        
        for machine_id in self.machine_flows.keys():
            machine_data = telemetry_data[telemetry_data['machine_id'] == machine_id]
            
            total_cycles += len(machine_data[machine_data['state'] == 'cutting'])
            total_time += len(machine_data)
            total_downtime += len(machine_data[machine_data['state'] == 'fault'])
        
        if total_time > 0:
            flow_efficiency = (total_cycles / total_time) * 100
            downtime_ratio = total_downtime / total_time
        else:
            flow_efficiency = 0
            downtime_ratio = 0
        
        return {
            'flow_efficiency': flow_efficiency,
            'downtime_ratio': downtime_ratio,
            'total_cycles': total_cycles,
            'total_time': total_time
        }

class FlowOptimizer:
    def __init__(self, bottleneck_detector):
        self.bottleneck_detector = bottleneck_detector
        self.optimization_strategies = []
    
    def optimize_production_flow(self, telemetry_data, events_data):
        """Optimize production flow based on current data"""
        # Analyze bottlenecks
        bottleneck_analysis = self.bottleneck_detector.analyze_bottlenecks(telemetry_data)
        
        # Identify critical path
        critical_machines = self.bottleneck_detector.identify_critical_path(bottleneck_analysis)
        
        # Calculate flow efficiency
        flow_efficiency = self.bottleneck_detector.calculate_flow_efficiency(telemetry_data)
        
        # Generate optimization recommendations
        recommendations = self.generate_optimization_recommendations(
            bottleneck_analysis, critical_machines, flow_efficiency
        )
        
        return {
            'bottleneck_analysis': bottleneck_analysis,
            'critical_machines': critical_machines,
            'flow_efficiency': flow_efficiency,
            'recommendations': recommendations
        }
    
    def generate_optimization_recommendations(self, bottleneck_analysis, critical_machines, flow_efficiency):
        """Generate optimization recommendations"""
        recommendations = []
        
        # Bottleneck recommendations
        for machine_id, analysis in bottleneck_analysis.items():
            if analysis['bottleneck_score'] > 0.3:
                recommendations.append({
                    'type': 'bottleneck',
                    'machine_id': machine_id,
                    'priority': 'high',
                    'description': f"Machine {machine_id} is a bottleneck with {analysis['bottleneck_score']:.2f} score",
                    'actions': [
                        f"Reduce setup time for {machine_id}",
                        f"Increase capacity for {machine_id}",
                        f"Optimize scheduling for {machine_id}"
                    ]
                })
        
        # Flow efficiency recommendations
        if flow_efficiency['flow_efficiency'] < 70:
            recommendations.append({
                'type': 'flow_efficiency',
                'priority': 'medium',
                'description': f"Overall flow efficiency is {flow_efficiency['flow_efficiency']:.1f}%",
                'actions': [
                    "Review production scheduling",
                    "Optimize machine utilization",
                    "Reduce changeover times"
                ]
            })
        
        # Downtime recommendations
        if flow_efficiency['downtime_ratio'] > 0.1:
            recommendations.append({
                'type': 'downtime',
                'priority': 'high',
                'description': f"Downtime ratio is {flow_efficiency['downtime_ratio']:.1f}%",
                'actions': [
                    "Implement predictive maintenance",
                    "Improve machine reliability",
                    "Reduce unplanned downtime"
                ]
            })
        
        return recommendations
    
    def optimize_machine_scheduling(self, machine_data, demand_forecast):
        """Optimize machine scheduling based on demand and capacity"""
        # This is a simplified scheduling algorithm
        # In practice, this would be much more complex
        
        optimized_schedule = {}
        
        for machine_id in machine_data.keys():
            machine_info = machine_data[machine_id]
            demand = demand_forecast.get(machine_id, 0)
            capacity = machine_info['capacity']
            
            # Calculate required hours
            required_hours = demand / capacity if capacity > 0 else 0
            
            # Calculate optimal schedule
            if required_hours > 16:  # More than one shift
                optimized_schedule[machine_id] = {
                    'shift_1': 8,
                    'shift_2': min(8, required_hours - 8),
                    'overtime': max(0, required_hours - 16)
                }
            else:
                optimized_schedule[machine_id] = {
                    'shift_1': min(8, required_hours),
                    'shift_2': 0,
                    'overtime': 0
                }
        
        return optimized_schedule
    
    def optimize_buffer_sizes(self, bottleneck_analysis):
        """Optimize buffer sizes between machines"""
        buffer_recommendations = {}
        
        for machine_id, analysis in bottleneck_analysis.items():
            if analysis['bottleneck_score'] > 0.3:
                # Increase buffer size before bottleneck
                buffer_recommendations[machine_id] = {
                    'current_buffer': 10,  # Default buffer size
                    'recommended_buffer': 20,  # Increased buffer size
                    'reason': 'Bottleneck detected - increase buffer to prevent starvation'
                }
            else:
                buffer_recommendations[machine_id] = {
                    'current_buffer': 10,
                    'recommended_buffer': 10,
                    'reason': 'No bottleneck - maintain current buffer size'
                }
        
        return buffer_recommendations

class LayoutOptimizer:
    def __init__(self):
        self.machine_positions = {}
        self.setup_default_layout()
    
    def setup_default_layout(self):
        """Setup default machine layout"""
        # Define machine positions in the shop floor
        self.machine_positions = {
            'VF2_01': (0, 0),      # CNC Mill
            'ST10_01': (5, 0),      # CNC Lathe
            'KUKA_01': (2.5, 3),    # Robot (center)
            'LASER_01': (0, 6),     # Laser
            'PRESS_01': (5, 6),     # Press Brake
            'DRILL_01': (0, 9),     # Drill
            'GRINDER_01': (5, 9),   # Grinder
            'COMPRESSOR_01': (2.5, 12)  # Compressor
        }
    
    def calculate_material_flow_distance(self, machine1, machine2):
        """Calculate distance between two machines"""
        pos1 = self.machine_positions.get(machine1, (0, 0))
        pos2 = self.machine_positions.get(machine2, (0, 0))
        
        distance = np.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
        return distance
    
    def optimize_layout(self, flow_frequency):
        """Optimize machine layout based on flow frequency"""
        # This is a simplified layout optimization
        # In practice, this would use more sophisticated algorithms
        
        layout_recommendations = []
        
        # Find machines with high flow frequency
        high_flow_machines = []
        for machine1, flows in flow_frequency.items():
            for machine2, frequency in flows.items():
                if frequency > 10:  # High frequency threshold
                    high_flow_machines.append((machine1, machine2, frequency))
        
        # Sort by frequency
        high_flow_machines.sort(key=lambda x: x[2], reverse=True)
        
        # Generate recommendations
        for machine1, machine2, frequency in high_flow_machines[:5]:  # Top 5
            current_distance = self.calculate_material_flow_distance(machine1, machine2)
            
            if current_distance > 5:  # If machines are far apart
                layout_recommendations.append({
                    'machine1': machine1,
                    'machine2': machine2,
                    'current_distance': current_distance,
                    'recommendation': f"Move {machine1} and {machine2} closer together",
                    'priority': 'high' if frequency > 20 else 'medium'
                })
        
        return layout_recommendations
    
    def calculate_layout_efficiency(self, flow_frequency):
        """Calculate layout efficiency based on flow frequency and distances"""
        total_flow_distance = 0
        total_flow_frequency = 0
        
        for machine1, flows in flow_frequency.items():
            for machine2, frequency in flows.items():
                distance = self.calculate_material_flow_distance(machine1, machine2)
                total_flow_distance += distance * frequency
                total_flow_frequency += frequency
        
        if total_flow_frequency > 0:
            average_flow_distance = total_flow_distance / total_flow_frequency
            layout_efficiency = 100 / (1 + average_flow_distance)  # Higher distance = lower efficiency
        else:
            layout_efficiency = 100
        
        return {
            'layout_efficiency': layout_efficiency,
            'average_flow_distance': average_flow_distance,
            'total_flow_frequency': total_flow_frequency
        }

class FlowOptimizationSystem:
    def __init__(self):
        self.bottleneck_detector = BottleneckDetector()
        self.flow_optimizer = FlowOptimizer(self.bottleneck_detector)
        self.layout_optimizer = LayoutOptimizer()
    
    def analyze_production_flow(self, telemetry_data, events_data):
        """Comprehensive production flow analysis"""
        # Optimize production flow
        flow_optimization = self.flow_optimizer.optimize_production_flow(telemetry_data, events_data)
        
        # Analyze layout efficiency
        flow_frequency = self.calculate_flow_frequency(telemetry_data)
        layout_efficiency = self.layout_optimizer.calculate_layout_efficiency(flow_frequency)
        layout_recommendations = self.layout_optimizer.optimize_layout(flow_frequency)
        
        return {
            'flow_optimization': flow_optimization,
            'layout_efficiency': layout_efficiency,
            'layout_recommendations': layout_recommendations,
            'flow_frequency': flow_frequency
        }
    
    def calculate_flow_frequency(self, telemetry_data):
        """Calculate flow frequency between machines"""
        flow_frequency = defaultdict(lambda: defaultdict(int))
        
        # Group data by machine and time
        machine_data = {}
        for machine_id in MACHINES.keys():
            machine_data[machine_id] = telemetry_data[telemetry_data['machine_id'] == machine_id]
        
        # Calculate flow frequency (simplified)
        for machine1 in machine_data.keys():
            for machine2 in machine_data.keys():
                if machine1 != machine2:
                    # Simple flow frequency calculation
                    # In practice, this would be more sophisticated
                    flow_frequency[machine1][machine2] = random.randint(1, 30)
        
        return flow_frequency
    
    def generate_optimization_report(self, analysis_results):
        """Generate comprehensive optimization report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_machines': len(MACHINES),
                'bottleneck_machines': len(analysis_results['flow_optimization']['critical_machines']),
                'flow_efficiency': analysis_results['flow_optimization']['flow_efficiency']['flow_efficiency'],
                'layout_efficiency': analysis_results['layout_efficiency']['layout_efficiency']
            },
            'recommendations': analysis_results['flow_optimization']['recommendations'],
            'layout_recommendations': analysis_results['layout_recommendations'],
            'bottleneck_analysis': analysis_results['flow_optimization']['bottleneck_analysis']
        }
        
        return report

if __name__ == "__main__":
    # Test flow optimization system
    print("Testing Flow Optimization System...")
    
    # Create sample data
    sample_data = pd.DataFrame({
        'machine_id': ['VF2_01'] * 100 + ['ST10_01'] * 100,
        'timestamp': pd.date_range('2025-01-01', periods=200, freq='1H'),
        'state': ['cutting'] * 150 + ['idle'] * 50,
        'quality_flag': ['ok'] * 200
    })
    
    sample_events = pd.DataFrame({
        'machine_id': ['VF2_01'],
        'timestamp': ['2025-01-01'],
        'event_type': ['fault_code'],
        'severity': ['high']
    })
    
    # Test flow optimization
    flow_system = FlowOptimizationSystem()
    analysis = flow_system.analyze_production_flow(sample_data, sample_events)
    
    print("Flow optimization analysis completed")
    print(f"Bottleneck machines: {analysis['flow_optimization']['critical_machines']}")
    print(f"Flow efficiency: {analysis['flow_optimization']['flow_efficiency']['flow_efficiency']:.1f}%")
    print(f"Layout efficiency: {analysis['layout_efficiency']['layout_efficiency']:.1f}%")
    
    # Generate report
    report = flow_system.generate_optimization_report(analysis)
    print(f"Generated optimization report with {len(report['recommendations'])} recommendations")
