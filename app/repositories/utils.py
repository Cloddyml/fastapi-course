from datetime import date

from sqlalchemy import Select, Subquery, func, select

# from app.database import engine
from app.models.bookings import BookingsOrm
from app.models.rooms import RoomsOrm


def rooms_ids_for_booking(
    date_from: date,
    date_to: date,
    hotel_id: int | None = None,
) -> Select:
    """
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
    where rooms_left > 0 and room_id in (select id from rooms where hotel_id = 1);
    """

    """
    with rooms_count as (
        select room_id, count(*) as rooms_booked from bookings
        where date_from <= '2026-02-15' and date_to >= '2026.02.17'
        group by room_id
    ),
    """
    rooms_count = (
        select(BookingsOrm.room_id, func.count("*").label("rooms_booked"))
        .select_from(BookingsOrm)
        .filter(
            BookingsOrm.date_from <= date_to,
            BookingsOrm.date_to >= date_from,
        )
        .group_by(BookingsOrm.room_id)
        .cte(name="rooms_count")
    )

    """
    rooms_left_table as (
        select rooms.id as room_id, quantity - coalesce(rooms_booked, 0) as rooms_left
        from rooms
        left join rooms_count on rooms.id = rooms_count.room_id
    )
    """
    rooms_left_table = (
        select(
            RoomsOrm.id.label("room_id"),
            (RoomsOrm.quantity - func.coalesce(rooms_count.c.rooms_booked, 0)).label("rooms_left"),
        )
        .select_from(RoomsOrm)
        .outerjoin(rooms_count, RoomsOrm.id == rooms_count.c.room_id)
        .cte(name="rooms_left_table")
    )

    """
    select * from rooms_left_table
    where rooms_left > 0 and room_id in (select id from rooms where hotel_id = 1);
    """

    rooms_ids_for_hotel = select(RoomsOrm.id).select_from(RoomsOrm)

    if hotel_id is not None:
        rooms_ids_for_hotel = rooms_ids_for_hotel.filter_by(hotel_id=hotel_id)

    rooms_ids_for_hotel_subq: Subquery = rooms_ids_for_hotel.subquery(name="rooms_ids_for_hotel")

    rooms_ids_to_get = (
        select(rooms_left_table.c.room_id)
        .select_from(rooms_left_table)
        .filter(
            rooms_left_table.c.rooms_left > 0,
            rooms_left_table.c.room_id.in_(rooms_ids_for_hotel_subq),  # type: ignore
        )
    )

    # print(rooms_ids_to_get.compile(bind=engine, compile_kwargs={"literal_binds": True}))

    return rooms_ids_to_get
