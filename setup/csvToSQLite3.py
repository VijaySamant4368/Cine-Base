#Rank,Title,Genre,Description,Director,Actors,Year,Runtime (Minutes),Rating,Votes,Revenue (Millions),Metascore

CSV_PATH = "IMDB-Movie-Data.csv"
DB_PATH = "movies.db"

CSV_PATH = "../"+CSV_PATH
DB_PATH = "../" +DB_PATH

import pandas as pd
import sqlite3

df = pd.read_csv(CSV_PATH)

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

genre_IDs = {}
current_genre_id = 1
person_IDs = {}
current_person_id = 1

done = 0

for _, row in df.iterrows():
    title_name = row["Title"]
    desc = row["Description"]
    year = row["Year"]
    runtime = row["Runtime (Minutes)"]
    rating= row["Rating"]
    votes = row["Votes"]
    revenue = row["Revenue (Millions)"]
    title_id = row["Rank"]

    genres = row["Genre"].split(",")
    directors = row["Director"].split(",")
    actors = row["Actors"].split(",")

    cursor.execute('''
        INSERT INTO titles(title_id, title_name, description, rating, rank, votes, revenue, runtime, year) VALUES 
                   (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (title_id, title_name, desc, rating, title_id, votes, revenue, runtime, year
    ))
    conn.commit()
    for genre_name in genres:
        try:
            genre_id = genre_IDs[genre_name]
        except KeyError:
            genre_id = current_genre_id
            current_genre_id+=1
            genre_IDs[genre_name] = genre_id

            cursor.execute('''
                INSERT INTO genres(genre_id, genre_name) VALUES(
                            ?, ?
                           )
            ''', (genre_id, genre_name))
            conn.commit()
        cursor.execute('''
                        INSERT INTO title_genres(genre_id, title_id) VALUES(?, ?)
                       ''', (genre_id, title_id))
        conn.commit()

    for person_name in actors:
        try:
            person_id = person_IDs[person_name]
        except KeyError:
            person_id = current_person_id
            current_person_id+=1
            person_IDs[person_name] = person_id
            cursor.execute('''
                INSERT INTO people(person_id, person_name) VALUES(
                            ?, ?
                           )
            ''', (person_id, person_name))
            conn.commit()
        cursor.execute('''
                        INSERT INTO actors(person_id, title_id) VALUES(?, ?)
                       ''', (person_id, title_id))
        conn.commit()            

    for person_name in directors:
        try:
            person_id = person_IDs[person_name]
        except KeyError:
            person_id = current_person_id
            current_person_id+=1
            person_IDs[person_name] = person_id
            cursor.execute('''
                INSERT INTO people(person_id, person_name) VALUES(
                            ?, ?
                           )
            ''', (person_id, person_name))
            conn.commit()
        cursor.execute('''
                        INSERT INTO directors(person_id, title_id) VALUES(?, ?)
                       ''', (person_id, title_id))
        conn.commit()   
    done+=1
    if done%10 == 0:
        print(done, "done")              
