from typing import Union

import asyncpg
from asyncpg import Connection
from asyncpg.pool import Pool

from data import config
from data.config import ADMINS


class Database:
    def __init__(self):
        self.pool: Union[Pool, None] = None

    async def create(self):
        self.pool = await asyncpg.create_pool(
            user=config.DB_USER,
            password=config.DB_PASS,
            host=config.DB_HOST,
            database=config.DB_NAME,
            port=5433
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
        telegram_id BIGINT NOT NULL UNIQUE,
        lang_code VARCHAR(4) NOT NULL
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

    async def create_table_admins(self):
        sql = """
            CREATE TABLE IF NOT EXISTS admins_table (
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT NOT NULL UNIQUE
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
        CREATE TABLE IF NOT EXISTS order_table (
        user_id BIGINT NOT NULL,
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

    @staticmethod
    async def format_admins_sql(sql_code: str, admins: list, command: str):
        if len(admins) > 0:
            sql_code += f"{command}={admins[0]} "
            admins = admins[1:]
            for i in admins:
                sql_code += f"AND NOT {command}={i}"
        else:
            sql_code += f"{command}={admins[0]}"
        return sql_code

    async def get_data_from_user_id(self):
        sql_code = "SELECT telegram_id FROM users WHERE NOT "
        sql = await self.format_admins_sql(sql_code, ADMINS, "telegram_id")
        return await self.execute(sql, fetch=True, execute=True)

    async def get_data_from_category_id(self, title):
        sql = "SELECT id FROM category WHERE title=$1"
        return await self.execute(sql, title, fetchval=True, execute=True)

    async def get_data_from_category_title(self, id_1):
        sql = "SELECT title FROM category WHERE id=$1"
        return await self.execute(sql, id_1, fetchval=True, execute=True)

    async def get_data_from_product_title(self, cat_id):
        sql = "SELECT title FROM product WHERE category_id=$1"
        return await self.execute(sql, cat_id, fetch=True, execute=True)

    async def get_data_from_product_title_id(self, pro_id):
        sql = "SELECT title FROM product WHERE id=$1"
        return await self.execute(sql, pro_id, fetchval=True, execute=True)

    async def get_data_from_product_cart(self, pro_id):
        sql = "SELECT title,price,discount FROM product WHERE id=$1"
        return await self.execute(sql, pro_id, fetch=True, execute=True)

    async def get_data_from_order_table(self, user_id):
        sql = "SELECT product_id,count FROM order_table WHERE user_id=$1"
        return await self.execute(sql, int(user_id), fetch=True, execute=True)

    async def get_data_from_product_id(self, cat_id, title):
        sql = "SELECT id FROM product WHERE category_id=$1 AND title=$2"
        return await self.execute(sql, cat_id, title, fetchval=True, execute=True)

    async def get_data_from_product_all(self, cat_id, pro_id):
        sql = "SELECT * FROM product WHERE category_id=$1 AND id=$2"
        return await self.execute(sql, cat_id, pro_id, fetch=True, execute=True)

    async def get_all_admins(self):
        sql = "SELECT telegram_id FROM admins_table"
        return await self.execute(sql, fetch=True, execute=True)

    async def delete_admin(self, user_id: int):
        sql = f"DELETE FROM admins_table WHERE telegram_id={int(user_id)};"
        return await self.execute(sql, execute=True)

    async def delete_order(self, user_id: int):
        sql = f"DELETE FROM order_table WHERE user_id={int(user_id)};"
        return await self.execute(sql, execute=True)

    async def add_product(self, title, description, category_id, image_url, price, discount):
        sql = "INSERT INTO product (title, description, category_id, image_url, price, discount) VALUES($1, $2, $3, " \
              "$4, $5,$6) returning *"
        return await self.execute(sql, title, description, category_id, image_url, price, discount, fetchrow=True)

    async def add_category(self, title: str):
        sql = "INSERT INTO category (title) VALUES($1) returning *"
        await self.execute(sql, title, fetchrow=True)

    async def add_admin(self, telegram_id):
        admins = await self.get_all_admins()
        for admin in admins:
            if admin['telegram_id'] == int(telegram_id):
                break
        else:
            sql = "INSERT INTO admins_table (telegram_id) VALUES($1) returning *"
            await self.execute(sql, telegram_id, fetchrow=True, execute=True)

    async def get_data_from_order_table_check(self, user_id, pro_id):
        sql = "SELECT product_id,count FROM order_table WHERE user_id=$1 AND product_id=$2"
        return await self.execute(sql, int(user_id), int(pro_id), fetchrow=True, execute=True)

    async def get_user_lang_code(self, user_id):
        sql = "SELECT lang_code FROM users WHERE telegram_id=$1"
        return await self.execute(sql, int(user_id), fetchval=True, execute=True)

    async def add_order(self, user_id, product_id, count=1):
        order = await self.get_data_from_order_table_check(user_id, product_id)
        if order:
            sql = "UPDATE order_table SET count=$3 WHERE user_id=$1 AND product_id=$2"
            return await self.execute(sql, int(user_id), int(product_id), int(order['count']) + int(count),
                                      fetchrow=True)
        else:
            sql = "INSERT INTO order_table (user_id, product_id, count) VALUES($1, $2, $3) returning *"
            return await self.execute(sql, int(user_id), int(product_id), int(count), fetchrow=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join(
            [f"{item} = ${num}" for num, item in enumerate(parameters.keys(), start=1)]
        )
        return sql, tuple(parameters.values())

    async def add_user_lang_code(self, lang_code, user_id):
        sql = "UPDATE users SET lang_code=$1 WHERE telegram_id=$2"
        await self.execute(sql, lang_code, user_id, execute=True, fetchrow=True)

    async def add_user(self, full_name, username, telegram_id):
        sql = "INSERT INTO users (full_name, username, telegram_id,lang_code) VALUES($1, $2, $3, NULL) returning *"
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

    async def delete_category(self, cat_id):
        await self.execute("DELETE FROM category WHERE id=$1", cat_id, execute=True)
        await self.execute("DELETE FROM product WHERE category_id=$1", cat_id, execute=True)

    async def delete_product(self, p_id, cat_id):
        await self.execute("DELETE FROM product WHERE id=$1 AND category_id=$2", p_id, cat_id, execute=True)

    async def drop_users(self):
        await self.execute("DROP TABLE Users", execute=True)
