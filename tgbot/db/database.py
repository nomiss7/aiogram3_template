import aiosqlite
import os


class MyDb:
    __dbname__ = "/app/db/db.db"

    async def db_setup(self):
        async with aiosqlite.connect(self.__dbname__) as db:
            async with db.cursor() as cursor:
                await cursor.execute(
                    "CREATE TABLE IF NOT EXISTS user(user_id INTEGER PRIMARY KEY UNIQUE NOT NULL, "
                    "username TEXT, "
                    "fullname TEXT, "
                    "last_public_time DATETIME , "
                    "is_active BOOLEAN)")
                await db.commit()

    async def sql_create_user(self, user_id=int, username=str, fullname=str, is_active=bool):
        async with aiosqlite.connect(self.__dbname__) as db:
            async with db.execute("SELECT user_id FROM user WHERE user_id = ?", (user_id,)) as cursor:
                existing_user = await cursor.fetchone()

                if existing_user is None:
                    await db.execute("INSERT INTO user (user_id, username, fullname, is_active) VALUES (?, ?, ?, ?)",
                                     (user_id, username, fullname, is_active))
                    await db.commit()
                return user_id

    async def sql_get_users(self):
        async with aiosqlite.connect(self.__dbname__) as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT user_id FROM user WHERE is_active = True")
                return await cursor.fetchall()

    async def sql_update_user_status(self, is_active, user_id):
        async with aiosqlite.connect(self.__dbname__) as db:
            await db.execute("UPDATE user SET is_active=? WHERE user_id=? ", (is_active, user_id))
            await db.commit()

    async def sql_update_user_last_public_time(self, last_public_time, user_id):
        async with aiosqlite.connect(self.__dbname__) as db:
            await db.execute("UPDATE user SET last_public_time=? WHERE user_id=? ", (last_public_time, user_id))
            await db.commit()

    async def sql_get_last_public_time(self, user_id):
        async with aiosqlite.connect(self.__dbname__) as db:
            async with db.cursor() as cursor:
                await cursor.execute("SELECT last_public_time FROM user WHERE user_id=?", (user_id,))
                last_public_time = await cursor.fetchone()
                if last_public_time:
                    return last_public_time[0]
                return False
