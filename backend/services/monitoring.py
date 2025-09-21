import psutil
import time
import threading
from datetime import datetime
from typing import Dict, Any
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from database.models.system_metric import SystemMetric, SystemLog
from services.alerting import AlertManager

class SystemMonitor:
    """System monitoring service that collects metrics and logs."""

    def __init__(self, alert_manager: AlertManager):
        self.alert_manager = alert_manager
        self.running = False
        self.monitor_thread = None

    def start(self):
        """Start the monitoring service."""
        if not self.running:
            self.running = True
            self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
            self.monitor_thread.start()

    def stop(self):
        """Stop the monitoring service."""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join()

    def _monitor_loop(self):
        """Main monitoring loop."""
        while self.running:
            try:
                self._collect_metrics()
                self._collect_logs()
                time.sleep(30)  # Collect metrics every 30 seconds
            except Exception as e:
                print(f"Error in monitoring loop: {e}")
                time.sleep(60)  # Wait longer on error

    def _collect_metrics(self):
        """Collect system metrics."""
        try:
            db = SessionLocal()

            # Get system metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')

            # Get uptime
            boot_time = psutil.boot_time()
            uptime_seconds = time.time() - boot_time
            uptime_hours = uptime_seconds / 3600

            # Get hostname
            hostname = psutil.os.uname().nodename

            # Store metrics
            metrics = [
                SystemMetric(
                    metric_name="cpu_usage",
                    metric_value=cpu_percent,
                    metric_unit="percentage",
                    hostname=hostname
                ),
                SystemMetric(
                    metric_name="memory_usage",
                    metric_value=memory.percent,
                    metric_unit="percentage",
                    hostname=hostname
                ),
                SystemMetric(
                    metric_name="disk_usage",
                    metric_value=disk.percent,
                    metric_unit="percentage",
                    hostname=hostname
                ),
                SystemMetric(
                    metric_name="uptime_hours",
                    metric_value=uptime_hours,
                    metric_unit="hours",
                    hostname=hostname
                ),
                SystemMetric(
                    metric_name="memory_available",
                    metric_value=memory.available / (1024**3),  # GB
                    metric_unit="GB",
                    hostname=hostname
                ),
                SystemMetric(
                    metric_name="disk_free",
                    metric_value=disk.free / (1024**3),  # GB
                    metric_unit="GB",
                    hostname=hostname
                )
            ]

            for metric in metrics:
                db.add(metric)

            db.commit()

            # Check for threshold alerts
            self._check_thresholds(cpu_percent, memory.percent, disk.percent, hostname)

        except Exception as e:
            print(f"Error collecting metrics: {e}")
        finally:
            db.close()

    def _collect_logs(self):
        """Collect system logs (simulated)."""
        try:
            db = SessionLocal()

            # Simulate log collection
            logs = self._generate_simulated_logs()

            for log_data in logs:
                log = SystemLog(
                    level=log_data["level"],
                    message=log_data["message"],
                    source=log_data["source"],
                    hostname=psutil.os.uname().nodename,
                    metadata=log_data.get("metadata")
                )
                db.add(log)

            db.commit()

        except Exception as e:
            print(f"Error collecting logs: {e}")
        finally:
            db.close()

    def _generate_simulated_logs(self) -> list:
        """Generate simulated system logs."""
        import random

        logs = []

        # Simulate various log types
        log_types = [
            {
                "level": "INFO",
                "message": "System health check completed successfully",
                "source": "health_monitor"
            },
            {
                "level": "INFO",
                "message": "User authentication successful",
                "source": "auth_service"
            },
            {
                "level": "WARNING",
                "message": "High memory usage detected",
                "source": "resource_monitor"
            },
            {
                "level": "ERROR",
                "message": "Database connection timeout",
                "source": "database"
            },
            {
                "level": "INFO",
                "message": "Backup process completed",
                "source": "backup_service"
            }
        ]

        # Randomly select 1-3 logs to generate
        num_logs = random.randint(1, 3)
        selected_logs = random.sample(log_types, num_logs)

        for log in selected_logs:
            logs.append(log)

        return logs

    def _check_thresholds(self, cpu_percent: float, memory_percent: float, disk_percent: float, hostname: str):
        """Check if metrics exceed thresholds and trigger alerts."""
        thresholds = {
            "cpu_usage": 80.0,
            "memory_usage": 85.0,
            "disk_usage": 90.0
        }

        # Check CPU threshold
        if cpu_percent > thresholds["cpu_usage"]:
            self.alert_manager.create_alert(
                title="High CPU Usage Alert",
                description=f"CPU usage is {cpu_percent:.1f}%, exceeding threshold of {thresholds['cpu_usage']}%",
                severity="high",
                source="system_monitor",
                metric_name="cpu_usage",
                threshold_value=thresholds["cpu_usage"],
                current_value=cpu_percent,
                hostname=hostname
            )

        # Check memory threshold
        if memory_percent > thresholds["memory_usage"]:
            self.alert_manager.create_alert(
                title="High Memory Usage Alert",
                description=f"Memory usage is {memory_percent:.1f}%, exceeding threshold of {thresholds['memory_usage']}%",
                severity="high",
                source="system_monitor",
                metric_name="memory_usage",
                threshold_value=thresholds["memory_usage"],
                current_value=memory_percent,
                hostname=hostname
            )

        # Check disk threshold
        if disk_percent > thresholds["disk_usage"]:
            self.alert_manager.create_alert(
                title="High Disk Usage Alert",
                description=f"Disk usage is {disk_percent:.1f}%, exceeding threshold of {thresholds['disk_usage']}%",
                severity="critical",
                source="system_monitor",
                metric_name="disk_usage",
                threshold_value=thresholds["disk_usage"],
                current_value=disk_percent,
                hostname=hostname
            )

def start_monitoring(alert_manager: AlertManager):
    """Start the system monitoring service."""
    monitor = SystemMonitor(alert_manager)
    monitor.start()
    return monitor

