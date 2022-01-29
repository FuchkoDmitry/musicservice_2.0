-- 1.
select genre_name, count(genre_id) from genre g 
join artist_genre ag on g.id = ag.genre_id
group by g.genre_name 
order by count(genre_id) desc;


-- 2.
select count(s.id) from song s 
join album on s.album_id = album.id 
where release_date between 2019 and 2020;


-- 3.
select album_name, round(avg(song.lenght) / 60, 1) from album
join song on song.album_id = album.id 
group by album_name
order by avg(song.lenght) desc;


--4
select a.artist_name from artist a 
join artist_album aa on a.id = aa.artist_id 
join album on aa.album_id = album.id 
where release_date not in ('2020')
group by a.artist_name 
having a.artist_name not in (select a2.artist_name from artist a2 
                             join artist_album aa2 on a2.id = aa2.artist_id 
                             join album on aa2.album_id = album.id
                             where album.release_date in ('2020')
                             group by a2.artist_name);


-- 5.
select p.title from playlist p
join playlist_songs ps on p.title = ps.playlist_name 
join song on ps.song_id = song.id  
join artist_album aa on song.album_id = aa.album_id 
join artist a2 on aa.artist_id = a2.id 
where artist_name = 'Gunna';

-- insert into song
--insert into song (song_name, album_id, lenght)
--select s.song_name, aa.album_id + 1, s.lenght from playlist p
--join playlist_songs ps on p.title = ps.playlist_name 
--join song s on ps.song_id = s.id  
--join artist_album aa on s.album_id = aa.album_id 
--join artist a2 on aa.artist_id = a2.id 
--where p.title = 'playlist-3';

--for 6th query
insert into artist_genre (genre_id, artist_id) values (5, 6), (6, 9), (8, 92);


-- 6.
select album_name from album a 
join artist_album aa on a.id = aa.album_id 
join artist_genre ag on aa.artist_id = ag.artist_id 
join genre g on ag.genre_id = g.id 
group by album_name
having count(g.id)> 1;


-- 7.
select s.id, s.song_name from song s 
left join playlist_songs ps on s.id = ps.song_id 
where ps.song_id is null;


-- 8.
select a.id, a.artist_name from artist a 
join artist_album aa on a.id = aa.artist_id 
join song s on aa.album_id = s.album_id 
where s.lenght = (select min(lenght) from song);


--9
select a.album_name from album a
left join song s on s.album_id = a.id
group by a.album_name
having count(s.id) = (select count(s.id) from album a
					  full outer join song s on s.album_id = a.id
					  group by a.album_name 
                      order by count(s.id)
                      limit 1) 
                     ;

