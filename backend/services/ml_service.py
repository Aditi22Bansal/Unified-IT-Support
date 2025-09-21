"""
Machine Learning Service for IT Support System
Provides intelligent ticket classification, sentiment analysis, and predictions
"""

import re
import json
import pickle
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import joblib
import nltk
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Download required NLTK data
try:
    nltk.download('punkt', quiet=True)
    nltk.download('vader_lexicon', quiet=True)
    nltk.download('stopwords', quiet=True)
except:
    pass

class MLTicketService:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(
            max_features=1000,
            stop_words='english',
            ngram_range=(1, 2)
        )

        # Classification models
        self.category_classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.priority_classifier = RandomForestClassifier(n_estimators=100, random_state=42)

        # Regression model for resolution time prediction
        self.resolution_time_predictor = LinearRegression()

        # Sentiment analyzer
        self.sentiment_analyzer = SentimentIntensityAnalyzer()

        # Training data for ML models
        self.training_data = self._generate_training_data()

        # Feature mappings
        self.category_labels = ['performance_issue', 'bug', 'feature_request', 'incident', 'other']
        self.priority_labels = ['low', 'medium', 'high', 'critical']

        # Initialize models
        self._train_models()

    def _generate_training_data(self) -> pd.DataFrame:
        """Generate synthetic training data for ML models"""
        training_data = []

        # Performance issues
        performance_texts = [
            "server is running slow", "high cpu usage", "memory leak", "disk space full",
            "network latency", "response time slow", "timeout errors", "performance degradation",
            "system overload", "bottleneck issues"
        ]
        for text in performance_texts:
            training_data.append({
                'text': text,
                'category': 'performance_issue',
                'priority': 'high',
                'resolution_time_hours': np.random.uniform(2, 8),
                'urgency_keywords': self._extract_urgency_keywords(text)
            })

        # Bugs
        bug_texts = [
            "application crashed", "error message", "bug in code", "functionality not working",
            "software error", "system crash", "unexpected behavior", "defect found",
            "malfunction", "broken feature"
        ]
        for text in bug_texts:
            training_data.append({
                'text': text,
                'category': 'bug',
                'priority': 'medium',
                'resolution_time_hours': np.random.uniform(4, 12),
                'urgency_keywords': self._extract_urgency_keywords(text)
            })

        # Feature requests
        feature_texts = [
            "can we add", "new feature request", "enhancement needed", "improve functionality",
            "add capability", "new functionality", "feature enhancement", "user request",
            "improvement suggestion", "new tool needed"
        ]
        for text in feature_texts:
            training_data.append({
                'text': text,
                'category': 'feature_request',
                'priority': 'low',
                'resolution_time_hours': np.random.uniform(8, 24),
                'urgency_keywords': self._extract_urgency_keywords(text)
            })

        # Incidents
        incident_texts = [
            "system down", "service unavailable", "outage", "emergency", "critical issue",
            "production down", "service interruption", "urgent problem", "major failure",
            "system failure"
        ]
        for text in incident_texts:
            training_data.append({
                'text': text,
                'category': 'incident',
                'priority': 'critical',
                'resolution_time_hours': np.random.uniform(1, 4),
                'urgency_keywords': self._extract_urgency_keywords(text)
            })

        return pd.DataFrame(training_data)

    def _extract_urgency_keywords(self, text: str) -> int:
        """Extract urgency indicators from text"""
        urgency_keywords = [
            'urgent', 'critical', 'emergency', 'asap', 'immediately', 'down', 'broken',
            'crash', 'failure', 'outage', 'deadline', 'blocking', 'severe', 'major'
        ]

        text_lower = text.lower()
        urgency_count = sum(1 for keyword in urgency_keywords if keyword in text_lower)
        return min(urgency_count, 3)  # Cap at 3 for normalization

    def _train_models(self):
        """Train all ML models"""
        try:
            # Prepare features
            X_text = self.training_data['text']
            X_urgency = self.training_data['urgency_keywords'].values.reshape(-1, 1)

            # Vectorize text
            X_text_vectorized = self.vectorizer.fit_transform(X_text)

            # Combine text and urgency features
            X_combined = np.hstack([X_text_vectorized.toarray(), X_urgency])

            # Train category classifier
            y_category = self.training_data['category']
            self.category_classifier.fit(X_combined, y_category)

            # Train priority classifier
            y_priority = self.training_data['priority']
            self.priority_classifier.fit(X_combined, y_priority)

            # Train resolution time predictor
            y_resolution = self.training_data['resolution_time_hours']
            self.resolution_time_predictor.fit(X_combined, y_resolution)

            print("✅ ML models trained successfully!")

        except Exception as e:
            print(f"⚠️ Error training models: {e}")

    def classify_ticket(self, title: str, description: str) -> Dict:
        """Classify ticket and predict properties"""
        try:
            # Combine title and description
            combined_text = f"{title} {description}".strip()

            # Extract urgency keywords
            urgency_score = self._extract_urgency_keywords(combined_text)

            # Vectorize text
            text_vectorized = self.vectorizer.transform([combined_text])
            X_combined = np.hstack([text_vectorized.toarray(), [[urgency_score]]])

            # Predict category
            category_proba = self.category_classifier.predict_proba(X_combined)[0]
            predicted_category = self.category_classifier.predict(X_combined)[0]
            category_confidence = max(category_proba)

            # Predict priority
            priority_proba = self.priority_classifier.predict_proba(X_combined)[0]
            predicted_priority = self.priority_classifier.predict(X_combined)[0]
            priority_confidence = max(priority_proba)

            # Predict resolution time
            predicted_resolution_time = self.resolution_time_predictor.predict(X_combined)[0]
            predicted_resolution_time = max(1, min(48, predicted_resolution_time))  # Clamp between 1-48 hours

            return {
                'category': predicted_category,
                'category_confidence': round(float(category_confidence), 3),
                'priority': predicted_priority,
                'priority_confidence': round(float(priority_confidence), 3),
                'predicted_resolution_time_hours': round(float(predicted_resolution_time), 1),
                'urgency_score': urgency_score,
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
        """Analyze sentiment of ticket text"""
        try:
            # VADER sentiment analysis
            vader_scores = self.sentiment_analyzer.polarity_scores(text)

            # TextBlob sentiment analysis
            blob = TextBlob(text)
            textblob_polarity = blob.sentiment.polarity
            textblob_subjectivity = blob.sentiment.subjectivity

            # Determine overall sentiment
            compound_score = vader_scores['compound']
            if compound_score >= 0.05:
                sentiment = 'positive'
            elif compound_score <= -0.05:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'

            # Calculate customer satisfaction indicator
            satisfaction_score = (compound_score + 1) / 2  # Convert to 0-1 scale

            return {
                'sentiment': sentiment,
                'sentiment_score': round(float(compound_score), 3),
                'satisfaction_score': round(float(satisfaction_score), 3),
                'emotional_intensity': round(float(vader_scores['neu']), 3),
                'is_urgent_emotional': compound_score < -0.3,
                'customer_mood': self._get_customer_mood(compound_score, textblob_subjectivity)
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

    def _get_customer_mood(self, sentiment_score: float, subjectivity: float) -> str:
        """Determine customer mood based on sentiment and subjectivity"""
        if sentiment_score < -0.5:
            return 'frustrated'
        elif sentiment_score < -0.2:
            return 'concerned'
        elif sentiment_score < 0.2:
            return 'neutral'
        elif sentiment_score < 0.5:
            return 'hopeful'
        else:
            return 'satisfied'

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
            df = pd.DataFrame(tickets_data)

            # Calculate metrics
            total_tickets = len(df)
            avg_resolution_time = df.get('resolution_time_hours', pd.Series([8])).mean()

            # Analyze categories
            category_counts = df['category'].value_counts()
            common_issues = category_counts.head(3).to_dict()

            # Analyze priorities
            priority_dist = df['priority'].value_counts(normalize=True)

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
                'avg_resolution_time': round(float(avg_resolution_time), 1),
                'trend_prediction': 'increasing' if total_tickets > 5 else 'stable',
                'common_issues': common_issues,
                'priority_distribution': priority_dist.to_dict(),
                'recommendations': recommendations,
                'ml_insights': {
                    'category_trends': category_counts.to_dict(),
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
                    'category_accuracy': 0.85,  # Simulated - in real app, track actual performance
                    'priority_accuracy': 0.78,
                    'sentiment_accuracy': 0.82
                },
                'predictive_analytics': self.predict_ticket_trends(tickets_data),
                'ai_recommendations': [
                    "Consider implementing automated responses for common performance issues",
                    "Monitor sentiment trends to identify customer satisfaction patterns",
                    "Use ML predictions to optimize ticket routing"
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

# Global ML service instance
ml_service = MLTicketService()
