import sqlalchemy
from sqlalchemy import exc
import random
from random import randint
import datetime as dt
from data import nationalities, genres, tracks, albums

db = 'postgresql://dmitry:123@localhost:5432/musicservice'
engine = sqlalchemy.create_engine(db)
connection = engine.connect()


def upload_genres(genres_list):
    for genre in genres_list:
        connection.execute(f"INSERT INTO genre(genre_name) values('{genre}');")


def upload_artists(artists_list):
    for artist in artists_list:
        dob = dt.date(randint(1960, 2002), randint(1, 12), randint(1, 28))
        connection.execute(f"INSERT INTO artist"
                           f"(artist_name, dob, nationality) "
                           f"values('{artist[0]}', "
                           f"'{dob}',"
                           f"'{random.choice(nationalities)}');")


def artist_genre(genres_list, artists_list):
    for artist in range(len(artists_list)):
        connection.execute(f"INSERT INTO artist_genre(artist_id, genre_id) "
                           f"VALUES({artist + 1}, "
                           f"{randint(1, len(genres_list))});")


def upload_albums(albums_list):
    for album in albums_list:
        connection.execute(f"INSERT INTO album(album_name,"
                           f" release_date, description) "
                           f"VALUES('{album[1]}', {album[2]}, "
                           f"'description here!');")


def artist_albums(albums_list):
    for album in albums_list:
        art_id = connection.execute(f"SELECT id FROM artist "
                                    f"WHERE artist_name = "
                                    f"'{album[0]}';").fetchone()
        alb_id = connection.execute(f"SELECT id FROM album "
                                    f"WHERE album_name = "
                                    f"'{album[1]}';").fetchone()
        connection.execute(f"INSERT INTO artist_album(artist_id, album_id) "
                           f"VALUES({art_id[0]}, {alb_id[0]});")


def upload_songs(track_list):
    for track in track_list:
        art_id = connection.execute(f"SELECT id FROM artist "
                                    f"WHERE artist_name = "
                                    f"'{track[0]}';").fetchone()
        alb_id = connection.execute(f"SELECT album_id FROM artist_album "
                                    f"WHERE artist_id ="
                                    f" {art_id[0]};").fetchone()
        connection.execute(f"INSERT INTO song(song_name, album_id, lenght)"
                           f"VALUES('{track[1]}', {alb_id[0]}, {track[2]});")


def create_playlist(count=10):
    for i in range(count):
        connection.execute(f"INSERT INTO playlist(title, "
                           f"release_date, description)"
                           f"VALUES('playlist-{i + 1}', "
                           f"{randint(2015, 2022)}, "
                           f"'playlist description');")
    playlists = connection.execute(
                                   "SELECT title FROM playlist;"
                                  ).fetchall()
    return playlists


def fill_playlist(playlists, tracks_count=15):
    for playlist in playlists:
        for track in range(tracks_count):
            try:
                connection.execute(f"INSERT INTO playlist_songs"
                                   f"(playlist_name, song_id) "
                                   f"VALUES('{playlist[0]}',"
                                   f" {randint(1, 155)});")
            except exc.IntegrityError:
                pass


if __name__ == '__main__':
    upload_genres(genres)
    upload_artists(albums)
    artist_genre(genres, albums)
    upload_albums(albums)
    artist_albums(albums)
    upload_songs(tracks)
    playlists_names = create_playlist()
    fill_playlist(playlists_names)
