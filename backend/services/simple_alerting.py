"""
Simple alerting service without external dependencies
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class AlertManager:
    """Simple alert manager"""

    def __init__(self):
        self.alerts = []

    def create_alert(self, title: str, message: str, severity: str = "medium"):
        """Create a new alert"""
        alert = {
            "title": title,
            "message": message,
            "severity": severity,
            "timestamp": "2024-01-01T00:00:00Z"
        }
        self.alerts.append(alert)
        logger.info(f"Alert created: {title}")

    def get_alerts(self):
        """Get all alerts"""
        return self.alerts
