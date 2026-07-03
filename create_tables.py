import asyncio
from infrastructure.database.connection import create_pool, close_pool
from infrastructure.database.create_tables import create_tables
  
async def main():
    await create_pool()
    await create_tables()
    await close_pool()

asyncio.run(main())

