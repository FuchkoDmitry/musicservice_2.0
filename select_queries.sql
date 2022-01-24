select album_name, release_date
from album
where release_date = 2018;


select song_name, lenght /60 as minutes
from song
where lenght = (select max(lenght) from song);


select song_name
from song
where lenght >= 210
order by lenght desc;


select title
from playlist
where release_date between 2018 and 2020;


select artist_name
from artist
where artist_name not like '% %';


select song_name
from song
where song_name ilike '%my%' or song_name ilike '%мой%';
