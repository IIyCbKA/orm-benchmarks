from django.db import models
from django.contrib.postgres.fields import ArrayField, DateTimeRangeField

class Booking(models.Model):
  book_ref = models.CharField(max_length=6, primary_key=True)
  book_date = models.DateTimeField()
  total_amount = models.DecimalField(max_digits=10, decimal_places=2)

  class Meta:
    db_table = 'bookings'
    managed = False

  def __str__(self):
    return self.book_ref


class Flight(models.Model):
  flight_id = models.IntegerField(primary_key=True)
  route_no = models.TextField()
  status = models.TextField()
  scheduled_departure = models.DateTimeField()
  scheduled_arrival = models.DateTimeField()
  actual_departure = models.DateTimeField(null=True, blank=True)
  actual_arrival = models.DateTimeField(null=True, blank=True)

  class Meta:
    db_table = 'flights'
    managed = False
    unique_together = (('route_no', 'scheduled_departure'),)

  def __str__(self):
    return f'{self.flight_id} ({self.route_no})'


class Ticket(models.Model):
  ticket_no = models.CharField(max_length=13, primary_key=True)
  book_ref = models.ForeignKey(
    Booking, db_column='book_ref', to_field='book_ref',
    on_delete=models.DO_NOTHING, related_name='tickets')
  passenger_id = models.TextField()
  passenger_name = models.TextField()
  outbound = models.BooleanField()

  class Meta:
    db_table = 'tickets'
    managed = False
    unique_together = (('book_ref', 'passenger_id', 'outbound'),)

  def __str__(self):
    return self.ticket_no


class Segment(models.Model):
  ticket = models.ForeignKey(
    Ticket, db_column='ticket_no', to_field='ticket_no',
    on_delete=models.DO_NOTHING, related_name='segments')
  flight = models.ForeignKey(
    Flight, db_column='flight_id', to_field='flight_id',
    on_delete=models.DO_NOTHING, related_name='segments')
  fare_conditions = models.TextField()
  price = models.DecimalField(max_digits=10, decimal_places=2)

  class Meta:
    db_table = 'segments'
    managed = False
    unique_together = (('ticket', 'flight'),)

  def __str__(self):
    return f'{self.ticket} - {self.flight_id}'


class AirplaneData(models.Model):
  airplane_code = models.CharField(max_length=3, primary_key=True)
  model = models.JSONField()
  range = models.IntegerField()
  speed = models.IntegerField()

  class Meta:
    db_table = 'airplanes_data'
    managed = False

  def __str__(self):
    return self.airplane_code


class AirportData(models.Model):
  airport_code = models.CharField(max_length=3, primary_key=True)
  airport_name = models.JSONField()
  city = models.JSONField()
  country = models.JSONField()
  coordinates = models.TextField()
  timezone = models.TextField()

  class Meta:
    db_table = 'airports_data'
    managed = False

  def __str__(self):
    return self.airport_code


class Seat(models.Model):
  airplane = models.ForeignKey(
    AirplaneData, db_column='airplane_code', to_field='airplane_code',
    on_delete=models.CASCADE, related_name='seats')
  seat_no = models.TextField()
  fare_conditions = models.TextField()

  class Meta:
    db_table = 'seats'
    managed = False
    unique_together = (('airplane', 'seat_no'),)

  def __str__(self):
    return f'{self.airplane} {self.seat_no}'


class BoardingPass(models.Model):
  ticket = models.ForeignKey(
    Ticket, db_column='ticket_no', to_field='ticket_no',
    on_delete=models.DO_NOTHING, related_name='boarding_passes')
  flight = models.ForeignKey(
    Flight, db_column='flight_id', to_field='flight_id',
    on_delete=models.DO_NOTHING, related_name='boarding_passes')
  seat_no = models.TextField()
  boarding_no = models.IntegerField(null=True, blank=True)
  boarding_time = models.DateTimeField(null=True, blank=True)

  class Meta:
    db_table = 'boarding_passes'
    managed = False
    unique_together = (
      ('ticket', 'flight'),
      ('flight', 'boarding_no'),
      ('flight', 'seat_no'),
    )

  def __str__(self):
    return f'BP {self.ticket_id} / {self.flight_id}'


class Route(models.Model):
  route_no = models.TextField(primary_key=True)
  validity = DateTimeRangeField()
  departure_airport = models.ForeignKey(
    AirportData, db_column='departure_airport', to_field='airport_code',
    on_delete=models.DO_NOTHING, related_name='departure_routes')
  arrival_airport = models.ForeignKey(
    AirportData, db_column='arrival_airport', to_field='airport_code',
    on_delete=models.DO_NOTHING, related_name='arrival_routes')
  airplane_code = models.ForeignKey(
    AirplaneData, db_column='airplane_code', to_field='airplane_code',
    on_delete=models.DO_NOTHING, related_name='routes')
  days_of_week = ArrayField(models.IntegerField())
  scheduled_time = models.TimeField()
  duration = models.DurationField()

  class Meta:
    db_table = 'routes'
    managed = False
    unique_together = (('route_no', 'validity'),)
    indexes = [models.Index(fields=['departure_airport', 'validity']), ]

  def __str__(self):
    return f'{self.route_no}'
