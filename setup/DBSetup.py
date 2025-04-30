import sqlite3

DB_PATH = "movies.db"
DB_PATH = "../" +DB_PATH

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute(
    '''
        CREATE TABLE IF NOT EXISTS titles (
            title_id INTEGER PRIMARY KEY,
            title_name TEXT,
            description TEXT,
            rating INTEGER,
            rank INTEGER,
            votes INTEGER,
            revenue INTEGER,
            runtime INTEGER,
            year INTEGER
        )
    ''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS genres (
               genre_id INTEGER PRIMARY KEY,
               genre_name TEXT
               )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS people (
               person_id INTEGER PRIMARY KEY,
               person_name TEXT
               )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS directors (
               person_id INTEGER,
               title_id INTEGER,
               FOREIGN KEY(title_id) REFERENCES titles(title_id),
               FOREIGN KEY(person_id) REFERENCES people(person_id),
               PRIMARY KEY(title_id, person_id)
               )
''')
cursor.execute('''
    CREATE TABLE IF NOT EXISTS actors (
               person_id INTEGER,
               title_id INTEGER,
               FOREIGN KEY(title_id) REFERENCES titles(title_id),
               FOREIGN KEY(person_id) REFERENCES people(person_id),
               PRIMARY KEY(title_id, person_id)
               )
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS title_genres (
               genre_id INTEGER,
               title_id INTEGER,
               FOREIGN KEY(title_id) REFERENCES titles(title_id),
               FOREIGN KEY(genre_id) REFERENCES genres(genre_id),
               PRIMARY KEY(title_id, genre_id)
               )
''')