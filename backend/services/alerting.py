import os
import smtplib
import json
import requests
from datetime import datetime
from typing import Dict, Any, Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy.orm import Session
from database.connection import SessionLocal
from database.models.alert import Alert, AlertSeverity, AlertStatus

class AlertManager:
    """Alert management service for handling system alerts and notifications."""

    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
        self.smtp_username = os.getenv("SMTP_USERNAME")
        self.smtp_password = os.getenv("SMTP_PASSWORD")
        self.slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")
        self.alert_email = os.getenv("ALERT_EMAIL", "admin@company.com")

    def create_alert(
        self,
        title: str,
        description: str,
        severity: str = "medium",
        source: str = "system",
        metric_name: Optional[str] = None,
        threshold_value: Optional[float] = None,
        current_value: Optional[float] = None,
        hostname: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> int:
        """Create a new alert and send notifications."""
        try:
            db = SessionLocal()

            # Create alert record
            alert = Alert(
                title=title,
                description=description,
                severity=AlertSeverity(severity),
                status=AlertStatus.ACTIVE,
                source=source,
                metric_name=metric_name,
                threshold_value=threshold_value,
                current_value=current_value,
                metadata=json.dumps(metadata) if metadata else None
            )

            db.add(alert)
            db.commit()
            db.refresh(alert)

            # Send notifications
            self._send_notifications(alert)

            return alert.id

        except Exception as e:
            print(f"Error creating alert: {e}")
            return None
        finally:
            db.close()

    def _send_notifications(self, alert: Alert):
        """Send notifications for an alert."""
        try:
            # Send email notification
            if self.smtp_server and self.smtp_username and self.smtp_password:
                self._send_email_alert(alert)

            # Send Slack notification
            if self.slack_webhook_url:
                self._send_slack_alert(alert)

        except Exception as e:
            print(f"Error sending notifications: {e}")

    def _send_email_alert(self, alert: Alert):
        """Send email notification for an alert."""
        try:
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.smtp_username
            msg['To'] = self.alert_email
            msg['Subject'] = f"[{alert.severity.upper()}] {alert.title}"

            # Create email body
            body = f"""
Alert Details:
- Title: {alert.title}
- Description: {alert.description}
- Severity: {alert.severity.upper()}
- Source: {alert.source}
- Timestamp: {alert.timestamp}
- Status: {alert.status}

"""

            if alert.metric_name:
                body += f"- Metric: {alert.metric_name}\n"
            if alert.threshold_value:
                body += f"- Threshold: {alert.threshold_value}\n"
            if alert.current_value:
                body += f"- Current Value: {alert.current_value}\n"

            msg.attach(MIMEText(body, 'plain'))

            # Send email
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            text = msg.as_string()
            server.sendmail(self.smtp_username, self.alert_email, text)
            server.quit()

            # Update alert status
            self._update_alert_notification_status(alert.id, email_sent=True)

        except Exception as e:
            print(f"Error sending email alert: {e}")

    def _send_slack_alert(self, alert: Alert):
        """Send Slack notification for an alert."""
        try:
            # Determine color based on severity
            color_map = {
                "low": "#36a64f",      # Green
                "medium": "#ff9500",   # Orange
                "high": "#ff0000",     # Red
                "critical": "#8b0000"  # Dark red
            }

            color = color_map.get(alert.severity, "#ff9500")

            # Create Slack message
            slack_message = {
                "attachments": [
                    {
                        "color": color,
                        "title": alert.title,
                        "text": alert.description,
                        "fields": [
                            {
                                "title": "Severity",
                                "value": alert.severity.upper(),
                                "short": True
                            },
                            {
                                "title": "Source",
                                "value": alert.source,
                                "short": True
                            },
                            {
                                "title": "Timestamp",
                                "value": alert.timestamp.strftime("%Y-%m-%d %H:%M:%S UTC"),
                                "short": True
                            },
                            {
                                "title": "Status",
                                "value": alert.status.upper(),
                                "short": True
                            }
                        ]
                    }
                ]
            }

            # Add metric information if available
            if alert.metric_name:
                slack_message["attachments"][0]["fields"].append({
                    "title": "Metric",
                    "value": alert.metric_name,
                    "short": True
                })

            if alert.threshold_value and alert.current_value:
                slack_message["attachments"][0]["fields"].append({
                    "title": "Values",
                    "value": f"Current: {alert.current_value}, Threshold: {alert.threshold_value}",
                    "short": False
                })

            # Send to Slack
            response = requests.post(
                self.slack_webhook_url,
                json=slack_message,
                headers={'Content-Type': 'application/json'}
            )

            if response.status_code == 200:
                # Update alert status
                self._update_alert_notification_status(alert.id, slack_sent=True)
            else:
                print(f"Slack notification failed: {response.status_code}")

        except Exception as e:
            print(f"Error sending Slack alert: {e}")

    def _update_alert_notification_status(self, alert_id: int, email_sent: bool = False, slack_sent: bool = False):
        """Update alert notification status."""
        try:
            db = SessionLocal()
            alert = db.query(Alert).filter(Alert.id == alert_id).first()

            if alert:
                if email_sent:
                    alert.email_sent = True
                if slack_sent:
                    alert.slack_sent = True

                db.commit()

        except Exception as e:
            print(f"Error updating alert notification status: {e}")
        finally:
            db.close()

    def acknowledge_alert(self, alert_id: int, user_id: int) -> bool:
        """Acknowledge an alert."""
        try:
            db = SessionLocal()
            alert = db.query(Alert).filter(Alert.id == alert_id).first()

            if alert and alert.status == AlertStatus.ACTIVE:
                alert.status = AlertStatus.ACKNOWLEDGED
                alert.acknowledged_at = datetime.utcnow()
                db.commit()
                return True

            return False

        except Exception as e:
            print(f"Error acknowledging alert: {e}")
            return False
        finally:
            db.close()

    def resolve_alert(self, alert_id: int, user_id: int) -> bool:
        """Resolve an alert."""
        try:
            db = SessionLocal()
            alert = db.query(Alert).filter(Alert.id == alert_id).first()

            if alert and alert.status in [AlertStatus.ACTIVE, AlertStatus.ACKNOWLEDGED]:
                alert.status = AlertStatus.RESOLVED
                alert.resolved_at = datetime.utcnow()
                db.commit()
                return True

            return False

        except Exception as e:
            print(f"Error resolving alert: {e}")
            return False
        finally:
            db.close()

    def get_active_alerts(self) -> list:
        """Get all active alerts."""
        try:
            db = SessionLocal()
            alerts = db.query(Alert).filter(Alert.status == AlertStatus.ACTIVE).all()
            return alerts
        except Exception as e:
            print(f"Error getting active alerts: {e}")
            return []
        finally:
            db.close()

    def get_alert_statistics(self) -> Dict[str, Any]:
        """Get alert statistics."""
        try:
            db = SessionLocal()

            # Count alerts by status
            status_counts = db.query(
                Alert.status,
                db.func.count(Alert.id)
            ).group_by(Alert.status).all()

            # Count alerts by severity
            severity_counts = db.query(
                Alert.severity,
                db.func.count(Alert.id)
            ).group_by(Alert.severity).all()

            # Count alerts by source
            source_counts = db.query(
                Alert.source,
                db.func.count(Alert.id)
            ).group_by(Alert.source).all()

            return {
                "status_counts": dict(status_counts),
                "severity_counts": dict(severity_counts),
                "source_counts": dict(source_counts),
                "total_alerts": db.query(Alert).count()
            }

        except Exception as e:
            print(f"Error getting alert statistics: {e}")
            return {}
        finally:
            db.close()

