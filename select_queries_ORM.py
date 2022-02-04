from ORM_classes import *
import sqlalchemy as sq
from sqlalchemy import func, desc, between, select

session = Session()

# название и год выхода альбомов, вышедших в 2018 году
# query = session.query(Album).filter_by(release_date='2018').all()
# for album in query:
    # print(album.title, album.release_date)

# название и продолжительность самого длительного трека
# query = session.query(Track).order_by(Track.duration.desc()).first()
# print(query.title, round(query.duration / 60, 2))

# название треков, продолжительность которых не менее 3,5 минуты
# query = session.query(Track).filter(
#                                     Track.duration >= 210
#                                     ).order_by(
#                                                Track.duration.desc()
#                                                ).all()
# for track in query:
#     print(track.title, track.duration)

# названия сборников, вышедших в период с 2018 по 2020 год включительно
# query = session.query(Playlist).where(Playlist.release_date.between(2018, 2020)).all()
# for playlist in query:
#     print(playlist.title)

# исполнители, чье имя состоит из 1 слова
# query = session.query(Artist).where(~Artist.name.like("% %")).all()
# for artist in query:
#     print(artist.name)

# название треков, которые содержат слово "мой"/"my"
# query = session.query(Track).filter(sq.or_(Track.title.ilike('%my%'),
#                                            Track.title.ilike('%мой%'))
#                                     ).all()
# for track in query:
#     album_id = track.album_id
#     album_name = session.query(Album).filter_by(id=album_id).first()
#     print(f' track: {track.title} artist:'
#           f' {album_name.artist[0].name} album: {album_name.title}')

# количество исполнителей в каждом жанре
# query = session.query(Genre).join(Genre.artists).order_by(func.count(Artist.id).desc()).group_by(Genre.id).all()
# for genre in query:
#     print(genre.title, len(genre.artists))
#
# query = session.query(Genre).all()
# for q in query:
#     print(q.title, len(q.artists))

# количество треков, вошедших в альбомы 2019-2020 годов
# query = session.query(Album, func.count(Track.id)).join(Track).filter(
#     Album.release_date.between(2019, 2020)
#     ).order_by(func.count(Track.id).desc()).group_by(Album.id).all()
# count = 0
# for album in query:
#     # print(album[0].title, album[1])
#     count += album[1]
# print(count)

# средняя продолжительность треков по каждому альбому
# query = session.query(Album, func.avg(Track.duration)).join(Track).group_by(Album.id).\
#     order_by(func.avg(Track.duration).desc()).all()
# for data in query:
#     print(data[0].title, round(data[1] / 60, 1))

# названия сборников, в которых присутствует конкретный исполнитель (выберите сами);
# query = session.query(Playlist).join(Playlist.tracks).join(Album).join(Album.artist).\
#     filter(Artist.name == 'Gunna').all()
# for playlist in query:
#     print(playlist.title)

# название альбомов, в которых присутствуют исполнители более 1 жанра
# query = session.query(Album.title).join(Album.artist).join(Artist.genres).\
#     group_by(Album.title).having(func.count(Artist.id) > 1).order_by(func.count(Artist.id).desc()).all()
# for album in query:
#     print(album[0])

# наименование треков, которые не входят в сборники
# query = session.query(Track).outerjoin(Track.playlists).filter(Playlist.title == None).order_by(Track.title).all()
# for track in query:
#     print(track.title)
