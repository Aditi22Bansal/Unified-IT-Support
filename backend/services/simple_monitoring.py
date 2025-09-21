"""
Simple monitoring service without external dependencies
"""
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def start_monitoring(alert_manager):
    """Start simple monitoring (placeholder)"""
    logger.info("Simple monitoring started")
    pass

def get_system_health() -> Dict[str, Any]:
    """Get basic system health metrics"""
    return {
        "status": "healthy",
        "cpu_usage": 0.0,
        "memory_usage": 0.0,
        "disk_usage": 0.0,
        "timestamp": "2024-01-01T00:00:00Z"
    }
