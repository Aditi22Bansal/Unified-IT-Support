"""
Prisma database client and connection management
"""
import asyncio
from prisma import Prisma
from prisma.errors import PrismaError
import logging

logger = logging.getLogger(__name__)

class DatabaseManager:
    def __init__(self):
        self.prisma = Prisma()
        self._connected = False

    async def connect(self):
        """Connect to the database"""
        try:
            await self.prisma.connect()
            self._connected = True
            logger.info("Database connected successfully")
        except PrismaError as e:
            logger.error(f"Failed to connect to database: {e}")
            raise

    async def disconnect(self):
        """Disconnect from the database"""
        try:
            await self.prisma.disconnect()
            self._connected = False
            logger.info("Database disconnected")
        except PrismaError as e:
            logger.error(f"Error disconnecting from database: {e}")

    async def health_check(self):
        """Check database health"""
        try:
            await self.prisma.user.find_first()
            return True
        except Exception as e:
            logger.error(f"Database health check failed: {e}")
            return False

    @property
    def is_connected(self):
        return self._connected

# Global database manager instance
db_manager = DatabaseManager()

# Dependency to get database instance
async def get_database():
    if not db_manager.is_connected:
        await db_manager.connect()
    return db_manager.prisma


