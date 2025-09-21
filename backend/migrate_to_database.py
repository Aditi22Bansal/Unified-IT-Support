#!/usr/bin/env python3
"""
Migration script to move from in-memory storage to database storage
This script helps users transition from simple_main_enhanced.py to main_dynamic.py
"""

import asyncio
import json
import os
from datetime import datetime
from database.prisma_client import db_manager
from services.auth_service import auth_service

async def migrate_to_database():
    """Migrate from in-memory storage to database storage"""
    print("🔄 Starting migration from in-memory storage to database...")

    try:
        # Connect to database
        await db_manager.connect()
        db = db_manager.prisma

        print("✅ Database connected successfully")

        # Check if database is already initialized
        existing_users = await db.user.find_many()
        if existing_users:
            print("ℹ️  Database already contains data. Skipping migration.")
            print(f"   Found {len(existing_users)} existing users")
            return

        # Initialize database with sample data
        print("🌱 Initializing database with sample data...")

        # Create admin user
        admin_data = {
            'username': 'admin',
            'email': 'admin@itsupport.com',
            'fullName': 'System Administrator',
            'password': 'admin123',
            'role': 'ADMIN'
        }
        admin_user = await auth_service.register_user(admin_data)
        print("✅ Admin user created")

        # Create agent user
        agent_data = {
            'username': 'agent',
            'email': 'agent@itsupport.com',
            'fullName': 'Support Agent',
            'password': 'agent123',
            'role': 'AGENT'
        }
        agent_user = await auth_service.register_user(agent_data)
        print("✅ Agent user created")

        # Create customer user
        customer_data = {
            'username': 'customer',
            'email': 'customer@example.com',
            'fullName': 'John Customer',
            'password': 'customer123',
            'role': 'CUSTOMER'
        }
        customer_user = await auth_service.register_user(customer_data)
        print("✅ Customer user created")

        # Create sample tickets
        sample_tickets = [
            {
                'title': 'Server Performance Issue',
                'description': 'The production server is running slowly and affecting user experience.',
                'priority': 'HIGH',
                'status': 'OPEN',
                'category': 'Hardware',
                'createdBy': customer_user['id'],
                'tags': json.dumps(['server', 'performance', 'urgent'])
            },
            {
                'title': 'Email Configuration Help',
                'description': 'Need help setting up email client with new server settings.',
                'priority': 'MEDIUM',
                'status': 'IN_PROGRESS',
                'category': 'Email',
                'createdBy': customer_user['id'],
                'assignedTo': agent_user['id'],
                'tags': json.dumps(['email', 'configuration', 'setup'])
            },
            {
                'title': 'Software Installation Request',
                'description': 'Request to install new development tools on workstation.',
                'priority': 'LOW',
                'status': 'PENDING_APPROVAL',
                'category': 'Software',
                'createdBy': customer_user['id'],
                'tags': json.dumps(['software', 'installation', 'development'])
            }
        ]

        for ticket_data in sample_tickets:
            await db.ticket.create(data=ticket_data)

        print("✅ Sample tickets created")

        # Create sample FAQs
        sample_faqs = [
            {
                'question': 'How do I reset my password?',
                'answer': 'To reset your password, go to the login page and click "Forgot Password". You\'ll receive an email with reset instructions.',
                'category': 'Account'
            },
            {
                'question': 'Why can\'t I log in?',
                'answer': 'If you\'re having trouble logging in, make sure you\'re using the correct username and password. Check if Caps Lock is on.',
                'category': 'Account'
            },
            {
                'question': 'How do I access my email?',
                'answer': 'You can access your email through the web interface or by configuring an email client with the provided settings.',
                'category': 'Email'
            },
            {
                'question': 'What should I do if my computer is slow?',
                'answer': 'Try restarting your computer, closing unnecessary programs, and checking for available disk space. If problems persist, contact IT support.',
                'category': 'Hardware'
            },
            {
                'question': 'How do I install software?',
                'answer': 'For software installation, ensure you have administrator privileges and sufficient disk space. Contact IT support for restricted software.',
                'category': 'Software'
            }
        ]

        for faq_data in sample_faqs:
            await db.faq.create(data=faq_data)

        print("✅ Sample FAQs created")

        # Create system configuration
        configs = [
            {'key': 'system_name', 'value': 'IT Support System', 'type': 'string', 'category': 'general'},
            {'key': 'max_tickets_per_agent', 'value': '10', 'type': 'number', 'category': 'tickets'},
            {'key': 'sla_critical_hours', 'value': '1', 'type': 'number', 'category': 'sla'},
            {'key': 'sla_high_hours', 'value': '4', 'type': 'number', 'category': 'sla'},
            {'key': 'sla_medium_hours', 'value': '24', 'type': 'number', 'category': 'sla'},
            {'key': 'sla_low_hours', 'value': '72', 'type': 'number', 'category': 'sla'},
            {'key': 'cpu_threshold', 'value': '80', 'type': 'number', 'category': 'monitoring'},
            {'key': 'memory_threshold', 'value': '85', 'type': 'number', 'category': 'monitoring'},
            {'key': 'disk_threshold', 'value': '90', 'type': 'number', 'category': 'monitoring'}
        ]

        for config in configs:
            await db.systemconfiguration.create(data=config)

        print("✅ System configuration created")

        print("\n🎉 Migration completed successfully!")
        print("📋 Default users created:")
        print("   - Admin: admin / admin123")
        print("   - Agent: agent / agent123")
        print("   - Customer: customer / customer123")
        print("📚 Sample tickets, FAQs and configuration added")
        print("\n💡 Next steps:")
        print("   1. Run: python main_dynamic.py (instead of simple_main_enhanced.py)")
        print("   2. Your tickets will now persist across server restarts!")
        print("   3. Use start_dynamic_system.bat for easy startup")

    except Exception as e:
        print(f"❌ Migration failed: {e}")
        print("Please check your database setup and try again.")
    finally:
        await db_manager.disconnect()

if __name__ == "__main__":
    asyncio.run(migrate_to_database())
