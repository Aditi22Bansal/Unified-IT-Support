"""
Database initialization script
"""
import asyncio
from database.prisma_client import db_manager
from services.auth_service import auth_service
import logging

logger = logging.getLogger(__name__)

async def init_database():
    """Initialize database with sample data"""
    try:
        # Connect to database
        await db_manager.connect()
        db = db_manager.prisma

        # Create admin user
        admin_user = await db.user.find_first(where={'username': 'admin'})
        if not admin_user:
            admin_data = {
                'username': 'admin',
                'email': 'admin@itsupport.com',
                'fullName': 'System Administrator',
                'password': 'admin123',
                'role': 'ADMIN'
            }
            admin_user = await auth_service.register_user(admin_data)
            logger.info("Admin user created")

        # Create agent user
        agent_user = await db.user.find_first(where={'username': 'agent'})
        if not agent_user:
            agent_data = {
                'username': 'agent',
                'email': 'agent@itsupport.com',
                'fullName': 'Support Agent',
                'password': 'agent123',
                'role': 'AGENT'
            }
            agent_user = await auth_service.register_user(agent_data)
            logger.info("Agent user created")

        # Create customer user
        customer_user = await db.user.find_first(where={'username': 'customer'})
        if not customer_user:
            customer_data = {
                'username': 'customer',
                'email': 'customer@example.com',
                'fullName': 'John Customer',
                'password': 'customer123',
                'role': 'CUSTOMER'
            }
            customer_user = await auth_service.register_user(customer_data)
            logger.info("Customer user created")

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
            existing_faq = await db.faq.find_first(where={'question': faq_data['question']})
            if not existing_faq:
                await db.faq.create(data=faq_data)

        logger.info("Sample FAQs created")

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
            existing_config = await db.systemconfiguration.find_first(where={'key': config['key']})
            if not existing_config:
                await db.systemconfiguration.create(data=config)

        logger.info("System configuration created")

        print("✅ Database initialized successfully!")
        print("📋 Default users created:")
        print("   - Admin: admin / admin123")
        print("   - Agent: agent / agent123")
        print("   - Customer: customer / customer123")
        print("📚 Sample FAQs and configuration added")

    except Exception as e:
        logger.error(f"Error initializing database: {e}")
        print(f"❌ Error initializing database: {e}")
    finally:
        await db_manager.disconnect()

if __name__ == "__main__":
    asyncio.run(init_database())


