create database musicservice;


create table if not exists genre (
	id serial primary key,
	genre_name varchar(40) not null unique
);


create table if not exists artist (
	id serial primary key,
	artist_name varchar(40) not null unique,
	dob date,
	nationality varchar(50)
);


create table if not exists artist_genre (
	genre_id integer references genre(id),
	artist_id integer references artist(id),
	constraint agpk primary key (genre_id, artist_id)
);


create table if not exists album (
	id serial primary key,
	album_name varchar(80) not null unique,
	release_date integer not null,
	description text
);


create table if not exists artist_album (
	artist_id integer references artist(id),
	album_id integer references album(id),
	constraint aapk primary key (artist_id, album_id)
);


create table if not exists song (
	id serial primary key,
	song_name varchar(80) not null,
	lenght integer not null,
	album_id integer references album(id)
);


create table if not exists playlist (
	title varchar(80) primary key unique not null,
	release_date integer not null,
	description text
);


create table if not exists playlist_songs (
	playlist_name varchar(80) references playlist(title),
	song_id integer references song(id),
	constraint pspk primary key (playlist_name, song_id)
);
