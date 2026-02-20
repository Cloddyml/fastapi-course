--create temporary table if not exists test1(
--  id int
--);
--
--create temporary table if not exists test2(
--  id int
--);
--
--start transaction;
--insert into test1 (id) values (35);
--insert into test1 (id) values (1 / 0);
--insert into test2 (id) values (255);
--end transaction;
--
--select * from test1;
--select * from test2;

insert into hotels (title, location) values ('Хотел 5 старс', 'Дубай');

select id, title, location from hotels;
select * from hotels;

select id, title, location
from hotels
--where id = 2 and title = 'Отель 5 звезд у моря'
limit 5
offset 5
;

set client_encoding = 'UTF-8';

update pg_database
set datcollate='ru_RU.UTF-8', datctype='ru_RU'
where datname='booking';

update pg_database set encoding = pg_char_to_encoding('UTF-8') where datname = 'booking' -- Добавляет кириллицу для корректной работы БД

select id, title, location
from hotels
where lower(location) like '%сочи%'
limit 5
offset 5
;


select * from bookings
where date_from <= '2026-02-15' and date_to >= '2026.02.17'
;
select room_id, count(*) from bookings
where date_from <= '2026-02-15' and date_to >= '2026.02.17'
group by room_id
;

with rooms_count as (
	select room_id, count(*) as rooms_booked from bookings
	where date_from <= '2026-02-15' and date_to >= '2026.02.17'
	group by room_id
)
select rooms.id as room_id, quantity - coalesce(rooms_booked, 0) as rooms_left
from rooms 
left join rooms_count on rooms.id = rooms_count.room_id
where quantity - coalesce(rooms_booked, 0) > 0;

with rooms_count as (
	select room_id, count(*) as rooms_booked from bookings
	where date_from <= '2026-02-15' and date_to >= '2026.02.17'
	group by room_id
),
rooms_left_table as (
	select rooms.id as room_id, quantity - coalesce(rooms_booked, 0) as rooms_left
	from rooms 
	left join rooms_count on rooms.id = rooms_count.room_id
)
select * from rooms_left_table
where rooms_left > 0;

with rooms_ids as (
	select id from rooms where hotel_id = 1
),
rooms_count as (
	select room_id, count(*) as rooms_booked from bookings
	where date_from <= '2026-02-15' and date_to >= '2026.02.17' -- and room_id in rooms_ids
	group by room_id
),
rooms_left_table as (
	select rooms.id as room_id, quantity - coalesce(rooms_booked, 0) as rooms_left
	from rooms 
	left join rooms_count on rooms.id = rooms_count.room_id
)
select * from rooms_left_table
where rooms_left > 0 and room_id in (select id from rooms where hotel_id = 1);

