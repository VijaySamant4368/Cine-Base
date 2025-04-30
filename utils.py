import sqlite3

TOTAL_ON_PAGE:int = 12
DB_NAME = "movies.db"

#TODO: Use IN keyword for array/list of IDs
def getPersonName(cursor:sqlite3.Cursor, person_id:str):
    cursor.execute("SELECT person_name FROM people WHERE person_id = ?", (person_id,))
    return cursor.fetchall()[0][0]

def getGenreName(cursor:sqlite3.Cursor, genre_id:int):
    # print(type(genre_id))
    cursor.execute("SELECT genre_name FROM genres WHERE genre_id = ?", (str(genre_id),))
    return cursor.fetchall()[0][0]

def getMovieGenresActorsDirectors(cursor:sqlite3.Cursor, title_id:int) -> tuple[list[dict], list[dict], list[dict]]:
    cursor.execute("""
    SELECT genre_id, genre_name FROM genres WHERE genre_id IN 
                   (SELECT genre_id FROM title_genres WHERE title_id = ?)
""", (title_id, ))
    title_genres = cursor.fetchall()
    genres = []
    for genre in title_genres:
        genres.append( {"id": genre[0], "name": genre[1]} )
    
    cursor.execute("""
    SELECT person_id, person_name FROM people WHERE person_id IN 
                   (SELECT person_id FROM actors WHERE title_id = ?)
""", (title_id, ))
    title_actors = cursor.fetchall()
    actors = []
    for actor in title_actors:
        actors.append( {"id": actor[0], "name": actor[1]} )
    
    cursor.execute("""
    SELECT person_id, person_name FROM people WHERE person_id IN 
                   (SELECT person_id FROM directors WHERE title_id = ?)
""", (title_id, ))
    title_directors = cursor.fetchall()
    directors = []
    for director in title_directors:
        directors.append( {"id": director[0], "name": director[1]} )
    
    return genres, actors, directors

def fetchDataOfMovies(cursor:sqlite3.Cursor, page_num:int = 1)    -> list[dict]:
    
    movies = []
    
    title_data = cursor.fetchall()
    for title_row in title_data:
        movie = {}
        movie["title_id"] = title_row[0]
        movie["title_name"] = title_row[1]
        movie["description"] = title_row[2]
        movie["rating"] = title_row[3]
        movie["rank"] = title_row[4]
        movie["votes"] = title_row[5]
        movie["revenue"] = title_row[6]
        movie["runtime"] = title_row[7]
        movie["year"] = title_row[8]

        movie_stuffs = getMovieGenresActorsDirectors(cursor, movie["title_id"])
        
        movie["genres"] = movie_stuffs[0]
        movie["actors"] = movie_stuffs[1]
        movie["directors"] = movie_stuffs[2] 

        movies.append(movie)
    return movies


def showAllMovies(page_num:int = 1, total_on_page:int=TOTAL_ON_PAGE):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
    SELECT * FROM titles LIMIT ? OFFSET ?;
