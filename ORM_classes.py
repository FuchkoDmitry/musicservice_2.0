import sqlalchemy as sq
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import exc
from data import nationalities, genres, tracks, albums
import random
from random import randint
import datetime as dt


Base = declarative_base()

db = 'postgresql://dmitry:123@localhost:5432/music'
engine = sq.create_engine(db)
Session = sessionmaker(bind=engine)


class Genre(Base):
    __tablename__ = 'genre'
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String, nullable=False, unique=True)
    artists = relationship('Artist', secondary='artist_genre', back_populates='genres')


artist_genre = sq.Table('artist_genre', Base.metadata,
                        sq.Column('genre_id', sq.Integer, sq.ForeignKey('genre.id')),
                        sq.Column('artist_id', sq.Integer, sq.ForeignKey('artist.id'))
                        )


class Artist(Base):
    __tablename__ = 'artist'
    id = sq.Column(sq.Integer, primary_key=True)
    name = sq.Column(sq.String, nullable=False, unique=True)
    dob = sq.Column(sq.Date)
    nationality = sq.Column(sq.String)
    genres = relationship(Genre, secondary='artist_genre', back_populates='artists')
    albums = relationship('Album', secondary='artist_album', back_populates='artist')


artist_album = sq.Table('artist_album', Base.metadata,
                        sq.Column('artist_id', sq.Integer, sq.ForeignKey('artist.id')),
                        sq.Column('album_id', sq.Integer, sq.ForeignKey('album.id'))
                        )


class Album(Base):
    __tablename__ = 'album'
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String)
    release_date = sq.Column(sq.Integer)
    description = sq.Column(sq.String)
    artist = relationship(Artist, secondary='artist_album', back_populates='albums')
    tracks = relationship('Track', backref='album')


class Track(Base):
    __tablename__ = 'track'
    id = sq.Column(sq.Integer, primary_key=True)
    title = sq.Column(sq.String, nullable=False)
    duration = sq.Column(sq.Integer, nullable=False)
    album_id = sq.Column(sq.Integer, sq.ForeignKey('album.id', ondelete='cascade'))
    playlists = relationship('Playlist', secondary='playlist_tracks', back_populates='tracks')
    # album = relationship(Album)


playlist_tracks = sq.Table('playlist_tracks', Base.metadata,
                           sq.Column('playlist_title',
                                     sq.String,
                                     sq.ForeignKey('playlist.title'),
                                     primary_key=True),
                           sq.Column('track_id',
                                     sq.Integer,
                                     sq.ForeignKey('track.id'),
                                     primary_key=True)
                           )


class Playlist(Base):
    __tablename__ = 'playlist'
    title = sq.Column(sq.String, primary_key=True, nullable=False, unique=True)
    release_date = sq.Column(sq.Integer, nullable=False)
    description = sq.Column(sq.String)
    tracks = relationship(Track, secondary='playlist_tracks', back_populates='playlists')


if __name__ == '__main__':
    session = Session()
    Base.metadata.create_all(engine)


    # добавляем жанры
    for genre in genres:
        title = Genre(title=genre)
        session.add(title)
        session.commit()

    #  добавляем артистов и альбомы
    for data in albums:
        dob = dt.date(randint(1960, 2002), randint(1, 12), randint(1, 28))
        nationality = random.choice(nationalities)
        artist = Artist(name=data[0], dob=dob, nationality=nationality)
        session.add(artist)
        album = Album(title=data[1], release_date=data[2])
        session.add(album)
        session.commit()

    #  определяем жанры и альбомы для артистов
    for artists in albums:
        genre_random = genres[randint(0, 21)]
        genre = session.query(Genre).filter_by(title=genre_random).first()
        artist = session.query(Artist).filter_by(name=artists[0]).first()
        album = session.query(Album).filter_by(title=artists[1]).first()
        artist.albums.append(album)
        artist.genres.append(genre)
        session.commit()

    #  добавляем треки и альбомы для треков
    for data in tracks:
        album = session.query(Artist).filter_by(name=data[0]).first()
        album_id = album.albums[0].id
        track = Track(title=data[1], duration=data[2], album_id=album_id)
        session.add(track)
        session.commit()

    # определяем плейлисты и треки для плейлистов
    for playlists in range(10):
        playlist_name = f'playlist-{playlists + 1}'
        release_date = randint(2015, 2022)
        playlist = Playlist(title=playlist_name, release_date=release_date)
        session.add(playlist)
        for tracks in range(15):
            track_id = session.query(Track).filter_by(id=randint(1, 155)).first()
            try:
                playlist.tracks.append(track_id)
            except exc.IntegrityError:
                pass
        session.commit()
