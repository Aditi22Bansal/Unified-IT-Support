"""
Enterprise Operations Management Service
For Digital Services, Customer Support, and Mainframe Operations
"""

import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import random

class OperationsManager:
    def __init__(self):
        self.sla_rules = {
            'critical': {'response': 1, 'resolution': 4},  # hours
            'high': {'response': 4, 'resolution': 24},
            'medium': {'response': 24, 'resolution': 72},
            'low': {'response': 72, 'resolution': 168}
        }

        # Department/Team structure
        self.departments = {
            'mainframe': {'name': 'Mainframe Operations', 'team_size': 8, 'specialization': 'zOS, CICS, DB2'},
            'network': {'name': 'Network Operations', 'team_size': 6, 'specialization': 'Network, Security'},
            'application': {'name': 'Application Support', 'team_size': 10, 'specialization': 'Java, .NET, Web'},
            'database': {'name': 'Database Administration', 'team_size': 4, 'specialization': 'DB2, Oracle, SQL Server'},
            'customer_support': {'name': 'Customer Support', 'team_size': 12, 'specialization': 'End-user Support'}
        }

        # Mainframe systems monitoring
        self.mainframe_systems = {
            'zOS_Production': {'status': 'operational', 'cpu_usage': 65, 'memory_usage': 78},
            'CICS_Region1': {'status': 'operational', 'transactions': 1250, 'response_time': 0.8},
            'DB2_Production': {'status': 'operational', 'connections': 45, 'query_time': 0.3},
            'IMS_Production': {'status': 'operational', 'transactions': 890, 'response_time': 0.5}
        }

    def calculate_sla_metrics(self, tickets: List[Dict]) -> Dict:
        """Calculate SLA performance metrics"""
        try:
            total_tickets = len(tickets)
            sla_metrics = {
                'total_tickets': total_tickets,
                'sla_compliance': {},
                'average_response_time': {},
                'average_resolution_time': {},
                'escalations': 0,
                'breaches': 0
            }

            for priority in ['critical', 'high', 'medium', 'low']:
                priority_tickets = [t for t in tickets if t.get('priority') == priority]
                if not priority_tickets:
                    continue

                # Calculate response times (simulated)
                response_times = [random.uniform(0.5, self.sla_rules[priority]['response'] * 1.5) for _ in priority_tickets]
                resolution_times = [random.uniform(1, self.sla_rules[priority]['resolution'] * 1.2) for _ in priority_tickets]

                sla_metrics['average_response_time'][priority] = round(sum(response_times) / len(response_times), 2)
                sla_metrics['average_resolution_time'][priority] = round(sum(resolution_times) / len(resolution_times), 2)

                # SLA compliance calculation
                sla_target = self.sla_rules[priority]['resolution']
                compliant = sum(1 for time in resolution_times if time <= sla_target)
                sla_metrics['sla_compliance'][priority] = round((compliant / len(resolution_times)) * 100, 1)

                # Count breaches
                sla_metrics['breaches'] += sum(1 for time in resolution_times if time > sla_target)

            return sla_metrics

        except Exception as e:
            print(f"⚠️ Error calculating SLA metrics: {e}")
            return {'error': str(e)}

    def get_operations_dashboard(self, tickets: List[Dict]) -> Dict:
        """Get comprehensive operations dashboard data"""
        try:
            # System health monitoring
            system_health = self._get_system_health()

            # Resource utilization
            resource_utilization = self._get_resource_utilization()

            # Performance metrics
            performance_metrics = self._get_performance_metrics(tickets)

            # Mainframe monitoring
            mainframe_status = self._get_mainframe_status()

            # Cost analysis
            cost_analysis = self._get_cost_analysis(tickets)

            return {
                'timestamp': datetime.now().isoformat(),
                'system_health': system_health,
                'resource_utilization': resource_utilization,
                'performance_metrics': performance_metrics,
                'mainframe_status': mainframe_status,
                'cost_analysis': cost_analysis,
                'departments': self.departments,
                'alerts': self._get_active_alerts(),
                'recommendations': self._get_operations_recommendations(tickets)
            }

        except Exception as e:
            print(f"⚠️ Error getting operations dashboard: {e}")
            return {'error': str(e)}

    def _get_system_health(self) -> Dict:
        """Get overall system health status"""
        return {
            'overall_status': 'operational',
            'uptime_percentage': 99.8,
            'active_incidents': random.randint(0, 3),
            'system_load': {
                'cpu': random.uniform(60, 85),
                'memory': random.uniform(70, 90),
                'disk': random.uniform(45, 75),
                'network': random.uniform(30, 60)
            },
            'services_status': {
                'authentication': 'operational',
                'database': 'operational',
                'messaging': 'operational',
                'monitoring': 'operational'
            }
        }

    def _get_resource_utilization(self) -> Dict:
        """Get resource utilization across departments"""
        utilization = {}
        for dept_id, dept_info in self.departments.items():
            utilization[dept_id] = {
                'name': dept_info['name'],
                'team_size': dept_info['team_size'],
                'utilization_percentage': random.uniform(65, 95),
                'active_tickets': random.randint(5, 25),
                'capacity_remaining': random.randint(2, 8),
                'specialization': dept_info['specialization']
            }
        return utilization

    def _get_performance_metrics(self, tickets: List[Dict]) -> Dict:
        """Get performance metrics"""
        if not tickets:
            return {'total_tickets': 0, 'resolution_rate': 0}

        total_tickets = len(tickets)
        resolved_tickets = len([t for t in tickets if t.get('status') == 'resolved'])
        resolution_rate = (resolved_tickets / total_tickets) * 100 if total_tickets > 0 else 0

        return {
            'total_tickets': total_tickets,
            'resolution_rate': round(resolution_rate, 1),
            'average_resolution_time': random.uniform(8, 24),
            'customer_satisfaction': random.uniform(85, 95),
            'first_call_resolution': random.uniform(70, 85),
            'escalation_rate': random.uniform(5, 15)
        }

    def _get_mainframe_status(self) -> Dict:
        """Get mainframe systems status"""
        return {
            'systems': self.mainframe_systems,
            'overall_status': 'operational',
            'critical_alerts': 0,
            'performance_summary': {
                'average_cpu': round(sum(s['cpu_usage'] for s in self.mainframe_systems.values() if 'cpu_usage' in s) / 2, 1),
                'average_memory': round(sum(s['memory_usage'] for s in self.mainframe_systems.values() if 'memory_usage' in s) / 2, 1),
                'total_transactions': sum(s.get('transactions', 0) for s in self.mainframe_systems.values()),
                'average_response_time': 0.6
            }
        }

    def _get_cost_analysis(self, tickets: List[Dict]) -> Dict:
        """Get cost analysis and ROI metrics"""
        total_tickets = len(tickets)
        cost_per_ticket = random.uniform(25, 75)  # USD

        return {
            'total_operational_cost': round(total_tickets * cost_per_ticket, 2),
            'cost_per_ticket': round(cost_per_ticket, 2),
            'cost_by_priority': {
                'critical': round(cost_per_ticket * 2, 2),
                'high': round(cost_per_ticket * 1.5, 2),
                'medium': round(cost_per_ticket, 2),
                'low': round(cost_per_ticket * 0.7, 2)
            },
            'roi_metrics': {
                'cost_savings': round(total_tickets * 15, 2),
                'efficiency_gain': random.uniform(15, 35),
                'automation_savings': round(total_tickets * 8, 2)
            }
        }

    def _get_active_alerts(self) -> List[Dict]:
        """Get active system alerts"""
        alerts = []

        # Simulate some alerts
        if random.random() > 0.7:
            alerts.append({
                'id': 1,
                'type': 'performance',
                'severity': 'medium',
                'message': 'High CPU usage detected on zOS_Production',
                'timestamp': datetime.now().isoformat(),
                'system': 'zOS_Production'
            })

        if random.random() > 0.8:
            alerts.append({
                'id': 2,
                'type': 'capacity',
                'severity': 'low',
                'message': 'Disk space usage approaching threshold',
                'timestamp': datetime.now().isoformat(),
                'system': 'DB2_Production'
            })

        return alerts

    def _get_operations_recommendations(self, tickets: List[Dict]) -> List[str]:
        """Get AI-powered operations recommendations"""
        recommendations = []

        if len(tickets) > 20:
            recommendations.append("High ticket volume detected - consider increasing team capacity")

        critical_tickets = len([t for t in tickets if t.get('priority') == 'critical'])
        if critical_tickets > 5:
            recommendations.append("Multiple critical tickets - consider emergency response procedures")

        recommendations.extend([
            "Consider implementing automated monitoring for mainframe systems",
            "Review SLA targets based on current performance metrics",
            "Schedule preventive maintenance for peak performance"
        ])

        return recommendations

    def get_customer_insights(self, tickets: List[Dict]) -> Dict:
        """Get customer support insights"""
        try:
            if not tickets:
                return {'total_customers': 0, 'satisfaction_score': 0}

            # Analyze customer sentiment from tickets
            sentiment_scores = []
            for ticket in tickets:
                if 'sentiment_analysis' in ticket:
                    sentiment_scores.append(ticket['sentiment_analysis'].get('satisfaction_score', 0.5))

            avg_satisfaction = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0.5

            return {
                'total_customers': len(set(t.get('created_by', 0) for t in tickets)),
                'satisfaction_score': round(avg_satisfaction * 100, 1),
                'top_issues': self._get_top_customer_issues(tickets),
                'response_times': {
                    'average': random.uniform(2, 8),
                    'target': 4,
                    'compliance': random.uniform(85, 95)
                },
                'customer_trends': {
                    'increasing_volume': len(tickets) > 10,
                    'satisfaction_trend': 'improving' if avg_satisfaction > 0.7 else 'declining'
                }
            }

        except Exception as e:
            print(f"⚠️ Error getting customer insights: {e}")
            return {'error': str(e)}

    def _get_top_customer_issues(self, tickets: List[Dict]) -> List[Dict]:
        """Get top customer issues"""
        category_counts = {}
        for ticket in tickets:
            category = ticket.get('category', 'other')
            category_counts[category] = category_counts.get(category, 0) + 1

        # Sort by count and return top 3
        sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
        return [{'issue': cat, 'count': count} for cat, count in sorted_categories[:3]]

# Global operations manager instance
operations_manager = OperationsManager()
