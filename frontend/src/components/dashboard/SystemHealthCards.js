import React from 'react';
import {
  Cpu,
  HardDrive,
  MemoryStick,
  Clock,
  AlertTriangle,
  Ticket
} from 'lucide-react';

const SystemHealthCards = ({ data = {} }) => {
  const cards = [
    {
      title: 'CPU Usage',
      value: `${(data.cpu_usage || 0).toFixed(1)}%`,
      icon: Cpu,
      color: (data.cpu_usage || 0) > 80 ? 'text-danger-600' : (data.cpu_usage || 0) > 60 ? 'text-warning-600' : 'text-success-600',
      bgColor: (data.cpu_usage || 0) > 80 ? 'bg-danger-50' : (data.cpu_usage || 0) > 60 ? 'bg-warning-50' : 'bg-success-50',
    },
    {
      title: 'Memory Usage',
      value: `${(data.memory_usage || 0).toFixed(1)}%`,
      icon: MemoryStick,
      color: (data.memory_usage || 0) > 85 ? 'text-danger-600' : (data.memory_usage || 0) > 70 ? 'text-warning-600' : 'text-success-600',
      bgColor: (data.memory_usage || 0) > 85 ? 'bg-danger-50' : (data.memory_usage || 0) > 70 ? 'bg-warning-50' : 'bg-success-50',
    },
    {
      title: 'Disk Usage',
      value: `${(data.disk_usage || 0).toFixed(1)}%`,
      icon: HardDrive,
      color: (data.disk_usage || 0) > 90 ? 'text-danger-600' : (data.disk_usage || 0) > 75 ? 'text-warning-600' : 'text-success-600',
      bgColor: (data.disk_usage || 0) > 90 ? 'bg-danger-50' : (data.disk_usage || 0) > 75 ? 'bg-warning-50' : 'bg-success-50',
    },
    {
      title: 'Uptime',
      value: `${(data.uptime_hours || 0).toFixed(1)}h`,
      icon: Clock,
      color: 'text-primary-600',
      bgColor: 'bg-primary-50',
    },
    {
      title: 'Active Alerts',
      value: (data.active_alerts || 0).toString(),
      icon: AlertTriangle,
      color: (data.active_alerts || 0) > 0 ? 'text-danger-600' : 'text-success-600',
      bgColor: (data.active_alerts || 0) > 0 ? 'bg-danger-50' : 'bg-success-50',
    },
    {
      title: 'System Status',
      value: data.status || 'Unknown',
      icon: data.status === 'operational' ? Cpu : AlertTriangle,
      color: data.status === 'operational' ? 'text-success-600' : 'text-danger-600',
      bgColor: data.status === 'operational' ? 'bg-success-50' : 'bg-danger-50',
    },
  ];

  return (
    <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-3">
      {cards.map((card, index) => {
        const Icon = card.icon;
        return (
          <div key={index} className="card p-6">
            <div className="flex items-center">
              <div className={`flex-shrink-0 p-3 rounded-lg ${card.bgColor}`}>
                <Icon className={`h-6 w-6 ${card.color}`} />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">{card.title}</p>
                <p className={`text-2xl font-semibold ${card.color}`}>
                  {card.value}
                </p>
              </div>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default SystemHealthCards;

