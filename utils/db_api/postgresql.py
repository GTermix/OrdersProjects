from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
            port=5432
        )

    async def execute(
            self,
            command,
            *args,
            fetch: bool = False,
            fetchval: bool = False,
            fetchrow: bool = False,
            execute: bool = False,
    ):
        async with self.pool.acquire() as connection:
            connection: Connection
            async with connection.transaction():
                if fetch:
                    result = await connection.fetch(command, *args)
                elif fetchval:
                    result = await connection.fetchval(command, *args)
                elif fetchrow:
                    result = await connection.fetchrow(command, *args)
                elif execute:
                    result = await connection.execute(command, *args)
            return result

    async def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(255) NOT NULL,
        username varchar(255) NULL,
        telegram_id BIGINT NOT NULL UNIQUE
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_category(self):
        sql = """
        CREATE TABLE IF NOT EXISTS category (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL unique
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_product(self):
        """Productlar jadvalini yaratish"""
        sql = """
        CREATE TABLE IF NOT EXISTS product (
        id SERIAL PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        description TEXT NULL,
        category_id INT NOT NULL,
        image_url text NOT NULL,
        price NUMERIC NOT NULL,
        discount NUMERIC DEFAULT 0
        );
        """
        await self.execute(sql, execute=True)

    async def create_table_order(self):
        sql = """
        CREATE TABLE IF NOT EXISTS order (
        user_id INT NOT NULL,
        product_id INT NOT NULL,
        count INT NOT NULL DEFAULT 1
        );
        """
        await self.execute(sql, execute=True)

    async def get_data_from_user(self):
        sql = "SELECT * FROM users"
        return await self.execute(sql, execute=True)

    async def get_data_from_product(self):
        sql = "SELECT * FROM product"
        return await self.execute(sql, fetchrow=True, execute=True)

    async def get_data_from_category(self):
        sql = "SELECT * FROM category"
        return await self.execute(sql, fetch=True, execute=True)

    async def get_data_from_category_id(self, title):
        sql = "SELECT id FROM category WHERE title=$1"
        return await self.execute(sql, title, fetchval=True, execute=True)

    async def get_data_from_category_title(self, id):
        sql = "SELECT title FROM category WHERE id=$1"
        return await self.execute(sql, id, fetchval=True, execute=True)

    async def get_data_from_product_title(self, cat_id):
        sql = "SELECT title FROM product WHERE category_id=$1"
        return await self.execute(sql, cat_id, fetch=True, execute=True)

    async def add_product(self, title, description, category_id, image_url, price, discount):
        sql = "INSERT INTO product (title, description, category_id, image_url, price, discount) VALUES($1, $2, $3, " \
              "$4, $5,$6) returning *"
        return await self.execute(sql, title, description, category_id, image_url, price, discount, fetchrow=True)

    async def add_category(self, title: str):
        sql = "INSERT INTO category (title) VALUES($1) returning *"
        await self.execute(sql, title, fetchrow=True)

    async def add_order(self, user_id, product_id, count=1):
        sql = "INSERT INTO order (user_id, product_id, count) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, user_id, product_id, count, fetchrow=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO users (full_name, username, telegram_id) VALUES($1, $2, $3) returning *"
        return await self.execute(sql, full_name, username, telegram_id, fetchrow=True)

    async def select_all_users(self):
        sql = "SELECT * FROM Users"
        return await self.execute(sql, fetch=True)

    async def select_user(self, **kwargs):
        sql = "SELECT * FROM Users WHERE "
        sql, parameters = self.format_args(sql, parameters=kwargs)
        return await self.execute(sql, *parameters, fetchrow=True)

    async def count_users(self):
        sql = "SELECT COUNT(*) FROM Users"
        return await self.execute(sql, fetchval=True)

    async def update_user_username(self, username, telegram_id):
        sql = "UPDATE Users SET username=$1 WHERE telegram_id=$2"
        return await self.execute(sql, username, telegram_id, execute=True)

    async def backup_products_to_category(self, base, copy):
        sql = f"UPDATE product SET category_id={int(copy)} WHERE category_id={int(base)}"
        return await self.execute(sql, execute=True)

    async def delete_users(self):
        await self.execute("DELETE FROM Users WHERE TRUE", execute=True)

    async def delete_category(self, id):
        await self.execute("DELETE FROM category WHERE id=$1", id, execute=True)

    async def delete_product(self, id):
        await self.execute("DELETE FROM product WHERE id=$1", id, execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)
