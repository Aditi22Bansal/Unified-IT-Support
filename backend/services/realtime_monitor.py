"""
Real-time system monitoring service
"""
import asyncio
import psutil
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from database.prisma_client import get_database
import logging

logger = logging.getLogger(__name__)

class RealtimeMonitor:
    def __init__(self):
        self.monitoring = False
        self.monitor_task = None
        self.alert_thresholds = {
            'cpu': 80.0,
            'memory': 85.0,
            'disk': 90.0,
            'response_time': 5.0
        }
        self.metrics_history = []
        self.max_history = 1000

    async def start_monitoring(self):
        """Start real-time monitoring"""
        if self.monitoring:
            return

        self.monitoring = True
        self.monitor_task = asyncio.create_task(self._monitor_loop())
        logger.info("Real-time monitoring started")

    async def stop_monitoring(self):
        """Stop real-time monitoring"""
        self.monitoring = False
        if self.monitor_task:
            self.monitor_task.cancel()
            try:
                await self.monitor_task
            except asyncio.CancelledError:
                pass
        logger.info("Real-time monitoring stopped")

    async def _monitor_loop(self):
        """Main monitoring loop"""
        while self.monitoring:
            try:
                await self._collect_metrics()
                await self._check_thresholds()
                await asyncio.sleep(5)  # Monitor every 5 seconds
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(10)  # Wait longer on error

    async def _collect_metrics(self):
        """Collect system metrics"""
        try:
            # Get system metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            # Calculate network I/O
            net_io = psutil.net_io_counters()

            # Get boot time for uptime calculation
            boot_time = psutil.boot_time()
            uptime_seconds = time.time() - boot_time

            metrics = {
                'timestamp': datetime.now(),
                'cpu_usage': cpu_percent,
                'memory_usage': memory.percent,
                'memory_available': memory.available / (1024**3),  # GB
                'memory_total': memory.total / (1024**3),  # GB
                'disk_usage': disk.percent,
                'disk_free': disk.free / (1024**3),  # GB
                'disk_total': disk.total / (1024**3),  # GB
                'uptime_hours': uptime_seconds / 3600,
                'network_bytes_sent': net_io.bytes_sent,
                'network_bytes_recv': net_io.bytes_recv,
                'process_count': len(psutil.pids())
            }

            # Store in database
            await self._store_metrics(metrics)

            # Add to history
            self.metrics_history.append(metrics)
            if len(self.metrics_history) > self.max_history:
                self.metrics_history.pop(0)

        except Exception as e:
            logger.error(f"Error collecting metrics: {e}")

    async def _store_metrics(self, metrics: Dict):
        """Store metrics in database"""
        try:
            db = await get_database()

            # Store CPU metric
            await db.systemmetric.create(data={
                'metricType': 'cpu',
                'value': metrics['cpu_usage'],
                'unit': '%',
                'timestamp': metrics['timestamp']
            })

            # Store Memory metric
            await db.systemmetric.create(data={
                'metricType': 'memory',
                'value': metrics['memory_usage'],
                'unit': '%',
                'timestamp': metrics['timestamp']
            })

            # Store Disk metric
            await db.systemmetric.create(data={
                'metricType': 'disk',
                'value': metrics['disk_usage'],
                'unit': '%',
                'timestamp': metrics['timestamp']
            })

        except Exception as e:
            logger.error(f"Error storing metrics: {e}")

    async def _check_thresholds(self):
        """Check if any metrics exceed thresholds"""
        if not self.metrics_history:
            return

        latest = self.metrics_history[-1]

        # Check CPU threshold
        if latest['cpu_usage'] > self.alert_thresholds['cpu']:
            await self._create_alert(
                title="High CPU Usage",
                message=f"CPU usage is {latest['cpu_usage']:.1f}%, exceeding threshold of {self.alert_thresholds['cpu']}%",
                severity="HIGH",
                source="system",
                threshold=self.alert_thresholds['cpu'],
                current_value=latest['cpu_usage']
            )

        # Check Memory threshold
        if latest['memory_usage'] > self.alert_thresholds['memory']:
            await self._create_alert(
                title="High Memory Usage",
                message=f"Memory usage is {latest['memory_usage']:.1f}%, exceeding threshold of {self.alert_thresholds['memory']}%",
                severity="HIGH",
                source="system",
                threshold=self.alert_thresholds['memory'],
                current_value=latest['memory_usage']
            )

        # Check Disk threshold
        if latest['disk_usage'] > self.alert_thresholds['disk']:
            await self._create_alert(
                title="High Disk Usage",
                message=f"Disk usage is {latest['disk_usage']:.1f}%, exceeding threshold of {self.alert_thresholds['disk']}%",
                severity="CRITICAL",
                source="system",
                threshold=self.alert_thresholds['disk'],
                current_value=latest['disk_usage']
            )

    async def _create_alert(self, title: str, message: str, severity: str,
                          source: str, threshold: float, current_value: float):
        """Create a new alert"""
        try:
            db = await get_database()

            # Check if similar alert already exists and is active
            existing_alert = await db.alert.find_first(
                where={
                    'title': title,
                    'status': 'ACTIVE',
                    'createdAt': {
                        'gte': datetime.now() - timedelta(minutes=5)  # Within last 5 minutes
                    }
                }
            )

            if existing_alert:
                return  # Don't create duplicate alerts

            await db.alert.create(data={
                'title': title,
                'message': message,
                'severity': severity,
                'source': source,
                'threshold': threshold,
                'currentValue': current_value
            })

            logger.warning(f"Alert created: {title}")

        except Exception as e:
            logger.error(f"Error creating alert: {e}")

    async def get_current_metrics(self) -> Dict:
        """Get current system metrics"""
        if not self.metrics_history:
            return {}
        return self.metrics_history[-1]

    async def get_metrics_history(self, hours: int = 24) -> List[Dict]:
        """Get metrics history for specified hours"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        return [m for m in self.metrics_history if m['timestamp'] >= cutoff_time]

    async def get_alerts(self, limit: int = 50) -> List[Dict]:
        """Get recent alerts"""
        try:
            db = await get_database()
            alerts = await db.alert.find_many(
                take=limit,
                order_by={'createdAt': 'desc'}
            )
            return alerts
        except Exception as e:
            logger.error(f"Error getting alerts: {e}")
            return []

    async def update_thresholds(self, thresholds: Dict[str, float]):
        """Update alert thresholds"""
        self.alert_thresholds.update(thresholds)
        logger.info(f"Alert thresholds updated: {thresholds}")

# Global monitor instance
realtime_monitor = RealtimeMonitor()


