from geoalchemy2 import Geometry
from sqlalchemy import (
    Integer,
    Numeric,
    ForeignKey,
    CHAR,
    Text,
    Boolean,
    Time,
    Interval
)
from sqlalchemy.dialects.postgresql import JSONB, TSTZRANGE, ARRAY, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class AirplaneData(Base):
    __tablename__ = "airplanes_data"

    aircraft_code: Mapped[str] = mapped_column(CHAR(3), primary_key=True, nullable=False)
    model: Mapped[str] = mapped_column(JSONB, nullable=False)
    range: Mapped[int] = mapped_column(Integer, nullable=False)
    speed: Mapped[int] = mapped_column(Integer, nullable=False)


class AirportData(Base):
    __tablename__ = "airports_data"

    airport_code: Mapped[str] = mapped_column(CHAR(3), primary_key=True, nullable=False)
    airport_name: Mapped[str] = mapped_column(JSONB, nullable=False)
    city: Mapped[str] = mapped_column(JSONB, nullable=False)
    country: Mapped[str] = mapped_column(JSONB, nullable=False)
    coordinates: Mapped[str] = mapped_column(Geometry(geometry_type='POINT'), nullable=False)
    timezone: Mapped[str] = mapped_column(Text, nullable=False)


class Booking(Base):
    __tablename__ = "bookings"

    book_ref: Mapped[str] = mapped_column(CHAR(6), primary_key=True, nullable=False)
    book_date: Mapped[str] = mapped_column(TIMESTAMP(timezone=True), nullable=False)
    total_amount: Mapped[float] = mapped_column(Numeric, nullable=False)


class Ticket(Base):
    __tablename__ = "tickets"

    ticket_no: Mapped[str] = mapped_column(Text, primary_key=True, nullable=False)
    book_ref: Mapped[str] = mapped_column(
        ForeignKey("bookings.book_ref"), nullable=False
    )
    passenger_id: Mapped[str] = mapped_column(Text, nullable=False)
    passenger_name: Mapped[str] = mapped_column(Text, nullable=False)
    outbound: Mapped[bool] = mapped_column(Boolean, nullable=False)


class Flight(Base):
    __tablename__ = "flights"

    flight_id: Mapped[int] = mapped_column(Integer, primary_key=True)
    flight_no: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(Text, nullable=False)
    scheduled_departure: Mapped[str] = mapped_column(TIMESTAMP(timezone=True))
    scheduled_arrival: Mapped[str] = mapped_column(TIMESTAMP(timezone=True))
    actual_departure: Mapped[str | None] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )
    actual_arrival: Mapped[str | None] = mapped_column(
        TIMESTAMP(timezone=True), nullable=True
    )


class BoardingPass(Base):
    __tablename__ = "boarding_passes"

    ticket_no: Mapped[str] = mapped_column(
        ForeignKey("tickets.ticket_no"), primary_key=True
    )
    flight_id: Mapped[int] = mapped_column(
        ForeignKey("flights.flight_id"), primary_key=True
    )

    seat_no: Mapped[str] = mapped_column(Text)
    boarding_no: Mapped[int] = mapped_column(Integer)
    boarding_time: Mapped[str] = mapped_column(TIMESTAMP(timezone=True))


class Seat(Base):
    __tablename__ = "seats"

    aircraft_code: Mapped[str] = mapped_column(
        ForeignKey("airplane_datas.aircraft_code"), primary_key=True, nullable=False
    )
    seat_no: Mapped[str] = mapped_column(Text, primary_key=True, nullable=False)
    fare_conditions: Mapped[str] = mapped_column(Text)


class Segment(Base):
    __tablename__ = "segments"
    ticket_no: Mapped[str] = mapped_column(ForeignKey("tickets.ticket_no"), primary_key=True, nullable=False)
    flight_id: Mapped[int] = mapped_column(ForeignKey("flights.flight_id"), primary_key=True, nullable=False)
    fare_conditions: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[float] = mapped_column(Numeric, nullable=False)


class Route(Base):
    __tablename__ = "routes"
    route_no: Mapped[str] = mapped_column(Text, primary_key=True)
    validity: Mapped[str] = mapped_column(TSTZRANGE)
    departure_airport: Mapped[str] = mapped_column(ForeignKey("airplane_datas.departure_airport"), nullable=False)
    arrival_airport: Mapped[str] = mapped_column(ForeignKey("airplane_datas.arrival_airport"), nullable=False)
    airplane_code: Mapped[str] = mapped_column(ForeignKey("airplane_datas.airplane_code"), nullable=False)
    days_of_week: Mapped[list[int]] = mapped_column(ARRAY(Integer), nullable=False)
    scheduled_time: Mapped[str] = mapped_column(Time, nullable=False)
    duration: Mapped[str] = mapped_column(Interval, nullable=False)
