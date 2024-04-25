import asyncio

import asyncpg

from src.config import Config


async def connect():
    return await asyncpg.connect(Config.DATABASE_URL)


def sanitize_int(value):
    if isinstance(value, int):
        return value
    else:
        value = value.strip()
        if '"' in value:
            value = value.replace('"', ".")
        if "lbs" in value:
            value = value.replace("lbs", "")
        if " " in value:
            value = value.replace(" ", "")
        try:
            return int(value)
        except Exception as e:
            print(f"error sanitizing int: {e}")
            return value


# Async CRUD operations


async def create_tables():
    conn = await connect()
    async with conn.transaction():
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS cards (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255) NOT NULL,
                hp INT NOT NULL,
                type VARCHAR(255) NOT NULL,
                height VARCHAR(10) NOT NULL,
                weight VARCHAR(10) NOT NULL,
                move1_name VARCHAR(255) NOT NULL,
                move1_info TEXT NOT NULL,
                move1_power INT NOT NULL,
                move2_name VARCHAR(255) NOT NULL,
                move2_info TEXT NOT NULL,
                move2_power INT NOT NULL,
                weakness VARCHAR(255) NOT NULL,
                resistance VARCHAR(255) NOT NULL,
                mood VARCHAR(255) NOT NULL,
                footer TEXT NOT NULL,
                color CHAR(7) NOT NULL,
                nth INT NOT NULL,
                image_url TEXT NOT NULL
            );
            """
        )
    await conn.close()


# Async CRUD for messages


async def create_card(
    title,
    hp,
    type,
    height,
    weight,
    move1_name,
    move1_info,
    move1_power,
    move2_name,
    move2_info,
    move2_power,
    weakness,
    resistance,
    mood,
    footer,
    color,
    nth,
    image_url,
):
    conn = await connect()
    async with conn.transaction():
        await conn.execute(
            """
            INSERT INTO cards (title, hp, type, height, weight, move1_name, move1_info, move1_power, move2_name, move2_info, move2_power, weakness, resistance, mood, footer, color, nth, image_url)
            VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18);
        """,
            title,
            sanitize_int(hp),
            type,
            str(height),
            str(weight),
            move1_name,
            move1_info,
            sanitize_int(move1_power),
            move2_name,
            move2_info,
            sanitize_int(move2_power),
            weakness,
            resistance,
            mood,
            footer,
            color,
            sanitize_int(nth),
            image_url,
        )
    await conn.close()


async def get_all_cards() -> list[dict]:
    conn = await connect()
    async with conn.transaction():
        records = await conn.fetch("SELECT * FROM cards;")
    return [dict(record) for record in records]


async def get_card_by_id(id):
    conn = await connect()
    async with conn.transaction():
        return await conn.fetchrow("SELECT * FROM cards WHERE id = $1;", id)


async def get_len() -> int:
    conn = await connect()
    async with conn.transaction():
        return await conn.fetchval("SELECT COUNT(*) FROM cards;")


if __name__ == "__main__":
    # asyncio.run(create_tables())
    # asyncio.run(drop_all())
    # print(asyncio.run(get_len()))
    print(asyncio.run(get_all_cards()))
