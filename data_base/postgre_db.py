import psycopg2 as sq


def sql_start():
    global base, cur
    base = sq.connect(
        dbname="postgres",
        user="postgres",
        password="trall100500",
        host="127.0.0.1",
        port="5432"
    )
    print('База данных запущена')

    cur = base.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS category
    (
        id SERIAL PRIMARY KEY,
        name VARCHAR
    );
    CREATE TABLE IF NOT EXISTS title
    (
        id SERIAL PRIMARY KEY,
        name VARCHAR,
        year TEXT,
        genres TEXT,
        description TEXT,
        image TEXT
    );
    CREATE TABLE IF NOT EXISTS titles_cat
    (
        id BIGSERIAL PRIMARY KEY,
        title_id INTEGER NOT NULL REFERENCES title ON DELETE CASCADE,
        cat_id INTEGER NOT NULL REFERENCES category ON DELETE CASCADE,
        UNIQUE (title_id, cat_id)
    );
    ''')
    base.commit()
    print('Таблицы созданы')


async def sql_add_title(state):
    async with state.proxy() as data:
        cur.execute("INSERT INTO title VALUES (DEFAULT, %s, %s, %s, %s, %s)", tuple(data.values()))
        base.commit()


async def sql_add_cat(name):
    cur.execute("INSERT INTO category VALUES (DEFAULT, %s)", name)
    base.commit()


async def sql_add_connection(title_name, cat_name):
    cur.execute(f'''INSERT INTO titles_cat VALUES(DEFAULT,
                (
                    SELECT id FROM title WHERE name = '{title_name}'
                ),
                (
                    SELECT id FROM category WHERE name = '{cat_name}'
                )
                );
                ''')
    base.commit()


async def sql_get_cats():
    cur.execute("SELECT name FROM category")
    return cur.fetchall()


async def sql_get_cats_noFilms():
    cur.execute("SELECT name FROM category WHERE name != 'ОНГОИНГИ' and name != 'ФИЛЬМЫ'")
    return cur.fetchall()


async def sql_get_title_by_cat(name):
    cur.execute(f'''SELECT title.name, title.year, title.genres, title.description, title.image 
                FROM titles_cat
                LEFT JOIN category ON category.id = titles_cat.cat_id
                LEFT JOIN title ON title.id = titles_cat.title_id
                WHERE category.name = '{name}'
                ORDER BY random() LIMIT 5;
                ''')
    return cur.fetchall()


async def sql_delete_title(name):
    cur.execute(f"DELETE FROM title WHERE name = '{name}'")
    base.commit()


async def sql_get_random_titles():
    cur.execute("SELECT * FROM title ORDER BY random() LIMIT 5;")
    return cur.fetchall()


async def sql_get_ongoing():
    cur.execute(f'''SELECT title.name, title.year, title.genres, title.description, title.image 
                    FROM titles_cat
                    LEFT JOIN category ON category.id = titles_cat.cat_id
                    LEFT JOIN title ON title.id = titles_cat.title_id
                    WHERE category.name = 'ОНГОИНГИ'
                    ORDER BY random() LIMIT 5;
                    ''')
    return cur.fetchall()


async def sql_get_films():
    cur.execute(f'''SELECT title.name, title.year, title.genres, title.description, title.image 
                    FROM titles_cat
                    LEFT JOIN category ON category.id = titles_cat.cat_id
                    LEFT JOIN title ON title.id = titles_cat.title_id
                    WHERE category.name = 'ФИЛЬМЫ'
                    ORDER BY random() LIMIT 5;
                    ''')
    return cur.fetchall()
