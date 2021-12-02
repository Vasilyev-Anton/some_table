create table if not exists singer (
	id serial primary key,
	name_singer varchar(100) not null
);

create table if not exists genre (
	id serial primary key,
	title text not null
);

create table if not exists songster (
	id serial primary key,
	title text not null,
	release_year integer
);

create table if not exists album (
	id serial primary key,
	title text not null,
	release_year integer
);

create table if not exists track (
	id serial primary key,
	title text not null,
	duration time not null,
	duration1 numeric(3, 2) not null,
	album_id integer references album(id)
);

create table if not exists singeralbum (
	id serial primary key,
	album_id integer references album(id),
	singer_id integer references singer(id)
);

create table if not exists genresinger (
	id serial primary key,
	genre_id integer references genre(id),
	singer_id integer references singer(id)
);

create table if not exists tracksongster (
	id serial primary key,
	track_id integer references track(id),
	songster_id integer references songster(id)
);

select title, count(singer_id) from genre g 
join genresinger g2 ON g.id = g2.genre_id 
group by g.title;
