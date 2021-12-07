import sqlalchemy

db = 'postgresql://postgres:314159W@localhost:5432/postgres'
engine = sqlalchemy.create_engine(db)
connection = engine.connect()

singer_in_genre = connection.execute("""
SELECT title, COUNT(singer_id) FROM genre
    JOIN genresinger ON genre.id = genre_id
    GROUP BY genre.title
    """).fetchall()
print('Количество исполнителей в каждом жанре', singer_in_genre)

track_in_album = connection.execute("""
SELECT release_year, COUNT(track.id) FROM album
    JOIN track ON album.id = track.album_id
    WHERE release_year BETWEEN 2019 AND 2020
    GROUP BY album.release_year
    """).fetchall()
print('Количество треков, вошедших в альбомы 2019-2020 годов:', track_in_album)

avg_duration_track = connection.execute("""
SELECT album.title, AVG(duration1) FROM track
    JOIN album ON album.id = track.album_id
    GROUP BY album.title
    """).fetchall()
print('Средняя продолжительность треков по альбомам:', avg_duration_track)

singer_without_album2020 = connection.execute("""
SELECT name_singer FROM singer
    WHERE NOT singer.id = (
    SELECT singer.id FROM singer
    JOIN singeralbum ON singer.id = singeralbum.singer_id
    JOIN album ON singeralbum.album_id = album.id
    WHERE album.release_year = 2020)
    """).fetchall()
print('Исполнители, не выпустившие альбомы в 2020году:', singer_without_album2020)

songster_with_The_Beatles = connection.execute("""
SELECT songster.title FROM songster
    JOIN tracksongster ON songster.id = songster_id
    JOIN track ON track_id = track.id
    JOIN album ON track.album_id = album.id
    JOIN singeralbum ON album.id = singeralbum.album_id
    JOIN singer ON singeralbum.singer_id = singer.id
    WHERE name_singer = 'The Beatles'
    """).fetchall()
print('Названия сборников в которых присутствует The Beatles:', songster_with_The_Beatles)

albums_with_singers_some_genres = connection.execute("""
SELECT album.title FROM genresinger
    JOIN singer ON genresinger.singer_id = singer.id
    JOIN singeralbum ON singer.id = singeralbum.singer_id
    JOIN album ON singeralbum.album_id = album.id
    GROUP BY album.title
    HAVING COUNT(genresinger.singer_id) > 1
    """).fetchall()
print('Названия альбомов в которых присутствует исполнители более 1 жанра:', albums_with_singers_some_genres)

tracks_not_in_songsters = connection.execute("""
SELECT track.title FROM track
    LEFT JOIN tracksongster ON track.id = tracksongster.track_id
    GROUP BY track.title
    HAVING COUNT(tracksongster.songster_id) = 0
    """).fetchall()
print('Наименование треков, которые не входят в сборники:', tracks_not_in_songsters)

singer_with_min_track = connection.execute("""
SELECT name_singer FROM singer
    JOIN singeralbum ON singer.id = singeralbum.singer_id
    JOIN album ON singeralbum.album_id = album.id
    JOIN track ON album.id = track.album_id
    WHERE duration1 = (
    SELECT MIN(duration1) FROM track)
    """).fetchall()
print('Исполнитель, написавший самый короткий трек:', singer_with_min_track)

min_album = connection.execute("""
SELECT album.title FROM album
    JOIN track ON album.id = track.album_id
    GROUP BY album.title
    HAVING COUNT(track.album_id) = (SELECT MIN(track.album_id) FROM track)
    """).fetchall()
print('Название альбомов, содержащих наименьшее количество треков:', min_album)
