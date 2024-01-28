import asyncpg
import asyncio
from data import config

class Database:
    def __init__(self):
        loop = asyncio.get_event_loop()
        self.pool: asyncpg.pool.Pool = loop.run_until_complete(
            asyncpg.create_pool(
                user=config.PGUSER,
                database=config.DBNAME,
                password=config.PGPASSWORD,
                host=config.IP,
                port=config.DBPORT,
                loop=loop
            )
        )

    async def user_info(self, id, zhanr, book_author,title_book):
        sql = 'INSERT INTO "user_info" (id, zhanr, book_author, title_book) VALUES($1, $2, $3, $4)'
        await self.pool.execute(sql, id, zhanr, book_author,title_book)