""", total_on_page, (page_num-1)*total_on_page)
    
    return fetchDataOfMovies(cursor)[page_num*TOTAL_ON_PAGE : (page_num + 1)*TOTAL_ON_PAGE ]
    
def getFilteredMovies(query: str = "",
                        genre_ids: list[int] | None = None,
                        not_genre_ids: list[int] | None = None,
                        actor_ids: list[str] | None = None,
                        director_ids: list[str] | None = None,
                        title_ids: list[int] | None = None,
                        page_num: int = 1,
                        total_on_page: int = TOTAL_ON_PAGE) -> tuple[list[dict], str, int]:
        # https://stackoverflow.com/a/1264693
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    where_clauses: list[str] = []
    params: list = []
    message_parts: list[str] = []
    if genre_ids:
        ph = ",".join("?" for _ in genre_ids)
        where_clauses.append(
            f"title_id IN (SELECT title_id FROM title_genres WHERE genre_id IN ({ph}) GROUP BY title_id HAVING COUNT(DISTINCT genre_id) = ?)"
        )
        params.extend(genre_ids)
        params.append(len(genre_ids))
        names = " ".join(getGenreName(cursor, gid) for gid in genre_ids)
        label = "Genres" if len(genre_ids) > 1 else "Genre"
        message_parts.append(f"{label}: {names}")
    if not_genre_ids:
        ph = ",".join("?" for _ in not_genre_ids)
        where_clauses.append(
            f"title_id NOT IN (SELECT title_id FROM title_genres WHERE genre_id IN ({ph}))"
        )
        params.extend(not_genre_ids)
        names = " ".join(getGenreName(cursor, gid) for gid in not_genre_ids)
        label = "Excluded Genres" if len(not_genre_ids) > 1 else "Excluded Genre"
        message_parts.append(f"{label}: {names}")
    if actor_ids:
        ph = ",".join("?" for _ in actor_ids)
        where_clauses.append(
            f"title_id IN (SELECT title_id FROM actors WHERE person_id IN ({ph}))"
        )
        params.extend(actor_ids)
        names = " ".join(getPersonName(cursor, aid) for aid in actor_ids)
        label = "Actors" if len(actor_ids) > 1 else "Actor"
        message_parts.append(f"{label}: {names}")
    if director_ids:
        ph = ",".join("?" for _ in director_ids)
        where_clauses.append(
            f"title_id IN (SELECT title_id FROM directors WHERE person_id IN ({ph}))"
        )
        params.extend(director_ids)
        names = " ".join(getPersonName(cursor, did) for did in director_ids)
        label = "Directors" if len(director_ids) > 1 else "Director"
        message_parts.append(f"{label}: {names}")
    if query:
        where_clauses.append("title_name LIKE ?")
        params.append(f"%{query}%")
        message_parts.insert(0, f"Search: {query}")
    order_clause = ""
    if title_ids:
        ph = ",".join("?" for _ in title_ids)
        where_clauses.append(f"title_id IN ({ph})")
        params.extend(title_ids)
        order_clause = (
            "CASE title_id "
            + " ".join(f"WHEN {tid} THEN {i}" for i, tid in enumerate(title_ids, 1))
            + " END"
        )
    where_sql = ""
    if where_clauses:
        where_sql = "WHERE " + " AND ".join(where_clauses)
    count_sql = f"SELECT COUNT(*) FROM titles {where_sql}"
    cursor.execute(count_sql, params)
    total_count = cursor.fetchone()[0]
    total_pages = (total_count + total_on_page - 1) // total_on_page
    select_sql = f"SELECT * FROM titles {where_sql}"
    if order_clause:
        select_sql += f" ORDER BY {order_clause}"
    select_sql += " LIMIT ? OFFSET ?"
    params.extend([total_on_page, (page_num - 1) * total_on_page])
    cursor.execute(select_sql, params)
    movies = fetchDataOfMovies(cursor)
    message = (
        "Showing All Movies"
        if not message_parts
        else "Showing results for:\n" + "\n".join(message_parts)
    )
    print(f"movies: {movies}")
    print(f"{select_sql=}, {params=}, {message=}")
    return movies, message, total_pages


def getMovieDetails(movie_id:int) -> dict:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM titles WHERE title_id = ?
                   ''', (movie_id, ))
    title_data = cursor.fetchall()
    movie_details = {}
    movie_details["title_id"] = title_data[0][0]
    movie_details["title_name"] = title_data[0][1]
    movie_details["description"] = title_data[0][2]
    movie_details["rating"] = title_data[0][3]
    movie_details["rank"] = title_data[0][4]
    movie_details["votes"] = title_data[0][5]
    movie_details["revenue"] = title_data[0][6]
    movie_details["runtime"] = title_data[0][7]
    movie_details["year"] = title_data[0][8]
    movie_details["genres"] = []
    movie_details["actors"] = []
    movie_details["directors"] = []

    movie_stuffs = getMovieGenresActorsDirectors(cursor, movie_details["title_id"])

    movie_details["genres"] = movie_stuffs[0]
    movie_details["actors"] = movie_stuffs[1]
    movie_details["directors"] = movie_stuffs[2] 

    return movie_details

def getAllGenres() -> list[dict]:
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM genres")
    genres = cursor.fetchall()
    genre_list = []
    for genre in genres:
        genre_list.append({"id": genre[0], "name": genre[1]})
    return genre_list