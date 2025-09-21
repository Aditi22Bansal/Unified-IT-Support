from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from sqlalchemy.sql import func
from database.connection import Base

class SystemMetric(Base):
    __tablename__ = "system_metrics"

    id = Column(Integer, primary_key=True, index=True)
    metric_name = Column(String(100), nullable=False)  # cpu_usage, memory_usage, disk_usage, etc.
    metric_value = Column(Float, nullable=False)
    metric_unit = Column(String(20), nullable=False)  # percentage, bytes, seconds, etc.
    hostname = Column(String(100), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    meta_data = Column(Text, nullable=True)  # JSON string for additional data

    def __repr__(self):
        return f"<SystemMetric(id={self.id}, name='{self.metric_name}', value={self.metric_value}, hostname='{self.hostname}')>"

class SystemLog(Base):
    __tablename__ = "system_logs"

    id = Column(Integer, primary_key=True, index=True)
    level = Column(String(20), nullable=False)  # INFO, WARNING, ERROR, CRITICAL
    message = Column(Text, nullable=False)
    source = Column(String(100), nullable=False)  # application, system, service name
    hostname = Column(String(100), nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    meta_data = Column(Text, nullable=True)  # JSON string for additional data

    def __repr__(self):
        return f"<SystemLog(id={self.id}, level='{self.level}', message='{self.message[:50]}...', hostname='{self.hostname}')>"

