import psycopg2 as sq


base = sq.connect(
    dbname="postgres",
    user="postgres",
    password="trall100500",
    host="127.0.0.1",
    port="5432"
)
print('База данных запущена')

cur = base.cursor()
title_name = 'Hunter x Hunter'
cat_name = 'КОМЕДИЯ'
cur.execute('''SELECT title.name, title.year, title.genres, title.description, title.image 
                FROM titles_cat
                LEFT JOIN category ON category.id = titles_cat.cat_id
                LEFT JOIN title ON title.id = titles_cat.title_id
                WHERE category.name = '{name}';

            ''')
# cur.execute('''SELECT id FROM title WHERE name = 'Hunter x Hunter' ''')

print(cur.fetchall())
# base.commit()
base.close()
