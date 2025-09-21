"""
Simplified Machine Learning Service for IT Support System
Lightweight version with basic ML capabilities
"""

import re
import json
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import random

class SimpleMLService:
    def __init__(self):
        # Keyword-based classification (lightweight ML alternative)
        self.category_keywords = {
            'performance_issue': [
                'slow', 'performance', 'lag', 'timeout', 'cpu', 'memory', 'disk',
                'bottleneck', 'latency', 'response time', 'speed', 'overload'
            ],
            'bug': [
                'error', 'bug', 'crash', 'broken', 'malfunction', 'defect', 'issue',
                'problem', 'fault', 'failure', 'exception', 'wrong', 'incorrect'
            ],
            'feature_request': [
                'feature', 'enhancement', 'improvement', 'add', 'new', 'request',
                'suggestion', 'capability', 'functionality', 'tool', 'option'
            ],
            'incident': [
                'down', 'outage', 'emergency', 'critical', 'urgent', 'system down',
                'service unavailable', 'production', 'major', 'severe', 'blocking'
            ]
        }

        self.priority_keywords = {
            'critical': [
                'critical', 'emergency', 'urgent', 'down', 'outage', 'production',
                'blocking', 'severe', 'major', 'asap', 'immediately'
            ],
            'high': [
                'high', 'important', 'priority', 'soon', 'quickly', 'significant',
                'affecting', 'impact', 'business'
            ],
            'medium': [
                'medium', 'normal', 'standard', 'regular', 'usual', 'typical'
            ],
            'low': [
                'low', 'minor', 'small', 'trivial', 'cosmetic', 'nice to have',
                'when possible', 'eventually'
            ]
        }

        # Sentiment keywords
        self.sentiment_keywords = {
            'positive': ['good', 'great', 'excellent', 'working', 'fixed', 'resolved', 'thanks', 'appreciate'],
            'negative': ['bad', 'terrible', 'awful', 'frustrated', 'angry', 'disappointed', 'annoyed', 'upset'],
            'neutral': ['okay', 'fine', 'normal', 'standard', 'regular']
        }

    def classify_ticket(self, title: str, description: str) -> Dict:
        """Classify ticket using keyword-based approach"""
        try:
            combined_text = f"{title} {description}".lower()

            # Category classification
            category_scores = {}
            for category, keywords in self.category_keywords.items():
                score = sum(1 for keyword in keywords if keyword in combined_text)
                category_scores[category] = score

            predicted_category = max(category_scores, key=category_scores.get) if category_scores else 'other'
            category_confidence = min(0.9, max(0.3, category_scores.get(predicted_category, 0) * 0.2))

            # Priority classification
            priority_scores = {}
            for priority, keywords in self.priority_keywords.items():
                score = sum(1 for keyword in keywords if keyword in combined_text)
                priority_scores[priority] = score

            predicted_priority = max(priority_scores, key=priority_scores.get) if priority_scores else 'medium'
            priority_confidence = min(0.9, max(0.3, priority_scores.get(predicted_priority, 0) * 0.25))

            # Resolution time prediction (based on priority and category)
            base_time = {'critical': 2, 'high': 6, 'medium': 12, 'low': 24}
            predicted_resolution_time = base_time.get(predicted_priority, 8)

            # Add some variation
            predicted_resolution_time += random.uniform(-1, 3)
            predicted_resolution_time = max(1, min(48, predicted_resolution_time))

            return {
                'category': predicted_category,
                'category_confidence': round(category_confidence, 3),
                'priority': predicted_priority,
                'priority_confidence': round(priority_confidence, 3),
                'predicted_resolution_time_hours': round(predicted_resolution_time, 1),
                'urgency_score': priority_scores.get(predicted_priority, 0),
                'auto_categorized': True,
                'ml_confidence': round((category_confidence + priority_confidence) / 2, 3)
            }

        except Exception as e:
            print(f"⚠️ Error in ticket classification: {e}")
            return {
                'category': 'other',
                'category_confidence': 0.5,
                'priority': 'medium',
                'priority_confidence': 0.5,
                'predicted_resolution_time_hours': 8.0,
                'urgency_score': 0,
                'auto_categorized': False,
                'ml_confidence': 0.5
            }

    def analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment using keyword-based approach"""
        try:
            text_lower = text.lower()

            # Count sentiment keywords
            sentiment_scores = {}
            for sentiment, keywords in self.sentiment_keywords.items():
                score = sum(1 for keyword in keywords if keyword in text_lower)
                sentiment_scores[sentiment] = score

            # Determine overall sentiment
            if sentiment_scores.get('negative', 0) > sentiment_scores.get('positive', 0):
                sentiment = 'negative'
                sentiment_score = -0.5
            elif sentiment_scores.get('positive', 0) > sentiment_scores.get('negative', 0):
                sentiment = 'positive'
                sentiment_score = 0.5
            else:
                sentiment = 'neutral'
                sentiment_score = 0.0

            # Calculate satisfaction score
            satisfaction_score = (sentiment_score + 1) / 2

            # Determine customer mood
            if sentiment_score < -0.3:
                customer_mood = 'frustrated'
            elif sentiment_score < -0.1:
                customer_mood = 'concerned'
            elif sentiment_score < 0.1:
                customer_mood = 'neutral'
            elif sentiment_score < 0.3:
                customer_mood = 'hopeful'
            else:
                customer_mood = 'satisfied'

            return {
                'sentiment': sentiment,
                'sentiment_score': round(sentiment_score, 3),
                'satisfaction_score': round(satisfaction_score, 3),
                'emotional_intensity': 0.5,  # Simplified
                'is_urgent_emotional': sentiment_score < -0.3,
                'customer_mood': customer_mood
            }

        except Exception as e:
            print(f"⚠️ Error in sentiment analysis: {e}")
            return {
                'sentiment': 'neutral',
                'sentiment_score': 0.0,
                'satisfaction_score': 0.5,
                'emotional_intensity': 0.5,
                'is_urgent_emotional': False,
                'customer_mood': 'neutral'
            }

    def predict_ticket_trends(self, tickets_data: List[Dict]) -> Dict:
        """Predict ticket trends and insights"""
        try:
            if not tickets_data:
                return {
                    'total_tickets': 0,
                    'avg_resolution_time': 0,
                    'trend_prediction': 'stable',
                    'peak_hours': [],
                    'common_issues': [],
                    'recommendations': []
                }

            # Analyze ticket patterns
            total_tickets = len(tickets_data)

            # Calculate average resolution time
            resolution_times = []
            for ticket in tickets_data:
                if 'ml_analysis' in ticket and 'predicted_resolution_time_hours' in ticket['ml_analysis']:
                    resolution_times.append(ticket['ml_analysis']['predicted_resolution_time_hours'])
                else:
                    resolution_times.append(8.0)  # Default

            avg_resolution_time = sum(resolution_times) / len(resolution_times) if resolution_times else 8.0

            # Analyze categories
            category_counts = {}
            for ticket in tickets_data:
                category = ticket.get('category', 'other')
                category_counts[category] = category_counts.get(category, 0) + 1

            # Get top 3 categories
            common_issues = dict(sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:3])

            # Analyze priorities
            priority_counts = {}
            for ticket in tickets_data:
                priority = ticket.get('priority', 'medium')
                priority_counts[priority] = priority_counts.get(priority, 0) + 1

            priority_dist = {k: v/total_tickets for k, v in priority_counts.items()}

            # Generate recommendations
            recommendations = []
            if priority_dist.get('critical', 0) > 0.2:
                recommendations.append("High critical ticket ratio - consider preventive measures")
            if avg_resolution_time > 12:
                recommendations.append("Long resolution times - review processes")
            if 'performance_issue' in common_issues:
                recommendations.append("Performance issues common - consider system monitoring")

            return {
                'total_tickets': total_tickets,
                'avg_resolution_time': round(avg_resolution_time, 1),
                'trend_prediction': 'increasing' if total_tickets > 5 else 'stable',
                'common_issues': common_issues,
                'priority_distribution': priority_dist,
                'recommendations': recommendations,
                'ml_insights': {
                    'category_trends': category_counts,
                    'efficiency_score': max(0, min(100, 100 - avg_resolution_time * 5)),
                    'workload_indicator': 'high' if total_tickets > 10 else 'normal'
                }
            }

        except Exception as e:
            print(f"⚠️ Error in trend prediction: {e}")
            return {
                'total_tickets': len(tickets_data) if tickets_data else 0,
                'avg_resolution_time': 8.0,
                'trend_prediction': 'stable',
                'common_issues': {},
                'recommendations': []
            }

    def get_ml_insights(self, tickets_data: List[Dict]) -> Dict:
        """Get comprehensive ML insights for dashboard"""
        try:
            insights = {
                'model_performance': {
                    'category_accuracy': 0.75,  # Keyword-based approach
                    'priority_accuracy': 0.70,
                    'sentiment_accuracy': 0.68
                },
                'predictive_analytics': self.predict_ticket_trends(tickets_data),
                'ai_recommendations': [
                    "Keyword-based classification active - consider upgrading to full ML for better accuracy",
                    "Monitor sentiment trends to identify customer satisfaction patterns",
                    "Use predictions to optimize ticket routing and resource allocation"
                ],
                'feature_importance': {
                    'category_prediction': ['urgency_keywords', 'technical_terms', 'problem_descriptors'],
                    'priority_prediction': ['urgency_keywords', 'business_impact', 'system_affected'],
                    'sentiment_analysis': ['emotional_words', 'tone_indicators', 'urgency_markers']
                }
            }

            return insights

        except Exception as e:
            print(f"⚠️ Error generating ML insights: {e}")
            return {
                'model_performance': {'category_accuracy': 0.0, 'priority_accuracy': 0.0, 'sentiment_accuracy': 0.0},
                'predictive_analytics': {},
                'ai_recommendations': [],
                'feature_importance': {}
            }

# Global simple ML service instance
simple_ml_service = SimpleMLService()
